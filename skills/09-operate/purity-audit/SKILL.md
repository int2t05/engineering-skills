---
name: purity-audit
description: Use when auditing whether code or docs read as first-written — flags tracing residue, decorative structure, dead content, doc/impl gaps, and language/platform residue against the 16-point purity checklist; produces an audit report. Triggers on "purity audit", "纯净审计", "残留审计", "洁净化" — also when user says "这些文件像改了好几遍" / "清掉历史残留". Not for syncing formal docs to code behavior (use documentation-audit) or reviewing a diff for bugs (use code-review).
---

# Purity Audit

Audit whether code or docs read as first-written — no tracing residue, no decoration, no dead
content, no doc/impl gap, no language/platform residue. Drives the 16-point purity-checklist
against a target and produces an audit report. The purity principle's "No residual artifacts" rule
made operational and reusable.

## When to use

- A file, skill, doc set, or the whole pack reads like it's been edited many times — version tags in prose, "previously X now Y", dead links, decorative diagrams, "保留 / 已观测" labels.
- Pre-ship cleanliness gate before a release or a doc refresh.
- Enforcing "No residual artifacts" on a concrete target.

**Not for:** syncing formal docs to code behavior / endpoints / TODOs (use `documentation-audit` — that's factual drift, this is cleanliness); bug-hunting a diff (use `code-review`); reducing code complexity (use `simplify`); machine-detectable lint (use `linting`); structural refactor (use `refactoring`). Dead-content removal *is* in scope; restructuring code is not.

## Steps

### 1. Scope the target + load the checklist

Pick the target: a single file, a skill folder, a doc set, or the whole pack. Load
[${CLAUDE_PLUGIN_ROOT}/references/purity-checklist.md](${CLAUDE_PLUGIN_ROOT}/references/purity-checklist.md) — the 16-point A–E grid is the audit criteria.

### 2. Grep-driven sweep — categories A / B / C

These yield to batch grep. Run the checklist's "怎么查" commands:

- **A (tracing residue)** — `（.*新` / `（.*保留` / `（.*事件` / `（.*已观测`; `v[0-9]\.[0-9]` in prose (not frontmatter / badges / dep declarations); "之前 / 原来 / 改为 / 迁移到 / 升级后" phrasing.
- **B (decoration + redundancy)** — duplicated assertions (same claim grep ≥2 hits → should link, not copy); `**除非**` / `**注意**` / `**例外**` / `// 特殊` / `// HACK` special-case guards.
- **C (dead content)** — dead links (`](x.md)` → nonexistent file); dead frontmatter / params (field name grep'd nowhere = unconsumed); "统一 / 一律 / 必须 / 全部" directives the body doesn't actually satisfy.

### 3. Human-judgment sweep — categories D / E

These need item-by-item comparison, not grep:

- **D (doc/impl gap)** — verify-item ↔ action correspondence (each Verify check has a Step action, and vice versa); Output declaration ↔ `docs/skill-outputs.md` matrix sync; shared-structure drift across instances (multi-mode spines, shared contracts); numbering continuity (no 1,2,3,5).
- **E (language + platform residue)** — language mixing in prose (identifiers in original are fine; narrative sentences must stay one language); platform / tool implementation traces (an MCP command name, a framework private API, a CI step id) leaking into generic rules.

### 4. Scale up with subagents (large target)

When the target is a whole pack or >~20 files, dispatch per-category auditor subagents — one per
A–E — each in an isolated context. Load
[references/subagent-dispatch.md](references/subagent-dispatch.md) for the constructed-context
template and a worked Category-A example. Subagents **report** findings (read-only); the main agent
**fixes** — never let five auditors edit the same files.

### 5. Classify findings

Each finding maps to a checklist point id (A1–E16) + `file:line` + the evidence + a concrete fix.
A residue can trip two categories (a version tag inside a dead link = A2 + C9) — label both.

### 6. Fix (surgical)

Remove residue; **recompose** batch-grouped sections by dimension (deleting the tag isn't enough —
A3 is structural residue); delete dead content; sync doc ↔ impl. Per the purity principle: **no
"待清理 / 下次清理" TODOs** — that is itself a tracing-residue finding. Fix now or flag for a human
decision in the report.

**Output:** `docs/audit/YYYY-MM-DD-purity.md` — audit report (scope, checklist coverage A–E, before/after, fixed, needs review). Template in [references/templates.md](references/templates.md).

## Verify

- [ ] Every category A–E covered, or marked N/A with a reason
- [ ] Each finding has a point-id (A1–E16) + `file:line` + concrete fix
- [ ] Grep sweep re-run clean for the residue classes it targeted (version tags, dead links, `// HACK`)
- [ ] No `待清理` / `下次清理` TODOs left — that's itself residue
- [ ] Audit report produced at `docs/audit/YYYY-MM-DD-purity.md` with before/after + needs-review
- [ ] If subagents were used: each had a constructed context (goal + inputs + boundaries + verify target); findings deduped before fixing

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, surgical scope, verify don't assume).
- [${CLAUDE_PLUGIN_ROOT}/references/purity-checklist.md](${CLAUDE_PLUGIN_ROOT}/references/purity-checklist.md) — the 16-point A–E checklist (the audit criteria).
- [references/subagent-dispatch.md](references/subagent-dispatch.md) — per-category auditor dispatch: constructed-context template + worked Category-A example.
- [references/templates.md](references/templates.md) — audit-report template.
