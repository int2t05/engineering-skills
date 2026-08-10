---
name: frontend-design
description: Use when building web components, pages, or applications with distinctive, production-grade design quality. Covers color, typography, layout, interaction states, and platform conventions. Triggers on "frontend", "UI", "design", "界面设计".
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
- Triggers on "frontend", "UI design", "组件设计", "界面设计", "视觉风格"

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

Use a dominant-surface-accent distribution, not timid even palettes:

- **Dominant (60%)** — the primary background/atmosphere color
- **Surface (30%)** — cards, panels, elevated layers
- **Accent (10%)** — sharp, high-contrast accent for CTAs and key actions
- Define **semantic tokens** (`text-primary`, `bg-surface`, `border-default`, `error`, `success`) — never raw hex in components
- **Contrast**: 4.5:1 for normal text, 3:1 for large text. Don't rely on color alone — pair with icon or text.
- Design **light and dark variants together** — dark mode uses desaturated lighter tonal variants, not inverted colors. Test contrast independently per theme.

- Load [references/palettes.md](references/palettes.md) for palette selection by product type, accessible color pairs, and dark-mode pairing rules

### 4. Typography pairing

Pair a distinctive display font with a refined body font. Avoid generic defaults. Vary between
generations — never converge on the same choice every time.

- **Type scale**: consistent ratio (e.g. 12 14 16 18 24 32). Don't skip heading levels.
- **Weight hierarchy**: bold headings (600–700), regular body (400), medium labels (500).
- **Line-height**: 1.5–1.75 for body. Line length: 65–75 chars desktop, 35–60 mobile.
- **Tabular figures** for data columns, prices, timers. Respect default letter-spacing per platform.

- Load [references/font-pairings.md](references/font-pairings.md) for the font pairing catalog by personality (elegant, playful, professional, modern, editorial) and Google Fonts selection

### 5. Specify interaction states and mark specs

Every interactive element needs all states: default, hover, focus, pressed, disabled, loading.

- **Touch targets**: 44×44pt (Apple) / 48×48dp (Material) minimum. 8px+ spacing between targets.
- **Timing**: 150–300ms for micro-interactions. Ease-out for entering, ease-in for exiting. Exit ~60–70% of enter duration.
- **Transform only**: animate `transform`/`opacity`, never `width`/`height`/`top`/`left`.
- **Focus rings**: 2–4px, visible. Never remove focus outlines without a replacement.
- **Loading**: skeleton/shimmer for >300ms operations. Never block input during animation.
- **Reduced motion**: respect `prefers-reduced-motion`; reduce or disable animations.

Mark specs — use consistent scales, not arbitrary values:

- **Spacing**: 4pt/8dp increments (0, 4, 8, 12, 16, 24, 32, 48)
- **Radius**: consistent scale (e.g. 0, 4, 8, 12, 16, full)
- **Elevation**: consistent shadow scale; avoid random shadow values
- **Icons**: one icon family, consistent stroke width and corner radius; SVG only

- Load [references/ux-guidelines.md](references/ux-guidelines.md) for the full UX rule catalog (accessibility, touch, performance, layout, forms, navigation, charts) and the pre-delivery checklist

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

- [../../references/engineering-principles.md](../../references/engineering-principles.md) — shared discipline (surface assumptions, push back, verify don't assume)
- [references/styles.md](references/styles.md) — 50+ UI styles with characteristics, when-to-use, and effects (shadows, blur, radius)
- [references/palettes.md](references/palettes.md) — color palette selection by product type, accessible pairs, dark-mode rules
- [references/font-pairings.md](references/font-pairings.md) — font pairing catalog by personality, type scale, Google Fonts selection
- [references/ux-guidelines.md](references/ux-guidelines.md) — 99 UX guidelines across 10 categories + pre-delivery checklist
- [references/apple-hig.md](references/apple-hig.md) — Apple HIG specs, routing table, URL construction, critical design rules
