# Cost Observability

Depth reference for the `observability` skill. FinOps applied to cloud spend — treating cost as an
observable signal, not a quarterly surprise. The skill teaches you to instrument behavior; this
teaches you to instrument spend and act on it. Cost is an NFR recorded at design time
(`architecture/references/nfr-checklist.md`); this is the post-launch practice of tracking and
optimizing against it.

## 1. Cost as an observability problem

Cost is a lagging, aggregated signal — the monthly bill arrives weeks after the spend that caused
it. The discipline: make cost observable in near-real-time, attributed to its cause, so a spike is
detected the day it starts, not when the bill arrives.

| Cost signal | Granularity | Lag | Source |
|---|---|---|---|
| Monthly bill | Account-level | 2-4 weeks | Vendor invoice |
| Cost dashboard | Service/dimension | Hours-days | Cloud cost explorer |
| Per-request cost metric | Request-level | Real-time | App instrumentation |
| Anomaly alert | Dimension-level | Minutes-hours | Cost monitoring tool |

The goal: move left on this table. The bill is too late; per-request cost in real-time is the
target.

## 2. Cost attribution — tag everything

You can't optimize what you can't attribute. Every resource must map to a cost owner:

- **Resource tags** — every cloud resource tagged with `team`, `service`, `env`, `cost-center`.
  Enforce via policy (untagged resources are rejected at creation, not flagged later).
- **Dimensional breakdown** — dashboards slice spend by service, environment, team, region,
  resource type. A single "we spent $50k" number is useless; "$12k on staging compute, of which
  $8k is the search service" is actionable.
- **Shared resources** — allocate shared cost (load balancers, NAT gateways, shared DB) to the
  consuming services by a documented rule (traffic-weighted, even-split, or direct attribution
  where measurable).

## 3. Per-request cost metric

The highest-fidelity signal: what does each request cost to serve?

```
cost per request = (service spend in window) / (requests served in window)
```

Instrument this as a metric, not a calculation. Track it over time; a rising cost-per-request
means either traffic is falling (fixed cost spread thinner) or per-request resource use is rising
(regression). A falling cost-per-request with stable traffic means optimization worked.

For multi-tenant products, break down per-tenant: some tenants cost more to serve than they pay.
The per-tenant cost/revenue ratio is the unit economics of the business.

## 4. Cost anomalies — detect, don't just report

| Anomaly type | Signal | Cause |
|---|---|---|
| **Sudden spike** | Spend jumps > 30% day-over-day | New resource, runaway job, misconfigured auto-scaling, abuse |
| **Gradual creep** | Spend rising steadily over weeks | Traffic growth, data accumulation, forgotten resources |
| **Orphan spend** | Resources costing money but not in use | Untagged, forgotten dev/test instances, unattached volumes |
| **Ratio shift** | cost-per-request rising while traffic stable | Performance regression, inefficient query, over-provisioning |

Alert on anomalies the same way you alert on error-rate spikes — cost is a reliability signal too
(a runaway job that 10×'s spend is also a reliability incident). Page on sudden spikes; ticket on
gradual creep.

## 5. Optimization levers

Order of impact (highest first):

| Lever | How | Impact |
|---|---|---|
| **Right-size** | Match instance type to actual load (CPU/mem utilization < 40% → downsize) | 20-50% on compute |
| **Kill orphans** | Find unattached volumes, stopped-but-billed instances, forgotten dev envs | 5-15% of total |
| **Reserved/Savings plan** | Commit to steady-state usage for discount | 30-60% on committed baseline |
| **Spot/Preemptible** | Use spot for batchable, interruptible work | 60-90% on batch workloads |
| **Auto-scale down** | Scale to zero off-hours; min instances = actual min | 20-40% on spiky workloads |
| **Architecture** | Move to serverless for low-traffic; consolidate services sharing a host | Variable, largest long-term |
| **Data lifecycle** | Move cold data to cheaper storage tiers; delete expired data | 10-30% on storage |

Rules:
- **Right-size before reserving** — reserving an over-sized instance locks in the waste.
- **Measure before and after** — same window, same load. "We optimized" without numbers is vibes.
- **Revisit quarterly** — traffic and pricing change; last quarter's right-size is this quarter's
  waste.

## 6. FinOps culture

Cost is everyone's job, not just finance's:

- **Engineers see cost in dashboards** — alongside latency and error rate, not in a separate
  finance portal nobody opens.
- **PRs estimate cost impact** — a change that 2×'s per-request cost is a review finding, same as
  a change that 2×'s latency.
- **Budget per service** — each service owns a cost budget; exceeding it is the team's problem to
  fix, not finance's problem to report.
- **No surprise bills** — anomaly alerts mean the team knows before finance does.

The principle: cost is a first-class engineering signal, treated with the same rigor as latency and
reliability. A service that's fast and reliable but 5× over cost target is not healthy.
