# Blameless Postmortem Template

A postmortem turns an incident into organizational learning. Blameless means: focus on the system
and process, never on individuals. "The deploy bypassed the canary" is a system gap; "X deployed
without checking" is blame. Every contributing factor is a system failure that allowed the human
action to cause an incident — fix the system, not the human.

## Contents

- [When to write a postmortem](#when-to-write-a-postmortem)
- [Template](#template)
- [Action-item tracking](#action-item-tracking)
- [What a blameless postmortem is not](#what-a-blameless-postmortem-is-not)

## When to write a postmortem

- Every SEV1 and SEV2 incident, within 48 hours of resolution
- Any near-miss that would have been SEV1/SEV2 had it reached users
- At the IC's discretion for SEV3 incidents with surprising root causes

## Template

```markdown
# Postmortem: [incident title] — [YYYY-MM-DD]

## Summary
[One paragraph: what happened, who was affected, for how long, and the root cause in one sentence.
A reader who skims only this paragraph should understand the incident.]

## Severity and impact
- Severity: SEV[N] (declared at [time], confirmed at [time])
- User impact: [N users / X% of traffic] experienced [specific degradation] for [duration]
- Data impact: [any data loss, corruption, or inconsistency — or "none"]
- Revenue impact: [estimate or "not material"]

## Timeline (all times UTC or local, state which)
- [HH:MM] — [detection: alert fired / user report / internal notice]
- [HH:MM] — [severity declared, IC assigned]
- [HH:MM] — [containment action taken: rollback / flag off / failover]
- [HH:MM] — [comms: internal update / status page update]
- [HH:MM] — [root cause identified: the evidence that confirmed it]
- [HH:MM] — [fix applied]
- [HH:MM] — [metrics returned to baseline, incident declared resolved]
- [HH:MM] — [postmortem started]

[Every minute with an action. Gaps in the timeline are questions: "what happened between
detection and containment?" If you can't fill a gap, that's a finding.]

## Root cause
[The confirmed cause, stated as a technical fact with supporting evidence — the log line, the
metric spike, the deploy diff, the config change. Not a guess. If multiple causes contributed,
list the primary and the contributors separately.]

## Contributing factors
[What made this possible — system and process gaps, not people. Each factor is a thing that,
if it had been different, would have prevented or shortened the incident:]
- [e.g. "The canary stage was bypassed because the deploy pipeline allowed a `--skip-canary`
  flag for 'urgent' deploys; the flag was used 12 times in the last quarter."]
- [e.g. "The alert fired 14 minutes after user impact began; the threshold was set for daily
  volume, not for the 5-minute window that would have caught the spike early."]
- [e.g. "The runbook linked from the alert pointed to a dashboard that was migrated last month;
  the operator spent 8 minutes finding the current dashboard."]

## What went well
[The parts of the response that worked — credit the system, not just the people:]
- [e.g. "Rollback completed in 90 seconds; the one-click rollback tool worked as designed."]
- [e.g. "The status page was updated within 5 minutes of SEV1 declaration."]

## Action items
[Specific, owned, dated. Each addresses a contributing factor. No action item without an owner
and a date — "we should improve testing" is not an action item.]

| # | Action | Owner | Due | Addresses |
|---|--------|-------|-----|-----------|
| 1 | Remove `--skip-canary` flag from deploy pipeline | @name | YYYY-MM-DD | contributing factor 1 |
| 2 | Lower alert threshold to 5-min window; test-fire | @name | YYYY-MM-DD | contributing factor 2 |
| 3 | Update runbook link to current dashboard; audit all runbook links | @name | YYYY-MM-DD | contributing factor 3 |

## Lessons learned
[1-3 sentences: what this incident taught the team about the system that wasn't obvious before.
The generalizable insight, not the specific fix.]

## Appendix
- Links: alert rule, deploy diff, dashboard snapshot at peak, relevant logs (redacted of PII)
- Chat transcript archive (the incident channel, exported)
- Related postmortems (if this incident shares a pattern with a prior one)
```

## Action-item tracking

Action items are worthless if they age into a backlog and die. Track them:

- Each action item has an owner (one person, not a team) and a due date
- Review open action items in a weekly or biweekly meeting until all close
- An item is "done" when the fix is deployed and verified, not when the ticket is moved
- If an item is deprioritized or dropped, record the decision and the reason — silent death is
  how the same incident recurs next year
- Patterns across postmortems: if three incidents cite the same contributing factor (e.g. "alert
  threshold too high"), that's a systemic gap, not three separate items — escalate to a structural
  fix

## What a blameless postmortem is not

- **Not a blame session.** No individual names in the "what went wrong" sections. The IC and
  responders appear in the timeline as roles, not targets. The phrase "human error" is banned —
  it's "the system allowed/required a human to make this error."
- **Not a rubber stamp.** A postmortem with no action items means either the incident was trivial
  (then why write one?) or the contributing factors weren't examined hard enough.
- **Not a spec.** Don't redesign the system here. The postmortem identifies what to fix; the fix
  is designed and implemented in normal engineering flow, linked from the action item.
