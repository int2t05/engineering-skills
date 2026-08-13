# The canonical install block

## Claude Code — the plugin (primary, with ambient principles)

`engineering-skills` ships as a Claude Code plugin. On install, a SessionStart hook injects
the 9 engineering principles into every session as ambient context.

```bash
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

Or, for local development / an unreleased commit:

```bash
claude --plugin-dir /path/to/clone
```

## Codex — per-skill `agents/openai.yaml`

Every skill carries an `agents/openai.yaml` beside its `SKILL.md` with Codex UI metadata
(`interface.display_name`, `interface.short_description`) and, for user-invoked skills,
`policy.allow_implicit_invocation: false`. To use the skills in Codex, copy the `skills/`
tree into your Codex skills directory; the `agents/openai.yaml` files populate Codex's skill
picker. Read `AGENTS.md` first each session for the principles + routing.

## Other agents (Cursor, Gemini, Copilot, Cline, Continue, OpenCode, Windsurf)

The skill content is plain markdown — any agent that reads `AGENTS.md` and `SKILL.md` files
can use it. Two routes:

**skills.sh (broadest, 70+ agents):**

```bash
npx skills@latest add int2t05/engineering-skills
```

Pick the skills you want and which agents to install them on. Note: skills.sh installs
content files only — the Claude Code SessionStart hook does not transfer, so in non-Claude
agents you get the skills but not ambient principle injection. Read `AGENTS.md` at the start
of each session instead.

**Manual copy:** copy `skills/` and `references/` and `AGENTS.md` into your agent's
instructions/skills directory. Point the agent at `AGENTS.md` for routing + principles.

## The two routes are exclusive

The Claude Code plugin is a managed bundle. skills.sh / manual copy writes files you own.
Installing both leaves you with every skill twice — pick one.
