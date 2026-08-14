# Changelog and Release Notes

Depth reference for the `shipping` skill. How to turn raw commit history into a
changelog users can read and release notes they can act on. The skill covers the launch
checklist and rollback plan; this covers the communication artifact that ships with the
release.

## Contents

- [1. Commit history is not a changelog](#1-commit-history-is-not-a-changelog)
- [2. keepachangelog format](#2-keepachangelog-format)
- [3. Commit to category mapping](#3-commit-to-category-mapping)
- [4. Writing user-language entries](#4-writing-user-language-entries)
- [5. Release notes vs changelog](#5-release-notes-vs-changelog)

## 1. Commit history is not a changelog

Commits are written for developers who know the codebase. Changelogs are written for
users who don't. The gap between them is the work this reference covers.

| Commit message | Changelog entry |
|---|---|
| `refactor: extract validation into middleware` | (internal — omit) |
| `feat: add /api/tasks/:id/comments endpoint` | Added: comments can now be attached to tasks via the API |
| `fix: handle null assignee in task serializer` | Fixed: tasks without an assignee no longer return a 500 |
| `chore: bump react to 18.3` | (internal — omit, unless it fixes a user-visible bug) |

### What to omit

- Internal refactors with no behavior change
- Dependency bumps (unless they fix a user-visible bug or break the API)
- Test additions
- CI / build changes
- Code style / formatting

If every commit appears in the changelog, the changelog is a git log — and users stop
reading it.

## 2. keepachangelog format

The de-facto standard. `CHANGELOG.md` with sections per version, categories within each.

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Task comments API (`POST /api/tasks/:id/comments`)

### Fixed
- Tasks without an assignee no longer return 500

## [1.2.0] - 2025-01-15

### Added
- Dark mode for the dashboard
- Bulk export of tasks to CSV

### Changed
- `GET /api/tasks` now returns `assignee` as an object instead of an ID

### Deprecated
- `GET /api/tasks?userId=` — use `?assigneeId=` instead (removed in 2.0)

### Removed
- `POST /api/tasks/legacy-create` (deprecated since 1.0)

### Security
- Patched XSS vulnerability in task description rendering (CVE-2025-XXXX)
```

### The six categories

| Category | When to use |
|---|---|
| **Added** | New feature, endpoint, or capability |
| **Changed** | Existing behavior modified (still compatible) |
| **Deprecated** | Feature will be removed in a future version |
| **Removed** | Feature removed in this version |
| **Fixed** | Bug fix |
| **Security** | Vulnerability fix, even if internal |

## 3. Commit to category mapping

Use Conventional Commits to automate categorization. The commit type maps to the
keepachangelog category:

| Commit type | Changelog category |
|---|---|
| `feat:` | Added |
| `fix:` | Fixed |
| `perf:` | Changed (or Fixed if it fixes a performance bug) |
| `BREAKING CHANGE:` footer | Removed / Changed (and bump major) |
| `deprecate:` | Deprecated |
| `security:` | Security |
| `refactor:` | Omit (internal) |
| `chore:` / `test:` / `docs:` | Omit (internal) |

### Automated generation

Tools like `conventional-changelog`, `standard-version`, or `release-please` read
conventional commits and generate the changelog section per release. The `[Unreleased]`
section accumulates entries as commits land; on release, it becomes the versioned section.

### The human gate

Automation gets you 80%. The remaining 20% — rewriting technical commits into
user-language, deciding what to omit, grouping related commits into one entry — is human
work. Review the generated changelog before publishing.

## 4. Writing user-language entries

| Technical (commit) | User-language (changelog) |
|---|---|
| `feat: implement OAuth2 flow with PKCE` | Added: sign in with GitHub and Google |
| `fix: null check in line 42 of serializer` | Fixed: exported CSV missing the status column for completed tasks |
| `perf: add index on orders.created_at` | Changed: order history loads 5× faster for accounts with 10,000+ orders |
| `BREAKING: rename userId to assigneeId` | Changed: the `userId` field in task responses is now `assigneeId` (see migration guide) |

### Rules

- Lead with the user outcome, not the implementation.
- Name the feature or surface the user sees, not the internal module.
- For breaking changes: state what changed, what breaks, and where the migration guide is.
- For security: state what was vulnerable, the severity, and whether action is needed.
- One entry per user-visible change, even if it spanned multiple commits.

## 5. Release notes vs changelog

| | Changelog | Release notes |
|---|---|---|
| **Audience** | Developers integrating the API / running the tool | End users reading the blog / GitHub release |
| **Format** | `CHANGELOG.md`, all versions, append-only | Per-release post or GitHub release body |
| **Detail** | Every user-visible change | Highlights plus breaking changes plus migration guide |
| **Tone** | Factual, terse | Contextual, explanatory |

The changelog is the complete record. Release notes are the highlight reel — pull the top
3–5 changes from the changelog, write a paragraph of context, and link to the full
changelog for the rest. Don't duplicate the full changelog in release notes.
