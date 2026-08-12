# Model-invoked vs user-invoked

Every `SKILL.md` in this pack is a skill. The one axis that splits them is **invocation** —
who can reach it:

- **User-invoked** — reachable **only by the human typing its name**. Set
  `disable-model-invocation: true` in the frontmatter (Claude Code) AND
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml` (Codex). The
  `description` is **human-facing**: a one-line summary for a person browsing slash-commands.
- **Model-invoked** — reachable by **model or user**. The default: omit
  `disable-model-invocation` and the `policy` block from `agents/openai.yaml`. The
  `description` is **model-facing** and keeps rich trigger phrasing ("Use when the user
  wants…, mentions…, asks for…") so auto-invocation fires. The test for whether a skill
  should stay model-invoked: _could the model usefully reach for this autonomously?_

Each harness excludes a user-invoked skill from the model's reach in its own way, so nothing
but the human can fire it — no other skill can. A user-invoked skill may invoke
model-invoked skills, but it can never reach another user-invoked skill.

Every skill carries an `agents/openai.yaml` beside its `SKILL.md`. It holds Codex UI
metadata — `interface.display_name` and `interface.short_description` for the skill picker —
and, for user-invoked skills, the `policy.allow_implicit_invocation: false` that pairs with
`disable-model-invocation`. **Keep the two in sync**: a skill is user-invoked in both
harnesses or neither.

## User-invoked skills in this pack

- `skills/01-product/brainstorm` — `disable-model-invocation: true` + `policy.allow_implicit_invocation: false`. A multi-turn grilling dialogue; auto-firing on fuzzy triggers would cause false positives.
- `skills/09-operate/handoff` — same. An explicit handoff action; should only fire when the user asks to hand off.

The other 40 skills are model-invoked.

## Dependencies between skills

Dependencies are expressed as **`/skill`-style prose invocation** ("run the `/tdd` skill",
"close with `/code-review`"), not deep `../other-skill/FILE.md` cross-references. A skill
that needs another skill's discipline says so in prose; it does not link across folders.

The one exception is the **shared engineering principles** (`references/engineering-principles.md`),
which is plugin-wide infrastructure (not owned by any one skill). Every skill links it in
`## References` so an agent can re-read it on demand. In Claude Code the link uses
`${CLAUDE_PLUGIN_ROOT}/...` (portable across projects); in other frameworks the principles
arrive via `AGENTS.md` at session start, and the link is informational.
