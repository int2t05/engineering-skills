---
name: imagegen-web
description: Website design reference image generation — one horizontal image per section, premium art direction for landing pages and marketing sites that developers or coding models can recreate. Triggers on "web design image", "website mockup", "landing page image", "section image", "网站设计图", "网页参考图", "落地页配图".
---

# Imagegen Web

Generate premium website design reference images — one horizontal image per section — that feel
art-directed, premium, and implementation-friendly, not generic AI slop. Output is images only,
never code.

## When to use

- Generating website design reference images for developers or coding models to recreate
- Landing pages, marketing sites, product comps, portfolio concepts
- Need premium art direction: composition variety, hero scale control, narrative spine
- Triggers on "web design image", "website mockup", "landing page image", "section image", "网站设计图", "网页参考图", "落地页配图"

**Not for:** frontend code (use `frontend-design`); mobile screens (use `imagegen-mobile`); brand identity (use `brandkit`); image-to-code pipeline (use `image-to-code`).

## Steps

### 1. Lock the section count — one image per section

The hard rule: **one horizontal image per section, always.** Never combine multiple sections into
one frame; never return a single tall slice of the whole page; never replace several sections with
one collage. This overrides any model default that collapses output.

- 1 section → 1 image; 8 sections → 8 images; 12 sections → 12 images.
- If the count is ambiguous, default high: "hero" → 1; "landing page" → 6; "full website" / "marketing site" → 8; "product page" / "portfolio" → 6.
- Announce the count out loud: "Generating N horizontal images, one per section."
- Format: horizontal — 16:9 or 21:9 for heroes, 16:10 for narrower content sections.
- If only one image can render per call, generate them sequentially in the same response, labeled "Section X of N: <name>", until the full set is delivered. Do not stop early.

### 2. Map the brief to a direction

Read the brief and bias the picks to match — never force a recipe that contradicts it. Then pick
one **Hero Scale** for the whole site and execute it decisively.

- **Minimalist / clean / swiss / typography-only** → Mini Minimalist hero; solid surfaces; stacked center; skip full-bleed.
- **Editorial / magazine / art-directed** → Mid or Giant hero; editorial side-image; off-grid offset; strong type contrast.
- **Cinematic / atmospheric / luxury / bold** → Giant hero; full-bleed image with tonal overlay; bottom-left or centered-low composition.
- **SaaS / product / dashboard / fintech / infra** → Mid Editorial hero; solid + inline asset; clear product framing; higher implementation clarity.
- **Agency / creative studio / portfolio** → Giant or Mini (decisive, not in-between); vary backgrounds boldly; off-grid poster-like.
- **E-commerce / shop** → Mid Editorial, product-led; full-bleed product photo; unmistakable CTAs.
- **Silent brief** → use defaults with confident background variety; pick one hero scale decisively.

Hero Scale: **Giant Statement** (massive type, dominant first viewport) / **Mid Editorial** (balanced
type/image, cinematic but not screen-filling) / **Mini Minimalist** (tiny logo + short statement +
thin CTA, lots of negative space — confident restraint, not weak).

### 3. Run the combinatorial variation engine

Pick one option from each category and commit to it consistently — don't mash everything into
chaos. These are visual-direction cues the generated image should imply, not code instructions.

- **Theme paradigm**: pristine light / deep dark / bold studio solid / quiet premium neutral
- **Background character**: subtle grid / pure solid with ambient gradient / full-bleed cinematic imagery / quiet textured material
- **Typography character**: clean grotesk / refined grotesk / expressive display / compressed statement / editorial serif+sans / Swiss rational sans
- **Hero architecture**: cinematic centered minimalist / asymmetric split / floating polaroid scatter / inline typography behemoth / editorial offset / massive image-first
- **Section system**: strict bento / alternating editorial / poster stacked / gallery cadence / Swiss grid / asymmetric marketing flow
- **Signature components** (pick exactly 4): diagonal masonry / cascading card deck / hover-accordion slice / gapless bento / brand marquee / polaroid arc / vertical rhythm lines / off-grid editorial / product UI panel stack / split testimonial wall / oversized metrics strip / layered crop frames
- **Motion-implied** (pick exactly 2): scrubbing text reveal / pinned narrative / staggered float-up / parallax drift / accordion expansion / cinematic fade-through
- **Narrative spine** (pick 1): artifact / journey / precision instrument / living system / stage spotlight / archive dossier
- **Second-read moment** (pick exactly 1): asymmetric bleed / oversized punctuation or numeral / single material switch / vertical side-rail note / macro brand-color crop

### 4. Vary composition per section — break the hero default

**The left-text / right-image hero is the most overused AI pattern.** It is allowed, but must not
be the first instinct. Before reaching for it, prefer: centered statement, bottom-left over image,
bottom-right CTA cluster, top-left lead, stacked center, image-as-canvas, off-grid editorial,
right-text / left-image (inverted), or mini minimalist.

Per section, pick a **composition anchor** and a **background mode**. Across the site:
- At least 3 different anchors must appear; same anchor must not repeat more than 2 sections in a row.
- Same background mode must not repeat more than 3 sections in a row.
- For non-minimalist briefs: include at least one full-bleed (or duotone / atmospheric) background and at least one mini minimalist section.

Background mode menu (per section): solid + inline asset / subtle texture / full-bleed image with
tonal overlay / editorial side-image / image-as-canvas / flat color block + detail crop / cinematic
tonal gradient / atmospheric photo grade / duotone / soft radial vignette + product / micro-noise
gradient / color-blocked diptych.

CTA variation: classic pill / outline ghost / underlined inline link / banner full-width / oversized
headline + tiny CTA hint / CTA as caption. Vary CTA style at least once; the primary action stays
unmistakable.

### 5. Apply hero minimalism and graphic restraint

- Strong opening scene; clean composition; do not overcrowd the first viewport.
- Headline reads like 5-10 strong words, not a paragraph — short and powerful.
- Prefer medium/light elegance, tight tracking, controlled line count, strong scale contrast.
- Avoid: random extra-bold shouting, gradient text as a lazy premium effect, 6-line startup headings.
- No giant meaningless outline numbers, cheap SVG filler, generic AI blobs, or random orb clutter.
- Use typography, image crops, real layout tension, premium materials, and strong framing instead.

### 6. Enforce continuity, creativity, and anti-slop

**Continuity across all per-section images** (one brand world): same palette and accent logic, same
type family and scale, same CTA family, same radius language, same image treatment, same tonal voice.
A viewer scrolling through all frames must read them as one site. Variation is allowed only in
composition anchor, background mode, section size, and which second-read moment appears.

**Creativity escalation**: push beyond generic SaaS. Actively increase at least 3 of: composition,
typography distinctiveness, scale contrast, hero concept memorability, image treatment, section
rhythm, framing/cropping, visual tension, layout structure. Creativity must feel intentional, not
chaotic.

**Section rhythm**: mix large art-directed sections, mini minimalist sections, and medium editorial
blocks deliberately. Keep spacing generous and fairly even — the page must breathe. Separate denser
sections with calmer ones.

**Anti-slop** (ban unless explicitly requested):
- Layout: endless centered sections, cloned left-text/right-image blocks, identical card rows, lifeless symmetry.
- Visual: default purple/blue AI gradients, floating spheres/blobs, glassmorphism without reason, glowing edges.
- Content: "unleash / elevate / revolutionize / next-gen / seamless / transformative platform"; fake brands (Acme, Nexus, Flowbit, Quantumly, NovaCore).
- Data: three identical stat columns, fake dashboards with pointless charts, infinity logo marquees.

## Verify

- [ ] **Image count equals section count** — one horizontal image per section, never fewer, never combined
- [ ] Hero composition is not a reflexive left-text / right-image default (or there is a clear reason it is the strongest fit)
- [ ] Hero scale (giant / mid / mini) chosen decisively and executed cleanly; headline is 5-10 strong words
- [ ] Composition anchors vary across sections (≥3 distinct; no anchor repeats >2 in a row)
- [ ] Background modes vary (no mode repeats >3 in a row); at least one full-bleed for non-minimalist briefs
- [ ] One consistent palette, type family, CTA family, radius, and image treatment across all images
- [ ] Exactly one disciplined "second-read" moment placed deliberately
- [ ] Creativity escalation visible (≥3 dimensions pushed beyond generic SaaS)
- [ ] Section rhythm mixes large / mini / medium; spacing is generous and fairly even
- [ ] No AI slop: no purple-blue gradients, no floating blobs, no cloned blocks, no fake KPI columns, no generic copy or fake brands
- [ ] Each image is horizontal and clearly one section only; a developer could code from it

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
