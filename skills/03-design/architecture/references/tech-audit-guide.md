# Tech Audit Guide

How TECH-class documents (architecture overviews, ADRs) earn trust: reference-first decision
making, the audit → confirm → revise → mature lifecycle, and what a human auditor actually
checks.

## Contents

- [Reference-first: no designing from nothing](#reference-first-no-designing-from-nothing)
- [Lifecycle: audit → confirm → revise → mature](#lifecycle-audit--confirm--revise--mature)
- [What a human audits in a TECH doc](#what-a-human-audits-in-a-tech-doc)
- [AUD and OPN table formats](#aud-and-opn-table-formats)

## Reference-first: no designing from nothing

Every pattern, datastore, and component choice names a real implementation that faced similar
requirements. A design with no nameable reference is unfinished, not creative.

- **What counts:** OSS repos (and their architecture docs / RFCs), engineering blogs from
  teams at comparable scale, official case studies, published postmortems. A nameable,
  checkable item — not "industry best practice".
- **Selection bar:** same problem class (not just same technology), comparable scale and
  constraints (traffic, team size, ops budget), link resolvable at audit time.
- **What to record per reference:** link + access date; what they did; what we adopt; what we
  adapt or reject; how our constraints differ. The differences are the value — they are where
  our design actually decides something.
- **No reference at hand?** Research first (web/repo search), record the retrieval date.
  Still nothing comparable? Say so explicitly in the DEC/ADR and mark the decision as
  unproven — don't manufacture confidence.
- **Fabrication ban:** never invent benchmarks, prices, adoption claims, or "confirmed"
  requirements. Unverified claims are marked as such, with what would verify them.

## Lifecycle: audit → confirm → revise → mature

Status lives on the first screen and moves only by human decision:

```
草案 draft ──→ 人工审计 in-audit ──→ 已确认 confirmed ──→ 成熟 mature
     ↑                │ findings                    │ new decisions
     └────── revise ──┘                             └──→ revise (preserve ADR numbers) → re-audit
```

- **草案 draft:** written, self-checked against Verify; AUD items listed but 未执行.
- **人工审计 in-audit:** a human works through the AUD items; each item ends 通过 / 需修改 /
  待确认 / 不适用, with evidence attached.
- **已确认 confirmed:** every AUD item closed; feedback incorporated or explicitly overridden
  with rationale.
- **成熟 mature:** confirmed AND tested by reality — the design survived implementation or
  production long enough to trust; later decisions revise via new ADRs, never by rewriting
  history (superseded ADRs record their successor).

Revisions preserve ADR numbers and IDs — an audited doc that renumbers itself destroys the
audit trail.

## What a human audits in a TECH doc

Structure correct ≠ decision correct; a citation exists ≠ it fits our constraints. The AUD
items make the human check judgment, not formatting:

| 审计维度 | 检查问题 |
|---|---|
| 参考真实性 | 每个决策引用的参考真实可访问？确属同类需求而非同名词？ |
| 参考适配 | 参考的规模/语言/团队/运维条件与我们可比？差异是否被说明并吸收进设计？ |
| 取舍完整 | 每个选择记录了被拒方案与理由？只有好处没有代价的决策 = 未完成 |
| NFR 可测 | 每类 NFR 有具体阈值或明确"不适用"？阈值与 PRD 目标对应？ |
| 失败恢复 | 每个组件有失败模式与缓解？降级、重试、回滚路径画出来了吗？分支有结果？ |
| 一致性 | 图 ↔ 组件 ↔ 数据层 ↔ PRD 目标互相一致？图表达的行为正文都有？ |
| 成本运维 | 运行成本、复杂度、权限边界被认真对待？估算与未知分开？ |
| 可逆性 | 难逆转的决策都有 ADR？有 ADR 的决策真的难逆转（没凑数）？ |
| 未决集中 | OPN 含问题/影响/建议/决策者？无虚构确认或未标注的猜测？ |

Trim by risk: a small service may merge 参考真实性与参考适配; a platform rebuild audits all
nine.

## AUD and OPN table formats

```markdown
| ID | 检查问题 | 关联 | 所需证据 | 关闭标准 | 负责人 |
|---|---|---|---|---|---|
| AUD-01 | 消息队列选型参考（Kafka @ LinkedIn 规模）与我们峰值吞吐可比？ | ADR-0002 | 参考链接+访问日期、峰值对比表 | 差异说明并写入 ADR | 待指定 |
| AUD-02 | 支付服务失败后能降级不阻塞主流程？ | FIG-03 | 故障演练记录 | 演练一次成功 | 待指定 |
```

Statuses: 未执行 / 通过 / 需修改 / 待确认 / 不适用。规则写清 ≠ 审核通过。

```markdown
| ID | 问题 | 影响 | 建议 | 决策者／最晚阶段 |
|---|---|---|---|---|
| OPN-01 | 自建 Kafka 还是托管服务？ | ADR-0002 成本项 | 先托管，迁移成本写入 ADR | 架构人／开发前 |
```
