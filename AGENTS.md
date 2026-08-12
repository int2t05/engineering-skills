# AGENTS.md

Universal entry point for AI coding agents working with this skill pack — Claude Code,
Codex, OpenCode, Cline, Continue, Cursor (agents mode), and any agent that reads
`AGENTS.md`.

> **Scope:** This file orients agents *using* the `engineering-skills` pack. The reusable
> assets are the 42 skills under `skills/`; this file routes work to them and loads the
> shared discipline.

## What this pack is

42 skills organized by the software development lifecycle, including a meta router.
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
| product | `brainstorm` | underspecified ask, "refine this idea", "头脑风暴" (*user-typed*) |
| product | `spec` | new project/feature/change, "write spec", "create prd", "写需求文档" |
| product | `oss-strategy` | OSS business model, COSS, "开源策略", "开源商业模式" |
| research | `research` | deep web research, cited report, "深度检索", "调研报告" |
| research | `market-research` | market sizing, competitor analysis, "市场调研", "竞品分析" |
| research | `tech-selection` | "技术选型", "方案对比", tech stack comparison |
| design | `architecture` | system design, "架构设计", "系统设计", ADR |
| design | `domain-modeling` | domain model, ubiquitous language, "领域模型", CONTEXT.md |
| design | `api-design` | REST/GraphQL contracts, "接口设计", "API 契约" |
| design | `codebase-design` | deep modules, "深化模块", "重构架构" |
| design | `frontend-design` | UI, "界面设计", "前端设计", production-grade frontend |
| design | `image-to-code` | "设计图转代码", "图片实现", image-first frontend pipeline |
| design | `brandkit` | "品牌识别", "logo 设计", brand identity images |
| design | `imagegen-web` | "网站设计图", "网页参考图", web section images |
| design | `imagegen-mobile` | "移动端设计图", "app 屏幕图", mobile screen/flow images |
| design | `schema-design` | "数据模型", "表结构设计", data model, schema design |
| design | `prompt-engineering` | "提示词工程", "LLM 特性", prompt design, eval harness |
| design | `prototype` | throwaway prototype, "原型", "试这个方案", "build a demo" |
| develop | `implement` | implement spec/tickets, "实现", "编码", "改这个配置", "搭项目骨架" |
| develop | `breakdown` | break work into tickets, "拆解任务", "拆票", decision map |
| develop | `context-engineering` | agent needs context, "解释这段代码", "带我过一遍代码库" |
| develop | `i18n` | "国际化", "本地化", "多语言", i18n, RTL, localization |
| tune | `performance` | "性能优化", "性能调优", profile, bottlenecks |
| tune | `simplify` | "too complex", "简化", "重构求清晰", refactor for clarity |
| test | `tdd` | "测试驱动开发", "红绿重构", red-green-refactor |
| test | `test-generation` | "生成测试", "补测试", generate test files |
| test | `api-testing` | contract testing, "API 测试", "接口测试", REST/GraphQL |
| test | `e2e-testing` | e2e, browser test, "端到端测试", "浏览器测试" |
| test | `load-testing` | "压测", "压力测试", "容量测试", load/stress test, capacity |
| verify | `code-review` | review before merge, "代码审查", "合并前审查" |
| verify | `debugging` | bug, "调试", "排查 bug", "读日志", "排查错误日志" |
| verify | `security-review` | security review, "安全审查", "安全审计", secrets, injection |
| ship | `shipping` | deploy, launch, "上线", "发布", "部署到生产" |
| ship | `git-workflow` | commit, merge conflict, "提交", "合并冲突", pre-commit |
| ship | `ci-cd` | CI pipeline, GitHub Actions, "流水线", "持续集成" |
| ship | `deprecation-migration` | deprecate, migrate, "迁移", "升级依赖", "更新这个库" |
| ship | `oss-polish` | "开源项目美化", "优化项目展示", README/topics polish |
| operate | `observability` | logs, metrics, "可观测性", "监控告警", instrumentation |
| operate | `documentation-audit` | docs drift, "写文档", "写 README", "文档化这个功能", sync docs |
| operate | `handoff` | hand off to another session, "交接" (*user-typed*) |
| operate | `incident-response` | "事故响应", "线上故障", "复盘", incident, on-call, postmortem |

Several skills carry **sub-task references** for focused scenarios — the main
`SKILL.md` links a `references/` file for depth:

- `context-engineering` → explains existing code / codebase tours (`references/code-explanation.md`)
- `debugging` → log triage without full reproduction (`references/log-triage.md`)
- `implement` → lightweight changes: small edits, renames, scaffolding (`references/lightweight-changes.md`)
- `documentation-audit` → writing new docs from scratch (`references/writing-docs.md`)
- `deprecation-migration` → dependency upgrades (`references/dependency-upgrade.md`)

Every skill's `## When to use` states a **negative boundary** (`NOT for` → the
adjacent skill it isn't), so adjacent tasks route to the right skill instead of
two firing at once.

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
  frameworks use the repo-relative path above). PM-side skills also link
  `references/product-principles.md`; UIUX skills also link `references/design-principles.md`.
- Validate: `bash scripts/validate-skills.sh`.
