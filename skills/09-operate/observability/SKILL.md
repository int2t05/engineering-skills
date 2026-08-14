---
name: observability
description: Use when adding logs, metrics, alerts, or instrumentation to a system — making runtime behavior observable and debuggable in production. Triggers on "add logging", "metrics", "alerting", "instrumentation", "加日志", "可观测性", "监控告警".
---

# Observability and Instrumentation

Code you can't observe is code you can't operate. Instrumentation is written alongside the feature, the same way tests are — if a feature ships without telemetry, the first user-reported bug becomes archaeology instead of a query.

## When to use

- Building a feature that will run in production (new service, endpoint, background job, external integration).
- A production incident took too long to diagnose because the system couldn't tell what happened.
- Adding or reviewing alerting rules.
- Reviewing a PR that adds I/O, retries, queues, or cross-service calls.

**Not for:** Diagnosing a live failure (use `debugging`) or profiling measured slowness (use `performance`). Observability is what makes those skills fast next time.

## Steps

### 1. Define "working" before instrumenting

Write down 2–4 questions an on-call engineer will ask about this feature. Every signal you add must answer one of them — if you can't name the questions, you'll log everything and learn nothing.

**If the service has no SLO, define one before setting alert thresholds.** An SLO turns "is it healthy?" from a feeling into a number — see [references/slo-methodology.md](references/slo-methodology.md) for SLI definition, error budgets, and burn-rate alerting.

### 2. Pick the right signal per question

- **Structured log** — "what happened in this specific case?" (per-event; grows with traffic)
- **Metric** — "how often / how fast, in aggregate?" (fixed per series; cheap to query)
- **Trace** — "where did time go across services?" (per-request; usually sampled)

Rule of thumb: metrics tell you **that** something is wrong, traces tell you **where**, logs tell you **why**.

### 3. Structured logging

Log events, not prose. Every line is a JSON object with a stable event name and machine-readable fields.

```typescript
// BAD: string interpolation — unqueryable, inconsistent
logger.info(`Payment ${id} failed for user ${userId} after ${n} retries`);

// GOOD: stable event name + structured fields
logger.warn({ event: 'payment_failed', paymentId: id, provider: 'stripe',
              errorCode: err.code, attempt: n }, 'payment failed');
```

Log levels: `error` (invariant broken, someone may act), `warn` (degraded but handled), `info` (significant business event), `debug` (off in production).

**Correlation IDs are mandatory.** Generate or accept a request ID at the system boundary and attach it to every log line, span, and outbound call — without it a single request can't be reconstructed from interleaved logs.

**Never log secrets, tokens, passwords, or full PII.** Telemetry pipelines are a classic data-leak path. Allowlist fields; don't log whole request bodies.

### 4. Metrics

For request-driven services instrument **RED** on every endpoint and external dependency: Rate, Errors, Duration (latency histogram, not average). For resources (queues, pools, hosts) use **USE**: Utilization, Saturation, Errors.

**Cardinality is the failure mode.** Every unique label combination is a separate time series. Labels must come from small, fixed sets (route template, status class, provider name). Never use user IDs, raw URLs, or error message text as labels — those belong in logs and traces.

Track averages never, percentiles always: p50/p95/p99 via histograms.

### 5. Distributed tracing

Use OpenTelemetry (vendor-neutral; auto-instrumentation covers HTTP, gRPC, common DB clients with near-zero code). Initialize before other imports. Add manual spans only around meaningful internal units of work (e.g. `applyDiscounts`, `chargeProvider`) with the attributes on-call will filter by. Propagate context across every async boundary — HTTP headers, queue message metadata — or the trace dies at the gap. Sample head-based at a low rate by default; keep 100% of errors if tail sampling is available.

### 6. Alerting

Alert on **symptoms users feel** (error rate, p99 latency, queue age), not on causes (CPU, disk, restarts) — cause-based alerts fire when nothing is wrong and miss failures you didn't predict.

Every alert must:
1. Be actionable — if the response is "ignore it, it self-heals", delete it.
2. Link to a runbook written **when you create the alert, before any incident** (minimum three lines: what it means, first query, escalation path). See [../incident-response/references/runbook-template.md](../incident-response/references/runbook-template.md) for the authoring structure — the alert author owns the runbook.
3. Have a threshold and duration justified by the SLO or historical data, not a guess.
4. Use one of two severities: **page** (user-facing, act now) or **ticket** (degradation, act this week).

### 7. Verify the telemetry itself

Instrumentation is code; it can be wrong. Trigger the paths and look at the actual output: force an error in staging and find it by correlation ID; send test traffic and confirm metric series appear with expected labels; follow one request end-to-end in the tracing UI with no broken spans; fire each new alert once (lower the threshold temporarily) and confirm it reaches the right channel with a working runbook link.

## Verify

- [ ] On-call questions for the feature are written down; each signal maps to one.
- [ ] All log output is structured JSON with stable event names and a correlation ID on every line.
- [ ] No secrets, tokens, or unredacted PII in any log line (spot-check actual output).
- [ ] RED metrics exist for every new endpoint and external dependency, with bounded label sets.
- [ ] Latency is a histogram; p95/p99 are queryable.
- [ ] A single request can be followed end-to-end in the tracing UI without broken spans.
- [ ] Every new alert is symptom-based, has a runbook link, and was test-fired once.
- [ ] An induced failure in staging was located via telemetry alone, without reading the source.

**Red flags:** a feature PR with retries, queues, or external calls and zero new telemetry; log lines built by string interpolation; no correlation ID on each line; metrics labeled with user IDs, raw URLs, or error text; latency tracked as an average with no percentiles; alerts firing daily and acknowledged without action; secrets or full request bodies in logs.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, enforce simplicity, surgical scope)
- [references/observability-checklist.md](references/observability-checklist.md) — at-a-glance instrumentation checklist + pre-launch gate
- [references/slo-methodology.md](references/slo-methodology.md) — SLI definition, error budgets, burn-rate alerting, SLO-based release gating
- [references/cost-observability.md](references/cost-observability.md) — FinOps: cost attribution, per-request cost, anomaly detection, optimization levers
- [../incident-response/references/runbook-template.md](../incident-response/references/runbook-template.md) — runbook authoring structure (write when you create the alert, not during the incident)
