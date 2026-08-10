# Engineering Skills

> **Languages:** English | [中文](README.zh-CN.md)

A unified Claude Code plugin — **33 engineering skills** organized by the software
development lifecycle, with shared engineering principles injected at every session start.

Consolidated from three source collections (83 → 33): 24 personal root skills,
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (24, MIT), and
[mattpocock/skills](https://github.com/mattpocock/skills) (35, MIT). Originals kept
locally (gitignored) for provenance.

## Install

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

Or for local development: `claude --plugin-dir /path/to/clone`.

On install, a SessionStart hook injects the 8 engineering principles
([`references/engineering-principles.md`](references/engineering-principles.md)) as ambient
context — every session starts with the discipline loaded. Skills auto-trigger on their
description phrases, or invoke explicitly by name (`/tdd`, `/code-review`, `/brainstorm`).

## How it works

- **Auto-trigger:** 31 skills activate when a task matches their `description:` triggers (incl. Chinese phrases like "技术选型", "生成测试", "性能优化").
- **Explicit call:** type `/skill-name` (e.g. `/tdd`, `/debugging`). `brainstorm` and `handoff` are user-typed only (`disable-model-invocation: true`).
- **Routing:** unsure which skill fits? invoke `using-skills` — it maps the task to a phase.
- **Planning:** uses Claude Code's built-in plan mode, not a custom skill (principle §7).
- **Progressive disclosure:** each `SKILL.md` is a lean core; encyclopedic data lives in per-skill `references/` loaded on demand.

## Catalog — all 33 skills by phase

### meta
**`using-skills`** — Router. Maps incoming work to the right skill across the 9 phases.
- Triggers: session start, or "which skill should I use".
- Output: the routed skill activates.

### 01-product — clarify what to build
**`brainstorm`** — One-question-at-a-time dialogue that sharpens a vague idea into a concrete proposal.
- Triggers: "brainstorm", "grill me", "interview me", "refine this idea". *User-typed only.*
- Output: a proposal the user confirms; a spec becomes writable.

**`spec`** — Writes a spec/PRD (objectives, structure, commands, code style, testing, boundaries) before any code.
- Triggers: "write spec", "create prd", "spec out", "to spec".
- Output: a spec document covering 6 core areas.

**`oss-strategy`** — Open source strategy: business model, COSS, open core, commercialization, growth.
- Triggers: "open source strategy", "OSS 策略", "DevHunt", "developer tools directory".
- Output: strategy decisions (not GitHub beautification — that's `oss-polish`).

### 02-research — investigate before building
**`research`** — Deep web research with source-backed investigation, producing a cited Markdown artifact.
- Triggers: "deep research", "source-backed investigation", "cited report".
- Output: a cited Markdown file (`research/YYYY-MM-DD-<slug>.md`).

**`market-research`** — Market sizing, competitor comparisons, investor due diligence, industry intelligence.
- Triggers: "market sizing", "competitor analysis", "due diligence".
- Output: a decision-oriented research summary with source attribution.

**`tech-selection`** — Choose/compare a tech stack, library, framework, or repo for a concrete requirement.
- Triggers: "技术选型", "方案对比", "选哪个", "tech stack", "library comparison".
- Output: a comparison matrix + recommendation.

### 03-design — design before coding
**`architecture`** — High-level system architecture: NFRs, patterns, components, ADRs.
- Triggers: "system design", "架构设计", "ADR", "scalability".
- Output: ADR(s) + architecture diagram. Refs: adr-template, architecture-patterns, database-selection, nfr-checklist, system-design.

**`domain-modeling`** — Build/sharpen a domain model: challenge terms, stress-test scenarios, update CONTEXT.md + ADRs.
- Triggers: "domain model", "ubiquitous language", "CONTEXT.md".
- Output: a shared ubiquitous language doc + ADRs.

**`api-design`** — API/interface design: REST/GraphQL contracts, versioning, error models, ergonomics.
- Triggers: "design API", "REST contract", "GraphQL schema".
- Output: a contract spec (Hyrum's Law, One-Version Rule applied).

**`codebase-design`** — Deep modules, refactoring/deepening opportunities, testability.
- Triggers: "deep modules", "refactor architecture", "deepening".
- Output: a deepening-opportunities report; works through the one you pick.

**`frontend-design`** — Distinctive, production-grade UI: color, typography, layout, interaction states.
- Triggers: "frontend", "UI", "design", "界面设计".
- Output: working UI code. Refs: styles (18), palettes (12), font-pairings (31), ux-guidelines (232), apple-hig.

**`prototype`** — Throwaway prototype to answer a design question (single HTML for logic, or toggleable UI variants).
- Triggers: "prototype", "compare layouts", "validate the interaction".
- Output: a throwaway HTML file; the design question answered.

### 04-develop — implement
**`implement`** — Implement work from a spec/tickets: TDD at seams, typechecks, full suite, code-review, commit.
- Triggers: "implement", "build this", "code the feature".
- Output: committed, tested, reviewed code. Refs: source-verification, doubt-cycle.

**`breakdown`** — Break a plan/spec into tracer-bullet tickets with blocking edges; decision map for huge work.
- Triggers: "break into tickets", "decompose", "wayfinder".
- Output: tickets with blocking edges, or a decision map.

**`context-engineering`** — Assemble the right files, definitions, and prior decisions before implementing.
- Triggers: "agent lacks context", "what files matter".
- Output: a packed working context. Refs: context-strategies.

### 05-tune — optimize
**`performance`** — Measure before optimizing: profile, identify bottlenecks, improve.
- Triggers: "webperf", "performance regression", "慢", "性能优化".
- Output: a profile + targeted fix. Refs: bottlenecks, anti-patterns.

**`simplify`** — Clarity over cleverness: remove speculative abstractions and dead complexity.
- Triggers: "simplify", "too complex", "refactor for clarity".
- Output: simpler code preserving behavior. Refs: opportunities.

### 06-test — prove it works
**`tdd`** — Red-green-refactor, one vertical slice at a time.
- Triggers: "tdd", "测试驱动开发", "red green refactor", "红绿重构".
- Output: passing tests + behavior verified. Refs: test-strategy (Test Pyramid, test-double hierarchy), mocking, good-tests, testing-anti-patterns.

**`test-generation`** — Generate test files for existing code or from a spec (not the TDD loop — use tdd). Any framework.
- Triggers: "generate tests", "write tests for", "生成测试".
- Output: test files with a coverage decision matrix.

**`api-testing`** — API test strategies: contract, REST/GraphQL, integration.
- Triggers: "test API", "contract testing", "integration test".
- Output: test scaffolds + schemas. Refs: templates, schemas.

**`e2e-testing`** — End-to-end/browser tests: Playwright flows, form submission, DevTools-driven.
- Triggers: "playwright", "e2e test", "browser test", "end-to-end".
- Output: E2E test files. Refs: playwright-rules.

### 07-verify — review before merge
**`code-review`** — Two-axis review: Standards (conventions + smell baseline) and Spec (faithful to issue), as parallel sub-agents.
- Triggers: "review this", "code review", "before merge".
- Output: verified findings report.

**`debugging`** — Disciplined diagnosis: build red loop → minimise → hypothesise → instrument → fix → regression-test.
- Triggers: "debug", "bug", "test failure", "unexpected behavior".
- Output: root cause + regression test. Refs: hitl-loop-template.

**`security-review`** — Security review of pending changes: secrets, auth, injection, access control, hardening.
- Triggers: "security review", "check for vulnerabilities".
- Output: a security findings report.

### 08-ship — deploy
**`shipping`** — Launch to production: checklist, feature flags, staged rollout, rollback, first-hour verify.
- Triggers: "ship", "deploy", "launch", "go live".
- Output: a launch with rollback readiness.

**`git-workflow`** — Commit/branch/merge-conflict/guardrails/pre-commit. Resolves conflicts by intent — never `--abort`.
- Triggers: "commit", "merge conflict", "rebase", "pre-commit".
- Output: clean commits / resolved conflict. Refs: block-dangerous-git, pre-commit-setup.

**`ci-cd`** — CI/CD pipelines and automation: build/test/deploy, pipeline design, strategies.
- Triggers: "CI pipeline", "GitHub Actions", "deployment strategy".
- Output: pipeline config + strategy.

**`deprecation-migration`** — Deprecate old code/APIs or migrate systems: staged paths preserving behavior.
- Triggers: "deprecate", "migrate", "sunset API".
- Output: a migration plan (strangler/adapter/expand-contract).

**`oss-polish`** — Polish an OSS project's GitHub presence: README, topics, narrative, trending positioning.
- Triggers: "polish my repo", "开源项目美化", "优化项目展示".
- Output: a polished README + topics + narrative. Refs: badges, scripts.

### 09-operate — run it
**`observability`** — Add logs/metrics/alerts/instrumentation; make runtime behavior observable.
- Triggers: "add logging", "metrics", "alerting", "instrumentation".
- Output: instrumentation + a pre-launch checklist. Refs: observability-checklist.

**`documentation-audit`** — Audit documentation drift; sync Swagger, feature docs, general docs to code.
- Triggers: "docs out of date", "documentation drift", "sync docs".
- Output: synced docs. Refs: templates.

**`handoff`** — Hand off work to another session/agent: structured brief (context, decisions, next steps).
- Triggers: "handoff", "hand over". *User-typed only.*
- Output: a handoff brief (saved or launched as a background agent).

## Conventions

- **Plugin layout:** `.claude-plugin/plugin.json` declares all 33 skills in a `skills[]` array (nested `./skills/<phase>/<skill>` paths — preserves the 9-phase taxonomy).
- **Every skill:** folder with `SKILL.md` (uppercase); frontmatter `name` + `description` (+ optional `disable-model-invocation`); body sections When to use / Steps / Verify / References.
- **Shared references:** at plugin root `references/`, linked from skills as `${CLAUDE_PLUGIN_ROOT}/references/...` (portable across projects).
- **Ambient principles:** SessionStart hook (`hooks/session-start`) injects `engineering-principles.md` into every session.
- **Validate:** `bash scripts/validate-skills.sh` (schema + manifest-sync check).

## Provenance

Consolidated 83 → 33 from: 24 personal root skills + [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (24, MIT) + [mattpocock/skills](https://github.com/mattpocock/skills) (35, MIT). Originals kept locally under `archive/` (gitignored).
