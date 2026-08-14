---
name: ci-cd
description: Use when working on CI/CD pipelines and automation — build, test, and deploy automation, pipeline design, and deployment strategies. Triggers on "CI pipeline", "GitHub Actions", "deployment strategy", "CI/CD", "流水线", "持续集成", "部署策略".
---

# CI/CD and Automation

Automate quality gates so no change reaches production without passing tests, lint, type checking, and build. CI/CD is the enforcement mechanism for every other skill — it catches what humans and agents miss, and it does so consistently on every change.

**Shift left:** catch problems as early in the pipeline as possible. A bug caught in linting costs minutes; the same bug caught in production costs hours. **Faster is safer:** smaller batches and more frequent releases reduce risk, not increase it. A deployment with 3 changes is easier to debug than one with 30.

## When to use

- Setting up a new project's CI pipeline.
- Adding or modifying automated checks (lint, types, tests, build, audit).
- Configuring deployment pipelines or deployment strategies.
- Debugging CI failures.
- When a change should trigger automated verification.

**Not for:** debugging runtime bugs (use `debugging`); production launch strategy and rollback (use `shipping`); routine commits (use `git-workflow`).

## Steps

### 1. Define the quality gate pipeline

Every change goes through these gates before merge — no gate can be skipped. If lint fails, fix lint (don't disable the rule). If a test fails, fix the code (don't skip the test).

```
Pull Request
  │
  ▼
LINT          → code style + static analysis
TYPE CHECK    → type safety (typed languages only)
UNIT TESTS    → behavior
BUILD         → artifact compiles / bundles
INTEGRATION   → API/DB tests against real deps
E2E (opt.)    → full user journeys in a browser/app
SECURITY      → dependency + secret scan
  │
  ▼
Ready for review
```

Detect the stack from its manifest, then map each gate to the right command — never assume `npm test`:

| Stack | Manifest | Lint | Test | Build |
|---|---|---|---|---|
| Node / TS | `package.json` | eslint / prettier | npm test (jest/vitest) | npm run build |
| Python | `pyproject.toml` | ruff / mypy | pytest | pip build / uv build |
| Go | `go.mod` | go vet / golangci-lint | go test ./... | go build |
| Rust | `Cargo.toml` | clippy | cargo test | cargo build --release |
| Java | `pom.xml` / `build.gradle` | spotbugs / checkstyle | mvn test / gradle test | mvn package / gradle build |

### 2. Configure the CI pipeline (GitHub Actions)

Example: Node.js. For other stacks, swap `setup-node` for the matching setup action (`setup-python`, `setup-go`, `rust-toolchain`, `setup-java`) and the commands from the table above. Basic CI (lint → typecheck → test → build → audit) and database-integration CI (Postgres `services:` block, secrets, migrations) are in [references/ci-templates.md](references/ci-templates.md) — copy and adapt.

E2E (Playwright, or your framework's equivalent) — same shape: install browser deps, build, run the E2E suite. Upload the report directory as an artifact `if: failure()` so the run isn't a black box.

### 3. Feed CI failures back to the agent

The power of CI with AI agents is the feedback loop. When CI fails, copy the failure output and feed it to the agent:

```
"The CI pipeline failed with this error:
[paste specific error]
Fix the issue and verify locally before pushing again."
```

- Lint failure → run your linter's auto-fix (`npm run lint --fix`, `ruff check --fix`, `golangci-lint run --fix`) and commit
- Type error → read the error location and fix the type
- Test failure → follow the debugging skill
- Build error → check config and dependencies

### 4. Choose a deployment strategy

**Preview deployments** — every PR gets a preview for manual testing (Vercel/Netlify/etc.).

**Feature flags** — decouple deployment from release. Ship code without enabling it; roll back without redeploying (disable the flag); canary (1% → 10% → 100%); A/B test. Flag lifecycle: create → enable for testing → canary → full rollout → **remove the flag and dead code**. Flags that live forever become technical debt — set a cleanup date when you create them. (See the `shipping` skill for the full flag rollout sequence and thresholds.)

**Staged rollouts** — PR merged to main → staging deployment (auto) → manual verification → production deployment → monitor 15-min window → roll back on errors or done.

**Rollback plan** — every deployment must be reversible. Provide a manual rollback workflow (`workflow_dispatch` with a version input) that redeploys the specified previous version. YAML templates for preview deployments and rollback are in `references/ci-templates.md`.

### 5. Manage environments and secrets

```
.env.example       → committed (template for developers)
.env               → NOT committed (local development)
.env.test          → committed (test environment, no real secrets)
CI secrets         → stored in GitHub Secrets / vault
Production secrets → stored in deployment platform / vault
```

CI should never have production secrets. Use separate secrets for CI testing.

### 6. Automate beyond CI

- **Dependabot / Renovate** for automated dependency updates (weekly, limited open PRs; template in `references/ci-templates.md`).
- **Build Cop** — designate someone responsible for keeping CI green. When the build breaks, the Build Cop fixes or reverts, not the person whose change caused the break.
- **PR checks** — required reviews (≥1 approval), required status checks (CI must pass), branch protection (no force-pushes to main), auto-merge (when all checks pass and approved).

### 7. Optimize when the pipeline exceeds 10 minutes

Apply in order of impact: cache dependencies (`setup-node` cache, `setup-python` cache, `actions/cache` for `~/.cargo` / `~/go/pkg`) → run jobs in parallel (split lint/typecheck/test/build into separate jobs; template in `references/ci-templates.md`) → only run what changed (path filters; skip e2e for docs-only PRs) → matrix builds (shard test suites) → optimize the test suite (move slow tests to a schedule) → use larger runners.

## Verify

After setting up or modifying CI:

- [ ] All quality gates are present (lint, types, tests, build, audit)
- [ ] Pipeline runs on every PR and push to main
- [ ] Failures block merge (branch protection configured)
- [ ] CI results feed back into the development loop
- [ ] Secrets are stored in the secrets manager, not in code
- [ ] Deployment has a rollback mechanism
- [ ] Pipeline runs in under 10 minutes for the test suite

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope, simplicity)
- [references/ci-templates.md](references/ci-templates.md) — Dependabot config, caching/parallelism split jobs, preview deployment, rollback workflow_dispatch
