---
name: imagegen
description: Use when generating premium design reference images across three modes — brand identity boards, website section images, or mobile app screens — art-directed and implementation-friendly, not generic AI slop. Output is images only, never code. Triggers on "brand kit", "logo 设计", "品牌系统", "web design image", "landing page image", "网站设计图", "mobile design image", "app screen image", "移动端设计图", "手机界面图". Not for frontend code (use frontend-design) or image-to-code pipeline (use image-to-code).
---

# Imagegen

Generate premium design reference images across three modes — brand identity, web sections, mobile
screens — that feel art-directed and implementation-friendly, not generic AI slop. Output is images
only, never code.

## When to use

- Brand identity boards, logo concepts, identity systems → **brand** mode
- Website section reference images (one horizontal image per section) → **web** mode
- Mobile app screen concepts and multi-screen flows → **mobile** mode
- Triggers on "brand kit", "logo 设计", "品牌系统", "web design image", "landing page image", "网站设计图", "mobile design image", "app screen image", "移动端设计图", "手机界面图"

**Not for:** frontend code (use `frontend-design`); image-to-code pipeline (use `image-to-code`).

**Tool note:** use an available image-generation tool — do not bind to a specific product.

## Steps

### 1. Pick the mode and load its workflow

Infer from the brief which mode fits, then load that mode's reference for the full workflow. Each
mode has its own section-count rule, composition logic, and anti-slop list.

- **brand** — brand-kit overview boards, logo concepting, identity systems → [references/brand-mode.md](references/brand-mode.md)
- **web** — one horizontal section image per section, premium art direction → [references/web-mode.md](references/web-mode.md)
- **mobile** — phone-mockup-framed app screens and multi-screen flows → [references/mobile-mode.md](references/mobile-mode.md)

If the brief spans modes (e.g. a brand system plus web mockups), lead with the primary mode and
note the secondary. Do not mash modes into one frame.

### 2. Hold one art direction across the set

Whatever the mode, lock one visual direction — palette, typography, imagery treatment, corner
radius, density — and keep it consistent across every image in the set. Screen 3 must not drift
into a different product world than screen 1. The mode reference defines the mode-specific bible;
this step is the shared consistency spine across the whole set.

### 3. Ban AI slop (all modes)

No purple-blue gradients, floating blobs, cloned blocks, fake KPI columns, generic copy ("elevate
your life", "unlock your potential"), fake brands (Acme, NovaCore, Flowbit), stock-template boards,
or phone-shaped websites. If a render is weak — tiny text, unclear spacing, fake navigation,
clutter, inconsistent framing — regenerate it. Do not settle for the first mediocre render.

### 4. Match references without copying

If the user provides reference images, extract their layout rhythm, grid, spacing, type scale,
visual density, and accent-color logic. Do NOT copy exact logos, brand names, compositions,
slogans, or unique visual assets. References are quality training, not templates.

**Output:** design reference image(s). Not code.

## Verify

- [ ] Mode chosen decisively (brand / web / mobile) and the mode reference loaded
- [ ] One art direction held across every image in the set (palette, type, radius, imagery treatment)
- [ ] No AI slop — no purple-blue gradients, blobs, cloned blocks, fake brands, generic copy
- [ ] Weak renders regenerated — no tiny text, fake navigation, or clutter settled for
- [ ] User references matched for quality/rhythm only — no exact logos, names, or compositions copied
- [ ] Output is images only — a developer or designer could use them as reference, never code

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/design-principles.md](${CLAUDE_PLUGIN_ROOT}/references/design-principles.md) — design discipline (CRAP, hierarchy before decoration, design every state, accessibility non-optional, consistency from systems)
- [references/brand-mode.md](references/brand-mode.md) — brand identity board workflow (strategy, visual modes, logo concepting, board composition)
- [references/web-mode.md](references/web-mode.md) — web section image workflow (section count, hero scale, 9-axis variation engine)
- [references/mobile-mode.md](references/mobile-mode.md) — mobile screen flow workflow (platform mode, design bible, phone mockup, safe areas)
