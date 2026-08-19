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

Route by the dominant signal in the ask — don't guess:

| Signal in the ask | Mode | Source strategy |
| --- | --- | --- |
| Tech / framework / library / SDK / repo / tool comparison | tech-selection | GitHub-first P0 |
| Market / competitor / investor / industry / pricing / TAM | market | SEC, reports, press |
| Everything else — concept, spec, state-of-the-art survey | general | Official docs, blog, paper, GitHub |

If the ask hits **two or more modes** (e.g. "research DeepSeek's harness" is both a tech-framework
question *and* a company deep-dive; "an AI company's stack + market" is both tech-selection and
market), **ask the user to pick one** — "技术选型（GitHub 源优先）/ 市场分析 / 通用深度？三选一" —
rather than silently choosing. A single dominant signal needs no question; state assumptions and
proceed.

Then restate the goal, scope, output language, and output path:

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
source. Mark access limits if all fail. If the fetch tool itself is unavailable (network policy,
auth wall) or a search tool's quota is exhausted, switch tools by quota dependency — see
[references/web-tool-fallback.md](references/web-tool-fallback.md). Prefer primary sources; discard
reposts, SEO listicles, off-topic, and low-signal duplicates. Collect both Chinese and English
sources where relevant. Source-code material (repo, SDK source, release notes whose canonical home
is a repo) → `git clone --depth 1` into `archive/` (gitignored provenance) and read locally, rather
than relying on remote fetch of individual files.

### 4. Adversarially verify claims

For each key claim, follow it back to the primary source that owns it. Record: title, URL,
published/updated date, access date, reliability class, claims supported. Surface conflicts, stale
data, missing dates, and access restrictions explicitly. Separate fact from inference; mark
uncertain claims as inference. Include contrarian evidence and downside cases; delete unsupported
claims or label them as inference.

Two checks are mandatory, not optional:

- **Falsify negative claims on GitHub.** If a conclusion asserts that something does *not* exist —
  "X 未发布 / 不存在 / 无官方实现 / 尚未开源 / 未开源" — search the org/product on GitHub before publishing
  it. "Didn't find it" ≠ "doesn't exist": record the search term, the org name tried, and the result
  (found / not found). If the negative cannot be falsified from a primary source, label it
  `UNVERIFIED:` with the search trail, and do not present a secondary source's "截至 X 月" snapshot
  as the current truth.
- **Re-check recency on secondary sources.** When a secondary source is dated "截至 X 月" / "as of X"
  and that point is more than one month old, check the official org's latest activity (GitHub
  release/commit, official blog, official X) before restating its claim. A stale "as of" is a lead,
  not a conclusion.

### 5. Synthesize the cited Markdown report

Default language: match the user's input language (Chinese input → Chinese report, English → English). The user can override with an explicit instruction. Proper nouns, code identifiers,
filenames, and license names stay in original form. Inline-cite at each claim (`[text](url)`), not
just a URL dump in the appendix. Use the **conclusion-first 9-section spine** shared by all modes —
§1 TL;DR → §2 核心认知 → §3-§7 主体 → §8 避坑清单 → §9 源附录与核查记录. Load
[references/report-spine.md](references/report-spine.md) for the full structure, main-thread rule,
mermaid rules, and shared skeleton. Each mode ref fills the mode-specific 主体 (§3-§7). Trim to fit
but keep fixed sections (§1/§2/§8/§9) in order.

### 6. Deliver a short chat summary

Report: file path, the key conclusion/recommendation, top reasons, main tradeoff or risk, source
count by source class, and any access limitations. If live browsing was unavailable or forbidden,
do not present the result as researched — explain the limitation and offer an offline-only draft.

**Output:** `docs/research/YYYY-MM-DD-<slug>.md` (general) / `docs/research/market.md` (market) / `docs/research/competitor.md` (tech-selection) — cited research artifact, archived cumulatively.

## Verify

- The `.md` file exists and contains no unresolved placeholders (`TBD`, `[标题]`, `https://example.com`, `github.com/org/repo`).
- Every key conclusion, recommendation, comparison point, and date-sensitive claim has an inline citation.
- Source appendix lists access dates and access limitations.
- The mode was chosen via the criteria table, not guessed; if the ask hit two or more modes, the user was asked to pick.
- Any negative claim ("未发布/不存在/尚未开源/无官方实现") carries a GitHub falsification record (search term, org, result) or an `UNVERIFIED:` label — never a bare secondary-source assertion.
- For any tech/framework/org topic, GitHub source evidence is present regardless of mode.
- For all modes: §1 TL;DR is conclusion-first (not process/method); §2 核心认知 states one main thread in a findable sentence and includes ≥1 decision flowchart; §8 避坑清单 has numbered negative claims each carrying evidence or a falsification trail; §9 源附录与核查记录 has 9.2 负面断言核查记录 + 9.3 UNVERIFIED + 9.4 访问限制与缺口 subsections.
- For general: 9-section conclusion-first structure; ≥3 mermaid (≥1 decision flowchart in §2), each serving information.
- For tech-selection: GitHub repo evidence + official docs present; stars alone did not drive the recommendation.
- For market: all numbers sourced or labeled estimates; old data flagged; recommendation follows from evidence.
- Final reply states: file path, source count, access limitations.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline for every skill (surface assumptions, verify don't assume, push back).
- [${CLAUDE_PLUGIN_ROOT}/references/product-principles.md](${CLAUDE_PLUGIN_ROOT}/references/product-principles.md) — product discipline (the real competitor is the current workaround). Linked by market + tech-selection modes.
- [references/report-spine.md](references/report-spine.md) — shared conclusion-first 9-section spine (TL;DR → 核心认知 → 主体 → 避坑 → 源附录与核查记录), main-thread rule, mermaid rules, shared skeleton.
- [references/general-mode.md](references/general-mode.md) — general mode: 9-section conclusion-first template, fan-out source strategy, mermaid/glossary patterns.
- [references/market-mode.md](references/market-mode.md) — market mode: 4 sub-modes (investor/competitive/sizing/tech-vendor), 9-section conclusion-first template, market frameworks.
- [references/tech-selection-mode.md](references/tech-selection-mode.md) — tech-selection mode: GitHub-first P0-P3 source priority, 9-section conclusion-first template, selection rubric.
- [references/web-tool-fallback.md](references/web-tool-fallback.md) — when a fetch tool is blocked or quota-exhausted: tiered fallback by quota dependency (GitHub → indexed docs → scrape → discovery), orthogonal to page-level retries.
- [references/pressure-scenarios.md](references/pressure-scenarios.md) — failure-mode pressure tests for this skill.
