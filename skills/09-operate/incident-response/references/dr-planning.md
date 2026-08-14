# Disaster Recovery Planning

Depth reference for the `incident-response` skill. The proactive sibling of incident response:
planning and rehearsing recovery *before* the failure. The skill handles the live incident; this
teaches how to design backup strategy, test restores, run DR drills, and validate RPO/RTO targets.
RPO/RTO targets are recorded at design time (`architecture/references/nfr-checklist.md`); this is
the ongoing practice of proving you can actually meet them.

## Contents

- [1. RPO and RTO — what you're planning for](#1-rpo-and-rto--what-youre-planning-for)
- [2. Backup strategy](#2-backup-strategy)
- [3. Restore testing — the practice most teams skip](#3-restore-testing--the-practice-most-teams-skip)
- [4. Failover orchestration](#4-failover-orchestration)
- [5. DR drill procedure](#5-dr-drill-procedure)
- [6. What DR planning is NOT](#6-what-dr-planning-is-not)

## 1. RPO and RTO — what you're planning for

| Target | Definition | Planning question |
|---|---|---|
| **RPO** (Recovery Point Objective) | Max acceptable data loss | How often do we back up? Can we tolerate losing N minutes/hours? |
| **RTO** (Recovery Time Objective) | Max acceptable downtime | How fast can we restore? Can we tolerate being down for N hours? |

RPO drives backup frequency; RTO drives recovery procedure complexity. Tight targets (RPO near 0,
RTO near 0) require replication + automated failover, not restore-from-backup.

| Target tier | RPO | RTO | How |
|---|---|---|---|
| Critical | < 1 min | < 15 min | Multi-region active-active or hot standby + automated failover |
| Important | < 1 hr | < 4 hr | Hot replica + automated or runbook-driven failover |
| Standard | < 24 hr | < 24 hr | Daily backup + documented restore procedure |
| Archive | whatever | whatever | Cold backup; restore when convenient |

Tier every service and document its target. A single RPO/RTO for "the system" hides that the
billing service can tolerate 4h downtime but the auth service cannot.

## 2. Backup strategy

| Strategy | RPO | Cost | When |
|---|---|---|---|
| **Continuous replication** | Near-zero | High (replica infra) | Critical tier; data loss unacceptable |
| **Snapshot + WAL/binlog shipping** | Minutes | Medium | Important tier; point-in-time recovery needed |
| **Scheduled full + incremental** | Hours | Low | Standard tier; daily backup sufficient |
| **Cold/offline backup** | Days | Lowest | Archive; data rarely needed |

Rules:
- **Backups are immutable** — ransomware/corruption that hits primary must not be able to delete
  backups. Use object-lock / WORM, or a separate account.
- **3-2-1 rule** (for critical data): 3 copies, 2 media, 1 off-site (or off-cloud-region).
- **Encrypt at rest** — backups contain production data; encrypt and test key recovery too (a
  backup you can't decrypt is no backup).
- **Document the restore**, not just the backup — a backup untested is a hope, not a recovery.

## 3. Restore testing — the practice most teams skip

A backup is only as good as the last successful restore. Untested backups fail silently (corrupted,
incomplete, wrong format, missing dependencies).

| Test cadence | What | Who |
|---|---|---|
| **Monthly** | Restore a random backup to a staging env; verify it boots + serves | On-call rotation |
| **Quarterly** | Full DR drill: restore all critical services from backup in a clean region | Whole team |
| **Annually** | Tabletop exercise: walk through a major scenario (region loss) end-to-end | Team + stakeholders |

### Restore test checklist
- [ ] Backup located and accessible (not just "exists" — actually downloadable)
- [ ] Restore completes within RTO target (measure, don't assume)
- [ ] Restored data is usable (queries return expected results, row counts match)
- [ ] Restored system boots and serves traffic (not just "DB is up" — app works end-to-end)
- [ ] Restore works from the oldest backup too (format hasn't drifted; old backups are not silently
      broken)
- [ ] Document the restore time — if RTO was 4h and restore took 6h, the target is a lie; fix it

## 4. Failover orchestration

For critical-tier services with automated failover:

- **Health-check driven** — failover triggers on health-check failure, not human decision. A human
  who takes 15 minutes to decide defeats a 15-minute RTO.
- **Failover is tested** — run failover in production regularly (Netflix Chaos Monkey philosophy).
  An untested failover fails when you need it.
- **Failback is planned** — failing over is half the job; failing back to the primary after repair
  is often harder (data divergence, replication lag). Document and test failback too.
- **DNS/routing automation** — traffic shifting must be automated (DNS, load balancer, service
  mesh). Manual DNS changes are too slow for tight RTO.
- **Region failover, not just instance** — for multi-region: test that the standby region can
  handle full load (it's often under-provisioned to save cost, defeating the purpose).

## 5. DR drill procedure

A DR drill is not "we restored a backup." It's a full rehearsal of the disaster scenario:

```
1. Declare the drill (scope, time, success criteria, abort conditions)
2. Simulate the failure (stop the primary, "lose" the region, corrupt data)
3. Execute the recovery procedure (as documented — no improvisation)
4. Measure: actual RPO (data lost), actual RTO (time to serve)
5. Verify: system serves real traffic correctly (run tests, check data)
6. Failback to normal
7. Postmortem: what worked, what didn't, what to fix
```

Rules:
- **No improvisation during drill** — if the runbook is wrong, that's a finding; fix the runbook.
  Improvising in a drill hides the gap you're drilling to find.
- **Drill the worst case** — not "primary DB is slow," but "primary region is unreachable." The
  worst case is what you're planning for; drill it.
- **Include people, not just systems** — who gets paged? Who decides? Who communicates? A DR
  procedure that assumes a specific person is available fails when they're on vacation.

## 6. What DR planning is NOT

- **Not a backup tool config** — the tool backs up; DR planning proves recovery works.
- **Not incident response** — incident response handles the live failure; DR planning is the
  rehearsal that makes the live failure survivable.
- **Not a one-time doc** — a DR plan untested in 6 months is fiction. Services change, backups
  drift, runbooks rot. Recurring drills are the point.
- **Not "we have multi-AZ"** — multi-AZ handles instance failure, not region failure or data
  corruption. A corrupted write replicated to all AZs is still corrupted everywhere. Test the
  scenario, not just the topology.
