# Engineering Skills

> **Languages:** English | [中文](README.zh-CN.md)

A Claude Code plugin — **42 engineering skills** organized by the software
development lifecycle. Skills organized by phase of real work, from shaping a
vague idea to shipping it and running it.

Shared engineering principles are injected at every session start, so the
discipline is ambient — not something you have to remember to load. PM-side and UIUX skills
additionally link `product-principles.md` / `design-principles.md` as domain discipline layers.

Doc-producing skills split output into two layers: project-level (`docs/PRD.md` etc., concise,
on main) and version-level (`docs/vX.Y/prd.md` etc., detailed, on version branches). Single-version
projects fall back to `docs/` root. See `docs/skill-outputs.md` for the full product matrix.

## Install

**Claude Code (primary):**

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

For local development: `claude --plugin-dir /path/to/clone`.

**Other agents (Codex, Cursor, Cline, Continue, OpenCode, Windsurf…):**

Skill content is plain markdown. [`AGENTS.md`](AGENTS.md) is the universal
entry — read it first each session.

```bash
npx skills@latest add int2t05/engineering-skills
# or copy skills/ + references/ + AGENTS.md into your agent's instructions dir
```

## How to use

- **Auto-trigger:** skills activate when a task matches their description
  (English or Chinese — e.g. "技术选型", "性能优化", "深度检索").
- **Explicit call:** type `/skill-name` (`/tdd`, `/code-review`, `/debugging`).
- **Not sure which skill?** `/using-skills` routes the task to a phase.
- **Planning:** uses the harness's built-in plan mode, not a custom skill.

## Catalog — 42 skills by phase

### meta
**`using-skills`** — Router. Maps incoming work to the right skill across the 9 phases.
- Triggers: "which skill should I use", "route this task", "用哪个技能", "路由".

### 01-product — clarify what to build
**`brainstorm`** — One-question-at-a-time dialogue that sharpens a vague idea into a concrete proposal.
- Triggers: "brainstorm", "grill me", "interview me", "refine this idea", "头脑风暴", "帮我打磨想法", "盘问我". *User-typed only.*

**`spec`** — Writes a spec/PRD (objectives, structure, commands, code style, testing, boundaries) before any code.
- Triggers: "write spec", "create prd", "spec out", "写需求文档", "写规格", "需求文档".

**`oss-strategy`** — Open source strategy: business model, COSS, open core, commercialization, growth.
- Triggers: "open source strategy", "OSS 策略", "DevHunt", "开源策略", "开源商业模式".

### 02-research — investigate before building
**`research`** — Deep web research with source-backed investigation, producing a cited Markdown artifact.
- Triggers: "deep research", "source-backed investigation", "cited report", "深度调研", "深度检索", "调研报告", "调研转文档".

**`market-research`** — Market sizing, competitor comparisons, investor due diligence, industry intelligence.
- Triggers: "market sizing", "competitor analysis", "due diligence", "市场调研", "市场规模", "竞品分析".

**`tech-selection`** — Choose/compare a tech stack, library, framework, or repo for a concrete requirement.
- Triggers: "技术选型", "方案对比", "选哪个", "tech stack", "library comparison", "技术对比".

### 03-design — design before coding
**`architecture`** — High-level system architecture: NFRs, patterns, components, ADRs.
- Triggers: "system design", "架构设计", "ADR", "scalability", "系统设计", "架构决策".

**`domain-modeling`** — Build/sharpen a domain model: challenge terms, stress-test scenarios, update CONTEXT.md + ADRs.
- Triggers: "domain model", "ubiquitous language", "CONTEXT.md", "领域模型", "统一语言", "领域建模".

**`api-design`** — API/interface design: REST/GraphQL contracts, versioning, error models, ergonomics.
- Triggers: "design API", "REST contract", "GraphQL schema", "接口设计", "API 契约", "API 设计".

**`codebase-design`** — Deep modules, refactoring/deepening opportunities, testability.
- Triggers: "deep modules", "refactor architecture", "deepening", "深化模块", "重构架构", "代码库设计".

**`frontend-design`** — Distinctive, production-grade UI: color, typography, layout, interaction states.
- Triggers: "frontend", "UI", "design", "界面设计", "前端设计".

**`image-to-code`** — Image-first frontend pipeline — generate design reference images, analyze them deeply, then implement code to match.
- Triggers: "image to code", "设计图转代码", "图片实现", "从设计图实现".

**`brandkit`** — Brand identity image generation — logo concepts, identity boards, color palettes, typography, mockups for premium brand systems.
- Triggers: "brand kit", "品牌识别", "logo 设计", "品牌系统".

**`imagegen-web`** — Website design reference image generation — one horizontal image per section, premium art direction for landing pages and marketing sites. Images only, never code.
- Triggers: "web design image", "website mockup", "landing page image", "section image", "网站设计图", "网页参考图", "落地页配图".

**`imagegen-mobile`** — Mobile app screen and flow image generation — iOS/Android/cross-platform concepts with phone mockup framing. Images only, never code.
- Triggers: "mobile design image", "app screen image", "mobile mockup", "app flow", "移动端设计图", "app 屏幕图", "手机界面图", "移动端流程图".

**`schema-design`** — Data model design for a new feature or bounded context — entities, relationships, normalization, indexing, constraints, partitioning.
- Triggers: "data model", "schema design", "database design", "ER model", "数据模型", "表结构设计", "数据库设计".

**`prompt-engineering`** — Designing prompts, evals, or LLM-powered features — prompt architecture, model selection, guardrails, eval harnesses.
- Triggers: "prompt engineering", "LLM feature", "eval harness", "prompt design", "提示词工程", "LLM 特性", "prompt 设计".

**`prototype`** — Throwaway prototype to answer a design question (single HTML for logic, or toggleable UI variants).
- Triggers: "prototype", "compare layouts", "validate the interaction", "sketch out", "try this quickly", "build a demo", "原型", "试做", "试这个方案", "搭个快速 demo".

### 04-develop — implement
**`implement`** — Implement work from a spec/tickets: TDD at seams, typechecks, full suite, code-review, commit. Also covers lightweight changes (small edits, renames, scaffolding).
- Triggers: "implement", "build this", "code the feature", "实现", "编码", "改这个配置", "重命名", "搭项目骨架".

**`breakdown`** — Break a plan/spec into tracer-bullet tickets with blocking edges; decision map for huge work.
- Triggers: "break into tickets", "decompose", "wayfinder", "拆解任务", "拆票", "任务分解".

**`context-engineering`** — Assemble the right files, definitions, and prior decisions before implementing, or explain existing code.
- Triggers: "agent lacks context", "what files matter", "解释这段代码", "这个模块怎么工作", "带我过一遍代码库".

**`i18n`** — Internationalizing an application — message extraction, ICU/MessageFormat, locale routing, RTL layout, pluralization, locale-aware formatting.
- Triggers: "i18n", "localization", "l10n", "RTL", "国际化", "本地化", "多语言".

### 05-tune — optimize
**`performance`** — Measure before optimizing: profile, identify bottlenecks, improve.
- Triggers: "webperf", "performance regression", "慢", "性能优化", "性能调优".

**`simplify`** — Clarity over cleverness: remove speculative abstractions and dead complexity.
- Triggers: "simplify", "too complex", "refactor for clarity", "简化", "太复杂", "重构求清晰".

### 06-test — prove it works
**`tdd`** — Red-green-refactor, one vertical slice at a time.
- Triggers: "tdd", "test-driven", "red green refactor", "测试驱动开发", "红绿重构", "测试驱动".

**`test-generation`** — Generate test files for existing code or from a spec (not the TDD loop — use tdd). Any framework.
- Triggers: "generate tests", "write tests for", "生成测试", "生成测试代码", "补测试".

**`api-testing`** — API test strategies: contract, REST/GraphQL, integration.
- Triggers: "test API", "contract testing", "integration test", "API 测试", "接口测试", "契约测试".

**`e2e-testing`** — End-to-end/browser tests: user journeys, form submission, runtime UI verification (Playwright by default, or equivalent).
- Triggers: "playwright", "e2e test", "browser test", "end-to-end", "端到端测试", "浏览器测试".

**`load-testing`** — Capacity validation under load — generate realistic/adversarial traffic, find breaking points, characterize saturation, validate autoscaling.
- Triggers: "load test", "stress test", "capacity", "k6", "Locust", "压测", "压力测试", "容量测试".

### 07-verify — review before merge
**`code-review`** — Two-axis review: Standards (conventions + smell baseline) and Spec (faithful to issue), as parallel sub-agents.
- Triggers: "review this", "code review", "before merge", "代码审查", "代码评审", "合并前审查".

**`debugging`** — Disciplined diagnosis: build red loop → minimise → hypothesise → instrument → fix → regression-test. Also covers log triage.
- Triggers: "debug", "bug", "test failure", "unexpected behavior", "调试", "排查 bug", "读日志", "排查错误日志".

**`security-review`** — Security review of pending changes: secrets, auth, injection, access control, hardening.
- Triggers: "security review", "check for vulnerabilities", "安全审查", "安全审计", "漏洞检查".

### 08-ship — deploy
**`shipping`** — Launch to production: checklist, feature flags, staged rollout, rollback, first-hour verify.
- Triggers: "ship", "deploy", "launch", "go live", "上线", "发布", "部署到生产".

**`git-workflow`** — Commit/branch/merge-conflict/guardrails/pre-commit. Resolves conflicts by intent — never `--abort`.
- Triggers: "commit", "merge conflict", "rebase", "pre-commit", "提交", "合并冲突", "分支管理".

**`ci-cd`** — CI/CD pipelines and automation: build/test/deploy, pipeline design, strategies.
- Triggers: "CI pipeline", "GitHub Actions", "deployment strategy", "CI/CD", "流水线", "持续集成", "部署策略".

**`deprecation-migration`** — Deprecate old code/APIs, migrate systems, or upgrade dependencies: staged paths preserving behavior.
- Triggers: "deprecate", "migrate", "sunset API", "弃用", "迁移", "升级依赖", "更新这个库", "upgrade dependency".

**`oss-polish`** — Polish an OSS project's GitHub presence: README, topics, narrative, trending positioning.
- Triggers: "polish my repo", "开源项目美化", "优化项目展示".

### 09-operate — run it
**`observability`** — Add logs/metrics/alerts/instrumentation; make runtime behavior observable.
- Triggers: "add logging", "metrics", "alerting", "instrumentation", "加日志", "可观测性", "监控告警".

**`documentation-audit`** — Sync drifted docs to code, or write new documentation from scratch.
- Triggers: "docs out of date", "documentation drift", "sync docs", "写文档", "写 README", "文档化这个功能", "文档同步".

**`handoff`** — Hand off work to another session/agent: structured brief (context, decisions, next steps).
- Triggers: "handoff", "hand over", "交接", "移交工作". *User-typed only.*

**`incident-response`** — Production incident response — severity classification, containment, comms, rollback-vs-fix decisions, blameless postmortem.
- Triggers: "incident", "on-call", "page", "postmortem", "事故响应", "线上故障", "复盘".

## Validate

```bash
bash scripts/validate-skills.sh          # schema + manifest-sync + adapter-sync + invocation-sync
python scripts/gen-agents-yaml.py        # regenerate Codex adapters after editing frontmatter
```

MIT.

## Provenance

Original skill concepts adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) and [mattpocock/skills](https://github.com/mattpocock/skills), kept locally under `archive/` (gitignored) for reference. This pack is a ground-up rewrite fusing those concepts with systematic PM/UIUX principles.
