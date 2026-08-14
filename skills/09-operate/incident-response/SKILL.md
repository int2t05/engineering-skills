---
name: incident-response
description: Use when a production incident is live or just resolved — severity classification, containment, comms, rollback-vs-fix decisions, and blameless postmortem. Triggers on "incident", "on-call", "page", "postmortem", "事故响应", "线上故障", "复盘".
---

# Incident Response

When production is failing, the first job is containment, not root cause. This skill structures
the live-incident workflow: classify severity, stop the bleeding, communicate, then diagnose — the
inverse of `debugging`, which builds a red loop first. A blameless postmortem follows every
incident so the system improves, not just the symptom.

## When to use

- A production incident is live (page fired, users affected, error spike)
- An incident just resolved and needs a postmortem
- Reviewing or rehearsing incident response readiness
- Triggers on "incident", "on-call", "page", "postmortem", "事故响应", "线上故障", "复盘"

**Not for:** diagnosing a dev-time bug (use `debugging`); adding telemetry after the fact (use
`observability`); launching a new release (use `shipping`). This skill is for when something
already running has broken.

## Steps

### 1. Declare and classify severity

Assign a severity within the first 5 minutes — severity drives everything downstream (who wakes
up, how fast you respond, what comms are required). Use a fixed scale, not ad-hoc:

- **SEV1** — user-facing outage or data loss. Page everyone. Incident commander assigned.
- **SEV2** — significant degradation, partial outage. Page on-call. IC assigned.
- **SEV3** — minor degradation, workaround exists. Ticket, address in business hours.

Record the declaration: start time, severity, initial symptom, who is IC. _Verify: severity is
written down with a timestamp, not just in someone's head._

### 2. Contain (stop the bleeding)

The first decision is containment vs. fix. Containment is faster and safer — rollback, disable
the offending feature flag, route around the failing dependency, shed load. A fix under pressure
is a second incident waiting to happen.

- Rollback to the last known-good deploy (fastest). Platform commands: `kubectl rollout undo deployment/<name>` (Kubernetes), `aws deploy create-deployment --revision REVISION<prev>` (AWS CodeDeploy), `gcloud run services update-traffic --to-revisions` (Cloud Run), `vercel rollback <url>` (Vercel). The `shipping` skill documents *when* to roll back (trigger conditions); these are the *how* commands for a live SEV1.
- Disable the feature flag that triggered the issue
- Fail over to a healthy replica or region
- Rate-limit or circuit-break the failing path

Only attempt a forward fix if rollback is impossible (irreversible migration, no prior deploy)
and the fix is small and obvious. _Verify: the bleeding has stopped — error rate dropping or
users recovering — before moving to diagnosis._

### 3. Communicate

The IC owns comms. Establish a single incident channel and a cadence:

- **Internal:** status update every 15–30 min (SEV1) or hourly (SEV2): current state, what's been
  tried, next step, owner, ETA. Stale silence breeds panic and duplicate work.
- **External:** status page update for user-facing incidents — users tolerate outage, they don't
  tolerate silence. Update at the same cadence as internal.
- **Stakeholders:** notify leadership for SEV1; keep them informed, not involved in the fix.

_Verify: the last update is less than 30 min old and states the next action with an owner._

### 4. Diagnose (after containment)

With the bleeding stopped, find root cause. Apply `debugging` discipline: build a hypothesis,
instrument, verify — but under the incident's time pressure, favor the fastest path to a confirmed
cause over exhaustive analysis. Use the telemetry `observability` built: traces, metrics, logs,
correlation IDs. If the diagnosis stalls, contain harder and hand off to a fresh responder.

_Verify: root cause is stated as a confirmed hypothesis with supporting evidence (log line, metric
spike, deploy diff), not a guess._

### 5. Fix and verify

Apply the smallest fix that addresses the root cause. Verify at runtime — error rate returned to
baseline, affected users recovered, no new regression. Re-enable any containment measures
disabled (feature flags, failover) only after the fix is confirmed.

_Verify: production metrics are at baseline for a sustained window (not a single point) before
declaring resolved._

### 6. Postmortem (blameless)

Within 48 hours, write a blameless postmortem. Blameless means: focus on the system and process,
not individuals — "the deploy bypassed the canary" not "X deployed without checking." Every
contributing factor is a system gap, not a personal failure.

- **Timeline:** minute-by-minute from detection to resolution
- **Impact:** users affected, duration, data loss, revenue
- **Root cause:** the confirmed cause from step 4
- **Contributing factors:** what made it possible (missing test, no alert, manual step)
- **What went well:** detection time, rollback worked, comms cadence held
- **Action items:** specific, owned, dated — each addresses a contributing factor

**Output:** `docs/postmortem/YYYY-MM-DD-<slug>.md` — one file per incident, archived for
organizational learning.

## Verify

- [ ] Severity declared within 5 min, written down with timestamp
- [ ] Containment chosen over forward-fix unless rollback was impossible
- [ ] Comms cadence established; last update <30 min old during the incident
- [ ] Root cause stated with evidence (not a guess)
- [ ] Production metrics at baseline for a sustained window before "resolved"
- [ ] Postmortem written within 48 hours, blameless, with owned action items

**Red flags:** diagnosing before containing; no written severity declaration; silent incident
channel; forward-fixing under pressure when rollback was available; postmortem that names
individuals instead of system gaps; action items with no owner or date.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surface assumptions)
- [references/runbook-template.md](references/runbook-template.md) — runbook format for alert-linked playbooks
- [references/postmortem-template.md](references/postmortem-template.md) — blameless postmortem template + action-item tracking
- [references/dr-planning.md](references/dr-planning.md) — load during postmortem action-item planning for proactive DR; backup strategy, restore testing, DR drills, failover orchestration
