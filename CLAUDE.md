# CLAUDE.md

This is a **Claude Code plugin** (`engineering-skills`) — a curated pack of 33 agent
skills organized by the software development lifecycle. See README.md for the full
catalog and install instructions.

> Note: this CLAUDE.md is contributor/maintainer documentation for the pack itself. It is
> NOT auto-loaded into sessions that use the plugin. The SessionStart hook
> (`hooks/session-start`) injects `references/engineering-principles.md` as ambient context
> instead — that is how the discipline reaches every session.

## Conventions
- Plugin manifest: `.claude-plugin/plugin.json` declares all 33 skills in a `skills[]` array (nested `./<phase>/<skill>` paths — preserves the 9-phase taxonomy).
- Skills live under `skills/` — `skills/meta/` plus 9 numbered phase dirs (`skills/01-product/` through `skills/09-operate/`).
- Every skill is a folder with SKILL.md (uppercase). See references/skill-anatomy.md.
- Every skill links `${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md` — the distilled discipline.
- Shared references use `${CLAUDE_PLUGIN_ROOT}/...` (portable); in-skill refs use plain `references/...`.
- Planning uses Claude Code's built-in plan mode (EnterPlanMode/ExitPlanMode), not a skill.
- Validate the collection: `bash scripts/validate-skills.sh`

## Skill discovery
Run /using-skills (meta) to route a task to the right phase skill, or invoke a skill
directly by name.

## Working in this repo
- Line endings: files are UTF-8; Git may warn LF→CRLF on Windows — harmless.
- The archive/upstream-* dirs hold the original source repos read-only for provenance;
  never edit them. New skills draw from them as needed.
- When adding/removing a skill, update BOTH the `skills[]` array in
  `.claude-plugin/plugin.json` AND run the validator (it checks the array stays in sync).
