---
name: documentation-audit
description: Use when documentation drifts from code — syncs PRD/TECH/API/FLOW/TODO to the codebase and produces an audit report. Triggers on "docs out of date", "documentation drift", "sync docs", "文档同步", "写文档", "写 README", "文档化这个功能", "文档审计".
---

# Documentation Audit

Sync the five formal docs (PRD/TECH/API/FLOW/TODO) to the code, then produce an audit report. Documentation must reflect reality — this skill brings drifted docs back into alignment and records what changed.

## When to use

- A formal doc (PRD/TECH/API/FLOW/TODO) contradicts the current code
- Documentation is stale or out of sync after a feature ship
- Manual request to synchronize all documentation with the codebase
- Writing new documentation from scratch (see `references/writing-docs.md`)

**Not for:** open source GitHub presence polishing (use `oss-polish`); designing API contracts (use `api-design`); writing the PRD/TECH themselves (use `spec`/`architecture`).

## Steps

### 1. Discovery — locate the five formal docs and code structure

Find every formal doc and map the codebase layout so later steps know where to look.

```bash
# Locate the five formal docs (project-level)
ls docs/PRD.md docs/TECH.md docs/TODO.md docs/API/*.md docs/FLOW/*.md 2>/dev/null
# Version-level variants (if multi-version project)
ls docs/v*/*.md 2>/dev/null
# Detect API framework for the API drift step
grep -Ei "express|fastify|@nestjs|fastapi|flask|django|gin|echo" package.json requirements.txt go.mod 2>/dev/null
```

Record which docs exist and which are missing. Missing docs are gaps to flag — not to create here (creation belongs to `spec`/`architecture`/`api-design`).

### 2. PRD & TECH drift — implementation vs spec

Read the code's actual behavior and compare against PRD/TECH:

- **Features in code but not in PRD** — shipped without spec; flag for `spec`.
- **Features in PRD but not in code** — spec aspirational or feature removed; update PRD to match reality.
- **Components in TECH but not in code** — planned but not implemented; update TECH.
- **Components in code but not in TECH** — undocumented; add to TECH.

### 3. API drift — endpoints vs docs/API/*.md

Extract every route declaration from code and match against `docs/API/`:

- **express:** `grep -rh "\(app\|router\)\.\(get\|post\|put\|delete\|patch\|all\)" --include="*.ts" --include="*.js"`
- **fastify:** `grep -rh "\(app\|fastify\)\.\(get\|post\|put\|delete\|patch\|all\)" --include="*.ts" --include="*.js"`
- **nestjs:** `grep -rh "@\(Get\|Post\|Put\|Delete\|Patch\|All\)" --include="*.ts"`
- **fastapi / flask:** `grep -rh "@app\.\(get\|post\|put\|delete\|patch\)" --include="*.py"`

Express routers register on `router.get` (not just `app.get`); Fastify often names the instance
`fastify` rather than `app`; NestJS `@All` is a catch-all route — the patterns above cover these.
For chains like `app.route('/x').get(handler)`, the `.get` match still catches it.

Every endpoint in code with no matching `docs/API/` entry is a drift gap. For each gap, add to the API doc: method, path, parameters, request/response shape, errors. If no `docs/API/` exists yet, flag for `api-design`.

### 4. FLOW drift — data flow vs docs/FLOW/*.md

For each business flow, trace the code path and compare against `docs/FLOW/`:

- Function call chains in code but not in the FLOW doc — add them.
- FLOW doc references functions that no longer exist — update or remove.
- New flows with no FLOW doc — flag for creation (use the workflow-prompts FLOW prompt).

### 5. TODO drift — code TODOs vs docs/TODO.md

```bash
grep -rn "TODO" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" src/ | grep -v node_modules
```

- TODOs in code but not in `docs/TODO.md` — add them (merged by business area).
- TODOs in `docs/TODO.md` already resolved in code — remove from TODO.md and delete the code TODO comment.

### 6. Sync — fix every drift

For each gap found in steps 2–5, update the doc to match the code (or flag for the owning skill if creation is needed). Docs reflect reality; reality is not edited to match docs.

### 7. Produce the audit report

Write `docs/audit/YYYY-MM-DD-documentation.md` using the template in `references/templates.md`:

- **Scope** — which docs were audited
- **Before/after** — drift counts per doc type
- **Fixed** — every sync applied
- **Needs manual review** — items requiring a human decision or another skill

**Output:** `docs/audit/YYYY-MM-DD-documentation.md` — audit report (scope, before/after, fixed, needs review). The synced docs are the primary product; the report is the trail.

## Verify

- [ ] All five formal docs discovered; missing ones flagged
- [ ] Every endpoint in code has a `docs/API/` entry (or flagged for `api-design`)
- [ ] `docs/TODO.md` matches code TODO comments (both directions)
- [ ] PRD/TECH reflect current implementation
- [ ] Audit report produced at `docs/audit/YYYY-MM-DD-documentation.md` with before/after + needs-review

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope)
- [references/templates.md](references/templates.md) — audit-report template
- [references/writing-docs.md](references/writing-docs.md) — writing new documentation from scratch (README, feature docs, API docs)
