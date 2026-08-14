# Design Token Architecture

Tokens are the single source of truth for design decisions — spacing, color, radius,
elevation, typography, z-index. This reference defines the token tiers, naming
conventions, and scales. Load when building or auditing a token system.

## Contents

- [When to load this](#when-to-load-this)
- [Token tiers](#token-tiers)
- [Naming convention](#naming-convention)
- [Token scales](#token-scales)
- [Color tokens](#color-tokens)
- [Implementation](#implementation)
- [Verify](#verify)

## When to load this

- Building a design token system from scratch.
- Auditing an existing system for token gaps or naming drift.
- Connecting design tokens to code (CSS custom properties, Tailwind config, W3C Design
  Tokens spec).

## Token tiers

Three tiers, each more specific than the last:

| Tier | Example | Purpose |
|---|---|---|
| **Global (primitive)** | `color-blue-500`, `spacing-4`, `radius-md` | Raw values, no semantic meaning. The palette. |
| **Semantic** | `color-accent-primary`, `spacing-gap-card`, `radius-card` | Intent-bound — "this is the accent color", "this is card gap". References global tokens. |
| **Component** | `button-bg`, `card-radius`, `modal-shadow` | Component-specific. References semantic tokens. |

Rules:
- **Global → Semantic → Component**, never skip a tier. A component token referencing a
  global token directly loses the semantic layer's indirection.
- **Change a global token → all semantics that alias it update.** That's the point.
- **Never hardcode hex/px in component code.** If a value appears in code, it must be a
  token or a token alias.

## Naming convention

```
<category>-<property>-<scale>
```

- `color-bg-surface` — the background color for surface elements.
- `spacing-gap-card` — the gap inside a card.
- `radius-border-button` — the border radius for buttons.
- `elevation-shadow-modal` — the shadow for modals.
- `typography-size-heading-1` — the font size for H1.

Use kebab-case. Scale modifiers: `xs / sm / md / lg / xl / 2xl` (not numbers — numbers
imply arithmetic, names imply a curated set).

## Token scales

### Spacing

| Token | Value | Use |
|---|---|---|
| `spacing-0` | 0 | No gap |
| `spacing-xs` | 4px | Tight: icon-to-label, inline gaps |
| `spacing-sm` | 8px | Compact: within a chip, small card padding |
| `spacing-md` | 12px | Standard: button padding, list item gap |
| `spacing-lg` | 16px | Comfortable: card padding, section-internal |
| `spacing-xl` | 24px | Section gap, modal padding |
| `spacing-2xl` | 32px | Large section gap |
| `spacing-3xl` | 48px | Page-level vertical rhythm |
| `spacing-4xl` | 64px | Hero / feature section spacing |

Base unit: 4px. All spacing is a multiple of 4 (the 4px grid). Never 5px, 7px, 13px.

### Radius

| Token | Value | Use |
|---|---|---|
| `radius-none` | 0 | Brutalist, tables, data grids |
| `radius-sm` | 4px | Inputs, chips, small buttons |
| `radius-md` | 8px | Buttons, cards (default) |
| `radius-lg` | 12px | Large cards, modals |
| `radius-xl` | 16px | Feature cards, hero elements |
| `radius-full` | 9999px | Pills, avatars, circular buttons |

### Elevation (shadow)

| Token | Value | Use |
|---|---|---|
| `elevation-none` | none | Flat surfaces, base layer |
| `elevation-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Resting cards, inputs |
| `elevation-md` | `0 4px 6px rgba(0,0,0,0.1)` | Hover cards, dropdowns |
| `elevation-lg` | `0 8px 16px rgba(0,0,0,0.12)` | Modals, popovers |
| `elevation-xl` | `0 16px 32px rgba(0,0,0,0.15)` | Floating panels, drag previews |

Shadow color: use a neutral at low opacity (`rgba(0,0,0,0.05–0.15)`), not pure black.
Dark mode: invert to `rgba(0,0,0,0.3–0.5)` with larger blur (shadows are less visible
on dark surfaces — compensate with deeper blur).

### Z-index

| Token | Value | Use |
|---|---|---|
| `z-base` | 0 | Normal flow |
| `z-dropdown` | 10 | Dropdowns, popovers |
| `z-sticky` | 20 | Sticky headers, persistent nav |
| `z-drawer` | 40 | Side drawers, slide-overs |
| `z-modal` | 100 | Modals, dialogs |
| `z-toast` | 1000 | Toast notifications (above everything) |

Never use `z-[9999]`. If you need above toast, add a new token — don't ad-hoc.

### Typography

| Token | Property | Example |
|---|---|---|
| `type-display` | family, size, weight, line-height | `font-display, 48px, 700, 1.1` |
| `type-heading` | | `font-body, 24px, 600, 1.3` |
| `type-body` | | `font-body, 16px, 400, 1.5` |
| `type-label` | | `font-body, 14px, 500, 1.4` |
| `type-caption` | | `font-body, 12px, 400, 1.4` |
| `type-mono` | | `font-mono, 14px, 400, 1.5` |

See `font-pairings.md` for the font family selection. Tokens reference the family
chosen there, not raw font names.

## Color tokens

Color tokens are defined in `palettes.md` (11 semantic tokens: text-primary,
text-secondary, bg-dominant, bg-surface, accent-primary, etc.). This reference defines
the tier structure — `palettes.md` defines the values.

## Implementation

### CSS custom properties

```css
:root {
  /* Global */
  --color-blue-500: #3b82f6;
  --spacing-4: 1rem;
  --radius-md: 8px;

  /* Semantic (alias global) */
  --color-accent-primary: var(--color-blue-500);
  --spacing-gap-card: var(--spacing-4);
  --radius-card: var(--radius-md);
}

[data-theme="dark"] {
  --color-accent-primary: var(--color-blue-400); /* lighter accent for dark */
}
```

### Tailwind config

```js
theme: {
  extend: {
    colors: { accent: { primary: 'var(--color-accent-primary)' } },
    spacing: { card: 'var(--spacing-gap-card)' },
    borderRadius: { card: 'var(--radius-card)' },
  }
}
```

### W3C Design Tokens spec

For cross-tool token exchange (Figma ↔ code, Style Dictionary), use the W3C Design
Tokens Format Module. Tokens are JSON with `$value` and `$type`:

```json
{ "color-accent-primary": { "$value": "{color.blue.500}", "$type": "color" } }
```

Use Style Dictionary to transform W3C tokens into platform-specific output (CSS, Tailwind,
Swift, Kotlin).

## Verify

- Three tiers present (global → semantic → component), no tier skipped.
- No hardcoded hex/px in component code — everything is a token.
- Spacing is a multiple of 4 (the 4px grid).
- Z-index uses the documented scale, no ad-hoc `z-[9999]`.
- Dark mode overrides semantic tokens, not component code.
- Token names follow the `<category>-<property>-<scale>` convention.
