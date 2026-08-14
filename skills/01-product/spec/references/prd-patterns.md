# PRD Patterns

Depth reference for the `spec` skill. PRD structure, user-story format, acceptance-criteria writing,
the INVEST criteria, success-criteria reframing, Non-Goals, and the anti-patterns that make PRDs fail
to function as a shared source of truth.

## Contents

- [1. PRD structure](#1-prd-structure)
- [2. User-story format](#2-user-story-format)
- [3. Acceptance criteria as executable tests](#3-acceptance-criteria-as-executable-tests)
- [4. INVEST criteria for stories](#4-invest-criteria-for-stories)
- [5. Success-criteria reframing](#5-success-criteria-reframing)
- [6. Non-Goals](#6-non-goals)
- [7. PRD anti-patterns](#7-prd-anti-patterns)
- [8. PRD vs vision](#8-prd-vs-vision)

## 1. PRD structure

A PRD is an interface specification + acceptance checklist for the business side. It is not a feature
list — every section traces to a decision the team needs to make.

| Section | Content | Why it exists |
|---|---|---|
| **Background & goals** | The problem, who has it, why now. Links to research/discovery. | Anchors every later decision; without it, scope drifts |
| **User stories** | What each user type needs to accomplish (story format, below) | Frames work as user value, not features |
| **Feature details** | Rules, boundaries, flow per feature — the spec proper | The negotiable middle; what gets built |
| **Data tracking** | Events, properties, funnels to instrument | Decided up front so tracking ships with the feature |
| **Non-functional** | Performance, a11y, security, i18n constraints | The constraints that shape implementation |

If a section has nothing to say, say why explicitly ("no perf constraint — internal tool, <50 users")
rather than omitting it. An omitted section is an unresolved question.

## 2. User-story format

```
As a [role], I want [action], so that [value].
```

The third clause — `so that [value]` — is the part that prevents feature-factory thinking. If you
cannot state the value, the story is a feature in search of a problem. Cut it or reframe it.

- **Role**: a real user type, not "the user" (admin vs end-user vs API consumer have different needs).
- **Action**: the capability, not the implementation ("export CSV" not "add a button that calls exportCsv()").
- **Value**: the outcome the user gets, not the metric you get.

## 3. Acceptance criteria as executable tests

AC mirrors TDD: write the assertions before the implementation. Use Given/When/Then:

```
Given [initial state / precondition]
When [the user takes this action]
Then [this observable outcome occurs]
```

- **Given** — the starting state (logged in, cart has 2 items, on checkout page).
- **When** — the action (clicks "Remove" on item A).
- **Then** — the observable result (item A disappears, subtotal updates, cart shows 1 item, event
  `cart.item_removed` fires).

Each criterion is falsifiable: there is a state where it fails. "The page looks good" is not a
criterion; "the empty cart shows a link to continue shopping within 100ms" is. If you cannot write
Given/When/Then, the requirement is not yet specific enough — go back and sharpen it.

## 4. INVEST criteria for stories

A story is ready to build when it passes INVEST:

| Letter | Criterion | Fails when |
|---|---|---|
| **I**ndependent | Can be built/shipped without blocking on another story | "Do A, then B, then C" as one story |
| **N**egotiable | The *what* is fixed; the *how* is open to the implementer | Spec dictates the implementation |
| **V**aluable | Delivers user value on its own (or is an explicit enabler) | "Refactor the DB" with no user-facing change |
| **E**stimable | The team can estimate effort within a 2× band | Unknown tech, undefined scope |
| **S**mall | Fits in one sprint / one session of focused work | "Build the whole checkout flow" |
| **T**estable | Has acceptance criteria that can pass or fail | "Make it intuitive" |

A story failing INVEST is not ready — split it, sharpen it, or move it to discovery.

## 5. Success-criteria reframing

Vague goals → testable metrics. The reframe is the spec's most leveraged step.

| Vague | Testable |
|---|---|
| "make the dashboard faster" | "LCP < 2.5s on 4G; initial load < 500ms; interactions < 100ms" |
| "improve onboarding" | "new user reaches first key action in < 60s; activation rate ≥ 40%" |
| "better search" | "top result relevant for 90% of test queries; p99 search latency < 200ms" |
| "more engaging" | "D7 retention ≥ 25%; sessions/user/day ≥ 1.5" |

The testable version is falsifiable — you can tell when it's done. The vague version is an aspiration
that never resolves.

## 6. Non-Goals

Non-Goals make scope trade-offs explicit. A Non-Goal is not "we'll do this later" — it is "we are
deliberately not doing this, and here is why."

```
## Non-Goals
- Delivery logistics — expensive, not the core problem; partner with existing tools instead.
- Customer acquisition — that's the platform's game; we serve existing customers.
- Mobile app — web-first; mobile is a later phase gated on retention.
```

Without Non-Goals, scope expands to absorb every reasonable suggestion. With them, "should we add X?"
has a default answer: does X serve the chosen user and job, or is it a Non-Goal asserting itself?

## 7. PRD anti-patterns

- **Feature list without goals** — 20 features, no problem statement. Every feature is unchallengeable
  because there's no goal to test it against.
- **No acceptance criteria** — "build a settings page." Done when? Builds that never converge.
- **Solution embedded in problem** — "users need a chatbot" (solution) instead of "users can't get
  answers fast enough" (problem). Locks in one solution before alternatives are considered.
- **Vanity success metrics** — "1M downloads." Downloads ≠ value; retention and activation do.
- **No boundaries** — missing Always/Ask-first/Never. Implementer guesses at every judgment call.
- **No Non-Goals** — scope is "everything the user mentioned." Inevitable drift.
- **Spec as contract not living doc** — written once, never updated. Decisions made after the spec
  live only in code; the spec rots into a lie.

## 8. PRD vs vision

| | PRD | Vision |
|---|---|---|
| **Scope** | One feature or project | The whole product, multi-version |
| **Horizon** | This sprint / this build | 1-3 years |
| **Question** | What are we building now and why? | Where is this product going? |
| **Artifact** | `docs/PRD.md` | `ROADMAP.md` |
| **Changes** | Living, updated on decision changes | Stable; revisited per release |

A PRD without a vision drifts feature to feature. A vision without PRDs never ships. The `brainstorm`
skill produces the vision (`ROADMAP.md`); the `spec` skill produces the PRD.
