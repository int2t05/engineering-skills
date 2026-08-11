# Dependency Upgrade

Sub-guide for the `deprecation-migration` skill. Use when upgrading a
dependency or framework version — the common case where "migration" is a
version bump, not a system replacement.

## When to use this sub-guide

- "Upgrade React to v19."
- "Update this library to the latest."
- "Bump a major version of a dependency."
- Patch/minor upgrades that carry a known breaking change.

## When NOT to use

- Patching a security vulnerability in place → `security-review`.
- A routine bump with no breaking changes and a green test suite → just
  `implement` the bump directly (this guide is overkill).
- Replacing one library with a different one → main `deprecation-migration`
  flow (strangler/adapter patterns).

## Steps

1. **Read the changelog and migration guide.** The upstream release notes
   tell you what breaks. Don't upgrade blind — find the "Breaking Changes"
   section and list every item that touches your usage.
2. **Check your usage of the dependency.** `grep` for imports and the
   specific APIs the changelog flags. You only need to act on breaking
   changes that affect code you actually call.
3. **Decide upgrade scope.**
   - **Patch/minor, no breaking change to your usage** → bump version, run
     tests, done.
   - **Major with breaking changes** → go incremental when possible (some
     libraries support upgrading through intermediate majors).
4. **Upgrade on a branch.** Bump the version in the manifest/lockfile,
   reinstall, run typecheck + full test suite. Expect failures exactly where
   the changelog flagged them.
5. **Fix each break at its root.** Don't suppress type errors or disable
   lint to force the upgrade through — each break is a real API change; adapt
   the call site to the new contract.
6. **Verify behavior, not just types.** Tests passing is necessary but not
   sufficient for runtime-behavior changes (e.g. a framework's rendering
   timing). Run the app and exercise the affected paths.
7. **Commit the upgrade alone.** One commit for the version bump + its
   required call-site fixes. Mixing a dependency upgrade with unrelated
   changes makes a rollback impossible if something breaks in production.

## Risk patterns

- **Peer dependency cascades** — upgrading A forces B and C to upgrade too.
  Resolve the full set in one pass, not piecemeal.
- **Transitive breakage** — a sub-dependency changes behavior silently. If
  tests fail in code you didn't touch, suspect a transitive change.
- **Lockfile drift** — regenerate the lockfile cleanly; a partially-updated
  lockfile is a common source of "works on my machine" failures.

## When to escalate

- The upgrade's breaking changes amount to a redesign of how you use the
  library → main `deprecation-migration` flow (adapter pattern).
- The upgrade surfaces a security issue in the old version → `security-review`.
- The upgrade fails and the cause is a bug, not a documented breaking change
  → `debugging`.

## Verify

- The manifest/lockfile reflects the target version.
- Typecheck passes with no suppressed errors.
- Full test suite passes.
- The app runs and the affected paths are exercised manually.
- The upgrade is its own commit, separable from unrelated changes.
