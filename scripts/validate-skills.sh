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

echo "Skills found: $count (expected 43)"
[ "$count" -eq 43 ] || { echo "FAIL: expected 43 skills, found $count"; errors=$((errors+1)); }

# --- Plugin manifest sync: skills[] array must match actual skills on disk ---
manifest=".claude-plugin/plugin.json"
if [ -f "$manifest" ]; then
  if command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; then
    PY=$(command -v python || command -v python3)
    sync_errors=$("$PY" - "$manifest" "$count" <<'PYEOF'
import json, os, sys
manifest, expected = sys.argv[1], int(sys.argv[2])
d = json.load(open(manifest))
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
pm_skills="skills/01-product/brainstorm skills/01-product/spec skills/01-product/oss-strategy skills/02-research/market-research skills/02-research/tech-selection"
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

# --- Output declaration vs skill-outputs.md sync (doc-producing skills) ---
if [ -f docs/skill-outputs.md ] && { command -v python >/dev/null 2>&1 || command -v python3 >/dev/null 2>&1; }; then
  PY=$(command -v python || command -v python3)
  out_errors=$("$PY" - <<'PYEOF'
import re, os, glob
matrix = open("docs/skill-outputs.md", encoding="utf-8").read()
errs = []
# Output declaration paths to check: the canonical doc-producing skills' declared outputs
declared = {
    "skills/01-product/brainstorm/SKILL.md": ["ROADMAP.md", "docs/research/interview.md"],
    "skills/01-product/spec/SKILL.md": ["docs/PRD.md", "docs/vX.Y/prd.md"],
    "skills/03-design/architecture/SKILL.md": ["docs/TECH.md", "docs/vX.Y/tech.md"],
    "skills/03-design/domain-modeling/SKILL.md": ["CONTEXT.md"],
    "skills/03-design/api-design/SKILL.md": ["docs/API/"],
    "skills/03-design/frontend-design/SKILL.md": ["docs/design/DESIGN.md", "docs/design/frontend-audit.md", "docs/research/ux-research.md"],
    "skills/03-design/schema-design/SKILL.md": ["docs/design/SCHEMA.md"],
    "skills/03-design/prompt-engineering/SKILL.md": ["docs/design/PROMPT.md"],
    "skills/03-design/prototype/SKILL.md": ["docs/design/prototype-findings.md"],
    "skills/03-design/codebase-design/SKILL.md": ["docs/design/codebase-audit.md"],
    "skills/04-develop/breakdown/SKILL.md": ["docs/PLAN.md", "docs/vX.Y/plan.md"],
    "skills/07-verify/code-review/SKILL.md": ["docs/TODO.md"],
    "skills/07-verify/security-review/SKILL.md": ["docs/security-report.md"],
    "skills/09-operate/incident-response/SKILL.md": ["docs/postmortem/"],
    "skills/09-operate/documentation-audit/SKILL.md": ["docs/audit/YYYY-MM-DD-documentation.md"],
    "skills/02-research/tech-selection/SKILL.md": ["docs/research/competitor.md"],
    "skills/02-research/market-research/SKILL.md": ["docs/research/market.md"],
    "skills/02-research/research/SKILL.md": ["docs/research/"],
    "skills/08-ship/oss-polish/SKILL.md": ["README.md", "REPOSITORY_SUMMARY.md", "THE_STORY_OF_THIS_REPO.md"],
    "skills/05-tune/performance/SKILL.md": ["PERF.md"],
    "skills/06-test/load-testing/SKILL.md": ["docs/CAPACITY.md"],
    "skills/03-design/design-research/SKILL.md": ["docs/design/references.md"],
}
for skill_md, outputs in declared.items():
    if not os.path.isfile(skill_md):
        continue
    for out in outputs:
        canon = re.sub(r'docs/vX\.Y/', 'docs/', out)
        if canon not in matrix and out not in matrix:
            errs.append(f"{skill_md} declares Output `{out}` but it's not in docs/skill-outputs.md")
for e in errs: print("FAIL: " + e)
import sys; sys.exit(1 if errs else 0)
PYEOF
)
  rc=$?
  [ $rc -eq 0 ] || { echo "$out_errors"; errors=$((errors+1)); }
fi

echo "Total errors: $errors"
exit $errors
