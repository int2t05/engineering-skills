# Anti-Tells — Forbidden AI Patterns

The signatures that make LLM-generated UI look generic. Avoid these unless the brief
explicitly asks for them. This reference consolidates the forbidden patterns and the
pre-flight check that catches them before delivery.

## Contents

- [When to load this](#when-to-load-this)
- [Visual & CSS tells](#visual--css-tells)
- [Typography tells](#typography-tells)
- [Layout & spacing tells](#layout--spacing-tells)
- [Content & data tells ("Jane Doe" effect)](#content--data-tells-jane-doe-effect)
- [External resources & component tells](#external-resources--component-tells)
- [Production-test tells (hard bans)](#production-test-tells-hard-bans)
- [Pre-flight check](#pre-flight-check)

## When to load this

Load during the Verify phase of `frontend-design` — run the pre-flight check before
delivering any UI. Also load when reviewing existing UI for "AI slop" remediation.

## Visual & CSS tells

- **No purple/blue AI gradients** — the default "AI slop" look (purple-to-indigo on white/dark). Choose a deliberate palette direction instead.
- **No glassmorphism without reason** — floating translucent cards over blurred blobs is the generic AI default; earn it with a brief justification.
- **No neon / outer glows** by default. Use inner borders or subtle tinted shadows.
- **No pure black (`#000000`)** — off-black, zinc-950, or charcoal.
- **No oversaturated accents** — desaturate to blend with neutrals.
- **No excessive gradient text** for large headers.
- **No custom mouse cursors** — outdated, accessibility-hostile, performance-hostile.

## Typography tells

- **Avoid Inter as the default.** See `font-pairings.md` for distinctive alternatives.
  The "Inter + slate-900" combo is the canonical LLM-default look — avoid it as a bundle.
  An override path exists, but the default must be a deliberate choice, not inertia.
- **No oversized H1s** that just scream. Control hierarchy with weight + color, not raw
  scale.
- **Serif constraints** — serif for editorial / luxury / publication. Not for dashboards
  or B2B SaaS.

## Layout & spacing tells

- **No mathematically perfect** padding and margins that feel robotic — break the grid
  deliberately when the dial calls for variance.
- **No 3-column equal feature cards.** The generic "three identical cards horizontally"
  feature row is banned. Use 2-column zig-zag, asymmetric grid, scroll-pinned, or
  horizontal-scroll alternatives.

## Content & data tells ("Jane Doe" effect)

- **No generic names** — "John Doe", "Sarah Chan", "Jack Su" → use creative, realistic,
  locale-appropriate names.
- **No generic avatars** — no SVG "egg" or generic user icons → use believable photo
  placeholders or specific styling.
- **No fake-perfect numbers** — avoid `99.99%`, `50%`, `1234567`. Use organic, messy
  data (`47.2%`, `+1 (312) 847-1928`).
- **No startup-slop brand names** — "Acme", "Nexus", "SmartFlow", "Cloudly", "Flowbit",
  "Quantumly", "NovaCore", "Quantix", "VeloPay" → invent contextual, premium names that
  sound real. This is the canonical list shared across `frontend-design`, `imagegen`, and
  `image-to-code`.
- **No filler verbs** — "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize",
  "Transformative", "Unlock", "Smarter" → concrete verbs only.

## External resources & component tells

- **No hand-rolled SVG icons.** Use Phosphor / HugeIcons / Radix / Tabler. Lucide on
  explicit request only.
- **No div-based fake screenshots.** Never build a fake product UI out of `<div>`
  rectangles to simulate a screenshot. Use real images, generated images, or skip the
  preview.
- **No broken Unsplash links.** Use `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`,
  generated photo placeholders, or actual assets.
- **shadcn/ui customization** — allowed, but NEVER in default state. Customize radii,
  colors, shadows, typography to the project aesthetic.

## Production-test tells (hard bans)

These patterns came out of real LLM-generated landing-page tests. Treat as hard bans
unless the brief explicitly calls for one.

**Hero & top-of-page**
- No version labels in the hero (`V0.6`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`) —
  only acceptable when the brief is explicitly about a product launch.
- No "Brand · No. 01"-style sub-eyebrows.

**Section numbering & micro-labels**
- No section-number eyebrows (`00 / INDEX`, `001 · Capabilities`, `06 · how it works`).
  Eyebrows should name the topic in plain language, not enumerate.
- No `01 / 4`-style pagination on images or bento tiles.

**Decorative noise**
- No scroll cues (`Scroll`, `↓ scroll`, `Scroll to explore`).
- No decorative dots (zero by default, only for real semantic state).
- No decoration text strips at hero bottom (`BRAND. MOTION. SPATIAL.`).
- No floating top-right sub-text in section headings.
- No photo-credit captions as decoration.
- No version footers (`v1.4.2`, `Build 0048`) on marketing pages.

## Pre-flight check

Run this matrix before outputting code. This is the last filter — not optional. If any
box fails, the output is not done.

**Inference & system**
- [ ] Brief inference declared (one-liner design read)?
- [ ] Dial values explicit and reasoned from the brief?
- [ ] Design system chosen or aesthetic labeled honestly?
- [ ] One design system per project (no mixing)?

**Consistency locks**
- [ ] Page theme lock — one theme (light/dark/auto) for the whole page, no mid-page flips?
- [ ] Color consistency lock — one accent used identically across all sections?
- [ ] Shape consistency lock — one corner-radius system applied consistently?
- [ ] Button contrast check — every CTA readable against its background (WCAG AA 4.5:1)?
- [ ] No CTA button wraps to 2+ lines at desktop?

**Hero discipline**
- [ ] Headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines?
- [ ] CTA visible without scroll?
- [ ] Hero top padding max `pt-24` at desktop — content does not float halfway down?
- [ ] Max 4 text elements in hero (eyebrow OR brand strip, headline, subtext, CTAs)?
- [ ] No version labels in hero unless the brief is a launch?

**Layout anti-repetition**
- [ ] No 3+ consecutive sections with the same image+text-split layout?
- [ ] No two sections share the same layout family (≥4 different families across 8 sections)?
- [ ] Eyebrow count ≤ ceil(sectionCount / 3)?
- [ ] No "left big headline + right small explainer" split-header pattern?

**Content & assets**
- [ ] Real images used (generated, Picsum-seed, or explicit placeholder slots) — no
      div-based fake screenshots, no hand-rolled decorative SVGs?
- [ ] No two CTAs with the same intent on the same page?
- [ ] Logo wall uses real SVG logos, not plain text wordmarks?
- [ ] Bento has rhythm AND exact cell count (N items → N cells, no empty cells)?
- [ ] Quotes ≤ 3 lines, attribution clean?

**Motion & performance**
- [ ] Every animation justifiable in one sentence (hierarchy / storytelling / feedback)?
- [ ] No `window.addEventListener('scroll')` — using Motion `useScroll()` / ScrollTrigger /
      IntersectionObserver / CSS scroll-driven only?
- [ ] Reduced motion wrapped for everything with `MOTION_INTENSITY > 3`?
- [ ] Core Web Vitals plausibly hit (LCP < 2.5s, INP < 200ms, CLS < 0.1)?
- [ ] Viewport stability: `min-h-[100dvh]`, never `h-screen`?

**Final sweep**
- [ ] No AI tells from the lists above (Inter default, AI-purple, three-equal cards,
      Jane Doe, Acme, filler verbs)?
- [ ] Empty / loading / error states provided?
- [ ] Icons from an allowed library only — no hand-rolled SVG paths?
- [ ] Mobile collapse explicit (`w-full`, `px-4`, `max-w-7xl mx-auto`)?

If a single checkbox cannot be honestly ticked, the page is not done. Fix it before
delivering.
