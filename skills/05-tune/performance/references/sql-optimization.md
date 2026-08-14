# SQL Optimization

Depth reference for the `performance` skill. Query-level optimization techniques: index
strategy for query design, pagination patterns, materialized views, and partitioning.
The operational DB layer — EXPLAIN plan reading, slow-query analysis, index maintenance,
N+1 detection, connection pooling — is in `references/database-performance.md`; this
reference covers the SQL-design techniques that prevent those problems at query time.

## Contents

- [1. Index strategy — composite, covering, partial](#1-index-strategy--composite-covering-partial)
- [2. Missing vs unused indexes — the audit](#2-missing-vs-unused-indexes--the-audit)
- [3. Pagination — cursor vs offset](#3-pagination--cursor-vs-offset)
- [4. Materialized views](#4-materialized-views)
- [5. Partitioning](#5-partitioning)
- [6. How this connects to the skill](#6-how-this-connects-to-the-skill)

## 1. Index strategy — composite, covering, partial

The right index makes the query a lookup instead of a scan. Design the index for the
query, not the table.

| Index type | When to use | Example |
|---|---|---|
| **Single-column** | Filter on one column | `CREATE INDEX ON orders(user_id)` |
| **Composite** | Filter on multiple columns in one query | `CREATE INDEX ON orders(user_id, created_at)` |
| **Covering** | Query selects only indexed columns (index-only scan) | `CREATE INDEX ON orders(user_id) INCLUDE (status, total)` |
| **Partial** | Query always filters on a subset | `CREATE INDEX ON orders(user_id) WHERE status = 'pending'` |
| **Expression** | Query filters on a function result | `CREATE INDEX ON orders(lower(email))` |

### Composite index column order

Order matters: the leftmost prefix must match the query's filter. A composite index on
`(user_id, created_at)` serves `WHERE user_id = ?` and `WHERE user_id = ? AND created_at > ?`,
but NOT `WHERE created_at > ?` alone. Rule: **equality columns first, then range, then sort.**

```
WHERE user_id = ? AND status = ? AND created_at > ? ORDER BY created_at
→ INDEX (user_id, status, created_at)
```

### Covering index (Index Only Scan)

When the index contains every column the query needs, the DB skips the table fetch
entirely — the fastest possible read. Use `INCLUDE` (Postgres) or a composite index that
covers the SELECT list. Verify with EXPLAIN: `Index Only Scan` = success (see
[references/database-performance.md](database-performance.md) §2 for the full EXPLAIN guide).

## 2. Missing vs unused indexes — the audit

Indexing is a tradeoff: every index speeds reads but slows writes (every INSERT/UPDATE/DELETE
maintains every index). Audit both sides regularly.

### Missing indexes (queries that scan)

| Signal | How to find | Fix |
|---|---|---|
| Seq Scan on a large table | EXPLAIN the slow query | Add index on the filter column(s) |
| High rows-removed-by-filter | EXPLAIN ANALYZE shows Filter removing most rows | Index the filter column |
| Nested Loop with large outer | Join where the inner lookup isn't indexed | Index the join key on the inner table |
| Slow WHERE on a common query | Slow-query log | Composite index matching the query's column order |

### Unused indexes (writes paying for nothing)

| Signal | How to find | Fix |
|---|---|---|
| idx_scan = 0 in stats | `pg_stat_user_indexes` | Drop the index |
| Index on low-cardinality column | boolean / status with 3 values | Replace with partial index |
| Duplicate indexes | Same columns, different names | Drop the redundant one |
| Index never appears in EXPLAIN | Query planner skips it | Drop or redefine |

### Audit cadence

- **Monthly**: query `pg_stat_user_indexes` for idx_scan = 0; drop unused candidates.
- **On new slow query**: EXPLAIN first — missing index is the most common fix.
- **After query pattern change**: re-verify indexes match the new WHERE/JOIN patterns.

For index bloat, REINDEX, and stats freshness, see
[references/database-performance.md](database-performance.md) §3.

## 3. Pagination — cursor vs offset

| | Offset pagination | Cursor pagination |
|---|---|---|
| **Query** | `LIMIT 20 OFFSET 40` | `WHERE created_at < ? ORDER BY created_at DESC LIMIT 20` |
| **Cost** | O(offset + limit) — scans skipped rows | O(limit) — seeks to the cursor |
| **Stability** | Items shift if data changes between pages | Stable — cursor is a fixed point |
| **Jump to page N** | Yes (offset = N × limit) | No (must traverse) |
| **When to use** | Small datasets, admin UIs, "jump to page" | Large datasets, infinite scroll, feeds |

### Why offset pagination degrades

`OFFSET 100000 LIMIT 20` reads 100,020 rows and discards 100,000. The cost grows linearly
with page depth. At scale this becomes a full-table scan per page.

### Cursor pagination pattern

```sql
-- Page 1
SELECT id, created_at FROM orders ORDER BY created_at DESC LIMIT 20;

-- Page 2 (cursor = last item's created_at, id from page 1)
SELECT id, created_at FROM orders
WHERE (created_at, id) < (?, ?)
ORDER BY created_at DESC LIMIT 20;
```

The `(created_at, id)` tuple cursor handles ties (same timestamp) — id is the tiebreaker.
An index on `(created_at DESC, id)` makes the seek an index range scan, not a sort. For
unordered data, use an opaque cursor encoding the last row's position. Avoid offset-based
"count then skip" on any table that will exceed 10,000 rows.

## 4. Materialized views

When a query aggregates or joins large tables and the result is read often but changes
slowly, precompute it.

```sql
CREATE MATERIALIZED VIEW order_summary AS
SELECT user_id, COUNT(*) AS order_count, SUM(total) AS lifetime_value
FROM orders GROUP BY user_id;

CREATE UNIQUE INDEX ON order_summary(user_id);
```

| When to use | When NOT to use |
|---|---|
| Read-heavy, write-light aggregates | Source data changes every request |
| Dashboard / reporting queries | Real-time accuracy required |
| Expensive joins run frequently | The view is larger than the source |

### Refresh strategies

| Strategy | Command | Tradeoff |
|---|---|---|
| **Full refresh** | `REFRESH MATERIALIZED VIEW name` | Blocks reads; simple; fine for small views |
| **Concurrent refresh** | `REFRESH MATERIALIZED VIEW CONCURRENTLY name` | No read block; requires unique index; slower refresh |
| **Scheduled** | Cron / pg_cron / CI job | Decouples refresh from reads; staleness window is explicit |

The staleness window is the design tradeoff: the view is correct as of the last refresh.
If the dashboard tolerates 1-hour-old data, an hourly scheduled concurrent refresh is the
right answer.

## 5. Partitioning

Split a large table into smaller physical partitions so queries scan only the relevant
partition (partition pruning).

| Strategy | Partition key | Example |
|---|---|---|
| **Range** | Date / timestamp | Monthly partitions of a logs table |
| **List** | Discrete value | Partition by region (US, EU, APAC) |
| **Hash** | Hash of a column | Distribute evenly by user_id |

### When to partition

- Table exceeds 50–100GB or 100M rows (query planner starts choosing bad plans).
- Queries always filter on the partition key (enables pruning — scan one partition, not all).
- Retention is time-based (drop old partitions instead of DELETE).

### Partition pruning

The planner prunes partitions the query can't match. `WHERE created_at >= '2025-01-01'`
on a monthly-partitioned table scans only January's partition. If the query doesn't
filter on the partition key, every partition is scanned — partitioning adds overhead
with no benefit.

### Maintenance

Create future partitions ahead of time — a write to a non-existent partition fails. Drop
old partitions instead of `DELETE` (instant, no vacuum, no bloat). Index each partition
individually — indexes are per-partition, not global (Postgres).

## 6. How this connects to the skill

The `performance` skill teaches: profile → find bottleneck → fix → measure. This
reference is the SQL-design depth for "fix" — index design, pagination, precomputation,
partitioning. Load [references/database-performance.md](database-performance.md) for
operational questions (EXPLAIN reading, index bloat, N+1, pooling); load this for design
questions (which index, which pagination, whether to materialize or partition).
