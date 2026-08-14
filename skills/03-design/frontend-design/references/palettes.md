# Color Palettes

Color selection guidance: the dominant-surface-accent formula, semantic tokens, accessible pairs,
dark-mode rules, and palette selection by product type.

## Contents

- [The color formula](#the-color-formula)
- [Semantic tokens](#semantic-tokens)
- [Contrast rules (WCAG 2.1 AA)](#contrast-rules-wcag-21-aa)
- [Dark mode](#dark-mode)
- [Palette selection by product type](#palette-selection-by-product-type)
- [Common pitfalls (AI aesthetic)](#common-pitfalls-ai-aesthetic)
- [Contrast verification](#contrast-verification)

## The color formula

Use a dominant-surface-accent distribution. Timid, evenly-distributed palettes look generic;
dominant colors with sharp accents outperform.

| Role | Proportion | Purpose |
|------|-----------|---------|
| **Dominant** | 60% | Primary background/atmosphere — sets the mood |
| **Surface** | 30% | Cards, panels, elevated layers — one step up from dominant |
| **Accent** | 10% | Sharp, high-contrast — CTAs, key actions, links |

One accent color is the primary CTA. Each screen has only one primary action; secondary actions
are visually subordinate.

## Semantic tokens

Define semantic color tokens — never use raw hex in components:

| Token | Light | Dark | Use |
|-------|-------|------|-----|
| `text-primary` | slate-900 | slate-50 | Primary body text |
| `text-secondary` | slate-600 | slate-400 | Secondary/helper text |
| `text-muted` | slate-400 | slate-500 | Tertiary/disabled text |
| `bg-dominant` | white / stone-50 | slate-950 | Page background |
| `bg-surface` | white | slate-900 | Cards, panels |
| `bg-elevated` | slate-50 | slate-800 | Modals, popovers |
| `border-default` | slate-200 | slate-700 | Default borders/dividers |
| `accent-primary` | indigo-600 / emerald-600 | indigo-400 / emerald-400 | Primary CTA |
| `error` | red-600 | red-400 | Errors, destructive |
| `success` | emerald-600 | emerald-400 | Success states |
| `warning` | amber-500 | amber-400 | Warnings |
| `focus-ring` | accent at 40% opacity | accent at 40% opacity | Focus outlines |

Map tokens per theme. Components reference tokens, never hex.

## Contrast rules (WCAG 2.1 AA)

| Element | Ratio | Standard |
|---------|-------|----------|
| Normal body text (<18pt) | 4.5:1 minimum | WCAG AA |
| Large text (≥18pt / 14pt bold) | 3:1 minimum | WCAG AA |
| UI components / graphical objects | 3:1 minimum | WCAG 2.1 |
| Non-text contrast (borders, icons) | 3:1 minimum | WCAG 2.1 |
| Data lines/bars vs background | 3:1 minimum | Charts |
| Data text labels | 4.5:1 minimum | Charts |

- **Don't rely on color alone** — pair every color-coded state with an icon, text, or pattern.
  Error red must include an icon/text; success green must include a checkmark.
- **Functional color** (error red, success green) must include icon/text; avoid color-only meaning.
- **Verify pairs** with a contrast checker — don't assume.

## Dark mode

Design light and dark variants together, not as an afterthought.

- **Don't invert** — dark mode uses desaturated lighter tonal variants, not raw color inversion.
- **Surfaces**: elevation via lighter dark layers (slate-800 over slate-900), not drop shadows.
- **Text**: primary text ≥4.5:1, secondary text ≥3:1 on dark surfaces.
- **Accents**: desaturate and lighten accent colors for dark mode (indigo-600 → indigo-400).
- **Borders/dividers**: must be visible in dark mode, not just light — define per theme.
- **State parity**: pressed/focused/disabled states must be equally distinguishable in both themes.
- **Scrim**: modal/drawer scrim 40–60% black — strong enough to isolate foreground content.
- **Test independently** — don't assume light-mode contrast values work in dark mode.

## Palette selection by product type

Match the palette to the product's industry and tone:

| Product type | Palette direction | Example |
|-------------|-------------------|---------|
| SaaS / B2B | Trust, calm — blue/indigo + neutral grays | indigo-600 accent, slate surfaces, white dominant |
| Fintech / Crypto | Trust + energy — deep blue/green + electric accent | navy dominant, emerald/emerald accent |
| E-commerce | Conversion — bold accent + clean neutrals | white dominant, black text, single bold accent (red/orange) |
| Healthcare / Wellness | Calm, clean — soft blues/greens + white | teal/emerald accent, white dominant, soft surfaces |
| Beauty / Spa | Soft, warm — pastels + muted gold | blush/sage dominant, gold accent, soft surfaces |
| Education | Friendly, focused — bright + readable | blue/green accent, white dominant, clear hierarchy |
| Entertainment / Social | Vibrant, immersive — saturated + dark | dark dominant, neon/electric accents |
| Portfolio / Editorial | Refined, content-first — muted + serif | stone/cream dominant, single accent, strong type |
| Gaming / Cyberpunk | Dark, electric — near-black + neon | true black dominant, cyan/magenta neon accents |
| Productivity / Tool | Functional, dense — neutral + status colors | slate dominant, blue accent, semantic status colors |
| Travel / Hospitality | Warm, inviting — earth tones + accent | sand/warm-white dominant, terracotta/ocean accent |
| Industrial / DevOps | Utility — dark/neutral + status colors | slate-950 dominant, terminal green/amber accents |

## Common pitfalls (AI aesthetic)

| AI default | Why it's a problem | What to do instead |
|-----------|-------------------|-------------------|
| Purple/indigo everything | Every app looks identical | Use the product's actual palette |
| Excessive gradients | Visual noise, clashes with design systems | Flat or subtle gradients matching the style |
| Timid even palettes | No hierarchy, no focus | Dominant 60% + accent 10% distribution |
| Raw hex in components | No theming, no dark mode | Semantic tokens mapped per theme |
| Color as sole indicator | Fails accessibility | Pair with icon/text/pattern |
| Inverted dark mode | Looks harsh, breaks contrast | Desaturated lighter tonal variants |
| Random shadow values | Inconsistent elevation | Consistent elevation scale per style |

## Contrast verification

For every foreground/background pair, verify the ratio meets the target:

```
Ratio = (L1 + 0.05) / (L2 + 0.05)
where L1 = relative luminance of lighter color
      L2 = relative luminance of darker color
```

Relative luminance: `L = 0.2126*R + 0.7152*G + 0.0722*B` (with sRGB gamma correction per channel).

If a pair fails, darken the text or lighten the background — don't pick a different color that
"looks fine" without verifying.
