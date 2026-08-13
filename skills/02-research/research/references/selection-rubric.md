# Selection Rubric

Depth reference for the `research` skill, **tech-selection** mode. The decision layer on top of the 10 evaluation
dimensions: weighted scoring, build-vs-buy, total cost of ownership (TCO), migration-cost estimation,
and the long-term-bet vs commodity distinction. The skill gathers evidence; this rubric turns it into a
defensible choice.

## 1. Weighted scoring model

The 10 dimensions are not equal. Weight them by what matters for *this* project, then score:

| Dimension | Weight (sum=100) | Candidate A | Candidate B | Candidate C |
|---|---|---|---|---|
| Capability fit | 20 | 4 / 5 | 3 / 5 | 5 / 5 |
| Integration cost | 15 | 3 | 5 | 2 |
| Maturity | 10 | 5 | 4 | 3 |
| Maintenance | 10 | 4 | 5 | 3 |
| License | 10 | 5 | 3 | 5 |
| Ecosystem | 10 | 4 | 5 | 2 |
| Performance | 10 | 3 | 4 | 5 |
| Security | 10 | 5 | 4 | 3 |
| Deployment complexity | 3 | 4 | 5 | 2 |
| Lock-in | 2 | 3 | 2 | 5 |
| **Weighted total** | | **3.95** | **4.10** | **3.35** |

Rules:
- **Weights are project-specific** — a regulated industry weights security/license higher; a prototype
  weights integration cost and speed higher. State the weights before scoring, not after.
- **Score on evidence, not stars** — a 5 means "verified in our context," not "the README says so."
- **The weighted total informs; it doesn't decide** — a candidate scoring 0.1 higher but locking you
  into a dying ecosystem loses. Use the matrix to surface trade-offs, then make the call explicitly.

## 2. Build vs buy

The decision tree — not "can we build it?" but "should we own this capability?"

```
Is this capability core to our product's differentiation?
├── Yes (strategic) ──→ Build, even if harder. Owning the core is the moat.
└── No (commodity) ──→ Is a mature solution available?
    ├── Yes ──→ Buy/adopt. Save effort for the core.
    └── No ──→ Is the gap bridgeable in reasonable time?
        ├── Yes ──→ Build (reluctantly), plan to replace when commodity appears.
        └── No ──→ Reconsider the product — you're solving a hard problem you don't own.
```

- **Core = differentiation** — the thing that makes users choose you (product-principles §5).
  Outsource the core and you outsource the moat.
- **Commodity = table stakes** — auth, logging, CI, email. Buy these; building them is burning time on
  non-differentiation.
- The trap: building a commodity because "it's just a few days of work." Maintenance, edge cases, and
  security accrue for years — the few days become hundreds.

## 3. Total cost of ownership (TCO)

License price is the tip of the iceberg. Real cost:

| Cost category | Often forgotten |
|---|---|
| **License / subscription** | Price increase at renewal; per-seat scaling |
| **Integration** | Initial wiring + the team's learning curve |
| **Maintenance** | Upgrades, patches, configuration drift |
| **Migration** | Cost to move off if it fails (see §4) |
| **Opportunity cost** | What the team could have built instead |
| **Operational** | Hosting, monitoring, support tickets, incident response |
| **Compliance** | Audit, data-residency, vendor-risk reviews |

Compute TCO over 3 years, not 1. A "free" OSS tool requiring a dedicated engineer to maintain costs
more than a $20k/yr managed service. A cheap tool that breaks at scale costs the incident plus the
migration.

## 4. Migration cost estimation

Before adopting, estimate the cost to *leave*. Low exit cost = safe to try; high exit cost = a bet.

| Factor | Low exit cost | High exit cost |
|---|---|---|
| Data format | Open standard (JSON, SQL) | Proprietary / locked |
| API surface | Standard (REST, GraphQL) | Vendor-specific SDK |
| Data volume | Small, exportable | Large, no bulk export |
| Team skill | Transferable | Tool-specific expertise |
| Integrations | Few, standard | Many, deeply wired |

A choice with high exit cost is not automatically wrong — but it's a commitment, not an experiment.
Stage the commitment: pilot in one service, evaluate, then expand. Never wire a high-lock-in tool
across the whole system on day one.

## 5. Long-term bet vs commodity technology

Not every dependency is the same kind of decision:

| | Long-term bet | Commodity technology |
|---|---|---|
| **Role** | Core to your product's future | Supports the product but isn't it |
| **Examples** | Primary data store, core framework, AI model | Linting, formatting, email, logging |
| **Decision depth** | Deep evaluation, TCO, migration cost, team alignment | "Does it work? Is it boring? Adopt." |
| **Wrong-choice cost** | Existential — expensive to reverse | Low — swap in a sprint |
| **Reversibility** | Design for it (open formats, abstraction) | Don't bother — just switch if needed |

Spend evaluation effort proportional to reversal cost. A week of evaluation on the primary database is
cheap insurance; a week on the linter is waste. The skill's ≥5-candidate search is for bets; commodities
need one or two.

## 6. Confidence and validation

Every selection comes with a confidence level — state it explicitly, then validate proportionally:

| Confidence | Why | Validation |
|---|---|---|
| **High** | Used it before in similar context; data backs claims | Ship it |
| **Medium** | Evidence is strong but untested in our context | Prototype the riskiest integration; spike |
| **Low** | Marketing claims, no hands-on, novel use | Migration spike + production trial on one service |

A Low-confidence selection that skips validation is a guess dressed as a decision. The validation plan
(prototype scope, success metrics, tests/benchmarks) is part of the selection, not a follow-up.
