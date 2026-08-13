# Documentation Audit Templates

Starting scaffold for the `documentation-audit` skill's audit report.

## Audit report template

`docs/audit/YYYY-MM-DD-documentation.md` — one file per audit.

```markdown
# Documentation Audit — [Project Name]

**Audit Date:** YYYY-MM-DD
**Scope:** PRD / TECH / API / FLOW / TODO

## Before / After

| Doc | Before | After | Status |
|-----|--------|-------|--------|
| PRD | [N] drifts | [N] fixed | [COMPLETE/PARTIAL] |
| TECH | [N] drifts | [N] fixed | [COMPLETE/PARTIAL] |
| API | [N] endpoints undocumented | [N] documented | [COMPLETE/PARTIAL] |
| FLOW | [N] flows stale | [N] updated | [COMPLETE/PARTIAL] |
| TODO | [N] mismatches | [N] synced | [COMPLETE/PARTIAL] |

## Fixed

- [doc] [what was synced to match code]

## Needs Manual Review

- [ ] [item requiring a human decision or another skill]
```
