---
name: breakdown
description: Use when breaking a plan, spec, or conversation into tracer-bullet tickets, each declaring its blocking edges. For work too large for one session, builds a shared map of decision tickets resolved one at a time.
---

# Breakdown

The plan itself comes from Claude Code's built-in plan mode
(engineering-principles §7). This skill breaks the result into tickets.

Two modes. For work that fits one session, break it into **tracer-bullet
tickets** with blocking edges. For work too large for one session, chart a
**decision map** — a shared index of decision tickets resolved one at a time
until the way to the destination is clear.

## When to use

- You have an approved plan, spec, or conversation result to break into tickets.
- The work spans multiple sessions and needs a shared decision map.
- You need to sequence work by blocking edges before implementation starts.

## Steps

### Mode 1 — Tracer-bullet tickets (work fits one session)

1. **Gather context.** Read the plan or spec. If the user passes a reference
   (path, issue number, URL), fetch its full body. Explore the codebase if you
   haven't, so ticket titles use the project's domain glossary and respect
   existing ADRs.

2. **Draft vertical slices.** Each slice cuts a narrow but COMPLETE path through
   every layer (schema, API, UI, tests) — vertical, not a horizontal layer. A
   completed slice is demoable on its own. Size each to a single fresh context.

3. **Declare blocking edges.** For each ticket, list the tickets that must
   complete before it can start. A ticket with no blockers starts immediately.

4. **Wide-refactor exception.** A single mechanical change fanning across the
   codebase (rename a column, retype a shared symbol) can't land green as a
   vertical slice. Sequence it as **expand–contract**: add the new form beside
   the old, migrate call sites in per-package batches (each its own ticket
   blocked by the expand), then delete the old form in a final ticket blocked
   by every batch.

5. **Quiz the user.** Present the breakdown as a numbered list — title, blocked
   by, what it delivers. Ask: granularity right? Blocking edges correct? Any
   tickets to merge or split? Iterate until approved.

6. **Publish the tickets.** One ticket per file under
   `.scratch/<feature-slug>/issues/<NN>-<slug>.md` (blockers first), or one
   issue per ticket on the tracker using native blocking links. Work the
   **frontier**: any ticket whose blockers are all done.

### Mode 2 — Decision map (work too large for one session)

1. **Name the destination.** Pin down what this effort is finding its way to —
   the spec, decision, or change. The destination fixes the scope; settle it
   first.

2. **Map the frontier, breadth-first.** Fan out across the whole space,
   surfacing open decisions and first takeable steps. If this surfaces no fog,
   the way is already clear — stop and ask the user how to proceed.

3. **Create the map** as a single tracker issue labelled `wayfinder:map`:
   Destination, Notes, empty Decisions-so-far, fog sketched into **Not yet
   specified**.

4. **Create the tickets you can specify now** as child issues, then wire
   blocking edges in a second pass (issues need ids before they can reference
   each other). Each ticket is a question sized to one session. What you can't
   yet phrase sharply stays in **Not yet specified** — don't pre-slice fog.

5. **Work the map one ticket per session.** Claim a frontier ticket, resolve
   it, post the answer as a resolution comment, close the issue, and append a
   one-line gist to the map's Decisions-so-far. Graduate fog that the answer
   makes specifiable into fresh tickets. Rule out-of-scope work by closing the
   ticket and noting it in **Out of scope** — never in Decisions-so-far.

6. **Stop** when no tickets remain and the way to the destination is clear.

## Verify

- Tickets written with blocking edges declared; each sized to a single session.
- Map (if used) resolves to a clear path: Decisions-so-far indexes every closed
  ticket, Not yet specified holds only fog you can't yet phrase sharply.
- Wide refactors sequenced as expand–contract, not forced into tracer bullets.
- Out-of-scope work ruled out explicitly, not left on the frontier.

## References

- [../../references/engineering-principles.md](../../references/engineering-principles.md) — discipline shared by every skill; §7 covers plan mode.
