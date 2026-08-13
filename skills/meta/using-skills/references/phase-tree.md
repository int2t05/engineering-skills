# Phase Decision Tree

Full routing map for `using-skills`. Each branch ends in the concrete skill to
activate via the Skill tool. When a task fits more than one branch, walk them
in phase order. Skills are listed by name as they appear under
`<phase>/<skill>/SKILL.md`.

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
    ├── 01 PRODUCT — shaping what to build
    │   ├── Vague idea, need to explore intent? ────────→ brainstorm
    │   ├── Need a spec / acceptance criteria? ─────────→ spec
    │   ├── Author/edit/evaluate a skill? ─────────────→ skill-authoring (meta)
    │   └── Open-source strategy / growth / COSS? ──────→ oss-strategy
    │
    ├── 02 RESEARCH — learning before deciding
    │   ├── Deep multi-source / market / tech-selection? → research (3 modes)
    │
    ├── 03 DESIGN — shaping the system
    │   ├── High-level system architecture? ────────────→ architecture
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
    │   └── Internationalize / multi-locale / RTL? ─────→ i18n
    │
    ├── 05 TUNE — improving working code
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
        ├── Production incident / on-call / postmortem? → incident-response
        └── Hand a session off to a colleague? ─────────→ handoff
```

## Typical sequences

A full feature often runs several phases in order:

```
brainstorm → spec → architecture → implement → tdd → code-review → simplify → git-workflow → shipping
```

A bug fix is shorter:

```
debugging → tdd → code-review → git-workflow
```

A greenfield effort too big for one session:

```
brainstorm → spec → breakdown → (implement per ticket) → ...
```

## Routing heuristics

- **Building new?** Start at `01-product` (`brainstorm` or `spec`), not `04-develop`.
- **Something broke?** `debugging` first, then `tdd` to lock the fix with a regression test.
- **Reviewing a diff?** `code-review`, then `simplify` if it's overcomplex.
- **Multiple skills fit?** Process skills (`brainstorm`, `debugging`, `code-review`)
  before implementation skills (`frontend-design`, `api-design`).
- **In doubt about the phase?** Default to the earliest phase that could apply —
  rework is cheaper upstream.
