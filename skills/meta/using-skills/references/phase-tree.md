# Phase Decision Tree

Full routing map for `using-skills`. Each branch ends in the concrete skill to
activate via the Skill tool. When a task fits more than one branch, walk them
in phase order. Skills are listed by name as they appear under
`<phase>/<skill>/SKILL.md`.

## Contents

- [How to read](#how-to-read)
- [The tree](#the-tree)
- [Typical sequences](#typical-sequences)
- [Routing heuristics](#routing-heuristics)

## How to read

Start at the top. Answer each question; follow the matching arrow to the next
question or the skill to invoke. When two skills both apply, the earlier phase
runs first.

## The tree

```
Task arrives
    │
    What phase is this work in?
    │
    ├── meta — authoring or routing skills themselves
    │   └── Author/edit/evaluate a skill? ─────────────→ skill-authoring
    │
    ├── 01 PRODUCT — shaping what to build
    │   ├── Vague idea, need to explore intent? ────────→ brainstorm
    │   ├── Need a spec / PRD — write, refactor, update? → spec
    │   └── Open-source strategy / growth / COSS? ──────→ oss-strategy
    │
    ├── 02 RESEARCH — learning before deciding
    │   ├── Deep multi-source / market / tech-selection? → research (3 modes)
    │
    ├── 03 DESIGN — shaping the system
    │   ├── High-level architecture / tech decisions / design audit? → architecture
    │   ├── Domain language / glossary / ADR? ──────────→ domain-modeling
    │   ├── API contracts / interface design? ──────────→ api-design
    │   ├── Module shape / seams / depth? ──────────────→ codebase-design
    │   ├── UI / component design? ─────────────────────→ frontend-design
    │   ├── Design ref images, then implement to match? → image-to-code
    │   ├── Brand / web / mobile design reference images? → imagegen
    │   ├── Retrieve real design refs (free public galleries)? → design-research
    │   ├── Data model / schema / entities / indexes? ─→ schema-design
    │   ├── Prompt / eval / LLM feature design? ────────→ prompt-engineering
    │   └── Throwaway code to answer a design question? → prototype
    │
    ├── 04 DEVELOP — writing the code
    │   ├── Slice-by-slice implementation? ─────────────→ implement
    │   ├── Execute via parallel/sequenced subagents? ──→ multi-agent-orchestration
    │   ├── Small change / rename / scaffold (no spec)? → implement (lightweight-changes ref)
    │   ├── Break a spec into verifiable tasks? ────────→ breakdown
    │   ├── Load the right context first? ──────────────→ context-engineering
    │   ├── Explain code / codebase tour? ─────────────→ context-engineering (code-explanation ref)
    │   ├── Internationalize / multi-locale / RTL? ─────→ i18n
    │   ├── Implement auth (login/sessions/JWT/OAuth)? → auth-implementation
    │   └── Design error-handling strategy (retry/circuit-breaker/fallback)? → error-handling
    │
    ├── 05 TUNE — improving working code
    │   ├── Cloud bill / spend too high? ───────────────→ cost-optimization
    │   ├── Measure then optimize hot paths? ───────────→ performance
    │   ├── Reduce complexity, preserve behavior? ──────→ simplify
    │   └── Restructure without changing behavior? ────→ refactoring
    │
    ├── 06 TEST — proving correctness
    │   ├── Red-green, test first? ─────────────────────→ tdd
    │   ├── Generate tests for a feature? ──────────────→ test-generation
    │   ├── API / contract / integration tests? ────────→ api-testing
    │   ├── Browser / end-to-end flows? ───────────────→ e2e-testing
    │   └── Capacity / load / breaking point? ─────────→ load-testing
    │
    ├── 07 VERIFY — checking the diff
    │   ├── Accessibility / WCAG conformance? ──────────→ a11y-review
    │   ├── Review the diff for bugs / cleanups? ───────→ code-review
    │   ├── Bug resists a first glance? ────────────────→ debugging
    │   ├── Just read an error log / triage? ───────────→ debugging (log-triage ref)
    │   ├── Security review of pending changes? ────────→ security-review
    │   └── Machine-detectable lint / static-analysis? → linting
    │
    ├── 08 SHIP — getting it out
    │   ├── Pre-launch checklist + rollback plan? ──────→ shipping
    │   ├── Atomic commits / branch hygiene? ───────────→ git-workflow
    │   ├── Automated quality gates? ───────────────────→ ci-cd
    │   ├── Retire old systems safely? ─────────────────→ deprecation-migration
    │   ├── Upgrade a dependency / framework version? ──→ deprecation-migration (dependency-upgrade ref)
    │   └── Polish OSS GitHub presence? ────────────────→ oss-polish
    │
    └── 09 OPERATE — running it
        ├── Logs / metrics / traces / alerts? ──────────→ observability
        ├── Docs drifted from code? ────────────────────→ documentation-audit
        ├── Write new docs from scratch? ───────────────→ documentation-audit (writing-docs ref)
        ├── Files read like edited many times? ─────────→ purity-audit
        ├── Production incident / on-call / postmortem? → incident-response
        └── Hand a session off to a colleague? ─────────→ handoff
```

## Typical sequences

Choose only steps needed for the task, reusing confirmed decisions:

- Clear edit: implement → relevant verification.
- Feature: spec when behavior is unresolved → architecture when design is consequential → implement → review.
- Bug: debugging with a real regression check → relevant review.
- Structural change: codebase-design when the boundary is undecided → refactoring → verification.
- Release: verified artifact → authorized Git/release operations → health checks.

## Routing heuristics

Match the problem, not an obligatory lifecycle stage. New code with clear requirements can go directly to implement.
Do not auto-invoke user-only brainstorm or handoff. TDD is a method within implementation, not a mandatory separate phase after implementation.
Multiple file changes do not imply unclear requirements. Route to spec only for consequential behavior ambiguity, and to architecture for consequential system choices.
If no skill adds useful guidance, use ordinary engineering judgment rather than force-fitting a workflow.
