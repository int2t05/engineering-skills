# General mode

Reference for the `research` skill, **general** mode. Deep multi-source web research with inline
citations and a 9-section conclusion-first Markdown report. Uses the shared spine — see
[references/report-spine.md](report-spine.md) for the fixed structure, main-thread rule, mermaid
rules, and shared skeleton.

## Contents

- [Source strategy](#source-strategy)
- [Quality rules](#quality-rules)
- [9-section output template](#9-section-output-template)
- [Verify (general mode)](#verify-general-mode)

## Source strategy

Fan out across ≥3 query angles and ≥3 source categories. Prioritize by reliability:

| Priority | Source type | Use |
| --- | --- | --- |
| P0 | Official docs, specs, RFCs, papers, release notes | Authoritative capability/behavior claims |
| P1 | GitHub repos (org + repo search), official project blogs | Implementation reality, maintenance, latest activity |
| P2 | Technical blogs, conference talks, community discussions | Adoption friction, operational pain, context |
| P3 | SEO listicles, tutorials, media summaries | Background only; never key evidence |

**Never a primary source:** Stack Overflow answers, random blog posts, AI-generated docs, model
training-data recall. Use them only to point toward a primary source.

Default depth for broad topics: ≥6 relevant sources. For narrow topics, state why fewer suffice.
Collect both Chinese and English sources.

### Search GitHub

When the topic touches a technology, framework, or organization, GitHub is a P0/P1 floor — search it
even though general mode is not GitHub-first by default:

- Search the official org name and likely repo names; collect URL, description, primary language,
  license, stars/forks, latest commit or release date, open issue/PR signal, docs quality.
- A repo's latest commit/release date is ground truth for "is this alive / released / open-sourced" —
  more reliable than any secondary "截至 X 月" claim.
- Record the org name and search terms tried, and the result (found / not found). "Not found" is a
  search outcome, not a fact about the world — see the negative-claim check in SKILL.md Step 4.

## Quality rules

- Fast-moving topics: use fresh sources with exact dates; flag stale data.
- Repository lists: do not sort by stars alone; weigh maintenance, docs quality, issue health, scope fit, integration cost.
- Distinguish tutorial content from production guidance; mark vendor-blog bias.
- Delete unsupported claims or label them as inference.
- Cite at the point where the claim appears, not only in the source appendix.

## 9-section output template

Conclusion-first. §1/§2/§8/§9 are fixed by [report-spine.md](report-spine.md); the 主体 (§3-§7) is
the general-mode survey dimensions. Keep numbering continuous (1→9, no gaps or reuse). Trim sections
to fit the topic, but keep order and fixed sections.

| § | Section | Purpose |
| --- | --- | --- |
| 1 | 结论 (TL;DR) | Key takeaways about the topic — the answer, not the method. Reader knows what matters after this. |
| 2 | 核心认知 | 2-3 mental models + one main thread + ≥1 decision flowchart (mermaid). Every 主体 section serves the thread. |
| 3 | 关系 | Upstream/downstream, related standards/platforms — how X sits in its ecosystem. |
| 4 | 实现 | Structure, selection, workflow — how X is built or how to build with it. |
| 5 | 能力 | Tool/component inventory, artifacts — what X can do. |
| 6 | 局限 | Capability boundaries, fallback paths — what X cannot do. |
| 7 | 评估 | Per-dimension evidence-backed analysis that **supports §1**, does not restate it. Dimension tables, not a decision Q&A. |
| 8 | 避坑清单 | Numbered negative claims, each with evidence or falsification trail (Step 4 output). |
| 9 | 源附录与核查记录 | 9.1 源参考 · 9.2 负面断言核查记录 · 9.3 UNVERIFIED 项 · 9.4 访问限制与缺口 · 术语表 (optional). |

- Inline-cite at each claim (`[text](url)`).
- ≥3 mermaid (≥1 decision flowchart in §2); each serves information (routing/decision/timing/structure), never decorates. No "mixing" requirement — flowchart-only is fine.
- Tables for comparisons, lists, decisions; prefer tables over prose. One sentence per idea.
- Inline-explain jargon on first use (`> **术语·X**: plain-language explanation`); aggregate a glossary in §9 only if not all terms were inline-explained.

### Skeleton

````markdown
# [研究标题]
生成日期：YYYY-MM-DD
范围：[检索了什么、排除了什么]

## 1. 结论 (TL;DR)
- [核心结论 1：关于 X，读者最该知道的一点]
- [核心结论 2]

## 2. 核心认知
**主线**：[一句贯穿全文的决策主线]
[认知一：…。认知二：…。]
```mermaid
flowchart LR
    A(["上游"]) --> B["本对象"] --> C(["下游"])
```

## 3. 关系
[本对象在生态中的位置。]
## 4. 实现
| 选项 | 关键属性 | 适配度 |
| --- | --- | --- |
| … | … | … |
## 5. 能力
| 能力 | 说明 |
| --- | --- |
| … | … |
## 6. 局限
| 边界 | 影响 | 回退 |
| --- | --- | --- |
| … | … | … |
## 7. 评估
| 维度 | 证据 | 判断 |
| --- | --- | --- |
| … | [来源](url) | … |

## 8. 避坑清单
1. [负面断言]——[证据/证否痕迹]
2. [负面断言]——[证据/UNVERIFIED + 搜索痕迹]

## 9. 源附录与核查记录
### 9.1 源参考
- [标题](url) — 访问：YYYY-MM-DD — 日期：[发布/更新或不可见] — 可靠性：[一级/二级] — 支持：[论点]
### 9.2 负面断言核查记录
- [断言]：搜索词 + org + 结果（found / not found / UNVERIFIED）
### 9.3 UNVERIFIED 项
- [无法在官方源证实或证伪的断言]
### 9.4 访问限制与缺口
- [访问限制 + 后续可调研]
````

## Verify (general mode)

- No unresolved placeholders (`TBD`, `[标题]`, `https://example.com`, `github.com/org/repo`).
- Every key conclusion, comparison point, and date-sensitive claim has an inline citation.
- §1 TL;DR is conclusion-first (not process/method); §2 核心认知 states one main thread and includes ≥1 decision flowchart.
- §8 避坑清单 present with numbered negative claims, each carrying evidence or a falsification trail.
- §9 has 9.2 负面断言核查记录 + 9.3 UNVERIFIED + 9.4 访问限制与缺口 subsections.
- 9-section conclusion-first structure (§1→§9, no gaps); ≥3 mermaid serving information.
- Final reply states: file path, source count, access limitations.
