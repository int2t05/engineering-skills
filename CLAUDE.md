# CLAUDE.md

This is a **Claude Code plugin** (`engineering-skills`) — a curated pack of 45 agent
skills organized by the software development lifecycle. See README.md for the full
catalog and install instructions.

> Note: this CLAUDE.md is contributor/maintainer documentation for the pack itself. It is
> NOT auto-loaded into sessions that use the plugin. The SessionStart hook
> (`hooks/session-start`) injects `references/engineering-principles.md` as ambient context
> instead — that is how the discipline reaches every session. Non-Claude agents get the same
> discipline via `AGENTS.md` at session start.

## Conventions
- Skills live under `skills/` — `skills/meta/` plus 9 numbered phase dirs (`skills/01-product/` through `skills/09-operate/`).
- Every skill is a folder with SKILL.md (uppercase). See references/skill-anatomy.md — including the `**Output:**` declaration convention and the two-layer (project-level + version-level) output pattern for PRD/TECH/PLAN.
- Every skill links `${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md` — the distilled discipline. PM-side skills (brainstorm, spec, oss-strategy, research market/tech-selection modes) also link `references/product-principles.md`; UIUX skills (frontend-design, image-to-code, imagegen, prototype) also link `references/design-principles.md` — domain discipline layers atop the shared engineering base.
- Shared references use `${CLAUDE_PLUGIN_ROOT}/...` (portable); in-skill refs use plain `references/...`.
- Multi-framework: `AGENTS.md` (universal entry) + `.agents/` (`invocation.md`, `install-block.md`) + per-skill `agents/openai.yaml` (Codex adapter).
- Planning uses Claude Code's built-in plan mode (EnterPlanMode/ExitPlanMode), not a skill.

## Skill discovery
Run /using-skills (meta) to route a task to the right phase skill, or invoke a skill
directly by name.
