---
name: architecture
description: Use when designing high-level system architecture, reviewing existing designs, or making architectural decisions — produces ADRs, architecture diagrams, and evaluates scalability/NFR trade-offs. Triggers on "system design", "架构设计", "ADR", "scalability", "系统设计", "架构决策".
---

# Architecture

Design system-level architecture: pick patterns, size components, choose datastores, and record
decisions as ADRs. Pragmatic trade-offs over theoretical purity — document what you chose, what you
rejected, and why.

## When to use

- Designing new system architecture or reviewing an existing one
- Choosing between architectural patterns (monolith vs microservices, event-driven, serverless)
- Making technology choices that carry lock-in (database, message bus, auth provider)
- Planning for scalability or evaluating NFR trade-offs (performance, availability, cost)
- Writing Architecture Decision Records (ADRs)
- Triggers on "system design", "architecture review", "scalability", "ADR", "架构设计"

**When NOT to use:** Code-level design patterns (use `simplify` or `codebase-design`), database-only design without system context, or feature-level API contracts (use `api-design`).

## Steps

### 1. Gather requirements (functional + non-functional)

Collect functional requirements, constraints (budget, timeline, team), and NFRs. Use the NFR
checklist to make scalability, performance, availability, security, reliability, and cost targets
explicit — never assume "it should be fast." _Verify: every NFR category has a concrete target or
an explicit "not applicable" decision recorded._

- Load `references/nfr-checklist.md` when gathering NFRs
- Load `references/system-design.md` for the full design template

### 2. Evaluate architectural patterns

Match requirements to patterns. Don't pick microservices because they sound modern — pick the
pattern whose trade-offs match your team size, domain complexity, and scaling needs.

- Load `references/architecture-patterns.md` for the pattern comparison (monolith, modular monolith,
  microservices, serverless, event-driven, CQRS) with when-to-use criteria
- For each candidate: write down what it makes easy and what it makes hard

### 3. Design components and data layer

Design component interactions, data flow, and the data layer. Choose datastores per workload —
relational for transactions, document for flexible schemas, key-value for caching, time-series for
metrics, graph for relationships, search for full-text.

- Load `references/database-selection.md` for the database decision matrix
- Load `references/error-resilience.md` for the cross-cutting error-handling strategy — throw-vs-return conventions, error propagation across layers, retry/circuit-breaker/backoff, idempotency under retry, fallback UX, error-to-user-message mapping
- Produce a high-level architecture diagram (Mermaid preferred — see
  `${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md`)
- Document failure modes and mitigations for each component

### 4. Record decisions as ADRs

Write an ADR for every significant decision — architectural shape, integration patterns,
technology choices with lock-in, boundary/scope decisions, deliberate deviations from the obvious
path. Skip ADRs for reversible or obvious decisions.

- Load `references/adr-template.md` for the ADR format and example
- Each ADR: Context, Decision, Consequences (positive/negative/neutral), Alternatives Considered
- Number sequentially: `docs/design/adr/0001-slug.md`

**Output:** Two layers:
- `docs/TECH.md` — project-level architecture overview (diagram, components, NFRs, data layer),
  concise (mermaid-heavy), on main.
- `docs/vX.Y/tech.md` — the current version's detailed architecture, on the version branch.
  Falls back to `docs/TECH.md` alone for single-version projects.
Plus `docs/design/adr/NNNN-slug.md` for each significant decision (shared across versions).
TECH.md is the overview; ADRs are the decision records — TECH.md references the ADRs it depends on.

### 5. Review with stakeholders

Validate the design with stakeholders before finalizing. If review fails, return to step 3 with
recorded feedback. _Verify: review feedback is incorporated or explicitly overridden with rationale._

## Verify

- [ ] ADR written for every significant decision (hard to reverse, surprising, real trade-off)
- [ ] Architecture diagram renders (Mermaid syntax valid; all components and data flows shown)
- [ ] Every NFR category addressed with a concrete target or explicit "not applicable"
- [ ] Trade-offs documented for each pattern/technology choice — not just benefits
- [ ] Failure modes identified with mitigations
- [ ] Operational complexity and cost considered, not just functional fit

**Red flags:** over-engineering for hypothetical scale; choosing technology without evaluating
alternatives; ignoring operational costs; designing without understanding NFRs; skipping security
considerations; no ADRs for decisions that will be hard to reverse.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md](${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md) — Mermaid syntax for architecture diagrams
- [references/nfr-checklist.md](references/nfr-checklist.md) — NFR categories (scalability, performance, availability, security, reliability, cost) with targets
- [references/architecture-patterns.md](references/architecture-patterns.md) — pattern comparison (monolith, microservices, event-driven, CQRS, serverless)
- [references/database-selection.md](references/database-selection.md) — database types and decision matrix
- [references/system-design.md](references/system-design.md) — full system design template
- [references/adr-template.md](references/adr-template.md) — ADR format, example, and naming convention
- [references/error-resilience.md](references/error-resilience.md) — throw-vs-return, error propagation, retry/circuit-breaker, idempotency, fallback UX, error-to-message mapping
