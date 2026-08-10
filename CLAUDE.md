# CLAUDE.md

This is a curated collection of agent skills organized by the software development
lifecycle. See README.md for the full catalog.

## Conventions
- Skills live under meta/ + 9 numbered phase dirs (01-product through 09-operate).
- Every skill is a folder with SKILL.md (uppercase). See references/skill-anatomy.md.
- Every skill links references/engineering-principles.md — the distilled discipline.
- Planning uses Claude Code's built-in plan mode (EnterPlanMode/ExitPlanMode), not a skill.
- Validate the collection: `bash scripts/validate-skills.sh`

## Skill discovery
Run /using-skills (meta) to route a task to the right phase skill, or invoke a skill
directly by name.

## Working in this repo
- Line endings: files are UTF-8; Git may warn LF→CRLF on Windows — harmless.
- The archive/upstream-* dirs hold the original source repos read-only for provenance;
  never edit them. New skills draw from them as needed.
