# UX Research

Depth reference for the `frontend-design` skill. Methods for understanding users before designing
(user research) and validating the design after (usability testing). This extends `frontend-design`'s
range into the discovery phase that precedes visual design. For product-side discovery (problem
validation, JTBD, opportunity trees), see the `brainstorm` skill's `discovery-methods.md`.

## Contents

- [1. Research vs testing — two phases](#1-research-vs-testing--two-phases)
- [2. User interviews (the Mom Test, UX variant)](#2-user-interviews-the-mom-test-ux-variant)
- [3. Personas](#3-personas)
- [4. Journey maps](#4-journey-maps)
- [5. Empathy maps](#5-empathy-maps)
- [6. Usability testing — task-based](#6-usability-testing--task-based)
- [7. The 5-user rule (Nielsen)](#7-the-5-user-rule-nielsen)
- [8. Think-aloud pitfalls](#8-think-aloud-pitfalls)
- [9. Heuristic evaluation (pre-test)](#9-heuristic-evaluation-pre-test)
- [10. When to research vs test](#10-when-to-research-vs-test)

## 1. Research vs testing — two phases

| | User research (before design) | Usability testing (after design) |
|---|---|---|
| **Question** | Who are the users? What do they need? | Can they use what we built? |
| **When** | Discovery, before specs/design | After prototype or build |
| **Methods** | Interviews, observation, personas, journey maps | Task-based tests, think-aloud, heuristic eval |
| **Output** | Understanding that shapes the design | Evidence the design works (or doesn't) |

Skipping research → designing for imagined users. Skipping testing → shipping unvalidated assumptions.
Both are required; they happen at different times.

## 2. User interviews (the Mom Test, UX variant)

The same Mom Test discipline from `discovery-methods.md` applies — ask about past behavior, not future
opinion. For UX specifically:

- **Observe, don't just ask** — watch users attempt the task in their real environment. Where do they
  hesitate? What workaround do they reach for? Observation surfaces what interviews miss (users
  rationalize; behavior doesn't).
- **Context matters** — a user in their office with their actual data reveals different friction than
  a user in a test lab with sample data.
- **Record the workflow** — note the tools they switch between, the copy-paste cycles, the "I always
  have to do X first" rituals. These are the friction points your design can eliminate.

## 3. Personas

Personas summarize research findings into a shared, memorable model of who you're designing for.

| Good persona | Bad persona |
|---|---|
| Based on real interviews | Invented from imagination |
| Behavior and goals first | Demographics first |
| 1-3, distinct from each other | 8, all vaguely similar |
| Names a specific job-to-be-done | "Wants a good experience" |

Structure:
```
Name: [memorable, not "User 1"]
Role: [their job / context]
Goals: [what they're trying to accomplish]
Frustrations: [what blocks them today]
Behavior: [how they currently work — the workaround]
Tech comfort: [novice / intermediate / expert]
```

Rules:
- **Personas are a communication tool, not a deliverable** — they exist so the team aligns on *who*.
  A persona no one references is dead weight.
- **Behavior > demographics** — "manages 200 SKUs manually in a spreadsheet" is useful; "female, 34,
  suburban" is usually not (unless culture/age genuinely shapes the task).
- **Don't design for the persona, design for the behavior the persona represents.**

## 4. Journey maps

The user's experience across time — stages, actions, emotions, pain points, opportunities (see
`design-foundations.md` §Information Architecture for the IA-journey connection):

| Stage | Action | Touchpoint | Emotion | Pain | Opportunity |
|---|---|---|---|---|---|
| Aware | Hears about tool | Referral / search | Curious | "Is this real?" | Social proof on landing |
| Try | Signs up | Onboarding | Hopeful → confused | Too many setup steps | Guide to first value fast |
| Use | Daily task | Main UI | Enabled | None (if designed well) | Power features surface |
| Leave | Stops using | (silence) | Indifferent | Forgot it exists | Re-engagement trigger |

Journey maps connect research (what users do/feel) to design (where to intervene). They surface the
emotion dips that need design attention — a flat journey map usually means you haven't researched
enough.

## 5. Empathy maps

A simpler synthesis than personas — four quadrants capturing what a user segment says/thinks/does/feels:

```
     SAYS            │   THINKS
  "This takes too    │   "There must be a
   long every time"  │    better way"
  ───────────────────┼──────────────────
     DOES            │   FEELS
  Workarounds in     │   Frustrated at
  spreadsheet,       │   repetition;
  copy-paste cycles  │   relieved when done
```

Empathy maps are fast (a workshop can produce one in an hour) and surface tensions — what users *say*
vs what they *do* often diverges, and that gap is the design opportunity. (product-principles §2:
behavior is data, statements are emotion.)

## 6. Usability testing — task-based

The core method: watch real users attempt specific tasks on the design.

**Procedure:**
1. **Define tasks** (not steps) — "book a flight to Tokyo next Tuesday," not "click the book button."
   Tasks state the goal; the user finds the path.
2. **Recruit 5 users** from the target segment (see §7 — 5 is usually enough).
3. **Think-aloud protocol** — ask users to narrate what they're thinking as they go. "I'm looking for
   the calendar... I expect it under... oh, it's here."
4. **Observe, don't help** — resist the urge to guide. Where they struggle is the finding.
5. **Record** the session (screen + audio) for later analysis.
6. **Analyze** — note where users hesitated, failed, took the wrong path, or expressed confusion.
   Patterns across users = real problems; one-off issues = lower priority.

**What to fix:** the places multiple users struggled, not the places one user was confused. If 4 of 5
couldn't find checkout, that's the design; if 1 of 5 misclicked, that may be the user.

## 7. The 5-user rule (Nielsen)

Nielsen's research: testing 5 users catches ~85% of usability problems. More users hit diminishing
returns — the same problems repeat.

```
Users tested    Problems found
1               ~30%
3               ~65%
5               ~85%
10              ~95% (but 2× the cost for 10% more)
```

Rules:
- **5 users from the target segment** — not 5 random people. A persona mismatch invalidates the test.
- **Test, fix, re-test** — 5 users → fix the big problems → 5 more users (different) to find what
  remains. Two rounds of 5 beat one round of 15.
- **For distinct user types, 5 per type** — if novices and experts use the tool very differently, test
  5 of each.

## 8. Think-aloud pitfalls

| Pitfall | Fix |
|---|---|
| User goes silent | Prompt: "What are you looking for right now?" (not "why did you click that?") |
| User asks "is this right?" | "What would you expect to happen?" — reflect, don't confirm |
| Researcher leads | Don't say "good" or "correct" — neutral acknowledgement only |
| User performs for the researcher | Emphasize: "we're testing the design, not you; you can't do this wrong" |

## 9. Heuristic evaluation (pre-test)

Before user testing, run a heuristic evaluation (`design-foundations.md` §Usability Heuristics) — expert walkthrough
catches structural issues cheaply. Heuristic eval → fix obvious problems → then spend user-testing
budget on the subtle issues experts missed.

Order: heuristic evaluation (cheap, fast, expert) → fix → usability test (real users) → fix → ship.
Testing users on problems experts could have found wastes the user's time and your budget.

## 10. When to research vs test

| Signal | Do |
|---|---|
| About to design a new feature, don't know user workflow | User research (interviews, observation) |
| Have a design/prototype, not sure if it works | Usability test (task-based, 5 users) |
| Live product, retention dropping | Research (interview churned users) + analytics (where do they drop in AARRR) |
| Competitor released a feature, evaluating | Research (use their product) — not testing yours |
| Design debate, can't resolve with opinions | Prototype (the `prototype` skill) + test both variants |

Research prevents building the wrong thing; testing prevents shipping it broken. The `frontend-design`
skill's When-to-use can trigger UX research before Step 1 (Define element) when the user/context is
unknown — load this reference then.
