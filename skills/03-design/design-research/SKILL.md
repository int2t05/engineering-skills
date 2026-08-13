---
name: design-research
description: Use when retrieving real design references — landing pages, user flows, visual styles — from free public galleries to ground imagegen or frontend-design work in what real products actually do. Triggers on "design references", "real UI references", "find design inspiration", "设计参考", "真实设计参考", "找设计灵感", "设计灵感". Not for generating design images (use imagegen) or writing frontend code (use frontend-design).
---

# Design Research

Retrieve real, published design references from free public galleries and curate them into a cited
reference board that grounds downstream design work in what real products actually do — not in
memory or generic AI patterns. Output is a reference board (URLs + analysis), never fabricated
screenshots.

## When to use

- Before `imagegen` or `frontend-design`, when the brief would benefit from real-market reference (how do fintech landing pages actually handle hero? how do SaaS pricing sections read?)
- Researching a design pattern across real products (onboarding flows, empty states, pricing layouts)
- Grounding a style direction in what the market already ships, not internal catalogs alone
- Triggers on "design references", "real UI references", "find design inspiration", "设计参考", "真实设计参考", "找设计灵感", "设计灵感"

**Not for:** generating design images (use `imagegen`); writing frontend code (use `frontend-design`); image-first code pipeline (use `image-to-code`); cited-text market/tech research (use `research` market/tech-selection modes).

## Steps

### 1. Frame the brief

Extract four dimensions that route the search:

- **Domain** — fintech, SaaS, AI, e-commerce, health, etc.
- **Surface** — landing page / user flow / visual style. This decides the source, not platform.
- **Intent** — feeding `imagegen` (art-direction inspiration), `frontend-design` (style grounding), or pattern research (standalone).
- **Scope** — how many references are enough (default 5-8; state the target).

### 2. Route to source

Match the surface to the source that covers it. Don't hit every source — route by surface. Full
matrix and per-source details in [references/sources.md](references/sources.md).

- Landing page + industry → Lapa Ninja (Finance/SaaS/AI categories) or Craftwork public pages (Finance/E-commerce/AI)
- User flow / onboarding → Pageflows (web + mobile flows by type)
- Visual style / aesthetic → Godly/Recent (discipline: Web/Interface/Branding) or Land-book (type: E-commerce/Apps & Software)

**Capability boundary (read before promising):** free public sources cover landing pages and user
flows well. iOS per-screen deep retrieval (Login/Wallet/Paywall/Settings tagged by screen type) is
weak — that is a paid-source capability. WebFetch returns markdown (image URLs + visible text),
not the screenshot pixels, so visual analysis is text-descriptive, not pixel-level. State this
limit when the brief demands pixel precision.

### 3. Build the query

For public galleries, a "query" is a category URL path + a search term, not an API call. Build the
specific URL for the source's category that matches the brief's domain.

- Lapa Ninja: `lapa.ninja/category/finance/`, `lapa.ninja/category/saas/`
- Pageflows: search by flow type (onboarding, checkout, signup)
- Godly/Recent: `recent.design/?type=interface` filtered by discipline
- Craftwork: `craftwork.design/curated/websites` filtered by Money/Tech categories

Per-goal example queries in [references/query-patterns.md](references/query-patterns.md).

### 4. Retrieve via WebFetch

WebFetch the category/search page. Extract, per result: the source URL (deep link to the page),
the image URL (CDN-hosted preview), the title, and any visible metadata (industry, type, tags).
Record the source URL for every reference — it is the citation.

- Fetch one category page at a time; extract 10-15 candidates, then curate down in Step 6.
- If a source page is JS-heavy and returns little content, note it and try the next source rather than fighting the renderer.

### 5. Analyze each reference

From the page's visible information, extract the design axes downstream skills need — as
**text description**, not pixel measurement (WebFetch gives markdown, not the image):

- Layout rhythm (section order, density, pacing)
- Grid (columns, alignment, asymmetry)
- Spacing (generous vs tight, breathing room)
- Type scale (display vs body contrast, weight hierarchy)
- Visual density (minimal vs rich, layering)
- Accent-color logic (where the one accent lands, how it recurs)

Full analysis lenses (8 dimensions, adapted from established UX-research frameworks) and output
templates in [references/analysis-framework.md](references/analysis-framework.md).

### 6. Curate + synthesize

Cross-reference the candidates, cluster patterns (e.g. "fintech heroes lead with trust signal, not
feature list"), pick the 5-8 strongest, and write `docs/design/references.md`. Each entry pairs:

- Source URL (markdown link) + image URL
- The extracted analysis (axes above)
- Which downstream skill it feeds (`imagegen` art direction / `frontend-design` style / `image-to-code` section plan)

**Never fabricate screenshots or URLs.** Every entry must trace to a real fetched page. If a
candidate couldn't be fetched, drop it.

### 7. Hand off

End the reference board with the load instruction: "Load this file in `imagegen` Step 4 (Match
references), `frontend-design` Step 2 (Pick a style), or `image-to-code` Step 1 (Plan sections)."

**Output:** `docs/design/references.md` — curated reference board (source URL + image URL + text analysis + downstream-skill tag), feeding imagegen/frontend-design/image-to-code.

## Verify

- [ ] Reference count meets the stated target (≥5)
- [ ] Every entry has a real source URL (fetched, not invented) + image URL + analysis
- [ ] No fabricated screenshots or URLs — each entry traces to a fetched page
- [ ] `docs/design/references.md` written to disk with the load instruction
- [ ] Capability boundary stated when the brief demanded pixel precision or iOS per-screen depth

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, verify don't assume, push back when warranted)
- [${CLAUDE_PLUGIN_ROOT}/references/design-principles.md](${CLAUDE_PLUGIN_ROOT}/references/design-principles.md) — design discipline (CRAP, hierarchy before decoration, consistency from systems)
- [references/sources.md](references/sources.md) — 5 free public sources (coverage, category URL patterns, WebFetch feasibility) + routing matrix + capability boundary (iOS per-screen, markdown-not-pixels)
- [references/query-patterns.md](references/query-patterns.md) — brief → category URL path + search term, with per-goal example queries (fintech landing, SaaS hero, onboarding flow, error/empty states)
- [references/analysis-framework.md](references/analysis-framework.md) — extraction axes (layout/grid/spacing/type/density/accent, text-descriptive) + 8 analysis lenses + 3 output frameworks (Reference Board / Competitive Comparison / Decision Log)
