# Database Performance

Depth reference for the `performance` skill. Database-specific optimization: slow-query analysis,
EXPLAIN plan reading, index maintenance, N+1 detection. The skill's `bottlenecks.md` and
`anti-patterns.md` are generic; this is the DB-depth layer. Design-time indexing is covered by
`schema-design`; this is ongoing performance management of a live database.

## 1. Symptom → cause for databases

| Symptom | Likely cause | First check |
|---|---|---|
| Query latency rising over time | Data growth + missing/ineffective index | EXPLAIN the query; check index usage |
| Sudden latency spike | Bad plan (stats stale) or lock contention | pg_stat_activity / SHOW PROCESSLIST; EXPLAIN |
| p99 much higher than p50 | A few slow queries (tail latency) | Slow-query log; identify the outliers |
| CPU high on DB server | Inefficient queries (scans, sorts) | Top queries by CPU (pg_stat_statements) |
| Disk I/O saturated | Table scans, missing index, bloat | EXPLAIN (seq scans); check table size vs index size |
| Connection pool exhaustion | Long-running queries holding connections | pg_stat_activity; queries > N seconds |

## 2. EXPLAIN — reading the plan

EXPLAIN tells you what the DB actually does, not what you think it does. Read it for the expensive
operations:

| Operation | Meaning | When it's bad |
|---|---|---|
| **Seq Scan** (sequential scan) | Reads every row in the table | On a large table without a filtering index |
| **Index Scan** | Uses an index to find rows | Usually good; check if index is selective enough |
| **Index Only Scan** | Uses a covering index; no table access | Best case — no heap fetch |
| **Hash Join / Merge Join** | Joins two row sets | Check if both inputs are indexed; hash on large input is memory-heavy |
| **Sort** | Sorts in memory (or spills to disk) | On large input without an index providing order |
| **Nested Loop** | For each row in A, find matching in B | Bad if A is large and B lookup isn't indexed |
| **Filter** | Filters rows after fetching | High rows-removed-by-filter = fetched way more than needed |

### The key metric: rows vs actual rows
EXPLAIN shows `rows` (estimated) and `actual rows` (with ANALYZE). When these diverge wildly, the
planner is guessing wrong — usually because stats are stale. Run `ANALYZE` (Postgres) /
`ANALYZE TABLE` (MySQL) to refresh stats.

### EXPLAIN ANALYZE (not just EXPLAIN)
`EXPLAIN` shows the plan; `EXPLAIN ANALYZE` runs the query and shows actual timing per node. Always
use ANALYZE for diagnosing (on a non-production replica, or a read-only query — it executes the
query). The timing per node tells you which step is actually slow, not which looks expensive.

## 3. Index maintenance

Indexes degrade over time. Design-time indexes (`schema-design`) are the start; ongoing maintenance
keeps them effective:

| Issue | How to detect | Fix |
|---|---|---|
| **Bloat** (index has empty space from deletes/updates) | `pgstatindex` or size-vs-rows ratio | `REINDEX` (or `REINDEX CONCURRENTLY` to avoid lock) |
| **Unused indexes** | `pg_stat_user_indexes` (idx_scan = 0) | Drop — it costs writes for no reads |
| **Duplicate indexes** | Two indexes on same columns | Drop the redundant one |
| **Stale stats** | EXPLAIN estimates vs actual diverge | `ANALYZE` (auto-vacuum may be too slow) |
| **Index on low-cardinality column** | Index on boolean/status with 3 values | Often unused; partial index is better |

### Index review cadence
- **Monthly**: review `pg_stat_user_indexes` for unused/low-scan indexes; drop candidates.
- **After large data load**: ANALYZE affected tables (stats are now stale).
- **On latency regression**: EXPLAIN the slow query; check if the index is still used (data growth
  can flip the planner from index scan to seq scan).

## 4. N+1 query detection

The most common ORM performance bug: 1 query to fetch the list, N queries to fetch each item's
relation.

```
# N+1 (bad): 1 + N queries
users = User.objects.all()          # 1 query
for u in users:
    print(u.profile.bio)            # N queries (one per user's profile)

# Fixed: 1 query with join/prefetch
users = User.objects.select_related('profile').all()   # 1 query, profile joined
```

### Detection
| Method | How |
|---|---|
| **ORM's prefetch/select_related** | Use eagerly; the ORM logs warn on N+1 (Django Debug Toolbar, Hibernate) |
| **Query count per request** | Instrument: count queries per HTTP request; alert if > threshold (e.g. > 50) |
| **Slow-query log patterns** | Same query repeated N times in one request = N+1 |
| **Distributed tracing** | Trace shows a span per query; a fan-out of N identical spans = N+1 |

N+1 is invisible in the query itself (each individual query is fast) but devastating in aggregate
(N round-trips). The fix is always eager loading (`select_related` / `includes` / `fetch`), not
caching or faster DB.

## 5. Query anti-patterns (DB-specific)

| Anti-pattern | Why slow | Fix |
|---|---|---|
| `SELECT *` | Fetches unnecessary columns; defeats covering indexes | Select only needed columns |
| `LIKE '%term%'` | Leading wildcard can't use index | Full-text search (tsvector/GIN) or external search index |
| `OR` across columns | Planner may seq scan | Split to UNION or add composite index |
| `COUNT(*)` on large table | Scans the table (or index) | Maintain a counter; approximate count |
| `ORDER BY RAND()` | Sorts entire table | Random-by-id approach; or pre-shuffled |
| Implicit type cast | `WHERE varchar_col = 123` may skip index | Match types explicitly |
| Function on column | `WHERE DATE(created_at) = ...` skips index | `WHERE created_at >= ... AND created_at < ...` |

## 6. Connection and pool

| Issue | Symptom | Fix |
|---|---|---|
| Too many connections | Pool exhaustion; "too many connections" error | Pool (PgBouncer, app-level); reduce per-request connection hold time |
| Long-running query holds connection | Pool starves | Query timeout; abort queries > N seconds |
| No connection pool | Each request opens/closes a connection | Pool with reasonable min/max; reuse across requests |
| Transaction held open across I/O | Connection held during slow external call | Commit before I/O; don't hold transactions across network calls |

## 7. How this connects to the skill

The `performance` skill teaches: profile → find bottleneck → fix → measure. This reference is the
DB-specific depth for "find bottleneck" (EXPLAIN, §2) and "fix" (indexes, N+1, anti-patterns).
Design-time indexing is `schema-design` (which indexes to create at design time); this is ongoing
performance management (which indexes to maintain, drop, or add as data grows and queries drift).

Load this when the bottleneck is the database: slow queries, high DB CPU, connection exhaustion.
Load `schema-design`'s `references/schema-patterns.md` when the question is "what index should this
table have" at design time. Load this when the question is "why did this query that used to be fast
get slow."
