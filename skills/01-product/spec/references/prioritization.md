# Prioritization

Depth reference for the `spec` skill. Frameworks for deciding what to build first: RICE, ICE, Kano,
MoSCoW, the Value×Feasibility matrix, and the true-need vs false-need check. No single framework fits
every stage — pick by signal quality.

## 1. RICE

The default when you have enough signal to score. Scores every item on four dimensions:

```
RICE = (Reach × Impact × Confidence) ÷ Effort
```

| Factor | Definition | Scale |
|---|---|---|
| **Reach** | How many users affected per period | Number (users/month, requests/day) |
| **Impact** | How much value per user on average | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **Confidence** | How sure you are of the other three | 100% = data-backed, 80% = team consensus, 50% = gut guess |
| **Effort** | Total person-time to ship | Include design + testing + support, not just coding |

Rules:
- **Effort includes everything** — design, QA, docs, post-launch support, not just engineering. Coding
  alone undercounts 2-3×.
- **Confidence penalizes guesses** — a high-impact, low-confidence item scores lower than a medium-impact,
  high-confidence one. This is the point: it pushes you to validate before betting.
- **Compare within a set, not across contexts** — RICE ranks items competing for the same resources.
  Cross-team RICE is noise.

## 2. ICE

RICE simplified for early-stage ideas where you cannot estimate Reach or Effort precisely:

```
ICE = Impact × Confidence × Ease
```

- **Ease** (1-5) replaces Effort-as-divisor — easier items score higher, same intent, less precision
  required.
- Use when every estimate is a guess (pre-MVP, greenfield). Switch to RICE once you have real data.

## 3. Kano model

Classifies features by how they affect satisfaction — guides *type* of investment, not just order.

| Type | Without it | With it | Strategy |
|---|---|---|---|
| **Basic** (must-have) | Dissatisfaction | No delight (expected) | Complete first — table stakes |
| **Performance** (linear) | Low satisfaction | Higher = better | Rank by RICE — more is better |
| **Excitement** (delight) | No complaints | Surprise delight | Use for differentiation — one or two, not many |

Strategy: ship all Basic first (their absence destroys the product), rank Performance by RICE, spend
Excitement budget on 1-2 signature differentiators. Over-investing in Excitement while Basic is broken
is a classic prioritization failure.

## 4. MoSCoW

Coarse bucketing for release scoping — decides what's in this release at all:

| Bucket | Meaning |
|---|---|
| **Must** | Without it, the release fails. Non-negotiable. |
| **Should** | High value, but the release succeeds without it. Include if time allows. |
| **Could** | Nice-to-have; include only if Must + Should are done with room to spare. |
| **Won't** | Explicitly out of this release. (This is a Non-Goal for this release — name it.) |

MoSCoW answers "what's in the release?" RICE answers "in what order within the release?" Use both:
MoSCoW sets the boundary, RICE orders inside it.

## 5. Value × Feasibility matrix

The 2×2 when you need a visual to align a team:

| | High feasibility | Low feasibility |
|---|---|---|
| **High value** | Do first | Worth the risk — schedule, de-risk |
| **Low value** | Only if trivial | Don't do |

Use **differentiation** (from the brainstorm evaluation rubric) as the tiebreaker between two items in
the same quadrant. High-value, high-feasibility, but zero differentiation = commodity work; do it only
if it's Basic (Kano).

## 6. True need vs false need

Before prioritizing, filter out false needs — things users say they want that don't survive contact
with behavior:

- [ ] Is there a real usage scenario (not a hypothetical)?
- [ ] What's the user's current alternative (workaround)?
- [ ] Is it high-frequency (daily/weekly), or a one-time request?
- [ ] Would the user pay real resources (money, time, data) — not just say they would?
- [ ] Does it solve a task (job-to-be-done), or is it a wanted feature?
- [ ] Is there behavioral data supporting it, or only stated intent?

A "need" failing most of these is a false need. It will surface in research as a request, get
prioritized by RICE (high Reach, high Impact, high Confidence — because the user asked!), and ship to
crickets. Filter before scoring.

## 7. Which framework when

| Stage | Signal quality | Use |
|---|---|---|
| Pre-MVP, greenfield | Everything is a guess | ICE + true-need filter |
| First release scoping | Some signal | MoSCoW (boundary) + Kano (type) |
| Iterating on live product | Real data | RICE (ordering) + Kano (differentiation budget) |
| Visual team alignment | Mixed | Value×Feasibility matrix + differentiation tiebreaker |

Switching frameworks as signal improves is correct — each is calibrated to a different certainty level.
