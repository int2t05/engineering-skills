# State Design

Depth reference for the `frontend-design` skill. Every interface hits four states beyond the happy
path: loading, error, empty, and partial. Designing all four is what separates a finished screen from a
mockup. This is the user-side state experience; `component-anatomy.md` covers the component-side state
architecture (default/hover/focus/pressed/disabled).

## Contents

- [1. The four states](#1-the-four-states)
- [2. Loading state](#2-loading-state)
- [3. Error state](#3-error-state)
- [4. Empty state](#4-empty-state)
- [5. Partial state](#5-partial-state)
- [6. How this connects](#6-how-this-connects)

## 1. The four states

| State | When | User's question | Design job |
|---|---|---|---|
| **Loading** | Waiting for data | "Is anything happening?" | Show structure, not just "wait" |
| **Error** | Something failed | "What went wrong, and what now?" | Explain + offer a next step |
| **Empty** | No data yet (first use, no results, no permission) | "Why is this empty? What do I do?" | Explain why + guide to action |
| **Partial** | Some loaded, some pending/failed | "What can I use now?" | Make loaded parts interactive |

A screen designed only for the happy path (data present, request succeeded) is unfinished. Walk every
view through all four states before shipping.

## 2. Loading state

### Skeleton screens vs spinners

| | Skeleton | Spinner |
|---|---|---|
| **Shows** | The structure that's coming (boxes where content will be) | Only "something is happening" |
| **Perceived speed** | Faster — the layout is already there, content fills in | Slower — the user waits with nothing |
| **Best for** | Content-heavy views (articles, lists, dashboards) | Quick waits (<300ms), full-screen transitions |
| **Risk** | If the skeleton doesn't match the real layout, it's a lie | Indeterminate; user can't tell if it's stuck |

Rules:
- **Skeleton must match the real layout** — same shapes, same proportions. A skeleton that shifts to a
  different layout on load causes a jarring reflow.
- **Shimmer animation** (subtle gradient sweep) signals "live, working," not "frozen." Keep it slow
  (1.5-2s loop) and subtle.
- **Don't use a spinner for >2s** — past 2s, the user thinks it's stuck. Switch to skeleton or
  progress-with-context ("Loading 47 of 120 items...").

### Progress with context
For longer loads, show *what's happening*, not just *that* something is:
- "Loading 47 of 120 items..." (progress)
- "Almost done — indexing search..." (current step)
- A determinate progress bar (60%) beats an indeterminate spinner every time.

## 3. Error state

The error message is the moment the user most needs the interface to help them. Don't waste it on a
code.

### Anatomy of a good error
| Part | Bad | Good |
|---|---|---|
| **What went wrong** | "Error 500" | "We couldn't save your changes." |
| **Why** | (omitted) | "Your connection dropped during the upload." |
| **What to do** | (omitted) | "Retry — your draft is still here." |
| **Tone** | Blaming ("You entered...") | Neutral ("That email doesn't match an account.") |

Rules:
- **Plain language, never codes** — "AUTH_USER_NOT_FOUND" is internal; "That email doesn't match an
  account" is for the user. (Nielsen #9.)
- **Blame the system, not the user** — "We couldn't..." not "You failed to..."
- **Offer the recovery action** — Retry, Restore, Contact support. An error with no next step is a
  dead end.
- **Preserve user work** — never clear a form on error. The draft survives; only the failed submit
  doesn't.
- **Distinguish error types** — validation error (inline, immediate) vs server error (full-state,
  retryable) vs permission error (explain + route to where they can fix it).

## 4. Empty state

Empty is not "no data" — it's a design opportunity. There are three kinds of empty, each with a
different message:

| Empty type | Why it's empty | The message |
|---|---|---|
| **First-use** | User hasn't created anything yet | "You have no projects. Create your first →" |
| **No results** | Filters/search returned nothing | "No projects match 'archived.' Clear filters →" |
| **No permission** | User lacks access to see anything | "No projects visible. Ask your admin for access." |

Rules:
- **Never just "No data"** — explain *why* empty and *what to do*. "No data" is a dead end; "Create
  your first project" is an invitation.
- **Provide the primary action** — in first-use empty, the empty state *is* the onboarding CTA.
- **Illustrate sparingly** — a simple illustration can soften the emptiness, but the action is the
  point, not the art.
- **For no-results, offer to relax constraints** — "No matches. Try fewer filters, or search all
  projects."

## 5. Partial state

Some data loaded, some still pending or failed. The loaded parts should be usable, not blocked.

| Approach | When | Example |
|---|---|---|
| **Progressive render** | Independent sections load at different speeds | Dashboard cards fill in as each loads; user reads what's there |
| **Optimistic UI** | You can predict the result of an action | "Liked" appears instantly; reconciles when server confirms |
| **Stale-while-revalidate** | Cached data exists, refresh in background | Show last-known data; update silently when fresh arrives |
| **Graceful degradation** | One part failed, the rest works | "Comments unavailable — rest of the article is readable" |

Rules:
- **Don't block the whole view for one failed section** — if comments fail to load, the article is
  still readable.
- **Mark stale/pending data** — a subtle "updating..." badge keeps the user informed without blocking.
- **Partial is better than blank** — something useful on screen beats a full-screen spinner.

## 6. How this connects

The four states are the user's experience of time and uncertainty in the interface:

- **Loading** — the interface acknowledges time.
- **Error** — the interface helps when things break.
- **Empty** — the interface guides when there's nothing yet.
- **Partial** — the interface is honest about incompleteness.

design-principles §4 ("Design every state") is the rule; this reference is the method. In
`frontend-design` Step 5 (Specify interaction states), every interactive view gets all four states
designed — not just the default/hover/focus set. The `docs/design/DESIGN.md` output lists these per
component.
