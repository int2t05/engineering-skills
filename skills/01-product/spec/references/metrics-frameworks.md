# Metrics Frameworks

Depth reference for the `spec` skill. How to define success criteria that measure outcomes, not outputs:
the North Star metric, the AARRR funnel, retention curves, cohort analysis, the Hook Model for habit
formation, and A/B-testing discipline. Spec defines the metric up front; operate measures it.

## Contents

- [1. North Star metric](#1-north-star-metric)
- [2. AARRR funnel (Pirate Metrics)](#2-aarrr-funnel-pirate-metrics)
- [3. Retention curves](#3-retention-curves)
- [4. Cohort analysis](#4-cohort-analysis)
- [5. Hook Model](#5-hook-model)
- [6. A/B testing discipline](#6-ab-testing-discipline)
- [7. Data-driven loop](#7-data-driven-loop)
- [8. Vanity metrics warning](#8-vanity-metrics-warning)

## 1. North Star metric

One metric that represents users truly receiving value. Not revenue, not downloads — the thing that
says "a user got what they came for."

| Criterion | Pass | Fail |
|---|---|---|
| **Represents user value** | "messages sent that get a reply" (Slack) | "daily active users" (could be confused clicks) |
| **Measurable** | You can instrument it this week | Needs a quarter of data plumbing first |
| **Guides the team** | Improving it clearly means the product improved | Teams can game it without helping users |

Build a **metric tree**: North Star at the top, decomposed into sub-metrics each team owns (like a
monitoring dashboard drilling from overview to module). Every feature's success criteria trace up to a
branch of this tree — if a metric doesn't connect to the North Star, it's measuring activity, not value.

## 2. AARRR funnel (Pirate Metrics)

The user's journey from stranger to advocate. Most products die between Activation and Retention — the
"leaky bucket" where acquisition pours in but value never sticks.

| Stage | Question | Metric example |
|---|---|---|
| **Acquisition** | How do users arrive? | Signups per channel |
| **Activation** | Did they reach the "aha" moment? | % reaching first key action within N min |
| **Retention** | Do they come back? | D7 / D30 retention rate |
| **Revenue** | Do they pay? | MRR, ARPU, conversion to paid |
| **Referral** | Do they bring others? | Invites sent, viral coefficient |

Diagnose which stage breaks: pour acquisition into a leaky activation = waste. Fix the broken stage
before scaling the one before it.

## 3. Retention curves

The single most honest signal of product value. Plot % of cohort still active over time:

| Curve shape | Meaning |
|---|---|
| **Fast drop to near-zero** | No value found — users tried and left |
| **Drops then flattens** | Some users found repeat value; the plateau is your real user base |
| **Flat / rising** | Habitual product; retention is healthy |

A flattening curve at 30 days means the product has real users. A curve still declining at 90 days
means you're still bleeding — acquisition without retention is burning money to fill a leaky bucket.

## 4. Cohort analysis

Group users by signup period (week or month) and compare retention curves across cohorts:

```
Cohort      D1     D7     D14    D30
2025-W03    100%   42%    30%    25%
2025-W04    100%   45%    33%    28%   ← improved (onboarding change?)
2025-W05    100%   38%    25%    19%   ← regressed (bug in signup flow?)
```

Cohorts isolate the effect of changes — a rising D7 across recent cohorts means something you shipped
worked; a falling one means something broke. Aggregate retention hides these signals.

## 5. Hook Model

Habit formation loop (Nir Eyal, *Hooked*) — for products that need to become routine:

```
Trigger → Action → Variable Reward → Investment
```

- **Trigger** — external (notification, email) or internal (boredom, anxiety). Internal triggers are
  stickier.
- **Action** — the simplest possible behavior in anticipation of reward (Fitts's Law: make it easy).
- **Variable reward** — unpredictable outcomes are the core of habit formation. Predictable rewards
  extinguish; variable ones don't.
- **Investment** — the user stores value (content, data, reputation) that improves the product and
  raises switching cost.

**Ethical guardrail:** design beneficial habits, not regret-inducing addiction. A loop the user is
ashamed of is a bug, not a feature. Variable-reward manipulation without user benefit is extraction.

## 6. A/B testing discipline

Randomized experiment with a control group. The method for resolving prioritization debates with data
instead of opinions.

**Flow:** hypothesis → single core metric → design A/B versions → calculate sample size → random split →
run ≥ 7 days → statistical analysis → decision.

**Three iron rules:**
1. **One variable at a time** — changing headline + button + layout means you can't attribute the effect.
2. **Sufficient sample size** — calculate it before running; under-powered tests produce noise read as
   signal.
3. **Confidence ≥ 95% and run a full week** — p < 0.05 means "probability this result is pure luck is
   under 5%." Run a full week to absorb day-of-week variance; a 3-day test confounds the effect with
   "it was the weekend."

**When NOT to A/B:** the change is too small to move a metric, traffic is too low to reach significance,
or it's a critical bug fix (ship it — don't gate a fix on an experiment).

## 7. Data-driven loop

```
Track (instrument) → Observe (dashboard/funnel/retention) → Identify problem
→ Hypothesize → Experiment → Analyze → Decide
```

Build three things to run this loop:
- **Tracking plan** — every event, its properties, where it fires (decided before implementation, not
  bolted on after).
- **Funnel analysis** — where in AARRR users drop.
- **Retention analysis** — cohort curves over time.

Principle: **ask the business question first, then write the SQL.** "What's our D30 by channel?" is a
question; `SELECT ... ` is a means. Data without a question is a dashboard no one acts on.

## 8. Vanity metrics warning

Metrics that go up regardless of whether the product improved — they flatter without informing.

| Vanity | Better |
|---|---|
| Total downloads | Activation rate (did they use it?) |
| Registration count | D7 retention (did they come back?) |
| Page views | Conversion per page (did it work?) |
| Total users | Active users / paying users |

A metric you cannot act on (no decision changes based on it) is vanity. Replace it with one that
changes a decision.
