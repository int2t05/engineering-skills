#!/bin/bash
# 可选执行钩子：阻止明显破坏性命令，不替代人工授权判断。
# 普通 push 的确认由工作流管理；此处只拦强推和破坏性本地操作。

command -v jq >/dev/null 2>&1 || { echo "This optional hook requires jq." >&2; exit 2; }

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

DANGEROUS_PATTERNS=(
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
  "push .*--force"
  "push[[:space:]]+([^[:space:]]+[[:space:]]+)*-f([[:space:]]|$)"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
