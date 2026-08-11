# CLAUDE.md

This is a **Claude Code plugin** (`engineering-skills`) — a curated pack of 33 agent
skills organized by the software development lifecycle. See README.md for the full
catalog and install instructions.

> Note: this CLAUDE.md is contributor/maintainer documentation for the pack itself. It is
> NOT auto-loaded into sessions that use the plugin. The SessionStart hook
> (`hooks/session-start`) injects `references/engineering-principles.md` as ambient context
> instead — that is how the discipline reaches every session. Non-Claude agents get the same
> discipline via `AGENTS.md` at session start.

## Conventions
- Plugin manifest: `.claude-plugin/plugin.json` declares all 33 skills in a `skills[]` array (nested `./<phase>/<skill>` paths — preserves the 9-phase taxonomy).
- Skills live under `skills/` — `skills/meta/` plus 9 numbered phase dirs (`skills/01-product/` through `skills/09-operate/`).
- Every skill is a folder with SKILL.md (uppercase). See references/skill-anatomy.md.
- Every skill links `${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md` — the distilled discipline.
- Shared references use `${CLAUDE_PLUGIN_ROOT}/...` (portable); in-skill refs use plain `references/...`.
- Multi-framework: `AGENTS.md` (universal entry) + `.agents/` (`invocation.md`, `install-block.md`) + per-skill `agents/openai.yaml` (Codex adapter). The invocation-sync invariant — `disable-model-invocation` (Claude Code) ↔ `policy.allow_implicit_invocation` (Codex) — is enforced by the validator.
- Planning uses Claude Code's built-in plan mode (EnterPlanMode/ExitPlanMode), not a skill.
- Validate the collection: `bash scripts/validate-skills.sh` (schema + manifest-sync + Codex-adapter + invocation-sync).
- Regenerate Codex adapters after editing frontmatter: `python scripts/gen-agents-yaml.py`.

## Skill discovery
Run /using-skills (meta) to route a task to the right phase skill, or invoke a skill
directly by name.

## Working in this repo
- Line endings: files are UTF-8; Git may warn LF→CRLF on Windows — harmless.
- Original upstream source repos (addyosmani/agent-skills, mattpocock/skills) are kept
  locally under archive/ (gitignored, not published) for provenance. See README for links.
- When adding/removing a skill, update BOTH the `skills[]` array in
  `.claude-plugin/plugin.json` AND run `python scripts/gen-agents-yaml.py` (generates the
  new skill's `agents/openai.yaml`) AND run the validator (it checks the array stays in sync
  and the Codex adapters stay in sync with frontmatter).
