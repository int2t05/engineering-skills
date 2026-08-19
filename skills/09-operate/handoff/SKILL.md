---
name: handoff
description: Use when handing off work to another session or agent — produces a structured handoff brief capturing context, decisions, and next steps. Triggers on "handoff", "hand over", "交接", "移交工作".
disable-model-invocation: true
---

# Handoff

Write a handoff brief summarizing the current conversation so a fresh agent can continue the work immediately. The brief is the only context the next session starts with — make it sufficient.

## When to use

- The current session is ending and another agent (or a future you) will continue the work.
- Switching between foreground and background agents mid-task.

**Not for:** continuing work in the same session — just keep going; summarizing work that's already captured in specs/plans/ADRs — reference those by path instead.

## Steps

1. **Summarize context and decisions.** Capture the goal, what was decided and why, what was tried and rejected, and the current state. Don't restate what's already in artifacts — reference specs, plans, ADRs, issues, commits, and diffs by path or URL.
2. **List concrete next steps.** Numbered, each independently actionable, starting from exactly where the work stopped.
3. **Suggest skills.** Add a "Suggested skills" section naming the skills the next agent should invoke (e.g. `tdd`, `code-review`).
4. **Redact sensitive information.** API keys, passwords, and PII must not appear in the brief — it may become a background agent's prompt or a shared file.
5. **Tailor to the next focus.** If the user passed an argument describing what the next session is for, weight the brief toward that focus.
6. **Deliver.** Save the brief to the OS temporary directory (not the current workspace), or launch a background agent seeded with it: `claude --bg --name "<descriptive name>" "<brief>"`. Always pass `--name` with a descriptive title (e.g. `"Fix login bug"`) — it sets the display name in the job list, session picker, and terminal title. The launched agent starts in the current working directory and returns immediately; manage it with `claude agents`.

## Verify

- [ ] A fresh agent given only the brief could continue the work without asking "what's the state?"
- [ ] Next steps are concrete and start from where work stopped
- [ ] No content duplicated from existing artifacts (referenced by path/URL instead)
- [ ] No secrets, tokens, or PII in the brief
- [ ] Brief saved to the temp dir, or a named background agent launched with it

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, verify don't assume, surgical scope)
- [references/on-call-shift.md](references/on-call-shift.md) — on-call shift handoff: active incidents, in-progress investigations, recent changes, known issues, escalation triggers, pre/mid/post-shift checklist
