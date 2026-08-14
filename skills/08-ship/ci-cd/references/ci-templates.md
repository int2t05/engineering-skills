# CI/CD Templates

YAML templates referenced by the `ci-cd` skill. Copy and adapt for your stack.

## Contents

- [Basic CI (Node)](#basic-ci-node)
- [Integration tests with database services](#integration-tests-with-database-services)
- [Dependabot — automated dependency updates](#dependabot--automated-dependency-updates)
- [Caching and parallelism — split jobs](#caching-and-parallelism--split-jobs)
- [Per-stack CI — Python and Go](#per-stack-ci--python-and-go)
- [Preview deployment — deploy on every PR](#preview-deployment--deploy-on-every-pr)
- [Rollback — manual redeploy of a previous version](#rollback--manual-redeploy-of-a-previous-version)

## Basic CI (Node)

The minimal quality pipeline — one job, sequential gates. The starting point before
splitting into parallel jobs.

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

## Integration tests with database services

Use the `services:` block and GitHub Secrets for credentials (never hardcode, even in CI):

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
        run: npx prisma migrate deploy   # Node/Prisma — swap for alembic (Python), goose/sqlx (Go), Flyway/Liquibase (Java)
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
      - name: Integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://ci_user:${{ secrets.CI_DB_PASSWORD }}@localhost:5432/testdb
```

## Dependabot — automated dependency updates

`package-ecosystem` can be `npm`, `pip`, `gomod`, `cargo`, `maven`, or `gradle` — add one entry per ecosystem your repo uses.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    open-pull-requests-limit: 5
```

## Caching and parallelism — split jobs

Each gate runs as its own job with the dependency cache enabled, so they run in
parallel and don't re-install dependencies. Node example:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npx tsc --noEmit

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm test -- --coverage
```

## Per-stack CI — Python and Go

The same gate structure adapted to other stacks. Swap the setup action, install step,
and commands to match the manifest detected in the `ci-cd` skill.

Python (`pyproject.toml` → ruff / mypy / pytest / pip-audit):

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy src
      - run: pytest --cov
      - run: pip-audit
```

Go (`go.mod` → golangci-lint / go test / govulncheck):

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.23'
          cache: true
      - run: golangci-lint run
      - run: go test ./... -race -coverprofile=coverage.out
      - run: govulncheck ./...
      - run: go build ./...
```

## Preview deployment — deploy on every PR

```yaml
# Deploy preview on PR. Example uses Vercel; for other platforms swap the deploy
# command (Cloud Run: gcloud run deploy; Netlify: npx netlify deploy; Docker:
# build+push image tag) — the workflow_dispatch + PR-gated shape is portable.
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - uses: actions/checkout@v4
    - name: Deploy preview
      run: npx vercel --token=${{ secrets.VERCEL_TOKEN }}
```

## Rollback — manual redeploy of a previous version

```yaml
# Manual rollback workflow
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Rollback deployment
        run: |
          # Deploy the specified previous version
          npx vercel rollback ${{ inputs.version }}
```
