# Engineering Skills

> **Languages:** English | [中文](README.zh-CN.md)

A unified agent skill pack — **33 engineering skills** organized by the software
development lifecycle. Ships as a Claude Code plugin (with shared engineering principles
injected at every session start) and works across Codex, Cursor, Cline, Continue, OpenCode,
and any agent that reads `AGENTS.md`.

Consolidated from three source collections (83 → 33): 24 personal root skills,
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (24, MIT), and
[mattpocock/skills](https://github.com/mattpocock/skills) (35, MIT). Originals kept
locally (gitignored) for provenance.

## Install

**Claude Code (primary — ambient principles via SessionStart hook):**

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

Or for local development: `claude --plugin-dir /path/to/clone`.

On install, a SessionStart hook injects the 8 engineering principles
([`references/engineering-principles.md`](references/engineering-principles.md)) as ambient
context — every session starts with the discipline loaded. Skills auto-trigger on their
description phrases, or invoke explicitly by name (`/tdd`, `/code-review`, `/brainstorm`).

**Other agent frameworks (Codex, Cursor, Cline, Continue, OpenCode, Windsurf…):**

The skill content is plain markdown. [`AGENTS.md`](AGENTS.md) is the universal entry — read
it first each session for routing + principles. Two routes (pick one — the Claude Code plugin
and a file-copy route are exclusive):

```bash
# skills.sh — broadest (70+ agents); installs content files only (no SessionStart hook)
npx skills@latest add int2t05/engineering-skills

# or manual copy: skills/ + references/ + AGENTS.md into your agent's instructions dir
```

Each skill carries an `agents/openai.yaml` (Codex adapter: `display_name`, `short_description`,
and `policy.allow_implicit_invocation` for user-invoked skills) so the two harnesses stay in
sync. See [`.agents/install-block.md`](.agents/install-block.md) for the canonical wording.

## How it works

- **Universal entry:** `AGENTS.md` orients any agent — routing table, invocation model, install. Claude Code reads it as part of the plugin; other frameworks read it at session start.
- **Auto-trigger:** 31 skills activate when a task matches their `description:` triggers (incl. Chinese phrases like "技术选型", "生成测试", "性能优化").
- **Explicit call:** type `/skill-name` (e.g. `/tdd`, `/debugging`). `brainstorm` and `handoff` are user-typed only (`disable-model-invocation: true` ↔ `agents/openai.yaml` `allow_implicit_invocation: false`).
- **Routing:** unsure which skill fits? invoke `using-skills` — it maps the task to a phase.
- **Planning:** uses the harness's built-in plan mode (Claude Code: `EnterPlanMode`/`ExitPlanMode`), not a custom skill (principle §7).
- **Progressive disclosure:** each `SKILL.md` is a lean core; encyclopedic data lives in per-skill `references/` loaded on demand.

## Catalog — all 33 skills by phase

### meta
**`using-skills`** — Router. Maps incoming work to the right skill across the 9 phases.
- Triggers: "which skill should I use", "route this task", "用哪个技能", "路由".
- Output: the routed skill activates.

### 01-product — clarify what to build
**`brainstorm`** — One-question-at-a-time dialogue that sharpens a vague idea into a concrete proposal.
- Triggers: "brainstorm", "grill me", "interview me", "refine this idea", "头脑风暴", "帮我打磨想法", "盘问我". *User-typed only.*
- Output: a proposal the user confirms; a spec becomes writable.

**`spec`** — Writes a spec/PRD (objectives, structure, commands, code style, testing, boundaries) before any code.
- Triggers: "write spec", "create prd", "spec out", "写需求文档", "写规格", "需求文档".
- Output: a spec document covering 6 core areas.

**`oss-strategy`** — Open source strategy: business model, COSS, open core, commercialization, growth.
- Triggers: "open source strategy", "OSS 策略", "DevHunt", "开源策略", "开源商业模式".
- Output: strategy decisions (not GitHub beautification — that's `oss-polish`).

### 02-research — investigate before building
**`research`** — Deep web research with source-backed investigation, producing a cited Markdown artifact.
- Triggers: "deep research", "source-backed investigation", "cited report", "深度调研", "深度检索", "调研报告", "调研转文档".
- Output: a cited Markdown file (`research/YYYY-MM-DD-<slug>.md`).

**`market-research`** — Market sizing, competitor comparisons, investor due diligence, industry intelligence.
- Triggers: "market sizing", "competitor analysis", "due diligence", "市场调研", "市场规模", "竞品分析".
- Output: a decision-oriented research summary with source attribution.

**`tech-selection`** — Choose/compare a tech stack, library, framework, or repo for a concrete requirement.
- Triggers: "技术选型", "方案对比", "选哪个", "tech stack", "library comparison", "技术对比".
- Output: a comparison matrix + recommendation.

### 03-design — design before coding
**`architecture`** — High-level system architecture: NFRs, patterns, components, ADRs.
- Triggers: "system design", "架构设计", "ADR", "scalability", "系统设计", "架构决策".
- Output: ADR(s) + architecture diagram. Refs: adr-template, architecture-patterns, database-selection, nfr-checklist, system-design.

**`domain-modeling`** — Build/sharpen a domain model: challenge terms, stress-test scenarios, update CONTEXT.md + ADRs.
- Triggers: "domain model", "ubiquitous language", "CONTEXT.md", "领域模型", "统一语言", "领域建模".
- Output: a shared ubiquitous language doc + ADRs.

**`api-design`** — API/interface design: REST/GraphQL contracts, versioning, error models, ergonomics.
- Triggers: "design API", "REST contract", "GraphQL schema", "接口设计", "API 契约", "API 设计".
- Output: a contract spec (Hyrum's Law, One-Version Rule applied).

**`codebase-design`** — Deep modules, refactoring/deepening opportunities, testability.
- Triggers: "deep modules", "refactor architecture", "deepening", "深化模块", "重构架构", "代码库设计".
- Output: a deepening-opportunities report; works through the one you pick.

**`frontend-design`** — Distinctive, production-grade UI: color, typography, layout, interaction states.
- Triggers: "frontend", "UI", "design", "界面设计", "前端设计".
- Output: working UI code. Refs: styles (18), palettes (12), font-pairings (31), ux-guidelines (232), apple-hig.

**`prototype`** — Throwaway prototype to answer a design question (single HTML for logic, or toggleable UI variants).
- Triggers: "prototype", "compare layouts", "validate the interaction", "sketch out", "try this quickly", "build a demo", "原型", "试做", "试这个方案", "搭个快速 demo".
- Output: a throwaway HTML file; the design question answered.

### 04-develop — implement
**`implement`** — Implement work from a spec/tickets: TDD at seams, typechecks, full suite, code-review, commit.
- Triggers: "implement", "build this", "code the feature", "实现", "编码", "改这个配置", "重命名", "搭项目骨架".
- Output: committed, tested, reviewed code. Refs: source-verification, doubt-cycle.

**`breakdown`** — Break a plan/spec into tracer-bullet tickets with blocking edges; decision map for huge work.
- Triggers: "break into tickets", "decompose", "wayfinder", "拆解任务", "拆票", "任务分解".
- Output: tickets with blocking edges, or a decision map.

**`context-engineering`** — Assemble the right files, definitions, and prior decisions before implementing.
- Triggers: "agent lacks context", "what files matter", "解释这段代码", "这个模块怎么工作", "带我过一遍代码库".
- Output: a packed working context. Refs: context-strategies.

### 05-tune — optimize
**`performance`** — Measure before optimizing: profile, identify bottlenecks, improve.
- Triggers: "webperf", "performance regression", "慢", "性能优化", "性能调优".
- Output: a profile + targeted fix. Refs: bottlenecks, anti-patterns.

**`simplify`** — Clarity over cleverness: remove speculative abstractions and dead complexity.
- Triggers: "simplify", "too complex", "refactor for clarity", "简化", "太复杂", "重构求清晰".
- Output: simpler code preserving behavior. Refs: opportunities.

### 06-test — prove it works
**`tdd`** — Red-green-refactor, one vertical slice at a time.
- Triggers: "tdd", "test-driven", "red green refactor", "测试驱动开发", "红绿重构", "测试驱动".
- Output: passing tests + behavior verified. Refs: test-strategy (Test Pyramid, test-double hierarchy), mocking, good-tests, testing-anti-patterns.

**`test-generation`** — Generate test files for existing code or from a spec (not the TDD loop — use tdd). Any framework.
- Triggers: "generate tests", "write tests for", "生成测试", "生成测试代码", "补测试".
- Output: test files with a coverage decision matrix.

**`api-testing`** — API test strategies: contract, REST/GraphQL, integration.
- Triggers: "test API", "contract testing", "integration test", "API 测试", "接口测试", "契约测试".
- Output: test scaffolds + schemas. Refs: templates, schemas.

**`e2e-testing`** — End-to-end/browser tests: user journeys, form submission, runtime UI verification (Playwright by default, or equivalent).
- Triggers: "playwright", "e2e test", "browser test", "end-to-end", "端到端测试", "浏览器测试".
- Output: E2E test files. Refs: playwright-rules.

### 07-verify — review before merge
**`code-review`** — Two-axis review: Standards (conventions + smell baseline) and Spec (faithful to issue), as parallel sub-agents.
- Triggers: "review this", "code review", "before merge", "代码审查", "代码评审", "合并前审查".
- Output: verified findings report.

**`debugging`** — Disciplined diagnosis: build red loop → minimise → hypothesise → instrument → fix → regression-test.
- Triggers: "debug", "bug", "test failure", "unexpected behavior", "调试", "排查 bug", "读日志", "排查错误日志".
- Output: root cause + regression test. Refs: hitl-loop-template.

**`security-review`** — Security review of pending changes: secrets, auth, injection, access control, hardening.
- Triggers: "security review", "check for vulnerabilities", "安全审查", "安全审计", "漏洞检查".
- Output: a security findings report.

### 08-ship — deploy
**`shipping`** — Launch to production: checklist, feature flags, staged rollout, rollback, first-hour verify.
- Triggers: "ship", "deploy", "launch", "go live", "上线", "发布", "部署到生产".
- Output: a launch with rollback readiness.

**`git-workflow`** — Commit/branch/merge-conflict/guardrails/pre-commit. Resolves conflicts by intent — never `--abort`.
- Triggers: "commit", "merge conflict", "rebase", "pre-commit", "提交", "合并冲突", "分支管理".
- Output: clean commits / resolved conflict. Refs: block-dangerous-git, pre-commit-setup.

**`ci-cd`** — CI/CD pipelines and automation: build/test/deploy, pipeline design, strategies.
- Triggers: "CI pipeline", "GitHub Actions", "deployment strategy", "CI/CD", "流水线", "持续集成", "部署策略".
- Output: pipeline config + strategy.

**`deprecation-migration`** — Deprecate old code/APIs or migrate systems: staged paths preserving behavior.
- Triggers: "deprecate", "migrate", "sunset API", "弃用", "迁移", "升级依赖", "更新这个库", "upgrade dependency".
- Output: a migration plan (strangler/adapter/expand-contract).

**`oss-polish`** — Polish an OSS project's GitHub presence: README, topics, narrative, trending positioning.
- Triggers: "polish my repo", "开源项目美化", "优化项目展示".
- Output: a polished README + topics + narrative. Refs: badges, scripts.

### 09-operate — run it
**`observability`** — Add logs/metrics/alerts/instrumentation; make runtime behavior observable.
- Triggers: "add logging", "metrics", "alerting", "instrumentation", "加日志", "可观测性", "监控告警".
- Output: instrumentation + a pre-launch checklist. Refs: observability-checklist.

**`documentation-audit`** — Audit documentation drift; sync Swagger, feature docs, general docs to code.
- Triggers: "docs out of date", "documentation drift", "sync docs", "写文档", "写 README", "文档化这个功能", "文档同步".
- Output: synced docs. Refs: templates.

**`handoff`** — Hand off work to another session/agent: structured brief (context, decisions, next steps).
- Triggers: "handoff", "hand over", "交接", "移交工作". *User-typed only.*
- Output: a handoff brief (saved or launched as a background agent).

## Conventions

- **Plugin layout:** `.claude-plugin/plugin.json` declares all 33 skills in a `skills[]` array (nested `./skills/<phase>/<skill>` paths — preserves the 9-phase taxonomy).
- **Every skill:** folder with `SKILL.md` (uppercase); frontmatter `name` + `description` (+ optional `disable-model-invocation`); body sections When to use / Steps / Verify / References.
- **Multi-framework:** `AGENTS.md` (universal entry) + `.agents/` (invocation model, install block) + per-skill `agents/openai.yaml` (Codex adapter). User-invoked skills keep `disable-model-invocation` (Claude Code) and `allow_implicit_invocation: false` (Codex) in sync — the validator enforces this.
- **Shared references:** at plugin root `references/`, linked from skills as `${CLAUDE_PLUGIN_ROOT}/references/...` (portable across projects in Claude Code; other frameworks read them via repo-relative paths from `AGENTS.md`).
- **Ambient principles:** SessionStart hook (`hooks/session-start`) injects `engineering-principles.md` into every Claude Code session; other frameworks read it via `AGENTS.md`.
- **Validate:** `bash scripts/validate-skills.sh` (schema + manifest-sync + Codex-adapter + invocation-sync). Regenerate Codex adapters: `python scripts/gen-agents-yaml.py`.

## Provenance

Consolidated 83 → 33 from: 24 personal root skills + [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (24, MIT) + [mattpocock/skills](https://github.com/mattpocock/skills) (35, MIT). Originals kept locally under `archive/` (gitignored).
