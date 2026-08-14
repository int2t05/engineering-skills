# State Management Architecture

State architecture for non-trivial frontends. `frontend-design` owns the visual surface; this
reference owns the data-flow architecture beneath it — where state lives, how it moves, and how it
stays consistent. A frontend without a state strategy accumulates prop drilling, duplicated fetches,
and stale data; this reference gives the decision framework to avoid that.

Framework-agnostic. Examples name React-ecosystem libraries (React Query, Zustand, XState) as
illustrative defaults; Vue, Svelte, and Solid have direct equivalents — apply the pattern, not the
import.

## Contents

- [1. Separate client state from server state](#1-separate-client-state-from-server-state)
- [2. Server-state caching](#2-server-state-caching)
- [3. Client-state stores](#3-client-state-stores)
- [4. State machines for complex flows](#4-state-machines-for-complex-flows)
- [5. Derived state](#5-derived-state)
- [6. Optimistic updates](#6-optimistic-updates)
- [7. State shape normalization](#7-state-shape-normalization)
- [8. Anti-patterns](#8-anti-patterns)

## 1. Separate client state from server state

The foundational decision. These two state types have different sources, lifecycles, and rules —
mixing them is the root of most state bugs.

| | Server state | Client state |
|---|---|---|
| Source | fetched from backend, owned by the server | created in the browser, owned by the UI |
| Lifespan | can become stale; needs invalidation | valid until the user closes the tab |
| Examples | user list, product detail, search results | modal-open, selected-tab, form draft, UI theme |
| Tool | cache/query library (React Query, SWR, Apollo cache) | component state, store (Zustand, Pinia, Jotai) |

Rule: server state goes in a cache library, client state goes in component state or a store. Never
copy server data into a global store "for convenience" — it immediately goes stale.

## 2. Server-state caching

Use a dedicated cache library (React Query / SWR / TanStack Query / Apollo) for anything fetched
from the backend. They solve problems hand-builders always get wrong:

- **Deduplication:** multiple components requesting the same key get one fetch
- **Invalidation:** `invalidateQueries` after a mutation, not manual refetch orchestration
- **Stale-while-revalidate:** show cached data instantly, refresh in the background
- **Loading/error states:** tracked per-query, not hand-rolled in every component
- **Pagination / infinite scroll:** built-in cursor and page management

Key strategy: use stable, serializable query keys (`['user', userId]`) so invalidation targets
the right cache slice. Derive the cache key from the request identity, not a component instance.

## 3. Client-state stores

For client state shared across many components (theme, auth session, UI flags, complex form state),
use a store (Zustand, Pinia, Jotai, Redux). Choose by complexity:

- **Component state** (`useState` / `ref` / `$state`): default. Only escalate when prop drilling
  exceeds 2 levels.
- **Lightweight store** (Zustand / Pinia / Jotai): shared client state, no boilerplate. The right
  call for most apps.
- **Redux (Toolkit)**: when you need serializable-action devtools, time-travel debugging, or strict
  patterns enforced across a large team. Justify the ceremony — don't reach for it by default.

Avoid the global-store-as-database anti-pattern: a store holding server snapshots duplicates the
cache library's job and will drift.

## 4. State machines for complex flows

When a UI element has more than 3 states with guarded transitions between them (a multi-step form,
a payment flow, a media player, onboarding), model it as an explicit state machine (XState /
Robot / native state pattern). State machines make invalid transitions impossible — you cannot
"submit" from a "loading" state because the transition doesn't exist.

Signs you need a state machine: boolean flags multiplying (`isLoading && !isError && hasData`),
impossible states you guard against with comments, transition bugs that only appear in edge
sequences. If the state is `idle → loading → success | error → idle`, a machine makes that explicit
and unbreakable.

## 5. Derived state

Compute values, don't synchronize them. If a value can be calculated from existing state, derive
it on read (`useMemo`, `derived`/`$derived`, selectors) — don't store it and try to keep it in
sync. Stored derived state is a second source of truth that drifts.

- `filteredList` = derive from `list` + `filter` — never store `filteredList` separately
- `isFormValid` = derive from field values — never store a validity flag and update it on every
  change
- Normalize selectors: derive the view shape from a normalized store, not the reverse

## 6. Optimistic updates

Update the UI immediately, reconcile when the server responds — if the mutation is likely to
succeed and the rollback is cheap. For high-risk mutations (payments, destructive actions), wait
for confirmation.

Pattern (with a cache library):
1. Capture the previous cache snapshot
2. Update the cache to the expected result (the optimistic value)
3. Fire the mutation
4. On success: invalidate / settle the cache to the server response
5. On error: roll back to the snapshot, surface the error

The rollback must restore the exact prior state, not a re-derivation — capture the snapshot before
mutating.

## 7. State shape normalization

For collections of entities, normalize by ID into a dictionary (`{ [id]: entity }`), not an array.
This makes lookups O(1), updates immutable-cheap (replace one entry, not filter/map the array),
and prevents duplicate copies of the same entity across the cache.

```
// Avoid: array of entities — O(n) lookup, full-copy updates
users: User[]

// Prefer: normalized by ID — O(1) lookup, single-entry updates
users: { [id: string]: User }
```

Denormalize at the component boundary (selectors) to produce the view shape the UI needs.

## 8. Anti-patterns

- **Prop drilling past 2 levels:** escalate to a store or context.
- **Server state in a global store:** duplicates the cache library, drifts immediately.
- **Stored derived state:** a second source of truth that must be kept in sync by hand.
- **Impossibly-combined flags** (`isLoading && !isError && hasData`): use a state machine.
- **Cache key from component instance** (not request identity): defeats deduplication.
- **Optimistic update without a rollback snapshot:** leaves the UI in a wrong state on failure.
- **Global event bus as state:** untraceable data flow; use a store with explicit reads/writes.
