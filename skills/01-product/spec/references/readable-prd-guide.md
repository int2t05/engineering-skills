# Readable Spec Guide

Craft rules for the spec skill: layout density, Mermaid figures, requirement and acceptance
writing, human audit and open items, updating an existing PRD without breaking it, and the
engineering sections for pre-code specs.

## Contents

- [Layout and density](#layout-and-density)
- [Mermaid figures — explain, don't decorate](#mermaid-figures--explain-dont-decorate)
- [Requirements and acceptance](#requirements-and-acceptance)
- [Human audit and open items](#human-audit-and-open-items)
- [Updating an existing PRD](#updating-an-existing-prd)
- [First screen and section map](#first-screen-and-section-map)
- [Requirement card, AUD and OPN tables](#requirement-card-aud-and-opn-tables)
- [Engineering sections (pre-code specs)](#engineering-sections-pre-code-specs)

## Layout and density

- First screen fits one glance: version, date, status, positioning, readers, goals, this
  version's scope, and the entry point to open blocking items. No repeated long paragraphs on it.
- Start from 6–10 main sections; split complex products by domain; move detail to appendices.
  Drop sections that don't apply — never keep empty placeholders. Headings at most 3 levels.
- Paragraphs usually 2–4 sentences. Parallel items become short lists; avoid deep nesting.
- Tables for scope, rules, status, trade-offs, and audits — usually 3–5 columns. Beyond ~6
  columns or when cells turn into paragraphs: split the table or convert to requirement cards.
- Bold only conclusions, boundaries, and open items — never whole paragraphs.
- A rule is stated in exactly one place; everywhere else references the ID.
- The spec writes user-visible behavior and acceptance boundaries. Database design and
  framework algorithms go to TECH; already-confirmed technical constraints may be summarized.
- Include competitor / commercialization / security sections by actual scenario — never fill
  chapters for completeness; never omit security and recovery requirements that do apply.

## Mermaid figures — explain, don't decorate

- Prefer several small figures over one giant. A typical multi-stage product uses 3–5:
  product boundary, core flow, state lifecycle, exception recovery, human review & release.
  Scale to complexity; never pad a single feature to hit a figure count.
- `flowchart TD` for branching flows; `stateDiagram-v2` for lifecycles; `sequenceDiagram`
  only when there is a real interaction order between parties.
- One figure answers one question. Usually 5–9 nodes; at most 5 nodes/participants
  horizontally; split rather than cram.
- Every figure carries a FIG ID, a title, a 1–2 sentence explanation, and its linked REQ
  IDs. State figures cover the failure / cancellation / recovery states that actually apply.
- Use mermaid fenced code blocks with short Chinese labels; quote any label containing
  punctuation or brackets. No HTML, no `click`, no inline config.
- Figures express only behavior already in the text. Suggested flows are marked as
  suggestions — a figure never grants approval or execution authority.
- Don't re-draw a single fact or simple list as a figure; exact rules go in tables. The body
  must be understandable without rendering.
- Validate every figure when a renderer is available; otherwise static-check each one and
  never claim render-verification.

## Requirements and acceptance

- Every requirement answers: trigger/input, behavior, output, exceptions. Complex items use
  requirement cards; simple items live in tables.
- Where applicable, state the explicit result for: repetition, concurrency, cancellation,
  retry, deletion, recovery, permissions, and configuration changes.
- Vague qualifiers (fast, accurate, low-cost) need a measure, condition, threshold, or a
  linked OPN entry. Newly proposed metrics are marked as suggestions.
- AC states precondition, operation, and observable result. Distinguish functional tests,
  human content review, and real-value validation.
- Separate automatic verification from human approval: correct structure and citations do
  not imply semantic correctness.
- A trial-run pass is not a full-scenario guarantee. Cost boundaries say what is estimated,
  what is in flight, and what usage is unknown.
- Verify external facts against reliable sources and record the retrieval time. Market
  research is not mandatory for every document — list it as to-be-researched when needed.

## Human audit and open items

- Always include an executable human-audit section — typically 6–12 items, trimmed by risk.
- Each AUD item has: ID, check question, linked REQ/AC, required evidence, and a close
  criterion. Owner and latest check stage go in a side table; use "to be assigned" when no
  name was provided.
- Statuses: not run / passed / needs changes / to confirm / not applicable. A written rule is
  not a passed audit.
- Audit coverage: goal scope, main flow, exception recovery, cost & permission, quality &
  value, delivery conditions. Don't turn the audit process itself into per-item product
  approval features without reason.
- OPN records question, impact, suggestion, decision owner / latest stage. Only items that
  truly block a step block that step.

## Updating an existing PRD

- Preserve existing IDs and the semantics of confirmed requirements; record a reason for
  every deletion or semantic change.
- Never silently shrink committed scope — surface reductions explicitly for the human to accept.
- Keep legacy numbering; when restructuring, provide an old→new ID mapping instead of
  renumbering for style.
- Merge confirmed decisions from discussion and audit rounds into the body; move still-open
  items to OPN. Don't re-litigate settled DEC entries.

## First screen and section map

```markdown
# <产品名> 需求文档

| 项 | 内容 |
|---|---|
| 版本 | vX.Y（YYYY-MM-DD） |
| 状态 | 草案 / 人工审计 / 已确认 / 成熟 |
| 定位 | 为 <谁> 解决 <什么问题>（一句话） |
| 读者 | 产品、研发、测试、审计人 |
| 本版范围 | <3–6 条>；明确不做 → SCP-001 |
| 阻塞项 | OPN-001（未决，阻塞 <阶段>） |
```

## Requirement card, AUD and OPN tables

Complex requirements use cards; simple ones share one table
(`ID | 名称 | 触发 | 行为 | 异常 | 验收 | 状态`):

```markdown
### REQ-003 <导出报表>

| 项 | 内容 |
|---|---|
| 关联目标 | G-01 |
| 触发／输入 | 用户在报表页点击“导出”，选择时间范围（≤90 天） |
| 行为 | 生成 CSV，含表头与合计行；超过 5 万行转异步任务并通知 |
| 输出 | CSV 下载；异步完成后站内通知 |
| 异常 | 范围超限 → 提示并建议拆分；生成失败 → 保留任务记录，可重试 |
| 验收 | AC-005、AC-006 |
| 状态 | P0 · 已确认 |
```

```markdown
| ID | 检查问题 | 关联 | 所需证据 | 关闭标准 | 负责人 |
|---|---|---|---|---|---|
| AUD-01 | 导出超 5 万行确实走异步且可重试？ | REQ-003 | 测试记录 + 通知截图 | 重现一次成功 | 待指定 |
```

```markdown
| ID | 问题 | 影响 | 建议 | 决策者／最晚阶段 |
|---|---|---|---|---|
| OPN-01 | 免费版是否限制导出次数？ | REQ-003 范围 | 先不限，上线后看数据 | 产品／开发前 |
```

## Engineering sections (pre-code specs)

These sections turn the spec into plan mode's input. Keep them in the version-level
`docs/vX.Y/prd.md`; summarize at project level.

- **Project Structure** — directory layout with descriptions: where source, tests, docs live.
- **Commands** — build, test, lint, dev: full executable commands with flags.
- **Code Style** — one real code snippet showing conventions: naming, formatting, key patterns.
- **Testing Strategy** — framework, test locations, coverage expectations, which test levels
  for which concerns. Identify test seams — prefer existing seams, use the highest seam
  possible (the fewer seams across the codebase, the better).
- **Boundaries** — Always (run tests before commits, validate inputs, follow naming
  conventions) / Ask first (schema changes, new dependencies, CI config changes) / Never
  (commit secrets, edit vendor dirs, remove failing tests without approval).
