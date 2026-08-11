---
name: git-workflow
description: Use when committing, branching, resolving merge or rebase conflicts, or setting up git guardrails and pre-commit hooks — resolves conflicts by intent traced to each side's source, never --abort. Triggers on "commit", "merge conflict", "rebase", "pre-commit", "提交", "合并冲突", "分支管理".
---

# Git Workflow and Versioning

Git is your safety net: commits are save points, branches are sandboxes, history is documentation. With AI agents generating code at high speed, disciplined version control is what keeps changes manageable, reviewable, and reversible.

## When to use

- Committing, branching, or organizing work across parallel streams.
- Resolving an in-progress merge or rebase conflict.
- Cutting a release, choosing a semantic version bump, tagging, or writing a changelog.
- Setting up git guardrails (blocking dangerous commands) or pre-commit hooks.

**Not for:** a simple commit of finished work with no conflicts (just commit it); designing CI pipelines (use `ci-cd`); production deployment strategy (use `shipping`).

## Steps

### 1. Work trunk-based with short-lived branches

Keep `main` always deployable. Work in short-lived feature branches that merge back within 1–3 days. Long-lived branches are a hidden cost — they diverge, create merge conflicts, and delay integration. DORA research consistently links trunk-based development with high-performing teams.

```
main ──●──●──●──●──●──●──●──●──●──  (always deployable)
        ╲      ╱  ╲    ╱
         ●──●─╱    ●──╱    ← short-lived feature branches (1-3 days)
```

Branch naming: `feature/<desc>`, `fix/<desc>`, `chore/<desc>`, `refactor/<desc>`. Delete branches after merge. Prefer feature flags over long-lived branches for incomplete features.

For parallel AI-agent work, use git worktrees so each agent works in its own directory with its own branch — no branch switching, no interference:

```bash
git worktree add ../project-feature-a feature/task-creation
# ...later
git worktree remove ../project-feature-a
```

### 2. Commit early, atomic, descriptive

Each successful increment gets its own commit (implement slice → test → verify → commit). If the next change breaks something, you can revert to the last known-good state instantly.

**Atomic** — each commit does one logical thing:

```
# Good: self-contained
feat: add task creation endpoint with validation
feat: add task creation form component
test: add task creation tests (unit + integration)

# Bad: mixed
feat: add task feature, fix sidebar, update deps, refactor utils
```

**Descriptive** — messages explain the *why*, not just the *what*:

```
<type>: <short description>

<optional body explaining why, not what>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`.

Don't combine formatting changes with behavior changes, or refactors with features. Each is a separate commit (and ideally a separate PR). Target ~100 lines per commit/PR; changes over ~1000 lines should be split.

### 3. Pre-commit hygiene

Before every commit:

```bash
git diff --staged                                         # see what you're committing
git diff --staged | grep -iE 'password|secret|api_key|token'   # no secrets
npm test && npm run lint && npx tsc --noEmit              # gates pass
```

Automate with Husky + lint-staged. See [references/pre-commit-setup.md](references/pre-commit-setup.md) for the full setup (package-manager detection, hook script, Prettier config).

### 4. Resolve merge conflicts hunk-by-hunk, by intent

When a merge or rebase conflicts, never `--abort`. Resolve by tracing each side's intent back to its source.

1. **See the current state.** Inspect git history and the conflicting files.
2. **Find the primary source for each conflict.** Read the commit messages, the PRs, the original issues/tickets. Understand deeply *why* each change was made — what intent does it encode?
3. **Resolve each hunk.** Preserve both intents where possible. Where they're incompatible, pick the one matching the merge's stated goal and note the trade-off. Do **not** invent new behaviour.
4. **Run the project's automated checks** — typecheck, then tests, then format. Fix anything the merge broke.
5. **Finish the merge/rebase.** Stage everything and commit. If rebasing, continue until all commits are rebased.

### 5. Block dangerous git commands

Install a PreToolUse hook that intercepts and blocks destructive git commands before Claude executes them: `git push` (including `--force`), `git reset --hard`, `git clean -f[d]`, `git branch -D`, `git checkout .` / `git restore .`. The hook script is at [references/block-dangerous-git.sh](references/block-dangerous-git.sh) — copy it to `.claude/hooks/` (project) or `~/.claude/hooks/` (global), `chmod +x`, and register it in `settings.json` under `hooks.PreToolUse` with matcher `Bash`.

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse` array — don't overwrite other settings.

Verify with:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
# expect: exit code 2, BLOCKED message on stderr
```

### 6. Handle generated files correctly

- **Commit** generated files the project expects tracked (`package-lock.json`, Prisma migrations).
- **Don't commit** build output (`dist/`, `.next/`), env files (`.env`), or IDE config unless shared.
- Maintain a `.gitignore` covering `node_modules/`, `dist/`, `.env`, `.env.local`, `*.pem`.

### 7. Use git for debugging

```bash
git bisect start && git bisect bad HEAD && git bisect good <known-good>   # find the commit that broke it
git log --oneline -20                                                       # recent history
git diff HEAD~5..HEAD -- src/                                               # what changed in src
git blame src/services/task.ts                                              # who last touched a line
git log --grep="validation" --oneline                                       # commits matching a keyword
```

### 8. Version, tag, and changelog for anything with consumers

A version is how *consumers* track change. The moment anything else depends on your code — another team, a published package, a deployed client — "latest on main" stops being a sufficient answer.

**Semantic versioning** — `MAJOR.MINOR.PATCH`:
- `MAJOR` — breaking change; consumers must change their code to upgrade.
- `MINOR` — new, backward-compatible functionality; safe to upgrade.
- `PATCH` — backward-compatible bug fix; safe to upgrade.

When unsure whether a change is breaking, assume it is (Hyrum's Law — a "patch" that changes behavior consumers relied on is a major wearing a disguise).

**Tag the release; let the tag be the source of truth.** A release is an immutable point in history, not a moving branch. Derive the version from the tag so artifact, tag, and changelog can never disagree:

```bash
git tag -a v1.4.0 -m "Release 1.4.0"
git push origin v1.4.0
```

**Keep a changelog written for humans.** A changelog is not `git log` — it's the curated, consumer-facing answer to "what changed and do I care?", grouped by `Added / Changed / Fixed / Deprecated / Removed / Security`, newest on top, every entry phrased around user impact. Write the entry in the same change that makes the change, while the impact is fresh — breaking changes get a migration note and a deprecation window (see the `deprecation-migration` skill).

```markdown
## [1.4.0] - 2025-06-12
### Added
- Bulk task import via CSV
### Fixed
- Timezone drift in recurring task due dates
### Deprecated
- `GET /v1/tasks/all` — use the paginated `GET /v1/tasks` (removal in 2.0)
```

## Verify

For every commit:
- [ ] Commit does one logical thing
- [ ] Message explains the why; follows type conventions
- [ ] Tests pass before committing
- [ ] No secrets in the diff
- [ ] No formatting-only changes mixed with behavior changes
- [ ] `.gitignore` covers standard exclusions

For every merge/rebase conflict:
- [ ] Each hunk's intent traced to its source (commit/PR/issue)
- [ ] Both intents preserved where possible; trade-offs noted where not
- [ ] Typecheck, tests, and format all pass after resolution

For every release (anything with consumers):
- [ ] The version bump matches the change: breaking → major, additive → minor, fix → patch
- [ ] The release is tagged, and the version is derived from the tag
- [ ] The changelog has a curated, human-readable entry grouped by impact for this version

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope, simplicity)
- [references/block-dangerous-git.sh](references/block-dangerous-git.sh) — PreToolUse hook blocking `git push`, `reset --hard`, `clean -f`, `branch -D`, etc.
- [references/pre-commit-setup.md](references/pre-commit-setup.md) — Husky + lint-staged + Prettier pre-commit hook setup
