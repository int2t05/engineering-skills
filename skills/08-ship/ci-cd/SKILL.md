---
name: ci-cd
description: Use when working on CI/CD pipelines and automation — build, test, and deploy automation, pipeline design, and deployment strategies.
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

## Steps

### 1. Define the quality gate pipeline

Every change goes through these gates before merge — no gate can be skipped. If lint fails, fix lint (don't disable the rule). If a test fails, fix the code (don't skip the test).

```
Pull Request
  │
  ▼
LINT          eslint, prettier
TYPE CHECK    tsc --noEmit
UNIT TESTS    jest/vitest
BUILD         npm run build
INTEGRATION   API/DB tests
E2E (opt.)    Playwright/Cypress
SECURITY      npm audit
BUNDLE SIZE   bundlesize
  │
  ▼
Ready for review
```

### 2. Configure the CI pipeline (GitHub Actions)

Basic CI:

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm test -- --coverage
      - run: npm run build
      - run: npm audit --audit-level=high
```

With database integration tests — use the `services:` block and GitHub Secrets for credentials (never hardcode, even in CI):

```yaml
  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        ports: [5432:5432]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - name: Run migrations
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - name: Integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

E2E (Playwright) — same shape: install (`npx playwright install --with-deps chromium`), build, `npx playwright test`. Upload `playwright-report/` as an artifact `if: failure()` so the run isn't a black box.

### 3. Feed CI failures back to the agent

The power of CI with AI agents is the feedback loop. When CI fails, copy the failure output and feed it to the agent:

```
"The CI pipeline failed with this error:
[paste specific error]
Fix the issue and verify locally before pushing again."
```

- Lint failure → `npm run lint --fix` and commit
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

Apply in order of impact: cache dependencies (`setup-node` cache option) → run jobs in parallel (split lint/typecheck/test/build into separate jobs; template in `references/ci-templates.md`) → only run what changed (path filters; skip e2e for docs-only PRs) → matrix builds (shard test suites) → optimize the test suite (move slow tests to a schedule) → use larger runners.

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
