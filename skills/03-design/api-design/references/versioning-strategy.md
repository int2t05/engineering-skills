# API Versioning Strategy

Depth reference for the `api-design` skill. How to version an API when a breaking change is
unavoidable, and how to deprecate old versions on a timeline. The skill's "One-Version Rule" and
"Addition Over Modification" cover design-time extension (avoid breaking changes); this covers what
happens when a breaking change is necessary and dual-version coexistence is needed.

## Contents

- [1. When to version vs extend](#1-when-to-version-vs-extend)
- [2. Versioning strategies](#2-versioning-strategies)
- [3. Sunset and deprecation headers](#3-sunset-and-deprecation-headers)
- [4. Dual-version coexistence](#4-dual-version-coexistence)
- [5. Sunset timeline](#5-sunset-timeline)
- [6. Breaking-change communication](#6-breaking-change-communication)
- [7. How this connects to the skill](#7-how-this-connects-to-the-skill)

## 1. When to version vs extend

Prefer extension over versioning — most "breaking changes" can be additive:

| Change | Breaking? | Approach |
|---|---|---|
| Add optional field to response | No | Extend (additive) |
| Add optional request parameter | No | Extend |
| Add new endpoint | No | Extend |
| Remove a field | Yes | Version or deprecate-then-remove |
| Change field semantics (same name, new meaning) | Yes | Version ( Hyrum's Law: clients depend on old meaning) |
| Change type of existing field | Yes | Version |
| Change error format | Maybe | Extend (add new error code), don't change existing |

Version only when extension can't achieve the goal. A new version is expensive: clients must
migrate, two versions must coexist, the old must be sunset. Reserve it for genuinely incompatible
redesigns.

## 2. Versioning strategies

| Strategy | Example | Pro | Con |
|---|---|---|---|
| **URI versioning** | `/v2/users` | Obvious; cacheable; easy to route | URL changes; SEO/bookmark breakage |
| **Header versioning** | `Accept: application/vnd.api+json; version=2` | URL stays clean; content negotiation | Invisible (hard to debug); harder to test in browser |
| **Query parameter** | `/users?version=2` | Simple | Looks optional (clients skip it); caching issues |
| **Content negotiation** | `Accept: application/json` vs `application/json+v2` | Standards-based | Same invisibility as header |

**Default: URI versioning.** It's the most visible, the easiest to route (gateway/proxy can split
traffic), and the easiest for clients to adopt correctly. Header versioning is "cleaner" but causes
real debugging pain (which version is this request using? you can't tell from the URL).

## 3. Sunset and deprecation headers

Don't just announce deprecation in docs — signal it in the response so clients see it programmatically.

### Deprecation header (informal but widely used)
```
Deprecation: true
Deprecation: Sun, 30 Jun 2025 00:00:00 GMT
```
Tells the client: this endpoint/version is deprecated. Date form (RFC 8594) gives the sunset date.

### Sunset header (RFC 8594 — the standard)
```
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
```
Tells the client: this resource will be unavailable after this date. The standard mechanism; pair
with a `Link` header pointing to the replacement:

```
Sunset: Sat, 31 Dec 2025 23:59:59 GMT
Link: </v2/users>; rel="successor-version"
```

### Deprecation lifecycle
```
1. Announce (docs + Deprecation header) — clients see the warning in responses
2. Sunset date set (Sunset header) — clients know the deadline
3. Log which clients still use the old version (identify stragglers)
4. Contact stragglers directly (outreach, not just docs)
5. Return 410 Gone (or 404) after sunset — the old version is gone
```

The header-based approach means monitoring tools and client SDKs can detect deprecation
automatically, not just humans reading changelogs.

## 4. Dual-version coexistence

While both versions run, keep them in sync where possible:

- **Shared business logic** — v1 and v2 controllers call the same service layer; only the
  request/response shaping differs. Don't fork the entire backend per version.
- **Data store** — one store, both versions read/write it. v2 may add fields; v1 ignores them
  (additive). Don't run two databases.
- **Feature parity** — new features ship to both versions where possible. A feature only in v2
  gives clients a reason to migrate; a feature only in v1 is a maintenance trap.
- **Bug fixes** — fix in both. A security bug in v1 is still a security bug even if v1 is
  deprecated.

## 5. Sunset timeline

| Stage | Duration | Action |
|---|---|---|
| **Deprecation announcement** | Day 0 | Docs + Deprecation/Sunset headers; changelog; blog post |
| **Migration window** | 6-12 months (min 6) | Clients migrate at their pace; monitor adoption |
| **Final notice** | 30-60 days before sunset | Direct outreach to remaining stragglers |
| **Sunset** | Deadline | Return 410 Gone; remove code |

Rules:
- **Minimum 6 months** from deprecation to sunset — large clients can't migrate faster.
- **Monitor adoption** — if 40% of traffic is still on v1 at month 5, the sunset date is wrong;
  extend or your sunset is an outage for those clients.
- **Never sunset without a successor** — `Link: rel="successor-version"` must point somewhere real.
- **Sunset is a commitment** — announcing a sunset date and then not following through trains
  clients to ignore future deprecations.

## 6. Breaking-change communication

| Channel | Audience | What |
|---|---|---|
| Deprecation/Sunset headers | Automated tools + SDKs | Machine-readable signal in every response |
| Changelog | Developers who read it | What changed, migration guide |
| Blog post / email | All registered API users | Announcement + deadline |
| Direct outreach | Top consumers (by traffic) | Personal contact; they matter most |
| Status page | Everyone | Deprecation as a scheduled event |

The header is necessary but not sufficient — it only reaches clients making requests. Active
outreach reaches clients who haven't made a request in months but will be broken by sunset.

## 7. How this connects to the skill

The `api-design` skill teaches:
- **One-Version Rule** — one version, extended additively (avoid breaking changes)
- **Addition Over Modification** — add fields, don't change/remove (extend, don't break)

This reference teaches the case those rules can't solve: **when a breaking change is unavoidable**
(redesign, removed field, changed semantics). Then: pick a versioning strategy (§2), signal
deprecation (§3), run dual-version coexistence (§4), and sunset on a documented timeline (§5).
Load this when the question is "we need to ship v2," not "can we add a field."
