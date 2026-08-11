---
name: frontend-design
description: Use when building web components, pages, or applications with distinctive, production-grade design quality — color, typography, layout, interaction states, and platform conventions. Triggers on "frontend", "UI", "design", "界面设计", "前端设计".
---

# Frontend Design

Build distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.
The method: pick a bold aesthetic direction, apply a color formula, pair typography deliberately,
specify interaction states, and execute with precision. Bold maximalism and refined minimalism both
work — the key is intentionality, not intensity.

## When to use

- Building web components, pages, or applications (HTML/CSS/JS, React, Vue, Svelte, etc.)
- Choosing a design direction, color palette, or typography system for a project
- Reviewing UI for visual quality, accessibility, or interaction polish
- Implementing responsive layouts, dark mode, or platform-specific conventions (Apple HIG, Material)
- Triggers on "frontend", "UI design", "组件设计", "界面设计", "前端设计", "视觉风格"

**When NOT to use:** pure data visualization (use dataviz); backend logic with no visual surface;
API contract design (use api-design).

## Steps

### 1. Define the element and project context

Before coding, commit to a bold aesthetic direction. Answer:

- **Element**: What are you building? (button, card, modal, navbar, page, full app)
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme — brutally minimal, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, industrial. Commit fully; never default to "safe."
- **Differentiation**: What makes this UNFORGETTABLE? The one thing someone will remember.

Match implementation complexity to the vision: maximalist designs need elaborate code; minimalist
designs need restraint and precision. NEVER use generic AI aesthetics — overused fonts (Inter,
Roboto, Arial), purple gradients on white, rounded-2xl everything, stock card grids, lorem ipsum.

### 2. Pick a style

Choose a concrete visual style that fits the product type and tone. Consistency across all pages is
non-negotiable — don't mix flat and skeuomorphic randomly. Use SVG icons (Lucide, Heroicons), never
emoji as structural icons. Effects (shadows, blur, radius) must align with the chosen style.

- Load [references/styles.md](references/styles.md) for the style catalog (glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, skeuomorphism, flat design, and more) with characteristics, when-to-use, and effects
- Load [references/apple-hig.md](references/apple-hig.md) when designing for Apple platforms (iOS, iPadOS, macOS, tvOS, visionOS, watchOS) — HIG specs, routing table, critical design rules

### 3. Apply the color formula

Use a dominant-surface-accent distribution, not timid even palettes. Define semantic tokens
(never raw hex in components), meet WCAG contrast, and design light/dark variants together.

- Load [references/palettes.md](references/palettes.md) for the 60/30/10 formula, semantic token table, contrast ratios, dark-mode rules, and palette selection by product type

### 4. Typography pairing

Pair a distinctive display font with a refined body font. Avoid generic defaults. Vary between
generations — never converge on the same choice every time.

- Load [references/font-pairings.md](references/font-pairings.md) for the type scale, weight hierarchy, line-height/line-length targets, tabular figures, and pairing catalog by personality

### 5. Specify interaction states and mark specs

Every interactive element needs all states: default, hover, focus, pressed, disabled, loading.
Use consistent scales for spacing, radius, elevation, and icons — not arbitrary values.

- Load [references/ux-guidelines.md](references/ux-guidelines.md) for touch-target sizes, animation timing, focus rings, reduced-motion, spacing scale, and the pre-delivery checklist

### 6. Implement and verify

Implement working code (HTML/CSS/JS, React, Vue, etc.) that is production-grade, functional,
visually striking, and meticulously refined. Then run the verification below.

## Verify

- [ ] Aesthetic direction is bold and intentional — not generic AI slop (no purple-on-white, no rounded-2xl everything, no stock card grids)
- [ ] Color formula applied: dominant/surface/accent distribution, semantic tokens, 4.5:1 contrast
- [ ] Typography: distinctive display + refined body, consistent type scale, no skipped heading levels
- [ ] Interaction states: every interactive element has default/hover/focus/pressed/disabled
- [ ] Touch targets ≥44pt; spacing on 4/8dp scale; consistent radius and elevation scales
- [ ] Responsive: works at 320px, 768px, 1024px, 1440px; no horizontal scroll on mobile
- [ ] Dark mode designed alongside light mode, not bolted on
- [ ] Accessibility: keyboard navigation, ARIA labels, focus management, reduced-motion support
- [ ] No emoji as icons; SVG icons from one consistent family

**Red flags:** purple/indigo everything; excessive gradients; rounded-2xl on everything; lorem
ipsum copy; oversized uniform padding; stock card grids; shadow-heavy layering; hardcoded hex in
components; text under 12px; gray-on-gray; color as sole state indicator.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [references/styles.md](references/styles.md) — 18 UI styles with effect specs (shadows, blur, radius)
- [references/palettes.md](references/palettes.md) — 12 palette directions by product type
- [references/font-pairings.md](references/font-pairings.md) — 31 font pairings across 10 personality categories
- [references/ux-guidelines.md](references/ux-guidelines.md) — 232 UX guidelines across 10 priority categories + pre-delivery checklist
- [references/apple-hig.md](references/apple-hig.md) — Apple HIG routing table + quick-reference specs
