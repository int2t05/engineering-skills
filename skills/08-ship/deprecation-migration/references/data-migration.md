# Data Migration

Depth reference for the `deprecation-migration` skill. Moving data between systems — bulk
transfer, dual-write, change data capture, backfill, cutover — the discipline the skill's
schema/code/API migration Steps don't cover. Schema migration (altering table structure in place)
is handled in the skill's expand/contract Steps; this is about moving data to a different system.

## 1. When this applies

- Replacing one datastore with another (MySQL → Postgres, monolith DB → service-owned DB).
- Splitting a shared table into per-service tables.
- Changing data shape across systems (not in-place schema change — a new system with new shape).
- Backfilling derived data into a new column/store after adding it.
- Migrating to a new search index, cache layer, or message broker.

If the data stays in the same system and only the schema changes, use the skill's expand/contract
Steps, not this reference.

## 2. Migration strategies

| Strategy | How | When | Risk |
|---|---|---|---|
| **Bulk copy + cutover** | Stop writes → copy all data → switch reads/writes to new → resume | Small dataset, can tolerate downtime | Cutover failure = downtime + manual rollback |
| **Dual-write + backfill** | Write to both old + new simultaneously; backfill historical; cut reads to new; stop old writes | Zero-downtime required, new schema compatible | Dual-write consistency; backfill window |
| **Change data capture (CDC)** | Stream changes from old to new in near-real-time; cut over when caught up | Large dataset, continuous operation, can't stop writes | CDC lag; ordering; tooling complexity |
| **Shadow + compare** | Write to new but don't use it; compare outputs; cut over when verified | High-stakes, need validation before trust | Extra write cost; comparison logic |

Default choice: dual-write + backfill for zero-downtime; bulk copy + cutover for small or
tolerant-of-downtime. CDC for large + can't-stop. The trade-off is always complexity vs downtime.

## 3. Dual-write + backfill (the most common zero-downtime pattern)

```
Phase 1: Dual-write (write to both old + new)
  - Every write goes to old (source of truth) AND new
  - New writes can be async (fire-and-forget) if eventual consistency is OK
  - Log failures; a failed write to new creates a gap to backfill

Phase 2: Backfill historical data
  - Copy existing rows from old to new in batches
  - Throttle: batch size + sleep to avoid overloading either system
  - Idempotent: re-running a batch must not duplicate (use upserts / natural keys)
  - Track progress: last-migrated-id cursor, not row count (deletes skew counts)

Phase 3: Verify
  - Row count reconciliation (with caveat: concurrent writes mean counts drift)
  - Content sampling: pick N random rows, compare field-by-field
  - Reconciliation job: hash old vs new per row, report mismatches
  - Do NOT skip this — silent data loss is the worst failure mode

Phase 4: Cut reads to new
  - Switch read traffic from old to new (feature flag, gradual rollout)
  - Keep dual-writing during this phase — rollback is still possible

Phase 5: Stop old writes
  - Only after reads are fully on new and verified stable for a sustained period
  - Keep old data read-only for a grace period (rollback safety net)
  - Eventually delete old (after the grace period + confirmed no reads)
```

## 4. Backfill discipline

Backfill is where most migrations fail silently.

- **Idempotent batches** — re-running batch N must not duplicate or overwrite newer data. Use
  `INSERT ... ON CONFLICT UPDATE` (upsert) with a `updated_at` guard: only update if the new row's
  `updated_at` >= existing.
- **Cursor, not offset** — paginate by a stable cursor (id, timestamp), not OFFSET (deletes +
  inserts make OFFSET skip or duplicate rows). `WHERE id > last_cursor ORDER BY id LIMIT N`.
- **Throttle** — batch size (1000-10000 rows) + sleep between batches. Watch both systems' load.
- **Resumable** — persist the cursor; a crash mid-backfill resumes from last position, not start.
- **Track gaps** — dual-write failures during Phase 1 create rows in old but not new. The backfill
  must catch them, not just pre-Phase-1 data.

## 5. Change data capture (CDC)

For large datasets where dual-write isn't feasible (can't modify every write path, or dataset is
too large to backfill in a maintenance window).

```
Old DB → transaction log (WAL/binlog) → CDC tool (Debezium, etc.) → stream → new DB
```

- **CDC reads the transaction log**, not the app — captures every write regardless of code path.
- **Near-real-time** — new DB lags old by seconds to minutes, not hours.
- **Ordering preserved** — transaction log is ordered; new DB applies in same order.
- **Cutover** — when new DB's lag is consistently near-zero, cut reads; then cut writes.

CDC risks:
- **Lag spikes** — under load, lag grows; monitor it, alert if lag exceeds SLO.
- **Schema changes mid-migration** — a schema change on old must propagate to new; pause schema
  changes during migration if possible.
- **Tooling complexity** — CDC tooling is operationally heavy; weigh vs dual-write.

## 6. Cutover

The moment reads/writes switch. Minimize blast radius:

- **Feature-flag the cutover** — route a percentage of reads to new first; monitor; ramp up.
- **Keep old writable during read cutover** — if new has issues, you haven't lost writes.
- **Write cutover is the point of no return** — once writes go to new only, old diverges. Keep old
  writable for a grace period as rollback safety; reconcile before final deletion.
- **Have a documented rollback** — what triggers rollback, who decides, how to execute. A cutover
  without a rollback plan is a bet, not a migration.

## 7. Verification

The migration is not done when cutover succeeds — it's done when verified.

| Check | How |
|---|---|
| **Row count** | old vs new; expect drift if concurrent writes — investigate large gaps |
| **Content hash** | hash each row (or a sample); compare old vs new |
| **Referential integrity** | foreign keys / joins produce same results on both |
| **Query equivalence** | run representative queries against both; diff results |
| **Business metric** | the business metric the data drives (e.g. revenue total) matches |
| **No new errors** | error rate on new is within baseline after cutover |

Silent data loss is the worst failure: cutover "succeeds," errors are zero, but 0.1% of rows are
missing or corrupted. Content hashing and sampling catch this; row count alone does not.

## 8. Common failure modes

- **Dual-write gap** — a write succeeds on old, fails on new, gap never backfilled. Mitigation: log
  failures, backfill catches them, verify detects them.
- **Backfill not idempotent** — re-running duplicates rows. Mitigation: upsert + idempotency keys.
- **OFFSET pagination** — skips/duplicates rows as data changes mid-backfill. Mitigation: cursor.
- **Cutover without rollback** — new has a latent bug, can't go back. Mitigation: keep old
  writable, document rollback trigger.
- **"It matched in staging"** — staging data is smaller/simpler; production reveals edge cases.
  Mitigation: verify against production-scale, not staging-scale.
- **Schema drift mid-migration** — old schema changes while migration runs; CDC/backfill breaks.
  Mitigation: freeze schema changes during migration.

## 9. How this connects to the skill

The `deprecation-migration` skill's Steps cover:
- **Code/API migration** (Strangler pattern, Adapter pattern, feature-flag switching)
- **Schema migration** (expand/contract — add new column, backfill, switch, drop old)
- **Dependency upgrade** (`references/dependency-upgrade.md`)

This reference covers **data migration between systems** — when the data moves to a new home, not
just a new shape. Load this when the migration is "move data to a different datastore/system,"
not "alter the existing schema."
