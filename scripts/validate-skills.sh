#!/usr/bin/env bash
# Validate every SKILL.md against the collection schema. Dependency-free (bash + awk + grep).
set -euo pipefail
cd "$(dirname "$0")/.."

phases="meta 01-product 02-research 03-design 04-develop 05-tune 06-test 07-verify 08-ship 09-operate"
errors=0
count=0

for phase in $phases; do
  for skill_dir in "$phase"/*/; do
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
echo "Total errors: $errors"
exit $errors
