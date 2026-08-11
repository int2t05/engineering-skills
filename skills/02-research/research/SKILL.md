---
name: research
description: Use when the user asks for deep web research, source-backed investigation, current technical/tool comparison, or a cited Markdown research artifact. Triggers on "deep research", "source-backed investigation", "cited report", "深度调研", "深度检索", "调研报告", "调研转文档".
---

## When to use

- Deep, multi-source research that needs inline citations and a source appendix.
- Source-backed investigation or current technical/tool comparison.
- User asks for a cited Markdown research artifact (深度调研, 调研转文档).
- NOT for short queries, quick answers, single-source lookups, or pure local-file analysis. Does not build embeddings, vector stores, crawl archives, or persistent knowledge indexes.
- NOT for market sizing or competitor business analysis (use `market-research`); concrete tool/library selection (use `tech-selection`).

## Steps

1. **Frame the question.**
   - Restate the goal, scope, output language, and output path with the user.
   - Default output: `research/YYYY-MM-DD-<slug>.md` in the workspace. Slug: 2-4 words, lowercase ASCII letters/digits/hyphens; transliterate or summarize non-ASCII; no redundant context prefixes. Accumulative docs (indexes, decision logs) skip the date prefix and use semantic names.
   - If the file exists, append `-2` or `-HHmmss`; overwrite only with explicit permission. Do not silently overwrite an existing research file.
   - If the topic is too broad to search usefully, ask one concise scoping question; otherwise state assumptions and proceed.
   - Consider delegating to a background agent so you keep working while it reads.

2. **Fan-out search.**
   - Split sub-topics: concept, implementation, tools, benchmarks, examples, risks.
   - Plan at least 3 query angles and 3 source categories (official docs, project blogs, papers, release notes, GitHub repos).
   - Default depth for broad topics: ≥6 relevant sources across ≥3 source categories. For narrow topics, state why fewer suffice.
   - For repository sources, collect URL, description, language, stars, forks, open issues, last updated date, and fit for the user's goal.

3. **Fetch sources.**
   - Search current information; never rely on memory.
   - Fetch the source page before summarizing — never treat search snippets as final evidence.
   - On empty or navigation-only pages, retry in order: add wait, switch format, switch canonical URL, try sitemap/site search, fall back to raw GitHub/API source. Mark access limits if all fail.
   - Prefer primary sources; discard reposts, SEO listicles, off-topic, and low-signal duplicates. Collect both Chinese and English sources.

4. **Adversarially verify claims.**
   - For each key claim, follow it back to the primary source that owns it.
   - Record: title, URL, published/updated date (if visible), access date, reliability class, claims supported.
   - Surface conflicts, stale data, missing dates, and access restrictions explicitly.
   - Separate fact from inference; mark uncertain claims as inference.
   - Include contrarian evidence and downside cases; delete unsupported claims or label them as inference.

5. **Synthesize cited Markdown.**
   - Default language: Chinese unless the user specifies otherwise. Proper nouns, code identifiers, filenames, and license names stay in original form — this is convention, not a violation.
   - Use the seven-section numbered structure below; keep numbering continuous (1→7, no gaps or reuse). Trim sections to fit the topic, but keep the order.
   - Inline-cite at each claim (`[text](url)`), not just a URL dump in the appendix.
   - ≥3 mermaid diagrams mixing `flowchart` (decisions/routing/fallbacks) and `sequenceDiagram` (timing/call chains). Diagrams serve information — never decorate.
   - Tables for comparisons, lists, and decisions; prefer tables over prose. One sentence per idea; avoid long stacked clauses.
   - Inline-explain jargon on first use (`> **Term·X**: plain-language explanation`); aggregate a glossary in §7.

   | # | Section | Purpose |
   | --- | --- | --- |
   | 1 | 概述 | Goal, current state, research method |
   | 2 | 关系 | Upstream/downstream, related standards/platforms |
   | 3 | 实现 | Structure, selection, workflow |
   | 4 | 能力 | Tool/component inventory, artifacts |
   | 5 | 局限 | Capability boundaries, fallback paths |
   | 6 | 评估 | Decision summary, tradeoff analysis, QA |
   | 7 | 索引 | Source references, glossary, gaps/follow-ups |

   Skeleton (shows inline citation, mermaid, table, and glossary patterns):
   ````markdown
   # [研究标题]
   生成日期：YYYY-MM-DD
   范围：[检索了什么、排除了什么]

   ## 1. 概述
   ### 1.1 目标
   [一两句说明这次调研要解决什么。]
   ### 1.2 调研方法
   [查询角度 / 源类别。]

   ## 2. 关系
   ```mermaid
   flowchart LR
       A(["上游"]) --> B["本对象"] --> C(["下游"])
   ```

   ## 3. 实现
   | 选项 | 关键属性 | 适配度 |
   | --- | --- | --- |
   | … | … | … |

   ## 6. 评估
   | # | 问题 | 决策 | 依据 |
   | --- | --- | --- | --- |
   | 1 | … | … | [来源](url) |

   ## 7. 索引
   ### 7.1 源参考
   - [标题](url) — 日期。可靠性：一级/二级。支持：[论点]。
   - 访问日期：YYYY-MM-DD。
   ### 7.2 术语表
   | 术语 | 通俗解释 |
   | --- | --- |
   | … | … |
   ````

6. **Quality rules.**
   - Fast-moving topics: use fresh sources with exact dates; flag stale data.
   - Repository lists: do not sort by stars alone; weigh maintenance, docs quality, issue health, scope fit, integration cost.
   - Distinguish tutorial content from production guidance; mark vendor-blog bias.
   - Delete unsupported claims or label them as inference.
   - Cite at the point where the claim appears, not only in the source appendix.

## Verify

- The `.md` file exists and contains no unresolved placeholders (`TBD`, `[标题]`, `https://example.com`).
- Every key conclusion, recommendation, comparison point, and date-sensitive claim has an inline citation.
- §7 source appendix lists access dates and access limitations.
- ≥3 mermaid diagrams present, mixing `flowchart` and `sequenceDiagram`.
- Tables dense; terms explained inline and aggregated in glossary.
- Final reply states: file path, source count, access limitations.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline for every skill.
- [references/pressure-scenarios.md](references/pressure-scenarios.md) — failure-mode pressure tests for this skill.
