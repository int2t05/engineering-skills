---
name: cost-optimization
description: Use when optimizing cloud spend — measure before you optimize: establish a cost baseline, identify the cost driver, then improve. Triggers on "cost", "cloud bill", "FinOps", "spend", "成本优化", "云账单", "费用". Not for latency tuning (use performance) or capacity/load validation (use load-testing).
---

# Cost Optimization

Spend is a metric with the same discipline as latency: measure a baseline, find the
dominant driver, change one thing, re-measure. A cost cut without a before/after
number is a guess. "Cheaper" is not a goal — "same behavior, lower bill, verified" is.

## When to use

- The cloud bill is rising without an obvious cause, or a specific service is over budget.
- Right-sizing resources, committing to reserved capacity, or cutting idle spend.
- Choosing between pricing models (on-demand vs reserved vs spot) for a workload.
- Building cost guardrails (budgets, alerts, per-team attribution) before spend grows.

**Not for:** latency tuning (use `performance`); capacity validation under load (use `load-testing`); deploying the cost dashboards themselves (use `observability`).

## Steps

### 1. Measure — establish a baseline with real billing data

Pull the last 1–3 months of actual spend from the billing system (AWS Cost Explorer, GCP Billing, Azure Cost Management), grouped by service and tag. A single number ("we spend $12k/mo") is not a baseline — you need the breakdown to know where the lever is. Note the unit economics: cost per request, cost per user, cost per job — the absolute number grows with the business; the unit cost is what optimization moves.

### 2. Identify the cost driver (not assumed)

Rank services by spend share. The top 1–2 services are almost always where the money goes — optimizing the long tail first is a classic misdirection. For each top service, classify the driver — see [references/cost-drivers.md](references/cost-drivers.md) for the symptom→cause map (over-provisioned compute, idle resources, egress/transfer, storage lifecycle, reserved-capacity gap).

### 3. Fix the specific driver

Change one thing at a time, same as performance. Common levers, in order of payoff:

- **Right-size** — drop the instance/container class to what the workload actually needs (check p95 CPU/memory against the current class).
- **Cut idle** — stop dev/staging outside hours, delete unattached volumes, expire old snapshots.
- **Commit** — reserved instances / savings plans / committed-use discounts for steady-state load; spot for interruptible batch.
- **Fix the architecture** — the highest-leverage and slowest: cache, batch, co-locate to cut egress, move cold storage tiers.

### 4. Verify — re-measure, keep or revert

Compare the next billing cycle (or a representative week) against the baseline. Same rules as performance: **neutral is a revert, not a keep** (you added complexity for no gain). **Correctness gates the metric** — if latency or reliability regressed, the cost cut failed even if the bill dropped.

### 5. Guard against regression

Record the change in an attempt ledger so the same cut isn't re-investigated. Set a budget alert at the new baseline + 20% so creep is caught early, not at month-end. Tag every resource with owner + environment so future attribution is automatic. For idle cuts (dev/staging schedules, unattached volumes), put a guard on re-provisioning — a policy/IaC rule or a tag-based alarm that flags the resource returning, so the cut persists rather than silently regrowing.

## Verify

- [ ] Baseline is a per-service breakdown from real billing data, not a single total
- [ ] The top 1–2 cost drivers were identified before any change was made
- [ ] One lever changed at a time; each has a before/after number
- [ ] Unit cost (per request/user/job) moved, not just the absolute bill
- [ ] Latency and reliability did not regress (correctness gates the metric)
- [ ] A budget alert guards the new baseline; idle-cut guards re-grow
- [ ] Changes recorded in the attempt ledger

**Red flags:** optimizing the cheap long tail while the top service is untouched; a cost cut with no before/after number; "we moved to spot" without a fallback for interruption; deleting resources to hit a short-term target with no guard against re-provisioning; a cut that regressed latency or p99 and was kept anyway.

**Output:** `COST.md` (optional) — attempt ledger of cost changes (kept + reverted), mirroring `PERF.md`. Project-level, so a future session doesn't re-investigate a closed lever.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, enforce simplicity, surgical scope)
- [references/cost-drivers.md](references/cost-drivers.md) — symptom→cause map for cloud spend: over-provisioning, idle resources, egress, storage lifecycle, reserved-capacity gaps, with per-platform levers
