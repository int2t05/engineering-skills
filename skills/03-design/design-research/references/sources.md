# Design Reference Sources

The 5 free, public, no-login sources `design-research` retrieves from. All are WebFetch-friendly
(server-rendered or cleanly extractable). **No paid MCP, no API key, no login.**

## Capability boundary (read first)

Two limits to state honestly when the brief demands more:

1. **Markdown, not pixels.** WebFetch returns a page's markdown (image URLs + visible text), not
   the screenshot itself. Visual analysis is **text-descriptive** — "generous spacing, single
   accent on CTA, display type ~3× body" — not pixel measurement. For pixel-level analysis (exact
   spacing values, color hex, component structure), the user must open the URL and look, or feed
   the image URL to an image-capable step (e.g. `imagegen` generation).

2. **iOS per-screen depth is weak.** Free sources cover **landing pages** and **user flows** well.
   Deep iOS per-screen retrieval (Login / Wallet / Paywall / Settings tagged individually by screen
   type, 600k+ screens) is a paid-source capability (Mobbin). Pageflows covers some mobile flows,
   but not per-screen tagging. If the brief is "show me 20 real iOS wallet screens," free sources
   cannot fully satisfy — say so, deliver what Pageflows' mobile flows offer, and flag the gap.

These limits follow the engineering principle: surface tradeoffs, don't fake capability.

## The 5 sources

### 1. Lapa Ninja — landing pages, industry-filtered

- **URL:** `lapa.ninja`
- **Coverage:** 7,300+ landing page designs, 15,000+ full-page screenshots
- **Industry categories (URL paths):** `/category/finance/`, `/category/saas/`, `/category/artificial-intelligence/`, `/category/technology/`, `/category/ecommerce/`, `/category/health-fitness/`, `/category/education/`, `/category/app/`, `/category/product/`, + 20 more
- **WebFetch:** High. `robots: index, follow`. Server-rendered, clean markdown. Images on `cdn.lapa.ninja/assets/...` (public).
- **Best for:** "fintech landing page", "SaaS landing page", industry-targeted landing inspiration.
- **Also has:** OG images section, Webflow/Framer templates, learn/books sections (skip for reference retrieval).

### 2. Pageflows — user flows and onboarding

- **URL:** `pageflows.com`
- **Coverage:** User flows and onboarding sequences (web + mobile), organized by flow type
- **Categories:** onboarding, signup, checkout, activation, cancellation, etc.
- **WebFetch:** High. Public, no login for flow browsing. Each flow is a sequence of screens with descriptions.
- **Best for:** "how do apps handle onboarding", "checkout flow patterns", "signup sequence". The only free source covering multi-step flows (the "onboarding" half of a brief like "fintech onboarding").
- **Mobile coverage:** partial — some mobile flows, but not per-screen tagged like a paid iOS library.

### 3. Godly / Recent — visual style and aesthetic

- **URL:** `recent.design` (was `godly.website`, 302-redirects)
- **Coverage:** Curated design references, discipline-based
- **Categories (discipline, not industry):** Web, Interface, Branding, Product, Typography, Motion, Illustration, 3D, Editorial, Print, Packaging
- **WebFetch:** High. Server-rendered, clean markdown. Images on `cdn.recent.design/items/.../poster/1200.webp`.
- **Best for:** aesthetic/style direction, "dark mode SaaS", "editorial typography". **Weak on industry targeting** — no "fintech" filter; infer industry from post titles/slugs.
- **Limit:** discipline categories don't map to industries; use as style supplement, not primary industry filter.

### 4. Land-book — landing page gallery

- **URL:** `land-book.com`
- **Coverage:** Landing page gallery, type-based
- **Categories:** Landing Pages, Portfolios, Agencies, E-commerce, Apps & Software, Corporate, Personal
- **WebFetch:** Medium-High. Server-rendered (121KB markdown). Image-heavy; target category URLs directly (`/category/...`).
- **Best for:** broad landing-page browsing, "apps & software" category. Industry filtering weaker than Lapa Ninja.

### 5. Craftwork / Curated — public industry-filtered pages

- **URL:** `craftwork.design/curated/websites` (was `curated.design`)
- **Coverage:** Curated websites, industry + section views
- **Categories (industry):** Money (E-commerce, Finance), Tech (Web3, AI), Apps (Productivity, Web Apps, Mobile Apps), Services, Tools
- **WebFetch:** High. Next.js server-rendered, public CDN images on `marketstorage.b-cdn.net`. Has a "Sections" view (design-pattern sections: Hero/Pricing/Footer).
- **Best for:** industry-filtered landing pages (Finance/E-commerce), section-level references (Hero patterns, Pricing patterns).
- **Note:** Craftwork ships a paid MCP, but the **public gallery pages are free and WebFetch-friendly** — use the public pages, not the MCP.

## Routing matrix

| Brief surface | Primary source | Secondary | Why |
|---|---|---|---|
| Landing page + industry (fintech/SaaS/AI) | Lapa Ninja (category) | Craftwork (industry) | Both have Finance/SaaS categories; Lapa Ninja has more pages |
| User flow / onboarding / checkout | Pageflows | — | Only free source covering multi-step flows |
| Visual style / aesthetic direction | Godly/Recent | Land-book | Discipline-filtered style curation |
| Section pattern (Hero/Pricing/Footer) | Craftwork (Sections view) | Lapa Ninja | Craftwork's section view is purpose-built for this |
| iOS per-screen (Login/Wallet/Paywall) | Pageflows (mobile flows, partial) | — | **Gap** — no free per-screen library; flag the limit |

## What is NOT here (and why)

- **Mobbin** — paid ($10/mo for MCP/API). Has the richest iOS screen library (621k+ screens), but excluded by the free-source constraint. If the user later allows paid sources, Mobbin's official MCP (`api.mobbin.com/mcp`) is the sanctioned path and would fill the iOS per-screen gap.
- **Dribbble / Behance** — ToS explicitly prohibits scraping; Dribbble's API is publishing-only (no search); Behance's API is dead (404). Not usable.
- **Savee** — no API, fully login-walled, ToS prohibits automated access, no structured taxonomy. Dead end.
- **Awwwards** — reCAPTCHA-protected, no industry filter, bot-hostile. Poor fit for automated retrieval.
- **SiteInspire** — domain repurposed (no longer a design gallery). Dead.

Do not add these to the retrieval flow. If a user asks why, point to the capability boundary above and the research record.
