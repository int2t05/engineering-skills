# Compliance Process

Depth reference for the `security-review` skill. The process layer around data privacy compliance
— GDPR, CCPA, HIPAA — that code-level review can't cover. The skill catches PII in code (secrets,
injection, field allowlists); this teaches the compliance workflow: data subject requests, retention
policies, right-to-erasure, privacy-by-design. The skill is "is this code secure?"; this is "can
this system demonstrate compliance to an auditor?"

## 1. Compliance is a process, not a feature

You cannot "add compliance" to a system the way you add auth. Compliance is a documented,
demonstrable practice covering: where data comes from, where it's stored, who accesses it, how long
it's kept, how users exercise their rights, and how you prove all of the above to an auditor.

| Code-level security (the skill) | Compliance process (this reference) |
|---|---|
| PII encrypted at rest | Can you prove it to an auditor? |
| No secrets in code | Data inventory: where is every PII field stored? |
| Input validation | Data subject request: can you find and export a user's data? |
| Access control | Right-to-erasure: can you delete a user's data across all stores? |

The skill is necessary but not sufficient. A system can pass security-review and fail compliance
because the process layer is missing.

## 2. Data inventory — the foundation

You cannot comply with "delete this user's data" if you don't know where it is.

| Field | Track per data element |
|---|---|
| **What** | The data field (email, phone, purchase history, IP log) |
| **Where** | Every store: primary DB, replica, analytics warehouse, search index, cache, backup, log |
| **Why** | The legal basis (consent, contract, legitimate interest, legal obligation) |
| **Who** | Who can access it; what role/permission |
| **How long** | Retention period; deletion trigger |
| **Origin** | Where it came from (user input, third-party, derived) |

Build this as a living document (data map), not a one-time audit. Every new data field added in a
PR updates the map. A field not in the map is a compliance gap.

## 3. Data subject requests (DSR / DSAR)

GDPR/CCPA grant users rights to their data. The system must be able to fulfill:

| Right | What it means | System capability needed |
|---|---|---|
| **Access** | "Give me all data you hold about me" | Export all user's data across all stores, in a portable format |
| **Erasure** | "Delete all data about me" | Delete across all stores (including backups, logs, analytics) |
| **Portability** | "Give me my data in a machine-readable format" | Structured export (JSON/CSV), not a PDF |
| **Rectification** | "Correct this wrong data" | Update across all stores; audit trail of the change |
| **Objection** | "Stop processing my data for purpose X" | Per-purpose consent flags; suppress processing without deleting |
| **Restriction** | "Temporarily stop processing" | Flag to freeze processing while dispute is resolved |

### Erasure is the hard one

Deleting a user's primary record is easy; deleting their data *everywhere* is the challenge:

- **Primary DB** — DELETE row (or anonymize: replace PII with hashes/nulls, keep the row for
  referential integrity).
- **Analytics warehouse** — delete or anonymize their events. This often requires a batch job, not
  a live DELETE.
- **Search index** — remove their documents; re-index.
- **Backups** — you cannot delete from a backup without restoring. Standard practice: the erasure
  takes effect on next backup rotation; document this policy (auditors accept it if documented).
- **Logs** — PII in logs (email in an access log) must be scrubbed or aged out per retention.
- **Third parties** — if you shared data with a processor (email tool, analytics SaaS), you must
  forward the erasure request to them and confirm.

An erasure that misses any store is a compliance failure. The data inventory (§2) is what makes
this possible — you can only delete everywhere if you know everywhere.

## 4. Retention policies

Keep data only as long as you have a documented reason. "Keep forever" is a compliance and cost
liability.

| Data type | Typical retention | Legal basis |
|---|---|---|
| Active user account | Until user deletes account or account goes dormant (then N days) | Contract |
| Transaction/financial | 7 years (varies by jurisdiction) | Legal obligation |
| Security/access logs | 90 days - 1 year | Legitimate interest (security) |
| Marketing data | Until consent withdrawn | Consent |
| Inactive user data | Delete or anonymize after N months dormant | Documented policy |

Implement retention as automated jobs, not manual cleanup:
- **Time-based** — `DELETE FROM logs WHERE created_at < NOW() - INTERVAL 90 DAY` (scheduled).
- **Event-based** — delete on event (user deletion, contract end).
- **Tiered** — move to cold storage after N days, delete after M days.
- **Documented exceptions** — litigation hold overrides retention; document why data is kept past
  its normal period.

## 5. Privacy by design

Bake privacy into the system, not bolt on after:

- **Data minimization** — collect only what you need. "We might want it later" is not a reason to
  store PII.
- **Purpose limitation** — each data field has a documented purpose; don't reuse data for a new
  purpose without new consent.
- **Default private** — default settings favor privacy (opt-in marketing, not opt-out; private-by-default
  profiles).
- **Pseudonymization** — where possible, store identifiers (user_id) instead of direct PII (email);
  map back through a controlled table.
- **Access minimization** — access to PII is role-scoped and logged; "all engineers can read all
  user data" is a compliance failure.

## 6. Cross-border data transfer

GDPR restricts transferring EU personal data outside the EU:

- **Adequate countries** — some regions are deemed adequate (transfer freely).
- **Standard Contractual Clauses (SCCs)** — contractual mechanism with the non-EU processor.
- **Data localization** — store EU users' data in EU regions (simplest compliance; the cloud
  region is a config, not a legal argument).

For most products: store user data in the region closest to the user (EU users → EU region, US
users → US region). This satisfies localization requirements and improves latency.

## 7. Demonstrating compliance (the audit)

An auditor asks: "prove you do what you say." Have ready:

- **Data inventory** (§2) — current, matches the actual system.
- **DSR procedure** — documented steps + log of past requests and response times.
- **Retention policy** — documented + evidence the jobs run (job logs, data age distribution).
- **Access logs** — who accessed PII, when, why (auditable trail).
- **Consent records** — for each user, what they consented to, when, how (version of consent text).
- **Vendor DPAs** — data processing agreements with every third party that touches PII.
- **Incident log** — security incidents involving PII + breach notification records (GDPR: 72-hour
  notification).

The audit is not "are we compliant?" but "can you prove it?" A practice you do but can't
demonstrate is indistinguishable from a practice you don't do.

## 8. When this applies vs the skill

| Situation | Use |
|---|---|
| Code has hardcoded secret, SQL injection, missing authz | `security-review` (code-level) |
| "Can we log this PII field?" | `security-review` (does the code log it) + this (should we, per policy) |
| "User requested all their data" | This (DSR fulfillment process) |
| "How long do we keep access logs?" | This (retention policy) |
| "Are we GDPR-ready for launch?" | This (the process audit) |
| "Is this endpoint vulnerable to XSS?" | `security-review` (code-level) |

The skill secures the code; this reference builds the process around it. Most products need both —
code-level security is necessary, but an auditor won't pass you on "the code looks secure" alone.
