# Block Dangerous Git — Hook Setup

The `settings.json` wiring for the `block-dangerous-git.sh` PreToolUse hook. The hook
script itself is at [block-dangerous-git.sh](block-dangerous-git.sh).

## Project (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

## Global (`~/.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse`
array — don't overwrite other settings.

## Verify

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
# expect: exit code 2, BLOCKED message on stderr
```
