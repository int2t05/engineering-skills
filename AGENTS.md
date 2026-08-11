# AGENTS.md

Universal entry point for AI coding agents working with this skill pack — Claude Code,
Codex, OpenCode, Cline, Continue, Cursor (agents mode), and any agent that reads
`AGENTS.md`. Adapted from the mattpocock invocation model.

> **Scope:** This file orients agents *using* the `engineering-skills` pack. The reusable
> assets are the 33 skills under `skills/`; this file routes work to them and loads the
> shared discipline.

## What this pack is

33 engineering skills organized by the software development lifecycle, plus a meta router.
Each skill is a folder `skills/<phase>/<name>/SKILL.md` with YAML frontmatter (`name`,
`description`, optional `disable-model-invocation`) and four sections: When to use / Steps /
Verify / References. Encyclopedic data lives in per-skill `references/` (progressive
disclosure).

## Read the engineering principles first

Before any task, load [`references/engineering-principles.md`](references/engineering-principles.md)
(repo-relative path — resolves in every framework). It holds the 8 shared principles every
skill assumes: surface assumptions, manage confusion, push back, enforce simplicity, surgical
scope, verify don't assume, plan with built-in plan mode, goal-driven execution.

> **Claude Code** gets these injected automatically at session start (SessionStart hook).
> **Other frameworks** — read the file above once per session.

## Intent → skill routing

When a task arrives, identify the phase and reach for the matching skill. If unsure, the
`using-skills` skill (in `skills/meta/`) maps the task to a phase.

| Phase | Skill | Triggers on |
|---|---|---|
| product | `brainstorm` | underspecified ask, "refine this idea" (*user-typed*) |
| product | `spec` | new project/feature/change, "write spec", "create prd" |
| product | `oss-strategy` | OSS business model, COSS, commercialization |
| research | `research` | deep web research, cited report |
| research | `market-research` | market sizing, competitor analysis, due diligence |
| research | `tech-selection` | "技术选型", "方案对比", tech stack comparison |
| design | `architecture` | system design, "架构设计", ADR, scalability |
| design | `domain-modeling` | domain model, ubiquitous language, CONTEXT.md |
| design | `api-design` | REST/GraphQL contracts, interface ergonomics |
| design | `codebase-design` | deep modules, refactoring/deepening |
| design | `frontend-design` | UI, "界面设计", production-grade frontend |
| design | `prototype` | throwaway prototype, compare layouts |
| develop | `implement` | implement spec/tickets, TDD at seams |
| develop | `breakdown` | break work into tickets, decision map |
| develop | `context-engineering` | agent needs better context |
| tune | `performance` | "性能优化", profile, bottlenecks |
| tune | `simplify` | "too complex", refactor for clarity |
| test | `tdd` | "测试驱动开发", red-green-refactor |
| test | `test-generation` | "生成测试", generate test files |
| test | `api-testing` | contract testing, REST/GraphQL |
| test | `e2e-testing` | Playwright, e2e, browser test |
| verify | `code-review` | review before merge |
| verify | `debugging` | bug, test failure, unexpected behavior |
| verify | `security-review` | security review, secrets, injection |
| ship | `shipping` | deploy, launch, go live |
| ship | `git-workflow` | commit, merge conflict, pre-commit |
| ship | `ci-cd` | CI pipeline, GitHub Actions |
| ship | `deprecation-migration` | deprecate, migrate, sunset API |
| ship | `oss-polish` | "开源项目美化", README/topics polish |
| operate | `observability` | logs, metrics, alerts, instrumentation |
| operate | `documentation-audit` | docs drift, sync docs to code |
| operate | `handoff` | hand off to another session (*user-typed*) |

## Invocation model — user-invoked vs model-invoked

Every skill is either **model-invoked** (default — the agent reaches for it autonomously on
trigger match) or **user-invoked** (only fires when the human types its name). Two skills
are user-typed: `brainstorm` and `handoff` (set `disable-model-invocation: true`). The rest
are model-invoked. See [`.agents/invocation.md`](.agents/invocation.md) for the full model
and how it syncs across Claude Code (`disable-model-invocation`) and Codex
(`agents/openai.yaml` → `policy.allow_implicit_invocation`).

## Planning

No custom plan skill. Use the harness's built-in plan mode (Claude Code: `EnterPlanMode` /
`ExitPlanMode`; other frameworks: their equivalent). The `spec` skill's output is plan
mode's input. For breaking a plan into tickets, use `breakdown`.

## Install

See [`.agents/install-block.md`](.agents/install-block.md) for the canonical install
commands (Claude Code plugin, Codex, and other agents).

## Conventions

- Skills live under `skills/<phase>/<name>/SKILL.md` (uppercase `SKILL.md`).
- Frontmatter: `name` + `description` (+ optional `disable-model-invocation`). Nothing else.
- Every skill's `## References` links the shared engineering principles
  (`${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md` in Claude Code; other
  frameworks use the repo-relative path above).
- Validate: `bash scripts/validate-skills.sh`.
