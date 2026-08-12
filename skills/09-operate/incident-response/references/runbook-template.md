# Runbook Template

A runbook is the playbook linked from an alert — the first thing an on-call engineer reads when
paged. It lives next to the alerting rule (alert → runbook link is mandatory; see `observability`
Step 6). A runbook is not documentation; it is an executable procedure written for a stressed
operator at 3am.

## Minimum viable runbook

Every runbook has three parts, nothing less:

```
# [Alert name] — [one-line symptom]

## What it means
[Plain-language: what this alert is telling you. Which user-facing system is affected.
What "normal" looks like vs. what the alert says is happening.]

## First query
[The exact query or command to run to see the current state. Copy-pasteable. Include the
dashboard link, the log query, or the CLI command — not "check the dashboard."]

## Escalation path
[Who to page or contact if the first query confirms the issue is real and beyond your authority.
Include the specific person/role, the channel, and the conditions under which to escalate.]
```

If a runbook has nothing beyond these three, it is still useful. Everything below extends it.

## Extended sections (add as the alert warrants)

### Severity and impact
- Expected severity (SEV1/2/3) — a starting point, the IC confirms
- User-facing impact (which users, what fraction, what they experience)
- Blast radius (which services, which regions, which features)

### Containment options (ordered by speed and safety)
The operator's menu, fastest-first. Each option states the command and the trade-off:

1. **Rollback** — `deploy rollback to <previous-deploy>` (fastest, loses any forward fixes in the
   bad deploy; preferred when the cause is a recent deploy)
2. **Feature flag off** — `<flag-name> = false in <config-service>` (isolates a feature-caused
   issue without rolling back unrelated work)
3. **Fail over** — `route traffic to <healthy-replica/region>` (for regional or
   infrastructure-caused issues; takes minutes, verify the target is healthy first)
4. **Rate limit / shed load** — `<limit config>` (protects the system from collapse under
   runaway traffic; users see degraded service, not outage)
5. **Scale up** — `<scale command>` (for capacity exhaustion; verify autoscaling isn't already
   trying and failing)

### Diagnosis steps (after containment)
- The likely root causes, ranked by probability and how to confirm each
- The log query / trace filter that reveals each cause
- What the metric should look like when the cause is fixed

### Recovery and verification
- How to re-enable any containment measure disabled (feature flag back on, traffic back to
   primary) — only after the fix is confirmed
- The metrics to watch for a sustained window before declaring resolved
- The postmortem trigger (every SEV1/SEV2 gets one; see `references/postmortem-template.md`)

## What a runbook is not

- **Not a debug session.** No "investigate the logs" — give the specific query. The operator is
  stressed; vague instructions produce vague results.
- **Not a design doc.** No architecture explanation. Link to the design doc if context is needed;
  the runbook is action.
- **Not static.** A runbook that references a deprecated dashboard or a service that was renamed
  is worse than no runbook (it misleads). Review runbooks on every service rename, dashboard
  migration, or alert ownership change. The alert-firing test (see `observability` Step 7) is the
  moment to verify the runbook link still resolves and the first query still works.

## Linking from alerts

The alert and the runbook are a pair. The alerting rule's notification template must include the
runbook URL (or a short ID that resolves to it). An alert without a runbook link is a defect —
the `observability` skill's verify checklist catches this. When the alert fires, the operator
should reach the runbook in one click.
