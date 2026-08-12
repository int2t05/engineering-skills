---
name: deprecation-migration
description: Use when deprecating old code or APIs, migrating to a new system, or upgrading dependencies — staged deprecation paths and migration strategies that preserve behavior across the transition. Triggers on "deprecate", "migrate", "sunset API", "弃用", "迁移", "升级依赖", "更新这个库", "upgrade dependency".
---

# Deprecation and Migration

Code is a liability, not an asset. Every line carries maintenance cost — bugs, dependency updates, security patches, onboarding overhead. Deprecation is the discipline of removing code that no longer earns its keep; migration is the process of moving users safely from old to new. Most organizations build things well; few remove them well.

Hyrum's Law makes removal hard: with enough users, every observable behavior becomes depended on — including bugs, timing quirks, and undocumented side effects. Deprecation therefore requires active migration, not just announcement. Plan removal at design time — systems with clean interfaces, feature flags, and minimal surface area are far easier to sunset.

## When to use

- Replacing an old system, API, or library with a new one.
- Sunsetting a feature that's no longer needed, or consolidating duplicate implementations.
- Removing dead code that nobody owns but everybody depends on.
- Planning the lifecycle of a new system (deprecation planning starts at design time).
- Deciding whether to maintain a legacy system or invest in migration.
- Upgrading a dependency or framework version, including major/breaking upgrades (see `references/dependency-upgrade.md`).
- Moving data between systems (dual-write, backfill, CDC, cutover) — see `references/data-migration.md`.

**Not for:** patching a security vulnerability in place (use `security-review`); routine commits (use `git-workflow`).

## Steps

### 1. Make the deprecation decision

Before deprecating anything, answer:

1. Does this system still provide unique value? If yes, maintain it.
2. How many consumers depend on it? Quantify the migration scope.
3. Does a replacement exist? If no, **build the replacement first** — never deprecate without an alternative.
4. What's the migration cost for each consumer? Trivially automated → do it; manual and high-effort → weigh against maintenance cost.
5. What's the ongoing cost of *not* deprecating? Security risk, engineer time, opportunity cost of complexity.

**Zombie-code diagnostic** — if the target shows these signs, it's zombie code: nobody owns it, but everybody depends on it.

- No commits in 6+ months; no assigned maintainer or team
- Failing tests that nobody fixes
- Dependencies with known vulnerabilities that nobody updates
- Documentation referencing systems that no longer exist

Response: assign an owner and maintain it properly, or deprecate it with a concrete migration plan. Zombie code cannot stay in limbo — it either gets investment or removal.

### 2. Choose advisory vs compulsory

| Type | When | Mechanism |
|------|------|-----------|
| **Advisory** | Migration optional; old system stable | Warnings, docs, nudges. Users migrate on their own timeline. |
| **Compulsory** | Security issues, blocks progress, or maintenance unsustainable | Hard deadline; removal by date X. Migration tooling *must* be provided. |

Default to advisory. Use compulsory only when the cost or risk justifies forcing migration — and never just announce a deadline; provide tooling, documentation, and support (the **Churn Rule**: if you own the infrastructure being deprecated, you migrate your users, or provide backward-compatible updates that require no migration).

### 3. Migrate incrementally

1. **Build the replacement** — covers all critical use cases, documented, proven in production (not "theoretically better").
2. **Announce and document** — deprecation notice with status, replacement, removal date, reason, and a migration guide with concrete steps and examples.
3. **Migrate consumers one at a time** — identify touchpoints, update to the replacement, verify behavior matches (tests, integration checks), remove old references, confirm no regressions.
4. **Remove the old system** — only after all consumers migrated. Verify zero active usage (metrics, logs, dependency analysis), then remove code, tests, docs, config, and the deprecation notices. Removing code is an achievement.

### 4. Pick a migration pattern

**Strangler** — run old and new in parallel; route traffic incrementally (0% → 10% canary → 50% → 100%); remove the old system when it handles 0%.

**Adapter** — translate calls from the old interface to the new implementation. Consumers keep using the old interface while you migrate the backend.

```typescript
class LegacyTaskService implements OldTaskAPI {
  constructor(private newService: NewTaskService) {}
  getTask(id: number): OldTask {
    return this.toOldFormat(this.newService.findById(String(id)));
  }
}
```

**Feature flag** — switch consumers one at a time:

```typescript
function getTaskService(userId: string): TaskService {
  if (featureFlags.isEnabled('new-task-service', { userId })) {
    return new NewTaskService();
  }
  return new LegacyTaskService();
}
```

**Concrete example — migrating test helpers to `@total-typescript/shoehorn`.** When the migration target is a library whose API replaces a problematic pattern (e.g. `as` type assertions in tests), the same incremental process applies:

1. Install the replacement: `npm i @total-typescript/shoehorn`.
2. Find call sites: `grep -rE ' as [A-Z]' --include='*.test.ts' --include='*.spec.ts'`.
3. Replace `as Type` → `fromPartial(...)` (partial data that still type-checks); replace `as unknown as Type` → `fromAny(...)` (intentionally wrong data for error tests). Use `fromExact()` to force a full object when you plan to swap to `fromPartial` later.
4. Add imports from `@total-typescript/shoehorn`, run typecheck, verify.

Test code only — never use shoehorn in production code.

**Database schema (expand/contract)** — the riskiest migration because data is the one thing you can't roll back by reverting a deploy. Never change a column in place. Migrate in additive phases so old and new code are both valid at every step:

```
EXPAND ──────→ MIGRATE ──────→ CONTRACT
add new       backfill rows,   once no code reads
column        dual-write       the old column,
(nullable)    old+new          drop it in a later,
              from app         separate deploy
```

Worked example — renaming `name` to `full_name`:

1. **Expand.** Add `full_name` nullable. Deploy. (Old code ignores it.)
2. **Dual-write.** App writes both `name` and `full_name` on every insert/update. Deploy.
3. **Backfill.** Copy `name → full_name` for existing rows, in throttled batches (don't lock the table).
4. **Switch reads.** Point the app at `full_name`, keep writing both. Deploy and bake.
5. **Contract.** Stop writing `name`; in a *separate, later* deploy, drop the column.

Rules: additive first, destructive last and alone; every migration has a tested `down` path; backfill in batches off the hot path; build large indexes without blocking writes (e.g. Postgres `CREATE INDEX CONCURRENTLY`); decouple cutover from code by feature flag when risky.

## Verify

After completing a deprecation:
- [ ] Replacement is production-proven and covers all critical use cases
- [ ] Migration guide exists with concrete steps and examples
- [ ] All active consumers migrated (verified by metrics/logs)
- [ ] Old code, tests, documentation, and config fully removed
- [ ] No references to the deprecated system remain in the codebase
- [ ] Deprecation notices removed (they served their purpose)

After a database schema migration:
- [ ] Change ships in additive phases (expand → backfill → contract), not a single in-place edit
- [ ] Old and new code are both valid against the schema at every deploy step
- [ ] Each migration has a tested down path; backfills run in throttled batches
- [ ] Destructive steps (drop/rename) ship in their own deploy after no code references the old shape

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope, simplicity)
- [references/dependency-upgrade.md](references/dependency-upgrade.md) — changelog/migration-guide reading, breaking-change triage, branch-based upgrade, root-cause fix per break
- [references/data-migration.md](references/data-migration.md) — moving data between systems: dual-write + backfill, CDC, cutover, verification, failure modes
