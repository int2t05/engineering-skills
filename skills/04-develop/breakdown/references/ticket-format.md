# Ticket Format

Reference for the `breakdown` skill. Templates, the staleness rule, and the
ticket-type routing used when publishing tracer-bullet tickets.

## Local-ticket template

One file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`,
numbered from `01` in dependency order (blockers first). Never combine tickets
into one file.

```markdown
# <NN> — <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the
user's perspective — not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or
"None — can start immediately".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
```

## Issue template

For a real tracker (GitHub, Linear, …). Publish in dependency order so each
ticket's blocking edges can reference real identifiers; use the platform's
native blocking / sub-issue relationship where it has one.

```markdown
## Parent

A reference to the parent issue on the tracker (if the source was an existing
issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective —
not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None — can start immediately".
```

For each acceptance criterion, name the observation that would show it false,
and confirm it fails at the commit the implementer starts from — a criterion
already true at the base commit grades nothing.

## Staleness rule

In either form, avoid specific file paths or code snippets — they go stale
fast. A ticket that names `src/api/handlers/user.ts:42` rots the moment the
file moves; a ticket that pastes a working code block implies the implementer
should copy it instead of deriving the code from the spec.

**Exception:** if a prototype produced a snippet that encodes a decision more
precisely than prose can — a state machine, a reducer, a schema, a type shape —
inline it and note briefly that it came from a prototype. Trim to the
decision-rich parts, not a working demo. The snippet stands for a decision, not
an implementation.

## Ticket types and routing

A breakdown may surface tickets that aren't straight implementation work. Route
each by type to the skill that owns it. HITL = human-in-the-loop (the user is
present); AFK = the user may be away, so the ticket must be self-contained.

| Type | What it is | Route |
| --- | --- | --- |
| **task** | Build a vertical slice to a spec — the default ticket type. | `04-develop/implement` |
| **research** | An open question that must be answered before a task can be specified — framework behaviour, API contract, data shape. | `02-research/research` |
| **prototype** | A throwaway built to resolve a design decision (state machine, schema, interaction) whose output feeds back into the spec. | `03-design/prototype` |
| **grilling** | Pressure-test a fuzzy idea or spec against the user until it is sharp enough to slice into tasks. | `01-product/brainstorm` |

A task ticket is ready for `implement` only when its acceptance criteria are
falsifiable at the base commit. A research or prototype ticket's output is a
decision that collapses into the spec, not a deliverable on its own. A grilling
ticket is HITL by nature — the user must be in the room.
