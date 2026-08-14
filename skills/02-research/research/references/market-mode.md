# Market mode

Reference for the `research` skill, **market** mode. Market sizing, competitor comparisons,
investor due diligence, industry intelligence, fund research, and technology scans that inform
business decisions.

## Contents

- [Research standards](#research-standards)
- [Source priority](#source-priority)
- [The 4 sub-modes](#the-4-sub-modes)
- [Output template](#output-template)
- [Verify (market mode)](#verify-market-mode)

## Research standards

- Every important claim needs a source.
- Prefer recent data; call out stale data explicitly.
- Include contrarian evidence and downside cases.
- Translate findings into a decision, not just a summary.
- Separate fact, inference, and recommendation clearly.

## Source priority

| Priority | Source type | Use |
| --- | --- | --- |
| P0 | SEC filings, public datasets (census, registry), investor/fund databases | Hard numbers, fund terms, ownership |
| P1 | Market reports (Gartner, IDC, CB Insights), analyst research, prospectuses | Market size, segmentation, forecasts |
| P2 | Press releases, company blogs, Crunchbase, funding announcements | Traction, positioning, pricing clues |
| P3 | SEO listicles, media summaries | Background only; never key evidence |

Final recommendations must be primarily supported by P0 and P1; use P2 to qualify confidence and
surface risk. If P0/P1 evidence is missing, label the number an estimate and state the gap.

## The 4 sub-modes

Run the sub-mode that fits the ask.

**Investor / Fund Diligence** — fund size, stage, and typical check sizes; relevant portfolio
companies and sector thesis; public recent activity and leadership; fit with the user's stage,
market, and geography; red flags (signaling risk, dead funds, heavy liquidation preferences).

**Competitive Analysis** — product reality (not marketing copy); funding and investor history;
traction metrics if public; distribution channel and pricing clues; strengths, weaknesses, and
positioning gaps the user can exploit. Build a feature matrix against the user's offering.

**Market Sizing** — top-down estimate from a report or public dataset; bottom-up sanity check
from realistic customer counts × price (see the worked example below); explicit assumption for
every leap in logic. State the gap between TAM (total addressable) and SOM (realistically
obtainable) — a big TAM with a tiny SOM is not a big opportunity.

**Technology / Vendor Research** — how it works; trade-offs and adoption signals; integration
complexity; lock-in, security, compliance, and operational risk; migration cost if replaced.

### Market sizing worked example (TAM / SAM / SOM)

For a developer tool targeting Python backend teams:

- **TAM** (Total Addressable Market) — the entire universe that could conceivably use the
  category. ~25M professional developers worldwide (P0/P1 source). This is an upper bound, not
  a forecast.
- **SAM** (Serviceable Available Market) — the slice your product can actually reach. ~4M Python
  backend developers (filter by language + role, P1 report or community survey).
- **SOM** (Serviceable Obtainable Market) — what you can realistically capture, typically
  year-one. If 2% of SAM could be reached via your channel and 10% of those convert at $50/yr:
  4M × 2% × 10% × $50 = **$400K ARR**. Show each multiplier's source or label it an assumption.

TAM answers "is the ceiling high enough to matter"; SOM answers "is the floor high enough to
survive." Always report SOM, not just TAM.

For SWOT, PEST, Porter's Five Forces, competitive feature matrix, and positioning quadrant —
load [references/market-frameworks.md](market-frameworks.md).

## Output template

Default path: `docs/research/market.md`. If the file exists, append `-2` or `-HHmmss`; overwrite
only with explicit permission. Trim to fit, keep section order. Default language: Chinese unless
the user specifies otherwise.

```markdown
# [主题] 市场研究

生成日期：YYYY-MM-DD
范围：[检索了什么、排除了什么]
输出：[报告路径]

## 1. 执行摘要
[一段话：核心发现 + 建议方向。决策导向，不是摘要堆砌。]

## 2. 关键发现
- [发现 1，带来源]
- [发现 2，带来源]
[按子模式组织：投资尽调 / 竞品 / 市场规模 / 技术供应商]

## 3. 市场规模（如适用）
| 指标 | 数值 | 来源 / 假设 |
| --- | --- | --- |
| TAM | [值] | [来源] |
| SAM | [值] | [来源 / 过滤逻辑] |
| SOM | [值] | [乘数链 + 假设] |

## 4. 影响
[这些发现对用户决策意味着什么。机会 = 需求 × 盲区 ÷ 难度。]

## 5. 风险与注意事项
[反方证据、下行风险、过时数据、假设的脆弱点。]

## 6. 建议
[明确的下一步行动，而非"值得继续研究"。]

## 7. 来源
- [标题](<url>) — 访问：YYYY-MM-DD — 日期：[发布/更新或不可见] — 可靠性：[P0/P1/P2/P3] — 支持：[论点]
```

**Output:** `docs/research/market.md` — a decision-oriented research summary with source attribution.

## Verify (market mode)

- All numbers are sourced or labeled as estimates with the assumption chain shown.
- Market sizing reports SOM (realistically obtainable), not just TAM.
- Old data is flagged.
- The recommendation follows from the evidence.
- Risks and counterarguments are included.
- The output makes a decision easier, not just longer.
