# Web mode

Reference for the `imagegen` skill, **web** mode. Generate premium website design reference images —
one horizontal image per section — that feel art-directed, premium, and implementation-friendly,
not generic AI slop.

## 1. Lock the section count — one image per section

The hard rule: **one horizontal image per section, always.** Never combine multiple sections into
one frame; never return a single tall slice of the whole page; never replace several sections with
one collage. This overrides any model default that collapses output.

- 1 section → 1 image; 8 sections → 8 images; 12 sections → 12 images.
- If the count is ambiguous, default high: "hero" → 1; "landing page" → 6; "full website" / "marketing site" → 8; "product page" / "portfolio" → 6.
- Announce the count out loud: "Generating N horizontal images, one per section."
- Format: horizontal — 16:9 or 21:9 for heroes, 16:10 for narrower content sections.
- If only one image can render per call, generate them sequentially in the same response, labeled "Section X of N: <name>", until the full set is delivered. Do not stop early.

## 2. Map the brief to a direction

Read the brief and bias the picks to match — never force a recipe that contradicts it. Pick one
Hero Scale (Giant Statement / Mid Editorial / Mini Minimalist) for the whole site and execute it
decisively.

- Load [${CLAUDE_PLUGIN_ROOT}/skills/03-design/frontend-design/references/visual-direction.md](${CLAUDE_PLUGIN_ROOT}/skills/03-design/frontend-design/references/visual-direction.md) §2 for the brief→hero-scale mapping and the axis picks that match each brief signal. Subsequent steps reference sections of this file.

## 3. Run the combinatorial variation engine

Pick one option from each axis and commit to it consistently — don't mash everything into chaos.
These are visual-direction cues the generated image should imply, not code instructions.

- Load visual-direction §1 for the 9-axis engine (theme paradigm, background, typography, hero architecture, section system, signature components, motion-implied, narrative spine, second-read moment).

## 4. Vary composition per section — break the hero default

**The left-text / right-image hero is the most overused AI pattern.** It is allowed, but must not
be the first instinct. Per section, pick a composition anchor and a background mode; vary them
across the site.

- Load visual-direction §3 for the composition-anchor menu, background-mode menu, and CTA variation rules (≥3 distinct anchors; no anchor repeats >2 in a row; no background mode repeats >3 in a row; at least one full-bleed for non-minimalist briefs).

## 5. Apply hero minimalism and graphic restraint

Strong opening scene; clean composition; headline reads like 5-10 strong words, not a paragraph.

- Load visual-direction §5 for the restraint rules and forbidden hero patterns (no gradient text as a lazy premium effect, no giant outline numbers, no AI blob clutter).

## 6. Enforce continuity, creativity, and anti-slop

All per-section images must read as one site (one palette, type, CTA, radius, image treatment).
Push beyond generic SaaS. Ban the anti-slop list.

- Load visual-direction §4 (continuity — one brand world), §5 (creativity escalation + section rhythm), §6 (anti-slop ban list).

## Verify (web mode)

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
