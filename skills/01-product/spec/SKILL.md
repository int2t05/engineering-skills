---
name: spec
description: Use when starting a new project, feature, or significant change — writes a spec/PRD covering objectives, structure, commands, code style, testing, and boundaries before any code; also refactors or updates an existing PRD into a human-readable, auditable form with stable IDs (G/REQ/AC/AUD/OPN), Mermaid figures, and merged confirmed decisions. Triggers on "write spec", "create prd", "spec out", "写需求文档", "写规格", "需求文档", "精简 PRD", "重构 PRD", "更新 PRD" — also when user says "要做什么" / "需求是什么" / "把这个 PRD 改得更可读". Not for syncing docs to built code → use documentation-audit.
---

# Spec

Write, refactor, or update the spec/PRD — the shared source of truth for what we're building,
why, and how we'll know it's done. Code without a spec is guessing. Core principle:
**concise, readable, easy to audit** — clarity and accuracy first, brevity second; never drop
a binding rule to save space. From the first screen a human reader can answer: for whom, what
problem, what this version ships, how the flow goes, what happens on exceptions, how it's
accepted, and what still needs a decision.

## When to use

- Starting a new project, feature, or significant change; requirements ambiguous or only a vague idea.
- The change touches multiple files or modules.
- Refactoring an existing PRD that is bloated, unreadable, or internally inconsistent.
- Updating a PRD by merging confirmed discussion/audit decisions into a new version.

**Not for:** single-line fixes, typos, or unambiguous changes; system-design decisions only →
use `architecture`; syncing docs to already-built code → use `documentation-audit`;
market/competitor investigation feeding the spec → use `research`.

## Steps

1. **Read everything; classify what you know.** Mark every claim in the source material and
   confirmed decisions: source fact / explicitly confirmed / proposed default / open (OPN) /
   to-be-tested. Never fabricate user confirmations, prices, measured results, or competitor
   capabilities.

2. **Surface assumptions.** List what you're assuming (tech stack, auth model, database,
   target environment). Ask the user to correct before proceeding.

3. **Ask sparingly.** 3–5 clarifying questions where the prompt is ambiguous — problem/goal,
   core functionality, scope, success criteria; lettered options for quick replies. At most 3
   per round when updating. If the user says "produce it directly", finish the document first
   and record unresolved items as OPN — don't loop on confirmations.

4. **Decide create vs update.** Updating an existing PRD: preserve existing IDs and
   requirement semantics, record why anything was deleted or changed, never silently shrink
   committed scope (see the guide's update discipline).

5. **Design before prose — TOC, IDs, figures.** Plan the section map (6–10 main sections to
   start; detail to appendices; no empty placeholders), the ID allocation, and what each
   figure explains. The first screen fits one glance: version, date, status, positioning,
   readers, goals, this version's scope, blocking items. Reframe vague requirements as
   testable criteria ("make the dashboard faster" → "LCP < 2.5s on 4G"). Load on demand:
   `references/prd-patterns.md` (PRD structure, user stories, Given/When/Then, INVEST),
   `references/readable-prd-guide.md` (layout, Mermaid, requirement cards, human audit,
   update discipline), `references/prioritization.md` (RICE, Kano, MoSCoW),
   `references/metrics-frameworks.md` (North Star, AARRR, retention).

6. **Write the body with stable IDs** (scheme below). User-visible behavior and acceptance
   boundaries — database and framework algorithm detail belongs in TECH. Every core
   requirement answers: trigger/input, behavior, output, exceptions; where applicable, state
   explicit results for repetition, concurrency, cancellation, retry, deletion, recovery,
   permissions, and config changes. Every core REQ links ≥1 G and ≥1 AC; high-risk REQs link
   AUD. A rule is stated once and referenced by ID. Never renumber on insert; never reuse a
   deleted ID.

7. **Publish.** Two layers: `docs/PRD.md` — project-level requirements, concise
   (mermaid-heavy), on main, the shared source of truth; `docs/vX.Y/prd.md` — the current
   version's detailed PRD, on the version branch (falls back to `docs/PRD.md` alone for
   single-version projects). Commit both — living documents; update when decisions or scope
   change; reference in PRs.

8. **User review gate.** Ask the user to review the written spec before any implementation.
   If they request changes, make them and re-verify. Only proceed once approved.

## Stable IDs

| Prefix | Object |
|---|---|
| G | product goal |
| SCN | user scenario |
| SCP | scope and non-goals |
| REQ | requirement / business rule (extendable: `REQ-SYNC-001`) |
| NFR | performance, security, reliability, availability |
| AC | executable acceptance criterion |
| AUD | human-audit item |
| DEC | key decision |
| OPN | open item — to confirm / to fill / to test |
| MS | milestone |

- Format `REQ-001`, unique across the document; sections `SEC-01`, figures `FIG-01`.
- IDs are decoupled from ordering — new items append; deleted IDs never reused; record
  deprecated/replaced relations. Legacy docs keep original numbering; provide a mapping on restructure.
- Don't number explanations, table headers, or figure nodes; keep a meaningful name after the ID.
- Figures explain relations; tables carry exact rules; figure nodes are not requirement IDs.

## Template

```markdown
# Spec: <名称>

<!-- 首页一屏：版本/日期/状态/定位/读者/本版范围/阻塞项入口（OPN） -->
| 版本 | vX.Y（日期） | 状态 | 草案/人工审计/已确认/成熟 | 定位 | 为<谁>解决<什么问题> |
| 读者 | 产品·研发·测试·审计 | 本版范围 | 3–6 条（→SCP） | 阻塞项 | OPN-xx |

## 目标 G-01…            为谁解决什么问题；成功标准可测
## 用户场景 SCN-01…      谁、在什么情况下、要完成什么
## 范围与非目标 SCP-01…  本版做什么；明确不做什么（Non-Goals）
## 核心流程 FIG-01…      mermaid：主流程 / 状态生命周期 / 异常恢复
## 需求 REQ-001…         触发/输入、行为、输出、异常（复杂项用卡片，简单项用表）
## 工程约定              Project Structure · Commands · Code Style · Testing Strategy
## 非功能需求 NFR-01…    性能/安全/可靠性，含具体阈值
## 验收标准 AC-001…      前置 / 操作 / 可观察结果
## 人工审计 AUD-01…      检查问题/关联/证据/关闭标准（6–12 项）
## 关键决策 DEC-01…      已拍板的取舍
## 待决事项 OPN-01…      待确认 / 待填 / 待测
## 边界                  Always / Ask first / Never
```

Adapt the map — drop sections that don't apply, split by domain when complex; never keep empty
placeholders. Engineering-section guidance (commands, code-style snippet, test seams) lives in
`references/readable-prd-guide.md`.

Planning the implementation FROM this spec uses Claude Code's built-in plan mode
(engineering-principles §7) — no custom plan skill; the spec is plan mode's input.

## Verify

- The spec file exists on disk and is committed to version control.
- First screen alone answers goal/scope/status; headings ≤ 3 levels; no over-wide tables or duplicated paragraphs.
- Every core REQ links ≥1 G and ≥1 AC; IDs unique; every reference resolves; updated docs preserve historical IDs.
- Confirmed / suggested / to-be-tested distinguishable; success criteria specific and
  testable, not vague; no committed scope silently dropped.
- Every figure has a FIG ID, title, caption, linked REQs; branch flows show outcomes; body stands without rendering.
- Normal, exception, and human-vs-automatic conflict rules explicit; automatic-check vs
  human-approval scopes separated.
- AC observable (precondition / operation / observable result); trial-run pass never claimed
  as full-scenario guarantee; cost boundaries separate estimate from unknown.
- AUD section present (6–12 items, risk-trimmed), each with evidence and a close criterion;
  Boundaries (Always / Ask first / Never) defined.
- Open items collected in OPN (question / impact / suggestion / decision owner / latest
  stage); no fabricated conclusions or confirmation records.
- The user has reviewed and approved the spec.

**Output:** `docs/PRD.md` (project-level, concise, main) + `docs/vX.Y/prd.md` (version-level, detailed, version branch). Single-version projects fall back to `docs/PRD.md` alone.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill; §7 covers plan mode for implementation planning.
- [${CLAUDE_PLUGIN_ROOT}/references/product-principles.md](${CLAUDE_PLUGIN_ROOT}/references/product-principles.md) — product discipline (need≠feature, outcomes over outputs, say no to good ideas, the real competitor is the workaround).
- [references/readable-prd-guide.md](references/readable-prd-guide.md) — readable-spec craft rules: layout density, Mermaid figures, requirement cards, human audit & OPN formats, update discipline, engineering sections.
- [references/prd-patterns.md](references/prd-patterns.md) — PRD structure, user stories, Given/When/Then acceptance criteria, INVEST, Non-Goals, success-criteria reframing, anti-patterns.
- [references/prioritization.md](references/prioritization.md) — RICE, ICE, Kano, MoSCoW, Value×Feasibility matrix, true-need vs false-need filter.
- [references/metrics-frameworks.md](references/metrics-frameworks.md) — North Star metric, AARRR funnel, retention curves, cohort analysis, Hook Model, A/B testing discipline, data-driven loop.
