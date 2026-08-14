# OpenAPI Lifecycle

Depth reference for the `api-design` skill. The spec-as-artifact lifecycle: design-first
vs code-first authoring, automated linting, SDK generation, and version management. The
skill covers the contract design (REST patterns, error models, naming); this covers the
toolchain that keeps the spec honest and consumable. Breaking-change deprecation and
sunset timelines are in `references/versioning-strategy.md`; this covers the spec-level
lifecycle tooling.

## Contents

- [1. Design-first vs code-first](#1-design-first-vs-code-first)
- [2. Spectral and Redocly linting](#2-spectral-and-redocly-linting)
- [3. SDK generation with openapi-generator](#3-sdk-generation-with-openapi-generator)
- [4. Versioning the spec](#4-versioning-the-spec)
- [5. CI integration](#5-ci-integration)

## 1. Design-first vs code-first

| | Design-first | Code-first |
|---|---|---|
| **Flow** | Write OpenAPI spec → generate server stubs → implement handlers | Write handlers → extract spec from annotations |
| **Spec authority** | The spec is the source of truth | The code is the source of truth; spec is derived |
| **Best for** | Multi-team contracts, public APIs, SDK consumers | Internal services, rapid prototyping |
| **Risk** | Spec drifts from implementation if not gated | Annotations are verbose; spec may be incomplete |

### Design-first (recommended for public APIs)

The spec is the contract. Clients and servers are generated from it. Review the spec in
PRs, not the implementation — the spec is what consumers see.

```
spec.yaml → openapi-generator → server stubs + client SDKs
          → implement handlers in the stubs
          → lint spec in CI (no drift)
```

### Code-first (acceptable for internal services)

Annotations on handlers generate the spec. Faster to start, but the spec is a byproduct
— it's only as complete as the annotations. Run a linter to catch missing fields,
examples, and error responses that annotations skipped.

### The drift test

Regardless of approach, add a CI check: the committed spec must match what the running
server exposes. For design-first, generate stubs and verify the server matches them. For
code-first, regenerate the spec and diff against the committed one. Drift = a failing build.

## 2. Spectral and Redocly linting

A spec without linting accretes inconsistencies: some endpoints document errors, others
don't; some use camelCase, others snake_case. A linter enforces conventions
automatically.

### Spectral (Stoplight / open-source)

```yaml
# .spectral.yaml — custom ruleset
extends: ["spectral:oas", "spectral:oas:api-design"]
rules:
  oas3-api-servers: off
  operation-operationId: error        # every operation needs an ID (SDK generation)
  operation-tags: error                # every operation needs a tag
  no-$ref-siblings: error              # don't mix $ref and sibling keys
  info-contact: error                  # API must have a contact
```

### Redocly (commercial, free tier available)

```yaml
# redocly.yaml
apis:
  main:
    root: openapi.yaml
rules:
  operation-4xx-response: warn         # every operation should document 4xx errors
  security-defined: error              # endpoints must declare security or opt out
  tag-description: warn
```

### Rules worth enforcing

| Rule | Why |
|---|---|
| `operationId` on every operation | SDK generation needs it; clients reference operations by ID |
| `4xx` and `5xx` responses documented | Consumers need to handle errors; missing = guessing |
| Consistent naming (camelCase or snake_case) | Pick one; enforce via rule |
| `example` on every response | Examples are the fastest documentation |
| No inline schemas (use `$ref` to components) | Reusable, DRY, consistent |
| `tags` with descriptions | Groups operations in generated docs |

## 3. SDK generation with openapi-generator

The spec isn't just documentation — it's the input for generating client SDKs in any
language. One spec, TypeScript / Python / Go / Java / Rust clients.

### Workflow

```
openapi.yaml
  → openapi-generator generate -i openapi.yaml -g typescript-fetch -o clients/ts
  → openapi-generator generate -i openapi.yaml -g python -o clients/py
  → openapi-generator generate -i openapi.yaml -g go -o clients/go
```

### Generator selection

| Generator | Use when |
|---|---|
| `typescript-fetch` | Browser / Node clients (fetch-based) |
| `typescript-axios` | Projects already using axios |
| `python` | Python SDK (requests-based) |
| `go` | Go module client |
| `java` | Java / Android / Spring |

### Configuration

```yaml
# openapi-generator-config.yaml
generatorName: typescript-fetch
additionalProperties:
  supportsES6: true
  typescriptThreePlus: true
  useSingleRequestParameter: false
```

### Gating in CI

1. Generate SDKs from the committed spec.
2. Diff against the committed SDKs — if the spec changed but SDKs weren't regenerated,
   fail the build.
3. Publish SDKs on spec release (tagged version → published package).

## 4. Versioning the spec

The OpenAPI `info.version` field is the spec version, separate from the API URL version
(`/v1`, `/v2`). They track different things:

| Version | What it tracks | When it changes |
|---|---|---|
| `info.version` (spec) | The spec document's revision | Any spec edit (additive or breaking) |
| URL version (`/v1`) | The API contract version | Breaking change requiring client migration |

### Semver for spec versions

- **Patch** (1.0.1): docs, examples, description fixes — no behavior change.
- **Minor** (1.1.0): additive (new endpoint, new optional field, new error code) — backward compatible.
- **Major** (2.0.0): breaking change (removed field, changed type, changed semantics).

### Breaking-change detection

Run `oasdiff` (or `openapi-diff`) in CI to detect breaking changes between the committed
spec and the PR's modified spec. A breaking change detected by diff means either:
- Bump the major version (and follow the sunset process in `references/versioning-strategy.md`), or
- Redesign the change to be additive (preferred — see the skill's Addition Over Modification principle).

## 5. CI integration

The full pipeline:

```
PR opened:
  1. Lint spec (Spectral / Redocly) → fail on errors
  2. Breaking-change diff (oasdiff) → fail on undocumented breaking changes
  3. Generate SDKs → diff against committed SDKs → fail if stale
  4. Render docs (Redoc / Swagger UI) → preview in PR

Merge to main:
  5. Publish rendered docs to docs site
  6. Tag spec version (semver)
  7. Publish SDKs to package registries (on minor/major)
```

This makes the spec a living artifact: linted, diffed, generated, and published — not a
file that drifts until someone notices.
