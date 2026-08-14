# SLO Implementation

Depth reference for the `observability` skill. The implementation layer beneath the SLO
methodology: Prometheus recording rules, alerting rules, error-budget queries, and review
cadence. The skill's `references/slo-methodology.md` covers the theory (SLI definition,
error budgets, burn-rate math); this covers the rules you commit to the repo.

## Contents

- [1. Recording rules — precompute the SLI](#1-recording-rules--precompute-the-sli)
- [2. Alerting rules — multi-window multi-burn-rate](#2-alerting-rules--multi-window-multi-burn-rate)
- [3. Error budget queries](#3-error-budget-queries)
- [4. Dashboards](#4-dashboards)
- [5. Review cadence](#5-review-cadence)

## 1. Recording rules — precompute the SLI

The SLI is computed continuously, not queried on demand. Recording rules evaluate the SLI
at fixed intervals and store the result — dashboards and alerts read the precomputed
series, not raw metrics.

```yaml
# slo-rules.yaml — recording rules
groups:
- name: slo
  interval: 30s
  rules:
  # SLI: success rate over 5m (good / total)
  - record: slo:request_success_rate:5m
    expr: |
      sum(rate(http_requests_total{status!~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)

  # SLI: latency compliance — % of requests < 200ms over 5m
  - record: slo:latency_compliance:5m
    expr: |
      sum(rate(http_request_duration_seconds_bucket{le="0.2"}[5m])) by (service)
      /
      sum(rate(http_request_duration_seconds_count[5m])) by (service)

  # Error rate (complement of success rate)
  - record: slo:error_rate:5m
    expr: 1 - slo:request_success_rate:5m

  # Replicate at longer windows for multi-window alerting
  - record: slo:error_rate:1h
    expr: 1 - avg_over_time(slo:request_success_rate:5m[1h])
  - record: slo:error_rate:6h
    expr: 1 - avg_over_time(slo:request_success_rate:5m[6h])
  - record: slo:error_rate:24h
    expr: 1 - avg_over_time(slo:request_success_rate:5m[24h])
```

### Why recording rules

- **Query cost**: dashboards and alerts read precomputed series, not raw histograms.
- **Consistency**: every alert and dashboard uses the same SLI definition — change it in
  one place.
- **Cardinality control**: the `by (service)` label keeps series bounded; the SLI has one
  series per service, not per request.

## 2. Alerting rules — multi-window multi-burn-rate

Alert on burn rate across two windows — a short window (fast detection) confirmed by a
long window (false-positive suppression). Page only if both exceed threshold.

```yaml
# slo-alerts.yaml
groups:
- name: slo-alerts
  rules:
  # PAGE: fast burn — budget exhausted in < 2 days
  # SLO 99.9% → allowed error rate 0.1% → burn thresholds
  #   1h: 14.4× allowed → 1.44%   |   6h: 6× allowed → 0.6%
  - alert: SLOFastBurn
    expr: |
      (slo:error_rate:1h > 14.4 * 0.001)
      and
      (slo:error_rate:6h > 6 * 0.001)
    for: 2m
    labels:
      severity: page
      service: "{{ $labels.service }}"
    annotations:
      summary: "Fast burn — {{ $labels.service }} error budget at risk"
      description: "Error rate 1h={{ $value | humanizePercentage }} exceeds 14.4× allowed"
      runbook: "https://runbooks.example.com/slo-fast-burn"

  # TICKET: slow burn — budget exhausted in < 30 days
  #   6h: 3× allowed → 0.3%   |   24h: 1× allowed → 0.1%
  - alert: SLOSlowBurn
    expr: |
      (slo:error_rate:6h > 3 * 0.001)
      and
      (slo:error_rate:24h > 1 * 0.001)
    for: 15m
    labels:
      severity: ticket
      service: "{{ $labels.service }}"
    annotations:
      summary: "Slow burn — {{ $labels.service }} error budget draining"
      runbook: "https://runbooks.example.com/slo-slow-burn"
```

### The thresholds (for SLO 99.9%)

| Alert | Short window | Long window | Burn rate | Budget exhausted in |
|---|---|---|---|---|
| Page (fast) | 1h > 14.4× | 6h > 6× | 14.4 / 6 | < 2 days |
| Ticket (slow) | 6h > 3× | 24h > 1× | 3 / 1 | < 30 days |

Both windows must exceed — a 1h spike that doesn't hold over 6h is noise. Adjust the
multipliers for your SLO: replace `0.001` with your allowed error rate (1 - SLO).

### Alert annotations are mandatory

Every SLO alert must link to a runbook. The alert without a runbook is noise that trains
on-call to ignore pages. See
[../incident-response/references/runbook-template.md](../incident-response/references/runbook-template.md)
for the runbook structure.

## 3. Error budget queries

Dashboards need to show the budget, not just the error rate — the budget is the decision
signal for release gating.

```promql
# Remaining error budget over 28 days (as a percentage)
1 - (slo:error_rate:24h * 28)

# Remaining error budget in minutes (for SLO 99.9% → 40.3 min/month)
40.3 * (1 - slo:error_rate:24h)

# Budget exhaustion forecast — days until budget hits zero at current burn rate
28 / (slo:error_rate:24h / 0.001)
```

### Budget states

| Budget remaining | State | Action |
|---|---|---|
| > 50% | Healthy | Ship freely |
| 25–50% | Caution | Ship with care; monitor post-deploy |
| 0–25% | At risk | Ship only fixes; freeze features |
| < 0% | Depleted | Freeze all releases; focus on reliability |

## 4. Dashboards

The SLO dashboard has four panels, no more:

1. **SLI trend** — success rate and latency compliance over 28 days, with the SLO line.
2. **Error budget** — remaining budget as a percentage, with the 0% line.
3. **Burn rate** — current burn rate (1h, 6h, 24h) with the page and ticket thresholds.
4. **Error budget burn-down** — budget consumed over the window, trending toward 0.

Avoid the "wall of metrics" — if a panel doesn't answer "is the service meeting its SLO?"
or "when will the budget run out?", it doesn't belong on this dashboard.

## 5. Review cadence

SLOs drift. Review quarterly:

| Signal | Diagnosis | Action |
|---|---|---|
| Budget never spent | SLO too tight | Relax the SLO (e.g. 99.9% → 99.5%) |
| Budget always depleted | SLO too loose, or system unreliable | Tighten SLO or fix the reliability issues |
| SLI green but users unhappy | Wrong SLI — doesn't capture user experience | Redefine the SLI (measurement point, good-event criteria) |
| No alerts fire | Burn-rate thresholds too high | Lower thresholds; verify recording rules are active |
| Alerts fire too often | Burn-rate thresholds too low, or noisy service | Raise thresholds; or fix the noise source |

### Review checklist (quarterly)

- [ ] SLI definition still matches user-perceived health
- [ ] SLO target still matches business expectations
- [ ] Error budget spent on intended risk (launches), not preventable bugs
- [ ] Alerts fired in the quarter were actionable (not noise)
- [ ] Recording rules active (no stale series)
- [ ] Runbooks linked from alerts are current
