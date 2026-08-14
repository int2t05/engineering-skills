# Visual Direction

Shared depth reference for the `imagegen` (web mode) and `image-to-code` skills. The combinatorial
variation engine, hero-scale mapping, composition anchors, background-mode menu, CTA variation,
continuity rules, creativity escalation, and the anti-slop ban list. Both skills load this file
instead of maintaining separate inline copies of the same engine — eliminating the duplication where
`imagegen` web mode carried 9 axes and `image-to-code` carried a 7-axis subset.

## 1. The combinatorial variation engine

Pick one option from each axis and commit to it consistently across the whole set — don't mash
everything into chaos. These are visual-direction cues the generated image should *imply*, not code
instructions.

- **Theme paradigm**: pristine light / deep dark / bold studio solid / quiet premium neutral
- **Background character**: subtle grid / pure solid with ambient gradient / full-bleed cinematic imagery / quiet textured material
- **Typography character**: clean grotesk / refined grotesk / expressive display / compressed statement / editorial serif+sans / Swiss rational sans
- **Hero architecture**: cinematic centered minimalist / asymmetric split / floating polaroid scatter / inline typography behemoth / editorial offset / massive image-first
- **Section system**: strict bento / alternating editorial / poster stacked / gallery cadence / Swiss grid / asymmetric marketing flow
- **Signature components** (pick exactly 4): diagonal masonry / cascading card deck / hover-accordion slice / gapless bento / brand marquee / polaroid arc / vertical rhythm lines / off-grid editorial / product UI panel stack / split testimonial wall / oversized metrics strip / layered crop frames
- **Motion-implied** (pick exactly 2): scrubbing text reveal / pinned narrative / staggered float-up / parallax drift / accordion expansion / cinematic fade-through
- **Narrative spine** (pick 1): artifact / journey / precision instrument / living system / stage spotlight / archive dossier
- **Second-read moment** (pick exactly 1): asymmetric bleed / oversized punctuation or numeral / single material switch / vertical side-rail note / macro brand-color crop

`image-to-code` uses the same 9 axes; the narrative-spine and second-read-moment axes are optional
there (the pipeline emphasizes analysis and faithful implementation, not narrative art direction).

## 2. Hero scale and brief→direction mapping

Pick one **Hero Scale** for the whole site and execute it decisively. Then bias the axis picks to
match the brief — never force a recipe that contradicts it.

| Brief signal | Hero scale | Direction |
|---|---|---|
| Minimalist / clean / swiss / typography-only | Mini Minimalist | Solid surfaces; stacked center; skip full-bleed |
| Editorial / magazine / art-directed | Mid or Giant | Editorial side-image; off-grid offset; strong type contrast |
| Cinematic / atmospheric / luxury / bold | Giant | Full-bleed image with tonal overlay; bottom-left or centered-low composition |
| SaaS / product / dashboard / fintech / infra | Mid Editorial | Solid + inline asset; clear product framing; higher implementation clarity |
| Agency / creative studio / portfolio | Giant or Mini (decisive, not in-between) | Vary backgrounds boldly; off-grid poster-like |
| E-commerce / shop | Mid Editorial | Product-led; full-bleed product photo; unmistakable CTAs |
| Silent brief | (pick one decisively) | Confident background variety; defaults with intention |

**Hero Scale definitions:**
- **Giant Statement** — massive type, dominant first viewport.
- **Mid Editorial** — balanced type/image, cinematic but not screen-filling.
- **Mini Minimalist** — tiny logo + short statement + thin CTA, lots of negative space. Confident
  restraint, not weak.

## 3. Composition anchors and background mode

**The left-text / right-image hero is the most overused AI pattern.** It is allowed, but must not be
the first instinct. Before reaching for it, prefer: centered statement, bottom-left over image,
bottom-right CTA cluster, top-left lead, stacked center, image-as-canvas, off-grid editorial,
right-text / left-image (inverted), or mini minimalist.

Per section, pick a **composition anchor** and a **background mode**. Across the site:
- At least 3 different anchors must appear; same anchor must not repeat more than 2 sections in a row.
- Same background mode must not repeat more than 3 sections in a row.
- For non-minimalist briefs: include at least one full-bleed (or duotone / atmospheric) background and
  at least one mini minimalist section.

**Background mode menu** (per section): solid + inline asset / subtle texture / full-bleed image with
tonal overlay / editorial side-image / image-as-canvas / flat color block + detail crop / cinematic
tonal gradient / atmospheric photo grade / duotone / soft radial vignette + product / micro-noise
gradient / color-blocked diptych.

**CTA variation**: classic pill / outline ghost / underlined inline link / banner full-width / oversized
headline + tiny CTA hint / CTA as caption. Vary CTA style at least once; the primary action stays
unmistakable.

## 4. Continuity — one brand world

All per-section images must read as one site. A viewer scrolling through all frames must feel one
brand, not a collage.

**Held consistent across all images:**
- Same palette and accent logic
- Same type family and scale
- Same CTA family
- Same radius language
- Same image treatment
- Same tonal voice

**Allowed to vary:** composition anchor, background mode, section size, which second-read moment
appears. Nothing else.

## 5. Creativity escalation

Push beyond generic SaaS. Actively increase at least 3 of: composition, typography distinctiveness,
scale contrast, hero concept memorability, image treatment, section rhythm, framing/cropping, visual
tension, layout structure. Creativity must feel intentional, not chaotic.

**Section rhythm**: mix large art-directed sections, mini minimalist sections, and medium editorial
blocks deliberately. Keep spacing generous and fairly even — the page must breathe. Separate denser
sections with calmer ones.

**Hero minimalism and graphic restraint:**
- Strong opening scene; clean composition; do not overcrowd the first viewport.
- Headline reads like 5-10 strong words, not a paragraph — short and powerful.
- Prefer medium/light elegance, tight tracking, controlled line count, strong scale contrast.
- Avoid: random extra-bold shouting, gradient text as a lazy premium effect, 6-line startup headings.
- No giant meaningless outline numbers, cheap SVG filler, generic AI blobs, or random orb clutter.
- Use typography, image crops, real layout tension, premium materials, and strong framing instead.

## 6. Anti-slop ban list

The shared ban list (banned brands, filler verbs, purple/blue AI gradients, glassmorphism, blobs,
glowing edges) lives in [anti-tells.md](anti-tells.md) — load and apply it. Layout-specific bans
to also enforce for web visuals:

- **Layout**: endless centered sections, cloned left-text/right-image blocks, identical card rows,
  lifeless symmetry.
- **Data**: three identical stat columns, fake dashboards with pointless charts, infinity logo marquees.

## 7. How the two skills use this file

- **`imagegen` (web mode)**: generates images only. Steps lock section count (1 image/section), then pick from
  this engine (§1-§3), then enforce continuity + creativity + anti-slop (§4-§6). No code output.
- **`image-to-code`**: generates images, deeply analyzes each (text, typography, spacing, components,
  colors, layout), then implements code faithfully. Uses §1 axes for planning; narrative-spine and
  second-read axes optional. Delegates color formula, typography pairing, and interaction states to
  the `frontend-design` skill.

Both `imagegen` (web mode) and `image-to-code` link this reference rather than inlining the engine —
the single source of truth for the web visual-direction system.
