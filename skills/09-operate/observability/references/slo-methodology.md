# SLO Methodology

Depth reference for the `observability` skill. The SLO layer above instrumentation: SLI definition,
error budgets, burn-rate alerting, and release gating. The skill teaches you to emit signals
(RED/USE, tracing, logs); this teaches you to close the loop from "what users feel" to "what the
error budget says about release cadence."

## 1. SLI / SLO / SLA — the hierarchy

| Term | Definition | Audience |
|---|---|---|
| **SLI** (Service Level Indicator) | A measurable signal of service health (request latency, error rate, availability) | Engineering — the raw signal |
| **SLO** (Service Level Objective) | The target you set on an SLI (99.9% of requests < 200ms over 28 days) | Engineering — the internal commitment |
| **SLA** (Service Level Agreement) | The contract with customers, looser than the SLO (99.5% or credits) | Business/legal — the external promise |

SLO is stricter than SLA on purpose: the error budget between SLO and SLA is your safety margin.
If SLO = 99.9% and SLA = 99.5%, you can burn 0.4% of requests before customers are owed anything.

## 2. Defining an SLI

A good SLI has four parts:

```
SLI = (good events) / (total events) over (window) measured at (measurement point)
```

- **Good events** — count of requests that met the bar (e.g. latency < 200ms, status < 500).
- **Total events** — all requests in the window.
- **Window** — the rolling window (28 days is standard; 7 days is more responsive).
- **Measurement point** — where you measure: at the load balancer? at the app? at the user? Measure
  as close to the user as possible; server-side SLIs miss client-side failures.

### Good vs bad SLIs

| Good SLI | Bad SLI |
|---|---|
| 99.9% of requests return < 200ms p99 | "Latency is low" |
| Error rate < 0.1% over 28 days | "Few errors" |
| Availability (successful requests / total) ≥ 99.95% | "Uptime" (what counts as up?) |
| % of queries returning correct results | "System is running" |

The bad SLIs are unmeasurable or gameable. The good ones are numeric, time-windowed, and tied to
user experience.

## 3. Error budget

The error budget is what SLOs buy you: a quantified allowance for unreliability.

```
SLO = 99.9% availability over 28 days
Error budget = 0.1% of requests can fail
  = 0.001 × (request volume × window)
  ≈ 43 minutes of downtime, or N failed requests
```

| SLO | Downtime budget (28 days) | Implication |
|---|---|---|
| 99% | ~6.7 hours | Low bar; users notice frequent outages |
| 99.9% | ~40 minutes | Standard for most services |
| 99.95% | ~20 minutes | High; needs redundancy + fast rollback |
| 99.99% | ~4 minutes | Very high; needs multi-region + automated failover |
| 99.999% | ~24 seconds | Extreme; expensive, only for critical infra |

The budget is a **resource to spend**, not a target to hit. Spending it on feature launches
(fast iteration, some risk) is valid. Burning it on preventable bugs is waste.

## 4. Burn rate

How fast you're consuming the error budget. Burns the budget in the window:

```
burn rate = (actual error rate) / (allowed error rate = 1 - SLO)
```

- Burn rate 1 = consuming budget at exactly the rate that exhausts it over the full window.
- Burn rate 2 = exhausting budget in half the window.
- Burn rate 10 = exhausting budget in 1/10 of the window — urgent.

### Multi-window multi-burn-rate alerting

Alert on burn rate across two windows — a short window (fast detection) confirmed by a long window
(avoid false positives):

| Alert | Short window (1h) | Long window (6h) | Meaning |
|---|---|---|---|
| **Page** (fast burn) | burn rate > 14.4 | burn rate > 6 | Budget exhausted in < 2 days if sustained |
| **Ticket** (slow burn) | burn rate > 3 | burn rate > 1 | Budget exhausted in < 30 days if sustained |

The two-window rule: page only if BOTH windows exceed threshold. A 1h spike that doesn't hold over
6h is noise; a 6h trend that didn't spike in the last 1h is already being addressed. Both together
mean "real and ongoing."

### Fast burn vs slow burn

| | Fast burn | Slow burn |
|---|---|---|
| **Pattern** | Sudden spike (deploy, outage) | Gradual drift (degradation, growth) |
| **Detection** | Short-window alert (minutes) | Long-window alert (hours/days) |
| **Response** | Page / rollback | Ticket / investigate next business day |
| **Cause** | Bad deploy, dependency outage | Capacity creep, query regression, data growth |

## 5. SLO-based release gating

The error budget gates release cadence:

- **Budget healthy** → ship freely; the budget absorbs the risk of a bad deploy.
- **Budget depleted** → freeze non-essential releases; focus on reliability until budget regenerates.
- **Budget near-depletion** → ship only fixes; no new risk.

This turns "should we ship?" from an opinion into a number. A team with a depleted budget shipping
features is violating the contract with users; a team with a healthy budget not shipping is
over-engineering reliability.

## 6. Reviewing SLOs

SLOs are not set-once. Review quarterly:

- **Too tight** (budget never spent, shipping slowed) → relax the SLO; you're over-investing in
  reliability.
- **Too loose** (budget always depleted, users complaining) → tighten the SLO; you're under-investing.
- **Wrong SLI** (SLI is green but users are unhappy) → the SLI doesn't capture user experience;
  redefine.
- **User behavior changed** (new feature, new scale) → the SLO may need recalibration.

A SLO that's never breached is as suspect as one always breached — the first means the target is
too conservative, the second means it's aspirational not real.
