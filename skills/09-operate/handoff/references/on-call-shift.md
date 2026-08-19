# On-Call Shift Handoff

Depth reference for the `handoff` skill. The on-call shift handoff: transferring
operational responsibility from one on-call engineer to the next. This is distinct from
the dev-work handoff (transferring a coding task between sessions) — the on-call handoff
transfers situational awareness of a live system, not a work-in-progress.

## Contents

- [1. What to hand off](#1-what-to-hand-off)
- [2. Pre-shift checklist (incoming)](#2-pre-shift-checklist-incoming)
- [3. Mid-shift responsibilities](#3-mid-shift-responsibilities)
- [4. Post-shift checklist (outgoing)](#4-post-shift-checklist-outgoing)
- [5. Escalation triggers](#5-escalation-triggers)
- [6. Distinction from dev-work handoff](#6-distinction-from-dev-work-handoff)

## 1. What to hand off

The incoming on-call needs to understand the system's current state without reading the
last 12 hours of logs. Five categories:

| Category | What to cover |
|---|---|
| **Active incidents** | What's broken right now, severity, current status, who's working on it |
| **In-progress investigations** | Anomalies being watched but not yet incidents; what's been ruled out |
| **Recent changes** | Deploys, config changes, feature flags toggled in the last 24h |
| **Known issues** | Chronic problems, degraded dependencies, workarounds in effect |
| **Escalation triggers** | What would make the incoming on-call page someone else |

### Active incidents

For each live incident:
- Severity (SEV1 through SEV3) and user impact
- When it started, what triggered it (deploy, dependency, traffic spike)
- Current status: mitigated / investigating / waiting on external dependency
- Who's engaged (incident commander, service owner, vendor support)
- Next step the incoming on-call should take

If there are zero active incidents, state that explicitly — "no active incidents" is
information, not an omission.

### In-progress investigations

Things that aren't incidents yet but are being watched:
- Anomaly in metrics (p99 latency trending up, error rate slightly elevated)
- Intermittent issue (fails 1 in 1000 requests, not reproducible)
- What's been checked and ruled out (so the incoming doesn't re-investigate)

### Recent changes

The last 24 hours of changes, because most incidents are caused by a recent change:
- Deploys (service, version, time)
- Feature flag toggles (flag name, rollout percentage, time)
- Infrastructure changes (scaling, config, DNS)
- Dependency upgrades

### Known issues

Chronic conditions the incoming on-call should be aware of:
- Degraded dependency (third-party API returning errors intermittently)
- Capacity pressure (DB at 80%, queue depth rising)
- Workarounds in effect (a feature disabled, a retry tuned higher than normal)

### Escalation triggers

The conditions under which the incoming on-call should escalate — defined now, not during
a 3am incident:
- When to page the service owner (not the on-call)
- When to declare a SEV-1 and engage incident response
- When to page a manager or executive
- Vendor escalation contacts and contract SLA windows

## 2. Pre-shift checklist (incoming)

Before taking the pager:

- [ ] Read the outgoing handoff brief (all five categories)
- [ ] Acknowledge active incidents — confirm you understand the current status and next step
- [ ] Review the dashboard for any new anomalies since the handoff was written
- [ ] Verify on-call tooling: paging app, dashboard access, runbook links resolve
- [ ] Confirm escalation contacts are current (service owners, vendor support numbers)
- [ ] Check the deploy calendar — is a deploy scheduled during your shift? Who's running it?
- [ ] Verify you can reach the chat channel and incident bridge

If any of these are unclear, ask the outgoing on-call before they go off-shift. After
they're off-shift, assumptions become guesses.

## 3. Mid-shift responsibilities

During the shift:

- **Acknowledge pages within the defined SLA** (typically 5 minutes for SEV-1, 15 for SEV-2).
- **Update the incident channel** with status every 30 minutes for active incidents —
  silence is the enemy of coordinated response.
- **Log every action** taken during an incident — timeline reconstruction depends on it.
- **Watch for cascading effects** — a fix for one service may shift load to another.
- **Hand off mid-shift if an incident spans shift boundary** — the incident commander
  role transfers explicitly, with a status update in the incident channel.

## 4. Post-shift checklist (outgoing)

Before handing off the pager:

- [ ] Write the handoff brief covering all five categories (§1)
- [ ] For each active incident: current status, next step, who's engaged
- [ ] For each investigation: what's been ruled out, what to check next
- [ ] List all deploys, flag toggles, and changes during your shift
- [ ] Note any new known issues or workarounds you put in place
- [ ] Confirm the incoming on-call has acknowledged the brief
- [ ] Stay available for 15 minutes after handoff for follow-up questions

The brief goes in the shared on-call document or channel — not in a DM. Future shifts
will reference it; a DM is invisible to them.

## 5. Escalation triggers

Define these before the shift, not during an incident:

| Trigger | Action |
|---|---|
| SEV-1 incident (user-facing outage) | Page incident-response IC; engage service owner; open bridge |
| Error budget depleted (SLO breached) | Freeze non-essential deploys; notify engineering lead |
| Incident exceeds 1 hour without mitigation | Escalate to service owner; consider rollback |
| Incident spans multiple services | Engage incident-response; coordinate across service owners |
| Vendor dependency down | Open vendor support ticket; check vendor status page; notify affected users |
| Security incident (suspected breach, vulnerability) | Page security on-call; follow security incident process |
| On-call unsure how to proceed | Page secondary on-call or service owner — uncertainty is a valid trigger |

### The uncertainty rule

Escalating because you don't know what to do is correct, not a failure. The failure is
sitting on an incident for 30 minutes hoping it resolves itself. Define the "if unsure,
escalate in 10 minutes" rule explicitly.

## 6. Distinction from dev-work handoff

| | Dev-work handoff | On-call shift handoff |
|---|---|---|
| **What transfers** | A coding task (context, decisions, next steps) | Operational responsibility (system state, active incidents) |
| **Audience** | The next agent/session continuing the work | The next on-call engineer taking the pager |
| **Artifacts** | Specs, plans, commits, diffs | Dashboards, alerts, incident channels, runbooks |
| **Timeframe** | Days to weeks | Hours (shift length) |
| **Success criteria** | Next session continues the work without asking "what's the state?" | Incoming on-call handles any incident without re-discovering context |

The `handoff` skill's Steps cover the dev-work handoff. This reference adds the on-call
shift variant — load it when the handoff is operational (pager transfer), not
developmental (task transfer).
