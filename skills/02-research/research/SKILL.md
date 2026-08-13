---
name: research
description: Use when the user asks for source-backed investigation — deep web research, market/competitor analysis, or technology selection — producing a cited Markdown artifact under docs/research/. Three modes: general, market, tech-selection. Triggers on "deep research", "调研报告", "市场调研", "竞品分析", "技术选型", "选哪个", "方案对比". Not for design visual references (use design-research) or writing the PRD/spec (use spec).
---

# Research

Source-backed investigation that produces a cited Markdown artifact under `docs/research/`. Three
modes share one spine — frame the question, search with the mode's source strategy, adversarially
verify, synthesize a cited report — but differ in sources, frameworks, and output template.

## When to use

- **general** — deep multi-source web research with inline citations (深度调研, 调研转文档)
- **market** — market sizing, competitor analysis, investor due diligence, industry intelligence (市场调研, 竞品分析)
- **tech-selection** — choosing/comparing a stack, library, framework, or repo for a concrete requirement (技术选型, 方案对比, 选哪个)
- Triggers on "deep research", "调研报告", "市场调研", "竞品分析", "技术选型", "选哪个", "方案对比"

**Not for:** short queries or single-source lookups; design visual references (use `design-research`); writing the PRD/spec itself (use `spec`). Does not build embeddings, vector stores, or persistent indexes.

## Steps

### 1. Pick the mode and frame the question

Infer the mode from the ask, then restate the goal, scope, output language, and output path.

- **general** → `docs/research/YYYY-MM-DD-<slug>.md` (slug: 2-4 words, lowercase ASCII; transliterate non-ASCII; no redundant prefixes). If the file exists, append `-2` or `-HHmmss`; overwrite only with explicit permission.
- **market** → `docs/research/market.md`
- **tech-selection** → `docs/research/competitor.md`

If the topic is too broad to search usefully, ask one concise scoping question; otherwise state
assumptions and proceed. Consider delegating to a background agent to keep working while it reads.

Load the mode reference for the mode-specific source strategy, frameworks, and output template:
- general → [references/general-mode.md](references/general-mode.md)
- market → [references/market-mode.md](references/market-mode.md)
- tech-selection → [references/tech-selection-mode.md](references/tech-selection-mode.md)

### 2. Search with the mode's source strategy

Every mode fans out across ≥3 source categories and ≥3 query angles, but the source priority differs:

- **general** — official docs, project blogs, papers, release notes, GitHub repos. ≥6 relevant sources for broad topics.
- **market** — investor/fund data, competitive intel, market reports, public datasets. Includes the 4 market sub-modes (investor diligence, competitive analysis, market sizing, technology/vendor research).
- **tech-selection** — GitHub-first (P0: repos/README/issues/PRs/releases), then official docs (P1), community signal (P2), SEO listicles background-only (P3). ≥5 credible candidates before narrowing.

### 3. Fetch sources — never trust snippets

Search current information; never rely on memory. Fetch the source page before summarizing — never
treat search snippets as final evidence. On empty or navigation-only pages, retry in order: add
wait, switch format, switch canonical URL, try sitemap/site search, fall back to raw GitHub/API
source. Mark access limits if all fail. Prefer primary sources; discard reposts, SEO listicles,
off-topic, and low-signal duplicates. Collect both Chinese and English sources where relevant.

### 4. Adversarially verify claims

For each key claim, follow it back to the primary source that owns it. Record: title, URL,
published/updated date, access date, reliability class, claims supported. Surface conflicts, stale
data, missing dates, and access restrictions explicitly. Separate fact from inference; mark
uncertain claims as inference. Include contrarian evidence and downside cases; delete unsupported
claims or label them as inference.

### 5. Synthesize the cited Markdown report

Default language: Chinese unless the user specifies otherwise. Proper nouns, code identifiers,
filenames, and license names stay in original form. Inline-cite at each claim (`[text](url)`), not
just a URL dump in the appendix. Use the mode's output template (7-section general / 6-section
market / 10-section tech-selection) — trim to fit but keep section order. ≥3 mermaid diagrams
mixing `flowchart` and `sequenceDiagram` for general; tables for comparisons; inline-explain jargon
on first use and aggregate a glossary.

### 6. Deliver a short chat summary

Report: file path, the key conclusion/recommendation, top reasons, main tradeoff or risk, source
count by source class, and any access limitations. If live browsing was unavailable or forbidden,
do not present the result as researched — explain the limitation and offer an offline-only draft.

**Output:** `docs/research/YYYY-MM-DD-<slug>.md` (general) / `docs/research/market.md` (market) / `docs/research/competitor.md` (tech-selection) — cited research artifact, archived cumulatively.

## Verify

- The `.md` file exists and contains no unresolved placeholders (`TBD`, `[标题]`, `https://example.com`, `github.com/org/repo`).
- Every key conclusion, recommendation, comparison point, and date-sensitive claim has an inline citation.
- Source appendix lists access dates and access limitations.
- For general: ≥3 mermaid diagrams mixing `flowchart` and `sequenceDiagram`; 7-section structure.
- For tech-selection: GitHub repo evidence + official docs present; stars alone did not drive the recommendation.
- For market: all numbers sourced or labeled estimates; old data flagged; recommendation follows from evidence.
- Final reply states: file path, source count, access limitations.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline for every skill (surface assumptions, verify don't assume, push back).
- [${CLAUDE_PLUGIN_ROOT}/references/product-principles.md](${CLAUDE_PLUGIN_ROOT}/references/product-principles.md) — product discipline (the real competitor is the current workaround). Linked by market + tech-selection modes.
- [references/general-mode.md](references/general-mode.md) — general mode: 7-section template, fan-out source strategy, mermaid/glossary patterns.
- [references/market-mode.md](references/market-mode.md) — market mode: 4 sub-modes (investor/competitive/sizing/tech-vendor), 6-section template, market frameworks.
- [references/tech-selection-mode.md](references/tech-selection-mode.md) — tech-selection mode: GitHub-first P0-P3 source priority, 10-section template, selection rubric.
- [references/pressure-scenarios.md](references/pressure-scenarios.md) — failure-mode pressure tests for this skill.
