# CI/CD Templates

YAML templates referenced by the `ci-cd` skill. Copy and adapt for your stack.

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
# Deploy preview on PR (Vercel/Netlify/etc.)
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
