---
name: architecture
description: Use when designing high-level system architecture, reviewing or auditing existing designs, or making architectural decisions — produces TECH docs and ADRs with evidence-grounded decisions (each cites real OSS or case references facing similar requirements) and a human-audit loop: draft → audit → confirmed → revised → mature. Triggers on "system design", "架构设计", "ADR", "scalability", "系统设计", "架构决策" — also when user says "这个技术方案怎么审计" / "技术决策要引用哪些参考".
---

# Architecture

Design system-level architecture: pick patterns, size components, choose datastores, and record
decisions as ADRs. Pragmatic trade-offs over theoretical purity. Core principle:
**evidence-grounded and auditable** — every decision cites real implementations that faced
similar requirements (never designed from nothing), and the document matures through a
human-audit loop: draft → human audit → confirmed → revised → mature.

## When to use

- Designing new system architecture, or reviewing/auditing an existing one
- Choosing between architectural patterns (monolith vs microservices, event-driven, serverless)
- Making technology choices that carry lock-in (database, message bus, auth provider)
- Planning for scalability or evaluating NFR trade-offs (performance, availability, cost)
- Writing Architecture Decision Records (ADRs)
- Triggers on "system design", "architecture review", "scalability", "ADR", "架构设计"

**Not for:** Code-level design patterns (use `simplify` or `codebase-design`), database-only design without system context, or feature-level API contracts (use `api-design`). Requirements/product-spec writing without system design (use `spec` — architecture takes the spec as input).

## Steps

### 1. Gather requirements (functional + non-functional)

Take the PRD (the `spec` output) as input. Collect functional requirements, constraints
(budget, timeline, team), and NFRs. Use the NFR checklist to make scalability, performance,
availability, security, reliability, and cost targets explicit — never assume "it should be
fast." Link each NFR to the goal it serves. _Verify: every NFR category has a concrete target
or an explicit "not applicable" decision recorded._

- Load `references/nfr-checklist.md` when gathering NFRs
- Load `references/system-design.md` for the full design template

### 2. Research references before designing

Reference-first: for every candidate pattern, datastore, or component, find real
implementations that faced similar requirements — OSS repos, engineering blogs, official case
studies, RFCs. A nameable reference item is mandatory; never design from nothing. If none is
at hand, research first and record the retrieval date. _Verify: every candidate carries ≥1
real reference with link, access date, and what matched vs differed from our constraints._

- Load `references/tech-audit-guide.md` for reference selection criteria and the evidence format

### 3. Evaluate architectural patterns

Match requirements to patterns. Don't pick microservices because they sound modern — pick the
pattern whose trade-offs match your team size, domain complexity, and scaling needs. Ground
each candidate in its references: what did they run, at what scale, what did they outgrow?

- Load `references/architecture-patterns.md` for the pattern comparison (monolith, modular monolith,
  microservices, serverless, event-driven, CQRS) with when-to-use criteria
- For each candidate: what it makes easy and what it makes hard; which references support it
  and where their constraints differ from ours

### 4. Design components and data layer

Design component interactions, data flow, and the data layer. Choose datastores per workload —
relational for transactions, document for flexible schemas, key-value for caching, time-series for
metrics, graph for relationships, search for full-text.

- Load `references/database-selection.md` for the database decision matrix
- Load `references/error-resilience.md` for the cross-cutting error-handling strategy — throw-vs-return conventions, error propagation across layers, retry/circuit-breaker/backoff, idempotency under retry, fallback UX, error-to-user-message mapping
- Produce high-level diagrams (Mermaid — see `${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md`).
  One figure answers one question; every figure carries a FIG ID, a title, a 1–2 sentence
  caption, and its linked components; branch flows show outcomes; the body stands without rendering
- Document failure modes and mitigations for each component

### 5. Record decisions as ADRs

Write an ADR when a decision is **hard to reverse**, **surprising without context**, and the
result of a **real trade-off**. Skip reversible or obvious ones — they clutter the log.

- Every ADR carries evidence: its References section names the real implementations consulted —
  what was adopted, what was adapted, and how our constraints differ. A bare link list is not evidence
- A minimal paragraph (context + decision + why + reference) is the default; most ADRs need nothing more
- Load `references/adr-template.md` for the expanded format (Status / Context / Decision /
  Consequences / Alternatives / References) when the trade-offs warrant recording in full
- Number sequentially: `docs/design/adr/0001-slug.md` — never renumber; superseded ADRs record their successor

### 6. Publish

Two layers: `docs/TECH.md` — project-level architecture overview (diagram, components, NFRs,
data layer), concise (mermaid-heavy), on main; `docs/vX.Y/tech.md` — the current version's
detailed architecture, on the version branch (falls back to `docs/TECH.md` alone for
single-version projects). Plus `docs/design/adr/NNNN-slug.md` per significant decision (shared
across versions). TECH.md is the overview; ADRs are the decision records — TECH.md references
the ADRs it depends on. Commit both — living documents.

### 7. Human-audit gate: audit → confirm → revise → mature

A TECH doc is not done when written — it's done when a human has audited it. Write an AUD
section into the doc (6–10 items covering reference authenticity, reference fit, alternatives,
NFR measurability, failure/recovery, consistency, cost & ops, reversibility — see
`references/tech-audit-guide.md`), each with required evidence and a close criterion. Status on
the first screen tracks the loop: 草案 draft → 人工审计 in-audit → 已确认 confirmed → 成熟
mature. Only the human moves the status. Findings drive revision; revisions preserve ADR
numbers and IDs; re-audit until every item closes. _Verify: audit feedback is incorporated or
explicitly overridden with rationale; all AUD items pass before the doc is called mature._

## Verify

- [ ] ADR written for every significant decision (hard to reverse, surprising, real trade-off)
- [ ] Every ADR and pattern/datastore candidate cites ≥1 real reference (link + access date) facing similar requirements — none designed from nothing
- [ ] Trade-offs documented for each choice — rejected alternatives with reasons, not just benefits
- [ ] Architecture diagram renders (Mermaid valid); figures have IDs/titles/captions; all components and data flows shown
- [ ] Every NFR category has a concrete target or explicit "not applicable", linked to the goal it serves
- [ ] Failure modes identified with mitigations; operational complexity and cost considered
- [ ] AUD section present (6–10 items) with evidence and close criteria; statuses tracked; unverified claims marked; no fabricated confirmations
- [ ] Status reflects the loop honestly (草案/人工审计/已确认/成熟); revisions preserved ADR numbers
- [ ] Human audit passed — every AUD item closed

**Red flags:** over-engineering for hypothetical scale; choosing technology without evaluating
alternatives; decisions without real references; ignoring operational costs; designing without
understanding NFRs; skipping security considerations; no ADRs for decisions that will be hard to
reverse; calling a doc done without human audit.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md](${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md) — Mermaid syntax for architecture diagrams
- [references/tech-audit-guide.md](references/tech-audit-guide.md) — reference-first discipline, the audit→confirm→revise→mature lifecycle, and the TECH-doc AUD catalog with table formats
- [references/nfr-checklist.md](references/nfr-checklist.md) — NFR categories (scalability, performance, availability, security, reliability, cost) with targets
- [references/architecture-patterns.md](references/architecture-patterns.md) — pattern comparison (monolith, microservices, event-driven, CQRS, serverless)
- [references/database-selection.md](references/database-selection.md) — database types and decision matrix
- [references/system-design.md](references/system-design.md) — full system design template
- [references/adr-template.md](references/adr-template.md) — ADR format, example, and naming convention
- [references/error-resilience.md](references/error-resilience.md) — throw-vs-return, error propagation, retry/circuit-breaker, idempotency, fallback UX, error-to-message mapping
