# Tech Debt Register

Depth reference for the `code-review` skill. Upgrades `docs/TODO.md` from a flat list to a
prioritized register with interest/principal/effort metadata — so tech debt is managed as a
portfolio, not a backlog that grows forever. The skill produces TODO.md with findings grouped by
business area; this teaches how to quantify and prioritize those findings for sustainable paydown.

## Contents

- [1. Why a register, not a list](#1-why-a-register-not-a-list)
- [2. The register fields](#2-the-register-fields)
- [3. Debt types](#3-debt-types)
- [4. Prioritization](#4-prioritization)
- [5. Sustainable paydown cadence](#5-sustainable-paydown-cadence)
- [6. "Accepted" debt is a decision, not a default](#6-accepted-debt-is-a-decision-not-a-default)
- [7. How this connects to the skill](#7-how-this-connects-to-the-skill)

## 1. Why a register, not a list

A flat TODO list has two failure modes: it grows without bound (everything is "some day"), and it
doesn't tell you what to pay down first. A register adds the metadata to decide: what's the cost of
leaving this (interest), what's the cost to fix it (principal), and what's the risk if we don't
(effort + blast radius).

| TODO list (flat) | Tech debt register |
|---|---|
| "Refactor auth module" | "Auth module: interest=2h/wk (every onboarding hits the mess), principal=3 days, risk=HIGH (security-adjacent), pay down in Q3" |
| "Upgrade dep X" | "Dep X: interest=0 (no pain yet), principal=1 day, risk=MEDIUM (CVE in old version), pay down next sprint" |
| "Add tests to checkout" | "Checkout tests: interest=1h/wk (manual verification), principal=2 days, risk=HIGH (revenue path), pay down now" |

The flat list says "there's a thing." The register says "this thing costs us 2h/week, takes 3 days
to fix, and is high-risk — fix it before the low-interest one."

## 2. The register fields

Each debt item carries:

| Field | Meaning | Example |
|---|---|---|
| **Item** | What the debt is | "Auth module uses deprecated crypto library" |
| **Type** | What kind | Code / Design / Dependency / Test / Docs |
| **Interest** | Recurring cost of leaving it | "2h/wk — every onboarding/debug session fights the mess" |
| **Principal** | One-time cost to pay it down | "3 dev-days" |
| **Risk** | What happens if we don't | HIGH / MEDIUM / LOW (with reason) |
| **Blast radius** | What breaks if paydown goes wrong | "Auth — all users affected; needs staged rollout" |
| **Status** | Where it is | Open / In progress / Paid / Accepted (won't fix) |
| **Target** | When to pay down | "Q3" / "Next sprint" / "When touching auth next" |

## 3. Debt types

| Type | Example | Typical interest pattern |
|---|---|---|
| **Code** | Deep nesting, duplicated logic, dead code | Steady — slows every change in the area |
| **Design** | Wrong abstraction, missing seam, tight coupling | Compounding — each feature added on the wrong shape costs more |
| **Dependency** | Outdated lib, deprecated API, CVE | Low then spiking — no pain until a CVE or breaking upgrade |
| **Test** | Missing tests, flaky tests, untested critical path | Spiking — each change risks regression; fear of refactoring |
| **Docs** | Stale docs, missing runbooks | Low but insidious — onboarding slow, wrong decisions from stale info |

Design debt compounds (each new feature on the wrong shape is harder than the last); code debt is
steady (the mess costs the same each week); dependency debt is latent (zero until it isn't). Prioritize
design debt that's still accumulating over code debt that's stable.

## 4. Prioritization

Rank by: `interest rate × risk`, not by `how annoying it is`.

| Priority | Criteria | Action |
|---|---|---|
| **Pay now** | High interest + high risk (or CVE) | Next sprint |
| **Pay soon** | High interest, any risk | This quarter |
| **Pay when touching** | Low interest, but in an area you'll change | Bundle with the next change there |
| **Accept** | Low interest, low risk, high principal | Document as accepted; revisit annually |
| **Delete the item** | Not real debt (was a TODO that's no longer relevant) | Remove — don't let the register grow like the list did |

The last row is critical: a register that never deletes items is just a slower-growing list. Items
that are no longer relevant (the code was rewritten, the dep was removed, the "debt" was a
misunderstanding) get deleted, not marked "accepted."

## 5. Sustainable paydown cadence

Tech debt paydown competes with feature work for the same engineering time. The discipline: reserve
a fixed fraction for paydown, not "when we have time" (you never have time).

- **~20% of sprint capacity** to debt paydown (industry common heuristic; tune to your context).
- **Bundle paydown with adjacent feature work** — when you're touching the auth module for a
  feature, pay down auth debt in the same PR (no extra context-switch cost).
- **Track the register's trend** — is total debt growing, stable, or shrinking? A growing register
  means paydown rate < accrual rate; either pay down faster or accept the growth consciously.

## 6. "Accepted" debt is a decision, not a default

Marking debt "accepted" (won't fix) is valid, but it must be a documented decision, not the default
state of items nobody got to:

| Accepted (valid) | Default-neglected (invalid) |
|---|---|
| "Low interest, low risk, principal > value — reviewed 2025-03, revisit 2026-03" | (no decision recorded; just sitting there) |
| "Legacy module scheduled for replacement in Q4 — paying down now is waste" | (no replacement scheduled; "we'll rewrite it" is a myth) |

An accepted item has a reviewer, a date, and a revisit trigger. A neglected item has none.

## 7. How this connects to the skill

The `code-review` skill produces `docs/TODO.md` — findings grouped by business area, with
code↔TODO.md bidirectional sync. This reference upgrades that TODO.md:

- Add the register columns (interest, principal, risk, status, target) to each finding.
- Review the register quarterly (not just add to it).
- Delete items that are no longer relevant.
- Track the trend (growing vs shrinking).

The skill finds the debt; the register manages it. Without the register, TODO.md becomes a
graveyard of good intentions. With it, debt paydown is a quantified, prioritized, sustainable
practice.
