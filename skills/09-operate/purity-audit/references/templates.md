# Purity Audit Templates

Starting scaffold for the `purity-audit` skill's audit report.

## Audit report template

`docs/audit/YYYY-MM-DD-purity.md` — one file per audit.

```markdown
# Purity Audit — [Target Name]

**Audit Date:** YYYY-MM-DD
**Scope:** [file / skill folder / doc set / whole pack]
**Target files:** [N] files across [paths]

## Checklist Coverage

| Category | Theme | Points | Findings |
|---|---|---|---|
| A | 溯源残留 (tracing residue) | A1–A3 | [N] |
| B | 装饰与冗余 (decoration + redundancy) | B4–B7 | [N] |
| C | 死内容 (dead content) | C8–C10 | [N] |
| D | doc/impl 裂隙 (gap) | D11–D14 | [N] |
| E | 语言与平台残留 (language + platform) | E15–E16 | [N] |

## Before / After

| Point | File:Line | Evidence (before) | Fix (after) | Status |
|---|---|---|---|---|
| A2 | <file>:NN | "自 v2.8 起…" | stated current fact; version pointer dropped | FIXED |
| C9 | <file>:NN | dead link `](x.md)` | link removed / retargeted | FIXED |
| D11 | <file>:NN | Verify check with no Step action | action added / check dropped | NEEDS REVIEW |

## Fixed

- [point-id] [file:line] [what was removed / recomposed / synced]

## Needs Manual Review

- [ ] [point-id] [file:line] [item requiring a human decision or another skill]
```
