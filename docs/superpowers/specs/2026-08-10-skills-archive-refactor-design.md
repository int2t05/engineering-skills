# Skills Archive Refactor — Design Spec

- **Date:** 2026-08-10
- **Location:** `C:\Users\int2t\Desktop\skills` (in-place refactor)
- **Status:** Design — pending implementation plan

## 1. Purpose

Consolidate 83 agent skills scattered across three unmanaged collections (24 root standalone skills, 24 from `addyosmani/agent-skills`, 35 from `mattpocock/skills`) into one unified, normalized, lifecycle-organized collection of ~33 canonical skills — concise, engineering-grade, and free of the duplication and convention drift that currently exists.

The refactor distills the recurring engineering discipline shared across all three collections into a single referenced file, so each skill stays small and links to shared principles rather than repeating them.

## 2. Goals & Success Criteria

**Goals**
- One canonical skill per function (eliminate the 7-testing-skill, 10+-requirements-skill, 5-frontend-skill clusters).
- Uniform lifecycle taxonomy: 9 SDLC phases.
- Uniform format: `SKILL.md` (uppercase), minimal frontmatter, lean body, progressive disclosure via `references/`.
- Recurring engineering principles factored out once, linked everywhere.
- Plan routing delegated to Claude Code's built-in plan mode (no custom plan skill).

**Success criteria (verifiable)**
- Exactly 33 skill folders, each with a `SKILL.md`, organized under `meta/` + 9 numbered phase dirs.
- Every `SKILL.md` validates against the frontmatter schema in §6 (name + description + optional `disable-model-invocation` only).
- No two skills overlap in core function (audit via the matrix in §5).
- `archive/upstream-addyosmani/` and `archive/upstream-mattpocock/` contain the original repos untouched.
- Root `README.md` indexes all 33 skills in a 9-phase table.
- Every skill's `## References` links `references/engineering-principles.md`.

## 3. Non-Goals

- Rewriting skill content from scratch (we merge-dedupe + normalize, preserving each skill's provenance精华).
- Multi-agent/Codex/Cursor packaging (out of scope; this is a Claude Code skill collection). The `agents/openai.yaml` files from the mattpocock repo are dropped.
- Maintaining upstream update-ability (originals become read-only archive; we do not pull future upstream changes).
- Custom plan/workflow-engine skills (built-in plan mode handles planning).

## 4. Architecture

### 4.1 Directory Structure

```
C:\Users\int2t\Desktop\skills\
├── README.md                      # Catalog: 9-phase table + install + conventions
├── CLAUDE.md                      # Collection-level agent conventions
├── references/
│   ├── engineering-principles.md  # Distilled discipline (linked from every skill)
│   ├── skill-anatomy.md           # Format spec for writing skills
│   ├── definition-of-done.md      # Project-wide completion bar
│   ├── clean-code.md              # Uncle Bob coding discipline (loaded by implement + principles)
│   └── mermaid-diagrams.md        # Mermaid syntax + examples (loaded by architecture/code-review/etc.)
├── meta/
│   └── using-skills/SKILL.md      # Router / meta-skill
├── 01-product/                    # 3 skills
├── 02-research/                   # 3 skills
├── 03-design/                     # 6 skills
├── 04-develop/                    # 3 skills
├── 05-tune/                       # 2 skills
├── 06-test/                       # 4 skills
├── 07-verify/                     # 3 skills
├── 08-ship/                       # 5 skills
├── 09-operate/                    # 3 skills
├── archive/
│   ├── upstream-addyosmani/       # Original agent-skills repo (read-only)
│   └── upstream-mattpocock/       # Original skills repo (read-only)
└── docs/superpowers/specs/        # This spec + future implementation plan
```

### 4.2 Skill Folder Layout

Each skill is a folder `<phase>/<skill-name>/SKILL.md` (uppercase filename — the sole convention; fixes the lone lowercase `test-generator/skill.md`).

```
03-design/frontend-design/
├── SKILL.md                       # Lean core: when-to-use + steps + verify + refs
└── references/                    # Progressive disclosure — loaded only when needed
    ├── palettes.md                # 161 color palettes (from ui-ux-pro-max)
    ├── font-pairings.md           # 57 font pairings
    └── apple-hig.md               # Apple-platform specifics (from apple-hig-design)
```

**Progressive disclosure principle:** `SKILL.md` is the always-loaded lean core (target 15-150 lines, matching function complexity). Encyclopedic data, long examples, and platform-specific detail live in `references/` subfiles that the skill loads on demand. This keeps token cost low when the skill activates and preserves detail when it's needed.

## 5. The 9-Phase Taxonomy + Skill Roster (83 → 33)

| Phase | Skill | Merged from | `disable-model-invocation` |
|---|---|---|---|
| **meta** | `using-skills` | root find-skills + using-superpowers + addy using-agent-skills + matt ask-matt | — |
| **01-product** | `brainstorm` | root brainstorming + addy idea-refine + interview-me + matt grill-me + grilling + grill-with-docs + to-questionnaire | true (user-typed: "brainstorm" / "grill me") |
| | `spec` | root prd + addy spec-driven-development + matt to-spec | — |
| | `oss-strategy` | root open-source-strategy (business model, COSS, commercialization, growth) | — |
| **02-research** | `research` | root research-to-md + matt research | — |
| | `market-research` | root market-research | — |
| | `tech-selection` | root github-tech-selection-research | — |
| **03-design** | `architecture` | root architecture-designer (system-level + ADRs) | — |
| | `domain-modeling` | matt domain-modeling (ubiquitous language + CONTEXT.md) | — |
| | `api-design` | addy api-and-interface-design | — |
| | `codebase-design` | matt codebase-design + improve-codebase-architecture (root + matt → deepening modules) | — |
| | `frontend-design` | root frontend-design + ui-ux-pro-max + apple-hig-design + addy frontend-ui-engineering (palettes/HIG → references/) | — |
| | `prototype` | matt prototype (throwaway design-question prototypes) | — |
| **04-develop** | `implement` | matt implement + addy incremental-implementation + source-driven-development + doubt-driven-development | — |
| | `breakdown` | matt to-tickets + wayfinder (work → tickets; planning itself uses built-in plan) | — |
| | `context-engineering` | addy context-engineering | — |
| **05-tune** | `performance` | addy performance-optimization | — |
| | `simplify` | addy code-simplification | — |
| **06-test** | `tdd` | root test-driven-development + addy test-driven-development + matt tdd | — |
| | `test-generation` | root test-generator | — |
| | `api-testing` | root api-testing-patterns | — |
| | `e2e-testing` | root e2e-playwright-testing + addy browser-testing-with-devtools | — |
| **07-verify** | `code-review` | addy code-review-and-quality + matt code-review | — |
| | `debugging` | addy debugging-and-error-recovery + matt diagnosing-bugs | — |
| | `security-review` | addy security-and-hardening | — |
| **08-ship** | `shipping` | addy shipping-and-launch | — |
| | `git-workflow` | addy git-workflow-and-versioning + matt resolving-merge-conflicts + git-guardrails-claude-code + setup-pre-commit | — |
| | `ci-cd` | addy ci-cd-and-automation | — |
| | `deprecation-migration` | addy deprecation-and-migration + matt migrate-to-shoehorn | — |
| | `oss-polish` | root readme-generator + oss-project-polish + github-topics + repo-story-time (开源项目美化: README, topics, narrative story, trending repos) | — |
| **09-operate** | `observability` | addy observability-and-instrumentation | — |
| | `documentation-audit` | root documentation-audit | — |
| | `handoff` | matt handoff + claude-handoff | true (user-typed: "handoff") |

**Total: 33 skills** (1 meta + 32 phase).

### 5.1 Discarded (not merged — moved to archive or folded into references)

| Source skill | Disposition | Reason |
|---|---|---|
| superpowers `writing-plans` / plan sub-skills | Drop; route to built-in plan mode | User decision: use Claude Code plan mode |
| matt `wait-what` | Fold into `engineering-principles.md` (§Manage Confusion) | Same discipline, no standalone value |
| root `clean-code` | Fold into `references/clean-code.md` | Reference material (coding discipline), not a workflow skill; loaded on demand by `implement` + principles |
| root `mermaid-diagrams` | Fold into `references/mermaid-diagrams.md` | Reference material (syntax guide), not a workflow skill; loaded on demand by `architecture`/`code-review`/etc. |
| matt `writing-for-agents` | Fold into `references/skill-anatomy.md` | It is the skill-writing guide |
| matt `teach`, `scaffold-exercises`, `setup-ts-deep-modules`, `setup-matt-pocock-skills` | Archive | Non-SDLC or collection-specific |
| matt `writing-beats`, `writing-fragments`, `writing-shape`, `loop-me` | Archive (in-progress) | Content-authoring, not engineering SDLC |
| matt `triage`, `wizard` | Archive (issue-tracker / bash-wizard utilities) | Narrow, tracker-specific |

### 5.2 Key Dedup Decisions

- **TDD (3→1):** Three same-named `test-driven-development` skills → one `06-test/tdd`. Red-green-refactor loop (addy) + lean shell (matt) + anti-patterns reference (root) → `references/testing-anti-patterns.md`.
- **Requirements (10+→2):** Ten "interrogate/refine/spec" skills → `brainstorm` (dialogue) + `spec` (artifact). One-question-at-a-time is a technique within `brainstorm`, not a separate skill.
- **Frontend (5→2):** `frontend-design`/`ui-ux-pro-max`/`apple-hig-design`/`frontend-ui-engineering` → one `frontend-design` with encyclopedic data in `references/`; `prototype` stays separate (different intent: throwaway vs production).
- **Code review (4→2):** → `07-verify/code-review` + `05-tune/simplify`. `clean-code` becomes a shared `references/clean-code.md` (coding discipline loaded by `implement` + `engineering-principles`, not a standalone skill).
- **Architecture (5→4):** Split by altitude — `architecture` (system), `domain-modeling` (language), `api-design` (interface), `codebase-design` (modules). Avoids one 1000-line monster.
- **Meta (4→1):** Four routers → one `using-skills`.
- **Handoff (2→1):** matt `handoff` + `claude-handoff` (near-duplicate split across buckets) → one `09-operate/handoff`.

## 6. Skill Schema & Conventions

### 6.1 Frontmatter (minimal, enforced)

```yaml
---
name: kebab-case-name
description: Use when [trigger conditions]. [What it does]. [Optional: triggers on "中文短语".]
disable-model-invocation: true   # OPTIONAL — only for user-typed skills
---
```

**Allowed fields:** `name`, `description`, `disable-model-invocation` (optional).

**Removed (non-standard, unnecessary):** `license`, `metadata`, `category`, `priority`, `agents`, `dependencies`, `tags`, `validation`, `origin`, `allowed-tools`, `model`, `user-invocable`, `argument-hint`. Model/tool scoping, if ever needed, is set at collection level — never per-skill.

### 6.2 Body Structure (uniform, lean)

```markdown
# <Title>

## When to use
<2-4 trigger conditions, including Chinese trigger phrases where relevant>

## Steps
<numbered, each step verifiable>

## Verify
<concrete completion check — evidence, not "looks right">

## References
- [engineering-principles](../../references/engineering-principles.md)
- <skill-specific reference docs>
```

### 6.3 Naming
- Skill folders & `name:` field: `kebab-case`.
- Main file: `SKILL.md` (uppercase) — no exceptions.
- In-skill reference docs: `kebab-case.md`.
- Collection-level shared docs: `kebab-case.md` under top-level `references/`.

### 6.4 Language
- **English-primary** for all skill bodies and documentation (consistent with upstream repos, shareable).
- **Chinese trigger phrases preserved** in `## When to use` where they already exist (技术选型, 苹果UI设计, 开源项目美化, 生成测试, etc.) and added where a skill serves a Chinese-speaking workflow.

## 7. Engineering Principles — distilled once, linked everywhere

`references/engineering-principles.md` holds the recurring discipline endorsed across all three source collections and the user's own CLAUDE.md. Every skill links it via `## References` rather than inlining it.

1. **Surface assumptions before implementing** — list assumptions explicitly; ask for correction before proceeding. (addy "Surface Assumptions"; CLAUDE.md §1)
2. **Manage confusion actively** — stop, name the confusion, ask, wait. Absorbs matt `wait-what`. (CLAUDE.md §1)
3. **Push back when warranted** — no sycophancy; quantify the downside; propose an alternative; accept human override with full information. (addy "Push Back When Warranted")
4. **Enforce simplicity** — minimum code that solves the problem; abstractions must earn their complexity. (CLAUDE.md §2 "Simplicity First"; Purity Principle)
5. **Surgical scope** — touch only what you must; no unsolicited refactoring; match existing style. (CLAUDE.md §3)
6. **Verify, don't assume** — evidence before assertions; "seems right" is never sufficient. Backed by `definition-of-done.md`. (addy "Verify, Don't Assume"; CLAUDE.md §4)
7. **Plan with built-in plan mode** — no custom plan skill; use Claude Code's EnterPlanMode/ExitPlanMode. The spec is its input. (User decision)
8. **Goal-driven execution** — transform tasks into verifiable goals; loop until passed. (CLAUDE.md §4)

This is the "engineering principle that can be distilled from the task design" the user named — distilled once, referenced everywhere.

## 8. Migration Plan (high-level — detailed in implementation plan)

1. **Stage 0 — Scaffold & git init:** Initialize a git repo at `C:\Users\int2t\Desktop\skills` (user-approved). Create `references/`, `meta/`, 9 phase dirs, `archive/`, `docs/`. Write `engineering-principles.md`, `skill-anatomy.md`, `definition-of-done.md`, `clean-code.md`, `mermaid-diagrams.md`, root `README.md`, `CLAUDE.md`. First commit = scaffold + this spec.
2. **Stage 1 — Archive upstream:** Move `agent-skills/` → `archive/upstream-addyosmani/`, `skills/` → `archive/upstream-mattpocock/` (preserve git history).
3. **Stage 2 — Migrate root skills:** Move the 24 root standalone skills into their phase dirs (or archive), merging/deduping per §5.
4. **Stage 3 — Pull from archives:** Merge canonical content from the two archived repos into the 33 skills per §5.
5. **Stage 4 — Normalize:** Apply §6 schema to every `SKILL.md`; fix frontmatter, filename case, structure; extract encyclopedic content into `references/`.
6. **Stage 5 — Wire meta:** Write `meta/using-skills/SKILL.md` router with the 9-phase decision tree; ensure every skill links `engineering-principles.md`.
7. **Stage 6 — Verify:** Audit against §2 success criteria — count, schema, overlap, archive integrity, index.

Each stage produces a verifiable checkpoint (the success criteria in §2 apply per-stage).

## 9. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Merge loses provenance / a skill's best content | Each merged skill's `## References` or a `provenance.md` notes which source skills contributed; originals stay in `archive/` for diff. |
| `frontend-design` merge becomes a monster | Progressive disclosure: main `SKILL.md` ≤150 lines; palettes/fonts/HIG in `references/` loaded on demand. |
| Built-in plan mode lacks features the custom plan skill had | Principles file §7 documents the routing; if a gap appears, add a thin `references/planning-with-built-in-plan.md` rather than a new skill. |
| Working dir was non-git | User approved git init at Stage 0; the scaffold + spec form the first commit, and each subsequent migration stage is its own commit. |
| 33-skill count drifts during implementation | §2 success criterion enforces exactly 33; any addition/removal requires updating this spec. |

## 10. Resolved Decisions

- **Git:** Initialize a git repo at `C:\Users\int2t\Desktop\skills` at Stage 0. The scaffold + this spec form the first commit; each subsequent migration stage is its own commit.
- **github-topics / repo-story-time:** Fold into `08-ship/oss-polish` (开源项目美化) alongside `readme-generator` and `oss-project-polish` — not archived, not in `research`. They are GitHub-presence beautification: trending-topic lookup + commit-history narrative are part of making an OSS project look good publicly.

---

*Next step: transition to the `superpowers:writing-plans` skill to produce the detailed implementation plan from this spec.*
