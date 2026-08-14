#!/bin/bash
# PreToolUse hook: block the agent from running destructive git commands.
# ALL `git push` is blocked — pushing is a user action, not an agent action
# (the agent prepares the commit; the user reviews and pushes). `--force` and
# `reset --hard` are listed separately so they are caught even without the
# `git` prefix (chained commands, aliases).

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

DANGEROUS_PATTERNS=(
  "git push"
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
  "push --force"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
