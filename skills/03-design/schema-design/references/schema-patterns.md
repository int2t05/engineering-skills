# Schema Patterns

Depth reference for the `schema-design` skill. Normalization trade-offs, index patterns,
partitioning strategies, and soft-delete policies — the decisions that recur across schema
design and are easy to get wrong on first pass.

## 1. Normalization trade-offs

### 3NF / BCNF (default)

Normalize by default. Eliminates update anomalies (same fact stored once), keeps the model
honest, and makes writes simple. The cost is joins on read — acceptable until measured query
patterns prove otherwise.

**When to keep:** the default. Most transactional schemas stay at 3NF for their lifetime.

### Deliberate denormalization

Denormalize only when a measured read pattern justifies the write complexity and consistency
risk. Document every denormalization as a trade-off: what read it optimizes, what write it
complicates, how consistency is maintained.

| Pattern | When to use | Consistency cost |
|---|---|---|
| **Calculated column** (e.g. `order_total`) | Hot read path; calculation is expensive or跨-row | Must update on every input change — trigger or app-level sync |
| **Pre-joined snapshot** (e.g. `user_name` copied into `comment`) | Avoid join on ultra-hot read; tolerate stale | Update lag when source changes; acceptable if source is near-static |
| **Aggregate table** (e.g. `daily_sales_summary`) | Reporting/analytics over large raw tables | Rebuild on late-arriving data; schedule or event-driven refresh |
| **Materialized view** | DB-maintained denormalization | Refresh policy (concurrent or rebuild); stale window |

Rule: every denormalized column has an owner — the mechanism that keeps it in sync (trigger,
app hook, refresh job). No orphan denormalized columns.

## 2. Index patterns

Index for the queries, not the columns. Every index has a cost (write amplification, storage);
justify each against a concrete access pattern.

### Composite index ordering

Order columns by: **equality predicates first, then range/sort, then include**.

```
-- Query: WHERE user_id = ? AND created_at > ? ORDER BY created_at DESC
-- Right index: (user_id, created_at DESC)
-- Wrong index: (created_at, user_id)  -- can't seek on user_id; seq scan
```

The leading column determines whether the index is usable at all. A composite index on (A, B)
does NOT accelerate `WHERE B = ?` — the index is ordered by A first.

### Covering index

Include all columns the query reads to avoid the table lookup (heap fetch):

```
-- Query: SELECT status, total FROM orders WHERE user_id = ?
-- Covering index: (user_id) INCLUDE (status, total)
-- The index satisfies the query entirely; no table access
```

Trade-off: larger index, more write amplification. Worth it for hot reads.

### Partial / filtered index

Index only the rows that match a common predicate — smaller index, faster:

```
CREATE INDEX ON orders (user_id) WHERE deleted_at IS NULL;
CREATE INDEX ON tasks (assignee_id) WHERE status = 'open';
```

The query must use the same predicate for the planner to choose the partial index.

### Unique index as invariant

Enforce business invariants that the application cannot guarantee alone:

```
-- One active subscription per user
CREATE UNIQUE INDEX ON subscriptions (user_id) WHERE status = 'active';

-- One primary email per user
CREATE UNIQUE INDEX ON emails (user_id) WHERE is_primary = true;
```

### Index anti-patterns

- **Indexing every column** — write amplification with no read benefit; most columns are never
  filtered on
- **Low-cardinality leading column** (e.g. `(status, user_id)` when status has 3 values) — the
  index is bloated and rarely chosen over a seq scan
- **Index without the query** — "index on user_id" without knowing the query shape; may not help
- **No EXPLAIN** — assume the index is used; verify with `EXPLAIN` / `EXPLAIN ANALYZE`

## 3. Partitioning strategies

Partition large tables before they become painful (100M+ rows, or when a single index no longer
fits in memory). Decide the strategy early — repartitioning a 500M-row table is a multi-day
operation.

### Range partitioning (by date)

The most common pattern for time-series or append-heavy data:

```
-- Monthly partitions by created_at
PARTITION BY RANGE (created_at);
-- Each partition holds one month; old partitions can be archived/dropped in O(1)
```

**Best for:** logs, events, orders — anything with a time dimension and a retention policy
(drop old partitions instead of `DELETE`).

### Hash partitioning (by key)

Distribute evenly across N partitions by hashing a key:

```
PARTITION BY HASH (user_id) PARTITIONS 16;
```

**Best for:** evenly distributing a hot table by tenant/user when there's no time dimension.
Beware: adding partitions requires rehashing all data.

### List partitioning (by category)

Partition by discrete values (region, tenant ID, category):

```
PARTITION BY LIST (region);
-- partition us VALUES ('US'), partition eu VALUES ('EU'), ...
```

**Best for:** multi-tenant or multi-region where queries are always scoped to one value.

### Partitioning pitfalls

- **Cross-partition queries** — a query without the partition key scans all partitions (slow);
  every hot query must filter on the partition key
- **Unique constraints** — a unique constraint must include the partition key (the DB enforces
  uniqueness only within a partition); plan primary keys accordingly
- **Foreign keys to partitioned tables** — supported in modern Postgres but with restrictions;
  verify before designing around them
- **Choosing too many partitions** — each partition has planner overhead; hundreds of tiny
  partitions degrade planning time

## 4. Soft-delete policies

Soft delete (`deleted_at` timestamp) vs. hard delete — choose per entity, document why.

### When to soft-delete

- **Audit/recovery needs** — financial records, user accounts, anything regulators may ask about
- **Referential integrity** — deleting a parent that children still reference; soft-delete avoids
  the cascade or orphan
- **Undo** — user-facing "trash" / restore features

### When to hard-delete

- **Ephemeral data** — sessions, cache entries, transient logs — soft-deleting these grows the
  table forever for no value
- **GDPR / right-to-be-forgotten** — PII that must actually disappear, not be hidden

### Soft-delete implementation

```
-- Column
deleted_at TIMESTAMPTZ NULL  -- NULL = active; non-NULL = deleted at this time

-- Partial index so active-row queries stay fast
CREATE INDEX ON orders (user_id) WHERE deleted_at IS NULL;

-- Every query must filter: WHERE deleted_at IS NULL
-- (enforce via a view or an ORM default scope so this isn't forgotten)
```

**Pitfall:** a soft-deleted row that's never cleaned up grows the table. Pair soft-delete with a
retention policy: archive or hard-delete soft-deleted rows older than N days/months. A
soft-delete without eventual cleanup is a slow memory leak.

## 5. Key and type choices

| Decision | Default | Reason |
|---|---|---|
| Primary key | Surrogate (UUID or bigint identity) | Natural keys mutate; surrogate keys are stable and join-friendly |
| UUID vs bigint | bigint for internal-only; UUID for distributed/public | bigint is 8 bytes, faster to index; UUID avoids collision and enumeration |
| Timestamps | `timestamptz` (never `timestamp`) | `timestamptz` stores UTC, displays in session timezone; `timestamp` drops zone info |
| Booleans | `boolean` | Not `int 0/1`, not `char Y/N` — the type exists, use it |
| Money | `numeric` / `decimal` (never `float`) | Float is binary, loses precision on currency; decimal is exact |
| Enums | DB `enum` for small stable sets; lookup table for growing sets | DB enum is fast but requires migration to add a value; lookup table is flexible |
| Text vs varchar(N) | `text` + `CHECK(length <= N)` if a limit is needed | `varchar(N)` has no performance benefit in modern Postgres; `text` + check is equivalent and composable |
