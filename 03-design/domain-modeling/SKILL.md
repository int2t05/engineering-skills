---
name: domain-modeling
description: Use when building or sharpening a project's domain model — challenging terms, stress-testing with scenarios, and updating CONTEXT.md and ADRs inline to establish a shared ubiquitous language.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline
— challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the
moment they crystallise. Merely *reading* `CONTEXT.md` for vocabulary is not this skill — that's a
habit any skill can do. This skill is for when you're **changing** the model.

## When to use

- Pinning down domain terminology or establishing a ubiquitous language
- A term the user uses conflicts with the existing `CONTEXT.md` glossary
- Stress-testing domain relationships against concrete edge-case scenarios
- Recording an architectural decision that is hard to reverse, surprising, or a real trade-off
- Another skill needs to maintain or update the domain model
- Triggers on "domain model", "ubiquitous language", "CONTEXT.md", "ADR", "领域模型", "统一语言"

## Steps

### 1. Locate the context

Most repos have a single `CONTEXT.md` at the root. If a `CONTEXT-MAP.md` exists, the repo has
multiple contexts — read it to find which context the current topic relates to. If neither exists,
create a root `CONTEXT.md` lazily when the first term is resolved. Create `docs/adr/` lazily when
the first ADR is needed.

### 2. Challenge terms against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out
immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

When terms are vague or overloaded, propose a precise canonical term. "You're saying 'account' —
do you mean the Customer or the User? Those are different things."

### 3. Stress-test with concrete scenarios

When domain relationships are being discussed, invent scenarios that probe edge cases and force the
user to be precise about the boundaries between concepts. The awkward cases — the happy path, a
tricky edge case, an attempt at something that should be illegal — are where the model breaks.

When the user states how something works, check whether the code agrees. If you find a
contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation
is possible — which is right?"

### 4. Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there — don't batch these up. Capture them as
they happen, using the format in `references/context-format.md`.

`CONTEXT.md` is a glossary and nothing else. No implementation details, no specs, no scratch-pad
notes. Be opinionated: when multiple words exist for the same concept, pick the best one and list
the others under `_Avoid_`.

### 5. Offer ADRs sparingly

Only offer to create an ADR when **all three** are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for
   specific reasons

If any of the three is missing, skip the ADR. Use the format in `references/adr-format.md`. An ADR
can be a single paragraph — the value is recording *that* a decision was made and *why*, not
filling out sections.

## Verify

- [ ] `CONTEXT.md` updated inline with every resolved term (not batched)
- [ ] Terms are opinionated — canonical word chosen, alternatives listed under `_Avoid_`
- [ ] `CONTEXT.md` contains only glossary entries, no implementation details
- [ ] ADR offered only for decisions meeting all three criteria (hard to reverse, surprising, real trade-off)
- [ ] ADRs record the decision and why, not boilerplate sections
- [ ] Contradictions between user's language and code surfaced, not papered over

## References

- [../../references/engineering-principles.md](../../references/engineering-principles.md) — shared discipline (surface assumptions, manage confusion, verify don't assume)
- [references/context-format.md](references/context-format.md) — CONTEXT.md structure, rules, single vs multi-context repos
- [references/adr-format.md](references/adr-format.md) — ADR template, numbering, what qualifies as an ADR-worthy decision
