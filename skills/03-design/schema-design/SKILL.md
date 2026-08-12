---
name: schema-design
description: Use when designing a data model for a new feature or bounded context — entities, relationships, normalization, indexing, constraints, partitioning. Triggers on "data model", "schema design", "database design", "ER model", "数据模型", "表结构设计", "数据库设计".
---

# Schema Design

Design the data model that sits beneath the API and beside the domain language. `architecture`
picks the datastore type; `domain-modeling` sharpens the vocabulary; this skill designs the actual
shape of the data — entities, relationships, indexes, constraints, and how the model scales. A
schema designed reactively (added-to-as-features-arrive) becomes a performance and correctness
liability that is expensive to fix later.

## When to use

- Designing entities and relationships for a new feature or bounded context
- Choosing normalization level, indexing strategy, or partitioning for a new model
- Reviewing a proposed schema for correctness, performance, or future evolution
- Triggers on "data model", "schema design", "database design", "ER model", "数据模型", "表结构设计"

**Not for:** choosing the datastore type (use `architecture`); ubiquitous-language glossary (use
`domain-modeling`); API request/response shapes (use `api-design`); changing an existing schema
in production (use `deprecation-migration`).

## Steps

### 1. Map entities and relationships

Start from the domain model (`domain-modeling` output / CONTEXT.md) and translate nouns into
entities, verbs into relationships. For each entity, identify its identity (primary key), its
attributes, and its lifecycle (created, mutated, archived, deleted).

- Draw an ER diagram (Mermaid erDiagram — see `${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md`)
- Cardinality for every relationship: one-to-one, one-to-many, many-to-many
- Resolve many-to-many with junction tables; never hide them in a comma-separated column

_Verify: every entity in the domain model is represented; every relationship has documented
cardinality._

### 2. Choose normalization level

Normalize by default (3NF / BCNF) — it eliminates anomalies and keeps the model honest. Denormalize
deliberately, only when a measured read pattern justifies the write complexity and consistency
risk. Document every denormalization as a trade-off: what read it optimizes, what write it
complicates, how consistency is maintained.

- Foreign keys for every relationship (enforce referential integrity at the DB level)
- Surrogate keys (UUID/serial) over natural keys unless the natural key is truly immutable
- NULL semantics: every nullable column has a documented meaning — "unknown" vs. "none" vs. "not yet"

_Verify: every FK is enforced; every denormalization is documented with its trade-off._

### 3. Design indexes

Index for the queries, not the columns. Start from the access patterns (how will this data be
read?), then create indexes that serve them. Every index has a cost — write amplification and
storage — so justify each one against a concrete query.

- Composite indexes ordered by selectivity and equality-before-range
- Covering indexes for hot read paths (include columns to avoid table lookups)
- Partial / filtered indexes for common WHERE predicates (e.g. `WHERE deleted_at IS NULL`)
- Unique indexes to enforce business invariants (one active subscription per user)

_Verify: every index maps to a named query; `EXPLAIN` on each access pattern uses an index, not a
seq scan._

### 4. Define constraints and invariants

The database is the last line of defense for data integrity. Push invariants into constraints —
they are enforced regardless of application bugs:

- `NOT NULL` unless the column genuinely can be absent
- `CHECK` constraints for range/format invariants (price ≥ 0, status in allowed set)
- `UNIQUE` constraints for business keys (email, slug, active-session-per-user)
- Foreign key actions: `ON DELETE` / `ON UPDATE` (RESTRICT / CASCADE / SET NULL) chosen deliberately

_Verify: every business invariant is backed by a constraint, not just application logic._

### 5. Plan for scale and evolution

Design the model to survive growth without a painful migration:

- Partitioning strategy for large tables (range by date, hash by tenant) — decide before the table
  hits 100M rows, not after
- Avoid hot writes to a single sequence (use scattered keys or per-tenant sequences at scale)
- Soft delete (`deleted_at` timestamp) for audit-relevant data; hard delete for ephemeral data —
  choose per entity, document why
- Forward-compatible types: `timestamptz` (not `timestamp`), `UUID` or `bigint` (not `int` for IDs
  that may exceed 2B)

_Verify: partitioning decision is documented; ID types won't overflow; soft/hard-delete policy is
stated per entity._

### 6. Document

**Output:** `docs/design/SCHEMA.md` — the data model document: ER diagram, entity definitions with
columns/types/constraints, index plan mapped to access patterns, partitioning strategy, and any
denormalization trade-offs. Reference ADRs for significant model decisions.

## Verify

- [ ] ER diagram drawn (Mermaid); every entity and relationship documented
- [ ] Normalization level stated; every denormalization documented with trade-off
- [ ] Foreign keys enforced at DB level; referential integrity does not rely on application code
- [ ] Indexes mapped to named queries; `EXPLAIN` confirms index usage on access patterns
- [ ] Business invariants backed by CHECK / UNIQUE constraints
- [ ] ID types won't overflow; partitioning strategy stated for growth tables
- [ ] `docs/design/SCHEMA.md` produced with ER diagram + entity/index/constraint plan

**Red flags:** comma-separated lists in a column; missing foreign keys; indexing every column (or
no indexes); `SELECT *` driving the schema; `int` IDs on tables that will grow; NULL with no
documented meaning; relying solely on application code for integrity; no partitioning plan for a
table that will exceed memory.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, enforce simplicity, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md](${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md) — Mermaid erDiagram syntax for entity-relationship diagrams
- [references/schema-patterns.md](references/schema-patterns.md) — normalization trade-offs, index patterns, partitioning strategies, soft-delete policies
