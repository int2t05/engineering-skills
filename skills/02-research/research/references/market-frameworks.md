# Market Frameworks

Depth reference for the `research` skill, **market** mode. Structured frameworks for sizing a market, analyzing
competition, and positioning — the analysis layer that turns raw research into decisions. Complements
the skill's four research modes (investor/competitive/market-sizing/technology), which define *how* to
gather; this defines *how to structure the analysis*.

## Contents

- [1. TAM / SAM / SOM](#1-tam--sam--som)
- [2. SWOT](#2-swot)
- [3. PEST](#3-pest)
- [4. Porter's Five Forces](#4-porters-five-forces)
- [5. Competitive analysis — 6 steps](#5-competitive-analysis--6-steps)
- [6. Competitive feature matrix](#6-competitive-feature-matrix)
- [7. Positioning quadrant](#7-positioning-quadrant)
- [8. Direct competitor ≠ real opponent](#8-direct-competitor--real-opponent)

## 1. TAM / SAM / SOM

Three concentric circles that prevent "the market is huge" from substituting for "we can reach these
people." The market question is not how big — it's how reachable (product-principles §6).

| Metric | Definition | How to estimate |
|---|---|---|
| **TAM** (Total Addressable) | Everyone with the problem, anywhere | Total people × annual spend per person |
| **SAM** (Serviceable Addressable) | The slice your model can reach (geography, segment, channel) | TAM × serviceable ratio |
| **SOM** (Serviceable Obtainable) | What you can win in year 1 | SAM × 1-5% (first-year realistic share) |

**Two methods, sanity-check each against the other:**
- **Top-down:** start from industry total, narrow down ("$10B market, 1% = $100M").
- **Bottom-up:** count real reachable users × price ("10k target users × $100/yr = $1M").

If top-down is 50× bottom-up, one of your assumptions is fiction. The bottom-up number is usually the
honest one.

## 2. SWOT

Internal vs external, positive vs negative — the 2×2 that forces you to look both ways:

| | Helpful | Harmful |
|---|---|---|
| **Internal** | **Strengths** (what you do better) | **Weaknesses** (what you do worse) |
| **External** | **Opportunities** (market shifts in your favor) | **Threats** (market shifts against you) |

Use: pair each Strength with an Opportunity it can exploit; pair each Weakness with a Threat it
amplifies. A SWOT without these pairings is a list, not an analysis.

## 3. PEST

Macro-environmental forces beyond the industry — for market-entry and timing decisions:

- **P**olitical — regulation, trade policy, data sovereignty laws.
- **E**conomic — purchasing power, funding climate, exchange rates.
- **S**ocial — demographics, user attitudes, cultural norms.
- **T**echnological — infrastructure availability, platform shifts, AI capability curves.

PEST answers "is the environment ready?" — SWOT answers "how do we compete in it?" Use both.

## 4. Porter's Five Forces

Industry attractiveness — why some markets are structurally harder than others:

| Force | Question | High when |
|---|---|---|
| **Supplier power** | Can suppliers raise prices / cut quality? | Few suppliers, high switching cost |
| **Buyer power** | Can buyers demand lower price / more? | Few buyers, commodity product |
| **New entrants** | How easily can a competitor enter? | Low capital, low regulation, weak brand |
| **Substitutes** | Can a different solution replace you? | Alternative solves the same job cheaply |
| **Rivalry** | How intense is existing competition? | Many equal players, slow growth, high fixed cost |

A market with high forces on all five is structurally unattractive — you'll fight for thin margins
regardless of execution. Low forces = room to profit. Use before committing to a market, not after.

## 5. Competitive analysis — 6 steps

1. **Define the purpose** — positioning? pricing? feature gap? The purpose shapes everything downstream.
2. **Select competitors** — direct (same product) + indirect (same job, different solution). Include the
   workaround (product-principles §8).
3. **Set dimensions** — the comparison axes (price, UX, integrations, performance, trust, support).
4. **Collect** — product reality, not marketing copy. Use the product; read their docs, changelogs,
   support forums, reviews.
5. **Analyze** — fill the feature matrix; mark gaps and strengths; plot positioning.
6. **Output** — gaps you can exploit, strengths you must match, positions that are taken vs open.

## 6. Competitive feature matrix

| Feature | You | Competitor A | Competitor B | Workaround |
|---|---|---|---|---|
| (concrete capability) | ✓ / ✗ / partial | ✓ / ✗ / partial | ✓ / ✗ / partial | ✗ (usually) |

Always include the **workaround column** — what users do today without any product in this category.
The workaround is your real baseline. A feature your competitors all have but the workaround lacks is
table stakes (Kano Basic); a feature no one has is potential differentiation.

## 7. Positioning quadrant

Plot competitors on two axes that matter to users (e.g., price × professional-grade, simplicity × power,
speed × accuracy):

```
            High
     professional │  Competitor A
                 │        ●
                 │            ● Competitor B
                 │
        ─────────┼─────────  (your open position?)
                 │      ● You
                 │
          low    │
            ────────────────────
                 low      high
                      price
```

The open quadrant (unserved position) is your opportunity — if real users sit there and you can serve
them. Don't claim a position you can't hold; competitors will move to defend it.

## 8. Direct competitor ≠ real opponent

The product that looks like yours is rarely your real competition. The real opponent is what users do
instead — the spreadsheet, the manual process, the status quo (product-principles §8).

- "Like X but better" fails when users weren't using X anyway.
- The switching cost from the workaround (usually zero) is the cost you must beat.
- If your acquisition pitch is "better than [competitor]" but users use [workaround], the pitch misses
  the actual comparison they're making.
