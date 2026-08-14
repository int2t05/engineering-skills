# Versioning, Tagging, and Changelog

Semantic versioning, release tags, and changelog format for anything with consumers
(another team, a published package, a deployed client). Load when cutting a release.

## Semantic versioning — `MAJOR.MINOR.PATCH`

- `MAJOR` — breaking change; consumers must change their code to upgrade.
- `MINOR` — new, backward-compatible functionality; safe to upgrade.
- `PATCH` — backward-compatible bug fix; safe to upgrade.

When unsure whether a change is breaking, assume it is (Hyrum's Law — a "patch" that
changes behavior consumers relied on is a major wearing a disguise).

## Tag the release

A release is an immutable point in history, not a moving branch. Derive the version
from the tag so artifact, tag, and changelog can never disagree:

```bash
git tag -a v1.4.0 -m "Release 1.4.0"
git push origin v1.4.0
```

## Keep a changelog written for humans

A changelog is not `git log` — it's the curated, consumer-facing answer to "what
changed and do I care?", grouped by `Added / Changed / Fixed / Deprecated / Removed /
Security`, newest on top, every entry phrased around user impact. Write the entry in
the same change that makes the change, while the impact is fresh — breaking changes
get a migration note and a deprecation window (see the `deprecation-migration` skill).

```markdown
## [1.4.0] - 2025-06-12
### Added
- Bulk task import via CSV
### Fixed
- Timezone drift in recurring task due dates
### Deprecated
- `GET /v1/tasks/all` — use the paginated `GET /v1/tasks` (removal in 2.0)
```
