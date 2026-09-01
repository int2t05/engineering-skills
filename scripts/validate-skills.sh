#!/usr/bin/env bash
# Validate every SKILL.md against the collection schema, plus the Codex adapter
# (agents/openai.yaml) and the invocation-sync invariant between the two. Bash + awk + grep.
set -euo pipefail
cd "$(dirname "$0")/.."

phases="meta 01-product 02-research 03-design 04-develop 05-tune 06-test 07-verify 08-ship 09-operate"
errors=0
count=0

for phase in $phases; do
  for skill_dir in "skills/$phase"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_md="$skill_dir/SKILL.md"
    if [ ! -f "$skill_md" ]; then
      echo "FAIL: $skill_dir has no SKILL.md (lowercase filename?)"
      errors=$((errors+1)); continue
    fi
    count=$((count+1))
    head -1 "$skill_md" | grep -q '^---' || { echo "FAIL: $skill_md missing frontmatter opener"; errors=$((errors+1)); }
    grep -q '^name:' "$skill_md" || { echo "FAIL: $skill_md missing name:"; errors=$((errors+1)); }
    grep -q '^description:' "$skill_md" || { echo "FAIL: $skill_md missing description:"; errors=$((errors+1)); }
    fm=$(awk 'NR==1{next} /^---$/{exit} {print}' "$skill_md")
    bad=$(echo "$fm" | grep -iE '^(license|metadata|category|priority|agents|dependencies|tags|validation|origin|allowed-tools|model|user-invocable|argument-hint):' || true)
    [ -z "$bad" ] || { echo "FAIL: $skill_md disallowed frontmatter: $bad"; errors=$((errors+1)); }
    # Description must carry trigger phrasing so auto-invocation can fire.
    echo "$fm" | grep -qiE 'Triggers on|触发' || { echo "FAIL: $skill_md description lacks trigger phrasing (Triggers on / 触发)"; errors=$((errors+1)); }
    # A2: structural drift — frontmatter name matches dir, kebab-case dir, description length
    fm_name=$(echo "$fm" | sed -n 's/^name:[[:space:]]*//p' | tr -d '[:space:]')
    dir_name=$(basename "${skill_dir%/}")
    [ "$fm_name" = "$dir_name" ] || { echo "FAIL: $skill_md name '$fm_name' != dir '$dir_name'"; errors=$((errors+1)); }
    echo "$dir_name" | grep -qE '^[a-z][a-z0-9]*(-[a-z0-9]+)*$' || { echo "FAIL: $skill_dir not kebab-case ('$dir_name')"; errors=$((errors+1)); }
    desc_val=$(echo "$fm" | sed -n 's/^description:[[:space:]]*//p')
    [ ${#desc_val} -le 1024 ] || { echo "FAIL: $skill_md description is ${#desc_val} chars (limit 1024)"; errors=$((errors+1)); }
    grep -q '^## When to use' "$skill_md" || { echo "FAIL: $skill_md missing ## When to use"; errors=$((errors+1)); }
    # When-to-use must state a negative boundary so adjacent tasks don't mis-route.
    wtu=$(awk '/^## When to use/{f=1;next} /^## /{f=0} f' "$skill_md")
    echo "$wtu" | grep -qiE 'NOT for|When NOT to use|不用于|Not for' || { echo "FAIL: $skill_md When-to-use lacks negative boundary (NOT for / When NOT to use)"; errors=$((errors+1)); }
    grep -q '^## Steps' "$skill_md" || { echo "FAIL: $skill_md missing ## Steps"; errors=$((errors+1)); }
    grep -q '^## Verify' "$skill_md" || { echo "FAIL: $skill_md missing ## Verify"; errors=$((errors+1)); }
    grep -q '^## References' "$skill_md" || { echo "FAIL: $skill_md missing ## References"; errors=$((errors+1)); }
    grep -q 'engineering-principles' "$skill_md" || { echo "FAIL: $skill_md doesn't link engineering-principles"; errors=$((errors+1)); }
    # --- Codex adapter: agents/openai.yaml must exist and stay in sync with frontmatter ---
    yaml_file="$skill_dir/agents/openai.yaml"
    if [ ! -f "$yaml_file" ]; then
      echo "FAIL: $skill_md missing agents/openai.yaml (run scripts/gen-agents-yaml.py)"
      errors=$((errors+1))
    else
      grep -q '^interface:' "$yaml_file" || { echo "FAIL: $yaml_file missing interface:"; errors=$((errors+1)); }
      grep -q 'display_name:' "$yaml_file" || { echo "FAIL: $yaml_file missing display_name"; errors=$((errors+1)); }
      grep -q 'short_description:' "$yaml_file" || { echo "FAIL: $yaml_file missing short_description"; errors=$((errors+1)); }
      # Invocation-sync: disable-model-invocation (Claude Code) must match
      # policy.allow_implicit_invocation (Codex) — user-invoked in both or neither.
      dmi=$(echo "$fm" | grep -ciE '^disable-model-invocation:[[:space:]]*true' || true)
      aii=$(grep -ciE 'allow_implicit_invocation:[[:space:]]*false' "$yaml_file" || true)
      if [ "$dmi" -gt 0 ] && [ "$aii" -eq 0 ]; then
        echo "FAIL: $skill_md is user-invoked (disable-model-invocation: true) but $yaml_file lacks allow_implicit_invocation: false"
        errors=$((errors+1))
      fi
      if [ "$dmi" -eq 0 ] && [ "$aii" -gt 0 ]; then
        echo "FAIL: $skill_md is model-invoked but $yaml_file sets allow_implicit_invocation: false (drift)"
        errors=$((errors+1))
      fi
    fi
  done
done

# --- A1: Security scan — flag malicious patterns in skill-bundled files ---
# Threat: a third-party skill bundles a script that exfiltrates, persists, backdoors, or
# injects instructions. Split by file type: prompt-injection phrases are a markdown
# (instruction) threat; execution/credential/persistence patterns are a script threat.
# Non-markdown files are scanned for the script threats so a skill that documents "watch
# for curl|bash" in its own markdown isn't false-flagged. Markdown is scanned only for
# prompt-injection phrases.
# Context-aware qualifiers avoid false positives on the pack's own legit usage:
#  - data exfil: curl/wget with a POST body (-d/--data/-X POST/--post-data), not plain GET
#  - global install: npm -g/--global or brew install (system-wide), not local npm install
#  - nohup: detached background process (backdoor signal); --silent/2>/dev/null stay deferred (too common)
#  - suspicious domains: in scripts only (non-markdown), so design-research's gallery URL docs don't match
sec_tmp=$(mktemp)
for phase in $phases; do
  for skill_dir in "skills/$phase"/*/; do
    [ -d "$skill_dir" ] || continue
    # Non-markdown bundled files (scripts, yaml, json): execution / credential / persistence
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      grep -nE 'nc -e |/dev/tcp/|mkfifo|socat |base64 -d|curl.*\| *bash|wget.*\| *bash|ghp_[0-9a-f]{36}|AKIA[0-9A-Z]{16}|sk-ant-|BEGIN.*PRIVATE KEY|http://[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|~/\.(ssh|aws|kube|gnupg|netrc)|crontab -|authorized_keys|systemctl |launchctl |nohup |--index-url|--registry |git\+https|rm -rf /|rm -rf ~|rm -rf \$|curl.*(-d |--data[ =]|-X *POST)|wget.*--post-data|npm (install|i) -g|npm (install|i) --global|brew install |pastebin\.com|ngrok\.io|bit\.ly|tinyurl\.com' "$f" >> "$sec_tmp" 2>/dev/null || true
    done < <(find "$skill_dir" -type f ! -name '*.md' ! -path '*/node_modules/*' 2>/dev/null)
    # Markdown files: prompt-injection phrases (instruction-injection threat)
    while IFS= read -r f; do
      [ -n "$f" ] || continue
      grep -nE '⚠️ CRITICAL REQUIREMENT|THE SKILL WILL NOT WORK|必须先执行' "$f" >> "$sec_tmp" 2>/dev/null || true
    done < <(find "$skill_dir" -type f -name '*.md' 2>/dev/null)
  done
done
if [ -s "$sec_tmp" ]; then
  while IFS= read -r line; do
    echo "FAIL: security scan — $line"
  done < "$sec_tmp"
  errors=$((errors + $(grep -c '' "$sec_tmp")))
fi
rm -f "$sec_tmp"

echo "Skills found: $count (expected 48)"
[ "$count" -eq 48 ] || { echo "FAIL: expected 48 skills, found $count"; errors=$((errors+1)); }

# --- Plugin manifest sync: skills[] array must match actual skills on disk ---
manifest=".claude-plugin/plugin.json"
if [ -f "$manifest" ]; then
  if command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; then
    PY=$(command -v python || command -v python3)
    sync_errors=$("$PY" - "$manifest" "$count" <<'PYEOF'
import json, os, sys
manifest, expected = sys.argv[1], int(sys.argv[2])
d = json.load(open(manifest, encoding="utf-8"))
arr = d.get("skills", [])
errs = []
if len(arr) != expected:
    errs.append(f"plugin.json skills[] has {len(arr)} entries, but {expected} skills found on disk")
for entry in arr:
    if not os.path.isfile(entry + "/SKILL.md"):
        errs.append(f"plugin.json skills[] entry '{entry}' has no SKILL.md")
# set comparison: array entries vs actual skill dirs
actual = set()
for root, dirs, files in os.walk("."):
    if "archive" in root.split(os.sep): continue
    if "SKILL.md" in files:
        actual.add("./" + root.replace("\\", "/").lstrip("./"))
arr_set = set(arr)
missing_in_manifest = actual - arr_set
extra_in_manifest = arr_set - actual
for m in missing_in_manifest: errs.append(f"skill on disk but not in manifest: {m}")
for e in extra_in_manifest: errs.append(f"in manifest but no SKILL.md on disk: {e}")
for e in errs: print("FAIL: " + e)
sys.exit(1 if errs else 0)
PYEOF
)
    rc=$?
    [ $rc -eq 0 ] || { echo "$sync_errors"; errors=$((errors+1)); }
  else
    echo "WARN: python not found — skipping plugin.json sync check"
  fi
fi

# --- Dead reference links: every in-skill references/x.md link must resolve ---
for phase in $phases; do
  for skill_dir in "skills/$phase"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_md="$skill_dir/SKILL.md"
    refs=$(grep -oE '\]\(references/[a-z0-9./_-]+\.md\)' "$skill_md" 2>/dev/null | sed 's/](//;s/)//' | sort -u || true)
    for ref in $refs; do
      [ -f "${skill_dir}${ref}" ] || { echo "FAIL: $skill_md links $ref but file does not exist"; errors=$((errors+1)); }
    done
  done
done

# --- Domain principles linking: PM skills link product-principles, UIUX skills link design-principles ---
pm_skills="skills/01-product/brainstorm skills/01-product/spec skills/01-product/oss-strategy skills/02-research/research"
uiux_skills="skills/03-design/frontend-design skills/03-design/image-to-code skills/03-design/imagegen skills/03-design/design-research skills/03-design/prototype"
for s in $pm_skills; do
  [ -f "$s/SKILL.md" ] && { grep -q 'product-principles' "$s/SKILL.md" || { echo "FAIL: $s/SKILL.md (PM skill) does not link product-principles.md"; errors=$((errors+1)); }; }
done
for s in $uiux_skills; do
  [ -f "$s/SKILL.md" ] && { grep -q 'design-principles' "$s/SKILL.md" || { echo "FAIL: $s/SKILL.md (UIUX skill) does not link design-principles.md"; errors=$((errors+1)); }; }
done

# --- Trigger-collision check: no two skills share a quoted trigger phrase ---
# A shared trigger phrase is a routing collision — the model can't decide which
# skill fires. Deterministic CI guard adapted from addyosmani's eval Tier 2.
collision_tmp=$(mktemp)
for phase in $phases; do
  for skill_dir in "skills/$phase"/*/; do
    [ -d "$skill_dir" ] || continue
    skill_md="$skill_dir/SKILL.md"
    [ -f "$skill_md" ] || continue
    skill_name=$(basename "$skill_dir")
    desc_line=$(grep '^description:' "$skill_md" | head -1)
    # Extract every quoted phrase from the description (Triggers-on list + natural-language cues)
    echo "$desc_line" | grep -oE '"[^"]+"' | tr -d '"' | while IFS= read -r p; do
      [ -n "$p" ] && printf '%s|%s\n' "$p" "$skill_name"
    done >> "$collision_tmp" || true
  done
done
collisions=$(awk -F'|' '{k=tolower($1); if(k in seen){print "FAIL: trigger phrase \"" $1 "\" shared by " seen[k] " and " $2} else {seen[k]=$2}}' "$collision_tmp")
rm -f "$collision_tmp"
if [ -n "$collisions" ]; then
  printf '%s\n' "$collisions"
  collision_count=$(printf '%s\n' "$collisions" | grep -c '^FAIL:')
  errors=$((errors+collision_count))
fi

# --- Discovery-surface presence check: every manifest skill appears in all 5 routing surfaces ---
# Catches the most dangerous drift — a skill added/renamed in the manifest but missing from a
# discovery surface. Uses word-boundary matching (grep -w) so "spec" won't match "specific".
# The catalog/ordering in these files is human-curated, so we check presence, not regeneration.
routing_files="README.md README.zh-CN.md AGENTS.md skills/meta/using-skills/references/phase-tree.md skills/meta/using-skills/SKILL.md"
if [ -f ".claude-plugin/plugin.json" ] && { command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; }; then
  PY=$(command -v python || command -v python3)
  skill_names=$("$PY" -c 'import json; d=json.load(open(".claude-plugin/plugin.json", encoding="utf-8")); print("\n".join(e.split("/")[-1] for e in d["skills"]))' | tr -d '\r')
  for name in $skill_names; do
    for rf in $routing_files; do
      [ -f "$rf" ] || { echo "FAIL: routing surface $rf not found"; errors=$((errors+1)); continue; }
      grep -qw "$name" "$rf" || { echo "FAIL: skill '$name' (in manifest) missing from $rf"; errors=$((errors+1)); }
    done
  done
fi

# --- Output declaration vs skill-outputs.md sync (dynamic scan) ---
# Scan every SKILL.md for **Output:** markers, extract declared md-paths, and verify each
# appears in docs/skill-outputs.md. The marker is the single source; the matrix is the derived
# view. Forward check only (every declared path must be in the matrix) — the reverse is omitted
# because the matrix also lists cross-task artifacts (FRONT.md, FEATURES.md, CLAUDE.md) that no
# single skill produces, which would false-positive. Code/descriptive declarations (no backtick
# md-path) are filtered out — they are artifacts but not md docs.
if [ -f docs/skill-outputs.md ] && { command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; }; then
  PY=$(command -v python || command -v python3)
  out_errors=$("$PY" - <<'PYEOF'
import re, glob, sys

ROOT_DOCS = {"README.md", "ROADMAP.md", "CONTEXT.md", "PERF.md",
             "REPOSITORY_SUMMARY.md", "THE_STORY_OF_THIS_REPO.md"}

def is_md_path(p):
    if p.startswith('references/'):
        return False  # a reference file the skill loads, not an output it produces
    return '.md' in p or p.startswith('docs/') or p in ROOT_DOCS

def normalize(p):
    return re.sub(r'docs/vX\.Y/', 'docs/', p)

matrix = open("docs/skill-outputs.md", encoding="utf-8").read()
errs = []

for skill_md in sorted(glob.glob("skills/*/*/SKILL.md")):
    skill_md = skill_md.replace("\\", "/")
    if skill_md.startswith("skills/meta/"):
        continue  # meta skills document the convention, not artifact producers
    text = open(skill_md, encoding="utf-8").read()
    m = re.search(r'\*\*Output:\*\*\s*(.*?)(?=\n## |\Z)', text, re.S)
    if not m:
        continue  # behavior-only skill — no marker, no check
    block = m.group(1)
    paths = re.findall(r'`([^`]+)`', block)
    md_paths = [p for p in paths if is_md_path(p)]
    for p in md_paths:
        n = normalize(p)
        if n not in matrix and p not in matrix:
            errs.append(f"{skill_md} declares Output `{p}` but it's not in docs/skill-outputs.md")

for e in errs:
    print("FAIL: " + e)
sys.exit(1 if errs else 0)
PYEOF
)
  rc=$?
  [ $rc -eq 0 ] || { echo "$out_errors"; errors=$((errors+1)); }
fi

# --- Reference ToC + SKILL.md length checks (WARN, non-blocking) ---
# Convention per references/skill-anatomy.md: references >100 lines need ## Contents;
# SKILL.md target 15-150 lines. Warn-only to flag drift without blocking CI.
if command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; then
  PY=$(command -v python || command -v python3)
  "$PY" - <<'PYEOF'
import glob, re
warns = []
# Reference ToC: >100 lines must have ## Contents
refs = []
refs.extend(glob.glob('references/**/*.md', recursive=True))
refs.extend(glob.glob('skills/**/references/**/*.md', recursive=True))
for f in sorted(refs):
    f = f.replace('\\', '/')
    with open(f, encoding='utf-8') as fh:
        lines = fh.readlines()
    if len(lines) > 100 and not any(re.match(r'^##\s*[Cc]ontents', l) for l in lines):
        warns.append(f"WARN: {f} has {len(lines)} lines but no ## Contents (see skill-anatomy.md progressive disclosure)")
# SKILL.md length: target ≤150
for f in sorted(glob.glob('skills/*/*/SKILL.md')):
    f = f.replace('\\', '/')
    with open(f, encoding='utf-8') as fh:
        n = sum(1 for _ in fh)
    if n > 150:
        warns.append(f"WARN: {f} is {n} lines (target ≤150 — move detail to references/)")
for w in warns:
    print(w)
if warns:
    print(f"Warnings: {len(warns)} (non-blocking)")
PYEOF
fi

echo "Total errors: $errors"
exit $errors
