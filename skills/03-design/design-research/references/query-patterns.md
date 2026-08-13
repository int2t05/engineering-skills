# Query Patterns

How to translate a design brief into a retrieval plan for the 5 free public sources. Public
galleries have no search API — a "query" is a **category URL path + a search term**, fetched via
WebFetch. Build the specific URL that matches the brief's domain and surface.

## The translation

```
brief → domain + surface → source → category URL path → WebFetch → extract candidates
```

Four parts:

1. **Domain** → pick the source's matching category (fintech → Finance, SaaS → SaaS, AI → Artificial Intelligence).
2. **Surface** → pick the source that covers it (landing → Lapa Ninja/Craftwork; flow → Pageflows; style → Godly).
3. **Category URL** → assemble the source's URL path for that category.
4. **Search term** → if the source supports on-site search, the term; else rely on the category page's listings.

## Per-source URL patterns

### Lapa Ninja (landing pages by industry)

| Domain | URL |
|---|---|
| Finance / fintech | `lapa.ninja/category/finance/` |
| SaaS | `lapa.ninja/category/saas/` |
| AI | `lapa.ninja/category/artificial-intelligence/` |
| E-commerce | `lapa.ninja/category/ecommerce/` |
| Health / fitness | `lapa.ninja/category/health-fitness/` |
| Education | `lapa.ninja/category/education/` |
| Tech / product | `lapa.ninja/category/technology/` or `/category/product/` |

Paginate with `?page=2` if the first page's candidates are thin.

### Pageflows (user flows by type)

No fixed URL pattern — browse `pageflows.com` by flow type. Fetch the flow-type listing page, then
individual flow pages. Flow types: onboarding, signup, checkout, activation, cancellation,
referral, empty-state, upgrade.

For a brief like "fintech onboarding", fetch the onboarding-flow listing and filter mentally for
fintech apps in the results (Pageflows titles name the app).

### Godly / Recent (style by discipline)

`recent.design/?type=interface` (or `?type=web`, `?type=product`). No industry filter — infer
industry from post titles/slugs after fetching. Use when the brief is about **style/aesthetic**,
not industry targeting.

### Craftwork (industry + section)

- Industry: `craftwork.design/curated/websites` → filter by Money (Finance/E-commerce) / Tech (AI) / Apps in the page UI. Fetch the filtered listing.
- Sections: `craftwork.design/curated/websites` → "Sections" view → Hero / Pricing / Footer / Features / CTA. Fetch the section-type page.

### Land-book (type-based)

`land-book.com/category/apps-software` or `/category/e-commerce` etc. Weaker industry mapping than
Lapa Ninja — use as secondary.

## Per-goal example queries

### "Fintech landing page, dark mode"

1. Surface = landing + industry → Lapa Ninja `/category/finance/`
2. WebFetch the page, extract candidates with "dark" in title/description or dark preview images
3. Secondary: Craftwork Money → Finance
4. Note: "dark mode" is a style filter Godly handles better — cross-check `recent.design/?type=web` for dark-mode fintech aesthetics

### "SaaS onboarding flow"

1. Surface = flow → Pageflows, onboarding-flow listing
2. Fetch the listing, filter for SaaS apps (titles name the product)
3. Extract each flow's screen sequence + descriptions
4. **iOS per-screen depth not available** — flag if the user wanted individual screen tags

### "How do SaaS pricing sections read?"

1. Surface = section pattern → Craftwork Sections view → Pricing
2. Fetch the pricing-section listing, extract 8-10 pricing-section references
3. Secondary: Lapa Ninja `/category/saas/`, extract pricing sections from full-page screenshots

### "Empty state patterns across apps"

1. Surface = flow/pattern → Pageflows, empty-state flow type
2. Fetch, extract empty-state screens + their handling pattern
3. This is where free sources are weakest (empty states are a per-screen concern) — deliver what's there, flag the gap

### "Editorial typography landing pages"

1. Surface = style → Godly/Recent `?type=web`, filter for editorial/typography discipline
2. Fetch, extract candidates with strong type contrast
3. Secondary: Lapa Ninja `/category/agency/` or `/category/studio/` (editorial-leaning categories)

## What makes a good query

- **Specific category, not homepage.** Fetch `lapa.ninja/category/finance/`, not `lapa.ninja` — the category page is pre-filtered.
- **One source at a time, routed by surface.** Don't fetch all 5 sources for every brief — route by the matrix in sources.md.
- **Extract 10-15, curate to 5-8.** Over-fetch candidates, then filter in the analysis step. A thin fetch (3 results) can't support pattern clustering.
- **Record the deep URL.** The candidate's link (e.g. `lapa.ninja/shot/revolut-onboarding`) is the citation — not the category page URL.

## What NOT to do

- Don't fabricate URLs or screenshots. If WebFetch returns nothing useful for a source, note it and move to the next — don't invent references.
- Don't try to scrape JS-heavy sources with headless browsers. WebFetch the server-rendered page; if it's too thin, skip the source.
- Don't query Dribbble/Behance/Savee — ToS-prohibited (see sources.md "What is NOT here").
