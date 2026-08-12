---
name: image-to-code
description: image-first frontend pipeline — generate design reference images, analyze them deeply, then implement code to match. Triggers on "image to code", "设计图转代码", "图片实现", "从设计图实现".
---

# Image to Code

For visually important web work, generate the design reference images yourself first, deeply
analyze them, then implement frontend code that faithfully matches. The images are the primary
visual source of truth; the code is the translation layer. Do not start with freeform coding when
image generation is available.

## When to use

- Hero sections, landing pages, marketing sites, product pages, portfolio sites — visually important web tasks
- Multi-section website concepts where image-first beats code-first
- Redesigns where visual quality matters heavily
- Requests described mainly in visual terms ("beautiful hero", "premium landing page", "creative website")
- Triggers on "image to code", "设计图转代码", "图片实现", "从设计图实现"

**Not for:** pure code implementation without image reference (use `frontend-design`); brand identity image generation (use `brandkit`); web/mobile screen reference images only, without code (use `imagegen-web`/`imagegen-mobile`).

**Tool note:** use an available image-generation tool — do not bind to a specific product.

## Steps

### 1. Plan sections and visual direction

Infer the section count from the request. Pick a coherent visual combination and commit to it
consistently — do not mash everything into chaos.

- Load [${CLAUDE_PLUGIN_ROOT}/skills/03-design/frontend-design/references/visual-direction.md](${CLAUDE_PLUGIN_ROOT}/skills/03-design/frontend-design/references/visual-direction.md) for the combinatorial variation engine (9 axes: theme paradigm, background, typography, hero architecture, section system, signature components, motion-implied, narrative spine, second-read moment), hero-scale mapping, and the anti-slop ban list. The narrative-spine and second-read axes are optional for image-to-code.
- Default section packs if unspecified: 4-section (hero, features, social proof, CTA); 8-section (hero, trust bar, features, product showcase, benefits, testimonials, pricing, CTA); 12-section (adds workflow, metrics, FAQ, footer).

### 2. Generate one large image per section

Use an available image-generation tool. Never compress many sections into one tiny unreadable
board — text becomes too small to analyze, spacing collapses, extraction quality drops.

- One section requested → one image. N sections → N section images.
- It is better to generate too many clear images than too few compressed ones.
- Default section packs if unspecified: 4-section (hero, features, social proof, CTA); 8-section (hero, trust bar, features, product showcase, benefits, testimonials, pricing, CTA); 12-section (adds workflow, metrics, FAQ, footer).
- Keep the hero especially clean: 1-3 line headline, single strong focal point, generous negative space. No pills, badges, tiny logos, or pseudo-system labels cluttering the first viewport. The first screen must stay readable on a small laptop.

### 3. Regenerate unclear sections as fresh standalone images

Never crop, slice, or zoom into a previously generated image for a section or detail view —
cropping destroys spacing accuracy, type-scale relationships, and layout proportions.

- Generate a fresh image preserving the same design language (palette, typography mood, button style, radius logic) but optimized for readability.
- Add extraction-oriented detail images when text or components are too small: closer hero render, pricing card detail, navbar treatment, testimonial close-up.
- If a section is still unclear after one regeneration, generate another — do not guess.

### 4. Deeply analyze every image

Treat the generated images as a design specification, not vibes. For each section image, extract:

- **Text:** headline, subheadline, CTA labels, section titles, navbar labels, pricing labels, testimonial names
- **Typography:** size/weight relationships, display vs body contrast, line count, tracking feel, serif/sans behavior
- **Spacing:** headline-to-subheadline distance, text-to-button distance, card gaps, section top/bottom spacing, side gutters, card padding
- **Buttons/components:** size, shape, radius, fill vs outline, icon usage, primary/secondary hierarchy, card structure, dividers, shadows
- **Colors:** background, panel colors, accents, button fills, text hierarchy, border logic, shadow mood, image tint
- **Layout:** grid logic, alignment, section ordering, density, visual rhythm, repeated motifs

If details are unclear, generate another image before coding. Do not fill ambiguity with generic defaults.

### 5. Implement frontend faithfully

Translate the analyzed design into real frontend code. Avoid design drift — the coded result must
feel like the same website as the generated references.

- Preserve layout logic, spacing rhythm, section ordering, text/image balance, typography mood, and component style.
- Do not simplify into default templates, compress generous spacing, or replace distinctive sections with generic rows.
- Avoid nested-box layouts: no cards-in-cards-in-cards, no giant rounded wrappers around every section, no dashboard-like compartment stacking. Use boxes only when they have a clear purpose.
- Reduce micro-UI clutter: remove pseudo-system markers, fake control labels, decorative code-like tags, filler chips, and fake dashboard jargon.
- Install missing packages as needed (`npm install <pkg>` / `pip install <pkg>` / equivalent).
- For color formula, typography pairing, and interaction states, follow `frontend-design`.

**Output:** frontend code (HTML/CSS/JS, React, Vue, Svelte, etc.) matching the generated reference images, plus the reference images themselves.

## Verify

- [ ] Image-first order followed: reference images generated before any code
- [ ] One large readable image per section — no compressed multi-section boards
- [ ] Enough images generated — no lazy under-generation
- [ ] No cropped/sliced old images — fresh standalone regenerations for detail views
- [ ] Deep analysis completed: text, typography, spacing, buttons, colors, layout all extracted
- [ ] Hero is clean: 1-3 line headline, single focal point, breathable negative space, readable on a small laptop
- [ ] No cards-in-cards-in-cards or giant rounded wrappers around every section
- [ ] No micro-UI clutter: pseudo-system labels, filler pills, fake dashboard jargon removed
- [ ] No design drift: implemented code matches the generated references (layout, spacing, typography, components)
- [ ] Color/typography/interaction states follow `frontend-design` conventions
- [ ] No AI-slop tells: purple/blue gradients, centered dark hero clichés, repeated left-text/right-image blocks, generic card spam

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, verify don't assume, surgical changes)
- [${CLAUDE_PLUGIN_ROOT}/references/design-principles.md](${CLAUDE_PLUGIN_ROOT}/references/design-principles.md) — design discipline (CRAP, hierarchy before decoration, design every state, accessibility non-optional)
- [${CLAUDE_PLUGIN_ROOT}/skills/03-design/frontend-design/references/visual-direction.md](${CLAUDE_PLUGIN_ROOT}/skills/03-design/frontend-design/references/visual-direction.md) — shared web variation engine (9 axes, hero scale, composition anchors, anti-slop)
