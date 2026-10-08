# Human Audit Block

The pack-wide baseline for every document a skill produces: **the doc is not done when
written — it's done when a human has audited it.** Humans audit the documents skills
produce; a doc a human cannot audit (no evidence, no close criteria, no explicit status)
is unfinished. Structure correct ≠ semantics correct; a rule written ≠ an audit passed.

`spec` (PRD) and `architecture` (TECH/ADR) carry their own domain-specific audit catalogs
(`readable-prd-guide.md`, `tech-audit-guide.md`) — this file is the baseline for every
other doc-producing skill.

## Contents

- [Two weights: AUD block vs 确认 block](#two-weights-aud-block-vs-确认-block)
- [AUD block — build-gating docs](#aud-block--build-gating-docs)
- [确认 block — reports, research, ledgers](#确认-block--reports-research-ledgers)
- [Status lifecycle](#status-lifecycle)
- [Stable IDs — every part addressable](#stable-ids--every-part-addressable)
- [Readability bar](#readability-bar)

## Two weights: AUD block vs 确认 block

| Weight | Artifact class | Examples | Human action |
|---|---|---|---|
| **AUD block** | Formal docs gating build work | PRD, TECH, PLAN, SCHEMA, API, PROMPT, CONTEXT, DESIGN, ROADMAP | Work through 6–12 audit items; confirm before implementation starts |
| **确认 block** | Reports, research, ledgers | audit reports, research, ux findings, capacity/cost ledgers, TODO | Work through findings/conclusions; mark 采纳/修正/驳回 with rationale |

Pick by what the doc gates: if people build/launch from it → AUD block; if it informs or
records → 确认 block.

## AUD block — build-gating docs

A section of executable audit items, each answering: what could be wrong here, and what
evidence closes it.

```markdown
| ID | 检查问题 | 关联 | 所需证据 | 关闭标准 | 负责人 |
|---|---|---|---|---|---|
| AUD-01 | <具体、可证伪的问题> | <ID/章节> | <要看的证据> | <怎样算通过> | 待指定 |
```

- IDs stable (never renumbered); statuses: 未执行 / 通过 / 需修改 / 待确认 / 不适用.
- Item count 6–12, trimmed by risk — no padding to hit the number.
- Each item names evidence (a run, a link, a diff, a演练 record) and a close criterion —
  "looks right" closes nothing.

## 确认 block — reports, research, ledgers

Findings and conclusions are claims; the human decides. The doc records the decision, not
just the claim:

```markdown
| 项 | 结论 | 证据 | 人工决定 | 理由 |
|---|---|---|---|---|
| F-01 | <finding/conclusion> | <数据/引用+访问日期> | 采纳/修正/驳回 | <一句话> |
```

- Every conclusion carries evidence: measurement, run output, citation with retrieval date.
- Unverified claims marked as such; no fabricated confirmations.
- Dismissed findings stay in the doc with the reason — deletion destroys the audit trail.
- Decision vocabulary maps to the domain: defect/finding reports (security, a11y, code review)
  use 修复/接受/驳回; conclusions, research, and plans use 采纳/修正/驳回. Both record the
  human's decision plus the reason.

Ephemeral artifacts are exempt — a handoff brief written to an OS temp dir has nothing durable
to audit; the baseline applies to docs that persist in the repo.

## Status lifecycle

```
草案 ──→ 人工审计 ──→ 已确认 ──→ 成熟
  ↑          │ 发现问题        │ 新决策/现实检验
  └─ 修订 ───┘                └─ 修订（保留编号）→ 重审
```

- Status lives on the first screen; **only the human moves it.**
- Revisions preserve IDs, ADR numbers, finding numbers — renumbering destroys the trail.
- 成熟 = 已确认 AND survived reality (implementation/production) long enough to trust.
- New decisions after confirmation enter as new items and re-open the loop; never rewrite
  confirmed history in place.

## Stable IDs — every part addressable

An audit item must point at a part unambiguously — "the third section" is not addressable;
`SEC-03` is. Every auditable doc numbers its parts:

- Sections `SEC-01`, figures `FIG-01`, audit items `AUD-01`, findings `F-01`, open items `OPN-01`.
- Domain items carry their own stable prefix, declared once per doc — spec's
  `G/SCN/SCP/REQ/NFR/AC/DEC/MS`, ADR numbers (`docs/design/adr/NNNN-slug.md`), endpoint groups,
  ledger entries.
- Rules: IDs unique across the doc; decoupled from ordering — new items append, deleted IDs are
  never reused; a rule is stated once and referenced by ID elsewhere; keep a meaningful name
  after the ID; figure nodes and table headers are not IDs.

## Readability bar

An unreadable doc cannot be audited — readability is an audit prerequisite, not styling:

- First screen answers: what/why, for whom, this version's scope, status, blocking items.
- Headings ≤ 3 levels; paragraphs 2–4 sentences; tables 3–5 columns (split beyond 6).
- Every part carries its stable ID (see Stable IDs above) — audit items reference parts by ID,
  never by position.
- Every figure: ID, title, 1–2 sentence caption, linked items; branch flows show outcomes;
  the body stands without rendering.
- A rule stated once and referenced by ID; bold only conclusions, boundaries, open items.
- Unknowns collected in one place (OPN), each with impact, suggestion, decision owner.
- External facts cite reliable sources with retrieval time; market research listed as
  to-be-researched rather than skipped silently.
