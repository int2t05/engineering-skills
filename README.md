# Skills

A unified collection of **33 agent skills** organized by the software development
lifecycle. Each skill is a lean workflow with progressive disclosure; shared engineering
discipline lives in [`references/`](references/).

Consolidated from three source collections (83 → 33): 24 root skills plus
[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (24) and
[mattpocock/skills](https://github.com/mattpocock/skills) (35), preserved read-only under
[`archive/`](archive/).

## Catalog

### meta
| Skill | Description |
|---|---|
| [using-skills](meta/using-skills/SKILL.md) | Use when starting a session or deciding which skill applies. Maps incoming work to the right skill across the 9 SDLC phases. |

### 01-product
| Skill | Description |
|---|---|
| [brainstorm](01-product/brainstorm/SKILL.md) | Use before any creative work, or when the ask is underspecified. One-question-at-a-time dialogue that sharpens a vague idea into a concrete proposal. |
| [spec](01-product/spec/SKILL.md) | Use when starting a new project, feature, or significant change. Writes a spec/PRD covering objectives, structure, commands, code style, testing, and boundaries before any code. |
| [oss-strategy](01-product/oss-strategy/SKILL.md) | Use when the user wants open source strategy, OSS commercialization, open core, COSS, or open source growth/business model. |

### 02-research
| Skill | Description |
|---|---|
| [research](02-research/research/SKILL.md) | Use when the user asks for deep web research, source-backed investigation, or a cited Markdown research artifact. |
| [market-research](02-research/market-research/SKILL.md) | Use when the user wants market sizing, competitor comparisons, investor due diligence, or technology scans that inform business decisions. |
| [tech-selection](02-research/tech-selection/SKILL.md) | Use when choosing or comparing a technology stack, library, framework, or repository for a concrete requirement. Triggers on "技术选型", "方案对比", "选哪个". |

### 03-design
| Skill | Description |
|---|---|
| [architecture](03-design/architecture/SKILL.md) | Use when designing high-level system architecture or making architectural decisions. Produces ADRs, diagrams, and evaluates scalability/NFR trade-offs. |
| [domain-modeling](03-design/domain-modeling/SKILL.md) | Use when building or sharpening a project's domain model — challenging terms, stress-testing with scenarios, updating CONTEXT.md and ADRs. |
| [api-design](03-design/api-design/SKILL.md) | Use when designing APIs or interfaces — REST/GraphQL contracts, versioning, error models, interface ergonomics. |
| [codebase-design](03-design/codebase-design/SKILL.md) | Use when designing deep modules, finding refactoring or deepening opportunities, or making a codebase more testable and AI-navigable. |
| [frontend-design](03-design/frontend-design/SKILL.md) | Use when building web components, pages, or applications with distinctive, production-grade design quality. Triggers on "frontend", "UI", "界面设计". |
| [prototype](03-design/prototype/SKILL.md) | Use when a design question is best answered by a throwaway prototype — a single HTML file for state/logic, or toggleable UI variations. |

### 04-develop
| Skill | Description |
|---|---|
| [implement](04-develop/implement/SKILL.md) | Use when implementing the work described by a spec or tickets. Drives TDD at pre-agreed seams, typechecks, and closes with code-review before committing. |
| [breakdown](04-develop/breakdown/SKILL.md) | Use when breaking a plan, spec, or conversation into tracer-bullet tickets, each declaring its blocking edges. |
| [context-engineering](04-develop/context-engineering/SKILL.md) | Use when the agent needs better context — assembling the right files, definitions, and prior decisions before implementing. |

### 05-tune
| Skill | Description |
|---|---|
| [performance](05-tune/performance/SKILL.md) | Use when optimizing performance. Measure before you optimize — profile, identify bottlenecks, then improve. Triggers on "慢", "性能优化". |
| [simplify](05-tune/simplify/SKILL.md) | Use when the code is too complex. Clarity over cleverness — removes speculative abstractions and earns-its-cost structures. |

### 06-test
| Skill | Description |
|---|---|
| [tdd](06-test/tdd/SKILL.md) | Use when implementing any feature or bugfix, before writing implementation code. Red-green-refactor loop, one vertical slice at a time. |
| [test-generation](06-test/test-generation/SKILL.md) | Use when asked to generate or write tests for a feature or bugfix. Language-agnostic. Triggers on "generate tests", "生成测试". |
| [api-testing](06-test/api-testing/SKILL.md) | Use when testing APIs or designing API test strategies — contract testing, REST/GraphQL, integration testing. |
| [e2e-testing](06-test/e2e-testing/SKILL.md) | Use when writing end-to-end or browser tests — Playwright flows, form submission, user journeys, DevTools-driven testing. |

### 07-verify
| Skill | Description |
|---|---|
| [code-review](07-verify/code-review/SKILL.md) | Use when reviewing code before merge. Two-axis review: Standards (repo conventions + smell baseline) and Spec (faithful to the originating issue). |
| [debugging](07-verify/debugging/SKILL.md) | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Disciplined diagnosis loop. |
| [security-review](07-verify/security-review/SKILL.md) | Use when reviewing changes for security — secrets, auth, injection, access control, hardening. |

### 08-ship
| Skill | Description |
|---|---|
| [shipping](08-ship/shipping/SKILL.md) | Use when deploying or launching to production. Faster is safer — checklist-driven launch with rollback readiness. |
| [git-workflow](08-ship/git-workflow/SKILL.md) | Use when committing, branching, resolving merge or rebase conflicts, or setting up git guardrails and pre-commit hooks. |
| [ci-cd](08-ship/ci-cd/SKILL.md) | Use when working on CI/CD pipelines and automation — build, test, deploy automation, pipeline design. |
| [deprecation-migration](08-ship/deprecation-migration/SKILL.md) | Use when deprecating old code or APIs, or migrating to a new system. Staged deprecation paths and migration strategies. |
| [oss-polish](08-ship/oss-polish/SKILL.md) | Use when polishing an open source project's GitHub presence — README, topics, commit-history narrative, trending positioning. Triggers on "开源项目美化". |

### 09-operate
| Skill | Description |
|---|---|
| [observability](09-operate/observability/SKILL.md) | Use when adding logs, metrics, alerts, or instrumentation — making runtime behavior observable in production. |
| [documentation-audit](09-operate/documentation-audit/SKILL.md) | Use when documentation drift is detected. Audits the codebase and syncs Swagger, feature docs, and general documentation. |
| [handoff](09-operate/handoff/SKILL.md) | Use when handing off work to another session or agent. Produces a structured handoff brief. |

## Conventions

- **Every skill** is a folder with `SKILL.md` (uppercase). See [`references/skill-anatomy.md`](references/skill-anatomy.md) for the format spec.
- **Frontmatter:** `name` + `description` (+ optional `disable-model-invocation: true` for user-typed skills). Nothing else.
- **Every skill** links [`references/engineering-principles.md`](references/engineering-principles.md) — the 8 distilled principles, applied across all phases.
- **Progressive disclosure:** `SKILL.md` is the lean, always-loaded core; encyclopedic data lives in per-skill `references/` loaded on demand.
- **Planning** uses Claude Code's built-in plan mode (`EnterPlanMode`/`ExitPlanMode`), not a custom skill. See principle §7.
- **Validate** the whole collection: `bash scripts/validate-skills.sh`

## Archive

[`archive/upstream-addyosmani/`](archive/upstream-addyosmani) and
[`archive/upstream-mattpocock/`](archive/upstream-mattpocock) hold the original source
repos (read-only, file content preserved) for provenance and diffing. Never edit them.
