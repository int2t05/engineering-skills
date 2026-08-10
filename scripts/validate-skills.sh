#!/usr/bin/env bash
# Validate every SKILL.md against the collection schema. Dependency-free (bash + awk + grep).
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
    grep -q '^## When to use' "$skill_md" || { echo "FAIL: $skill_md missing ## When to use"; errors=$((errors+1)); }
    grep -q '^## Steps' "$skill_md" || { echo "FAIL: $skill_md missing ## Steps"; errors=$((errors+1)); }
    grep -q '^## Verify' "$skill_md" || { echo "FAIL: $skill_md missing ## Verify"; errors=$((errors+1)); }
    grep -q '^## References' "$skill_md" || { echo "FAIL: $skill_md missing ## References"; errors=$((errors+1)); }
    grep -q 'engineering-principles' "$skill_md" || { echo "FAIL: $skill_md doesn't link engineering-principles"; errors=$((errors+1)); }
  done
done

echo "Skills found: $count (expected 33)"
[ "$count" -eq 33 ] || { echo "FAIL: expected 33 skills, found $count"; errors=$((errors+1)); }

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

echo "Total errors: $errors"
exit $errors
