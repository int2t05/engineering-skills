---
name: documentation-audit
description: Use when documentation drift is detected. Comprehensively audits the codebase and syncs Swagger, feature docs, and general documentation to match the code.
---

# Documentation Audit

Comprehensive documentation sync when drift is detected. Analyzes the codebase and creates or updates all documentation artifacts to achieve full synchronization. Documentation must reflect reality — this skill brings it into alignment.

## When to use

- API documentation drift detected (endpoints in code missing from OpenAPI/Swagger).
- Features documentation drift detected (shipped features missing from features docs).
- Documentation files are missing, stale, or contradict the current code.
- Manual request to synchronize all documentation with the codebase.

## Steps

### 1. Discovery — find all documentation and code artifacts

Locate every documentation file and identify the API framework so later phases know where to look.

```bash
# Find documentation files
find . \( -name "*.md" -o -name "*.yaml" -o -name "*.json" \) \
  | grep -Ei "(doc|api|swagger|openapi|feature|guide|readme)" \
  | grep -v node_modules | grep -v .git

# Locate API spec and features doc
find . \( -name "openapi.yaml" -o -name "swagger.yaml" -o -name "openapi.json" \) | head -1
find . \( -name "features.md" -o -name "FEATURES.md" \) | head -1
```

Detect the API framework by grepping `package.json` / `requirements.txt` / `go.mod` for `express`, `fastify`, `@nestjs`, `fastapi`, `flask`, or a Go module. The framework determines the endpoint extraction pattern.

### 2. API audit — extract endpoints from code

Pull every route declaration from the codebase so they can be matched against the OpenAPI spec.

- **express / fastify:** `grep -rh "app\.\(get\|post\|put\|delete\|patch\)" --include="*.ts" --include="*.js"`
- **nestjs:** `grep -rh "@\(Get\|Post\|Put\|Delete\|Patch\)" --include="*.ts"`
- **fastapi / flask:** `grep -rh "@app\.\(get\|post\|put\|delete\|patch\)" --include="*.py"`

Compare extracted endpoints against `openapi.yaml` paths. Every endpoint in code with no matching path entry is a drift gap to fix.

### 3. Features audit — extract user-facing features

Discover features shipped in the UI so they can be documented.

- React components in `pages/` or `views/` (`find . -path "*/pages/*" -name "*.tsx" -o -path "*/views/*" -name "*.tsx"`).
- Feature flags (`grep -rh "featureFlag\|feature:" --include="*.ts" --include="*.tsx"`).
- User-facing config options (`grep -rh "config\.\|settings\." --include="*.ts"`, excluding imports).

Compare discovered features against `features.md`. Every shipped feature with no entry is a drift gap.

### 4. Generate missing documentation

For each gap found in phases 2–3, create or extend the relevant artifact. Templates for a new OpenAPI file (skeleton with `info`, `servers`, `paths`, `components.schemas`, `securitySchemes`) and a new features doc (overview, core features with description/how-to-use, additional features) are in `references/templates.md`. Use them as starting scaffolds, then fill in real content from the code.

### 5. Update existing documentation

For each discovered but undocumented item, add it to the existing doc:

1. **API endpoints** — add to OpenAPI spec: path and method, parameters (from function signature), request body schema (from DTO/type), response schema (from return type), basic description.
2. **Features** — add to features doc: feature name, basic description, placeholder for how-to-use, note to review and enhance.

### 6. Validation

Validate every artifact the audit touched before reporting done.

```bash
# Validate OpenAPI is parseable YAML/JSON
yq '.' openapi.yaml > /dev/null 2>&1 && echo "OpenAPI: Valid YAML" || echo "OpenAPI: Invalid YAML"

# Check markdown docs have section headers
for file in docs/*.md; do [ -f "$file" ] && grep -q "^## " "$file" || echo "WARNING: $file missing section headers"; done

# Completeness: endpoints documented vs endpoints in code
ENDPOINTS_DOCUMENTED=$(yq '.paths | keys | length' openapi.yaml 2>/dev/null || echo 0)
ENDPOINTS_IN_CODE=$(extract_endpoints | wc -l)
```

If `ENDPOINTS_DOCUMENTED < ENDPOINTS_IN_CODE`, some endpoints are still undocumented — loop back to phase 5.

## Verify

- [ ] All documentation files discovered (markdown, YAML, JSON)
- [ ] API framework detected; every endpoint extracted from code
- [ ] Every user-facing feature extracted from code
- [ ] Missing documentation files created (OpenAPI spec, features doc)
- [ ] Existing documentation updated to cover every endpoint and feature
- [ ] All files validated: OpenAPI parses as YAML/JSON, markdown has section headers
- [ ] Endpoint count in code equals endpoint count documented
- [ ] Audit report produced (before/after counts, files created/updated, items needing manual review)

**Quality standards:** every endpoint/feature listed (completeness); YAML/JSON validates (validity); required sections present (structure); clear placeholders for manual review; generated-by-skill attribution noted so reviewers know to enhance descriptions.

## References

- [../../references/engineering-principles.md](../../references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope, goal-driven execution)
- [references/templates.md](references/templates.md) — OpenAPI skeleton, features-doc template, audit-report template
