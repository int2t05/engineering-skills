# Color Theory

Depth reference for the `frontend-design` skill. The theory beneath `palettes.md`: the HSB model, the
five color-scheme methods, the 70:25:5 distribution rule, color psychology and cultural variance, the
gray-test, and color temperature. Load this when the question is "why these colors together"; load
`palettes.md` when the question is "what tokens and ratios."

## 1. HSB model

Work in HSB (Hue, Saturation, Brightness), not RGB — it maps to how humans perceive color.

| Channel | Range | Controls |
|---|---|---|
| **Hue (H)** | 0-360° | The color itself (red 0°, yellow 60°, green 120°, cyan 180°, blue 240°, magenta 300°) |
| **Saturation (S)** | 0-100% | How intense (0% = gray, 100% = full color) |
| **Brightness (B)** | 0-100% | How light (0% = black, 100% = full) |

Why HSB over RGB: to make a palette "lighter," you change Brightness; to make it "muted," you change
Saturation; to shift hue, you change Hue. RGB mixes these — adjusting "lighter" in RGB changes all
three channels unpredictably. HSB separates the dimensions the way you actually think about color.

```
Hue wheel:  0°=red  60°=yellow  120°=green  180°=cyan  240°=blue  300°=magenta  360°=red
```

## 2. Five color schemes

Pick hues from the wheel by relationship. Each scheme has a different feel and use:

| Scheme | How | Visual | Best for |
|---|---|---|---|
| **Monochromatic** | One hue, vary S/B | | Most stable; low-risk; single-tone brand |
| **Analogous** | Adjacent hues (±30°) | | Harmonious; natural; calm palettes |
| **Complementary** | Opposite hues (180°) | | Strongest contrast; use sparingly (one accent) |
| **Triadic** | Three equidistant (120°) | | Lively; balanced; needs careful proportion |
| **Split-complementary** | One + two adjacent to its opposite | | Softer than complementary; contrast without tension |

Rules:
- **Complementary is for accents, not pairs** — red text on green background vibrates and is
  exhausting. Use complementary as one accent against a neutral.
- **Triadic needs proportion discipline** — three equal colors fight; pick one dominant, one secondary,
  one accent (the 70:25:5 rule, below).
- **Analogous rarely clashes** — the safest scheme for beginners; hard to make ugly, easy to make bland.

## 3. The 70:25:5 rule

Color proportion, not just choice. A palette of three great colors in equal thirds looks noisy; the
same three in 70/25/5 looks designed.

| Role | Proportion | Hue role |
|---|---|---|
| **Neutral** | 70% | Backgrounds, large surfaces — usually a near-white or near-black, low-saturation |
| **Primary** | 25% | Brand color — secondary surfaces, headings, key UI |
| **Accent** | 5% | The single sharp color — CTAs, critical alerts, the one thing per screen (Von Restorff) |

`palettes.md` expresses this as 60/30/10 (dominant/surface/accent) — same principle, finer split. The
constant: one accent, used sparingly, carries the eye. If two things share the accent color, neither
stands out (cognitive-laws.md §5).

## 4. Color psychology

Hue carries emotional association — not absolute (culture and context modulate), but with stable
tendencies in a given market:

| Hue | Common association | Typical use |
|---|---|---|
| **Red** | Urgency, danger, passion | Errors, destructive actions, alerts |
| **Orange** | Energy, warmth, affordability | CTAs, enthusiasm, budget brands |
| **Yellow** | Optimism, caution | Warnings, highlights, cheerful accents |
| **Green** | Success, growth, go | Confirmations, positive states, finance |
| **Blue** | Trust, calm, competence | Enterprise, finance, security, tech |
| **Purple** | Creativity, luxury, mystery | Premium, creative tools, AI |
| **Pink/Magenta** | Playful, modern, bold | Consumer, lifestyle, bold brands |
| **Neutral (black/white/gray)** | Professional, minimal, timeless | Default for serious tools |

Rules:
- **Psychology is a tendency, not a law** — a red CTA can work if the brand is red; context overrides
  default associations.
- **Don't rely on hue alone for meaning** — red = error is meaningless to a color-blind user or on a
  monochrome display. Always pair with an icon, word, or shape (gestalt-and-hierarchy.md §2).
- **Semantic colors are non-negotiable** — error/success/warning/info each get a dedicated hue, used
  consistently everywhere (`palettes.md` token table).

## 5. Cultural variance

Color meaning shifts across cultures — critical for i18n products:

| Color | West | East |
|---|---|---|
| **Red** | Danger, stop | Luck, prosperity, celebration (China) |
| **White** | Purity, weddings | Mourning, funerals (parts of Asia) |
| **Green** | Safety, money | Religion (Islam), infidelity (China, historically) |
| **Blue** | Corporate, male | Immortality, heaven (parts of Middle East) |

For products with international users: research the target market's color associations before locking
the palette. A "trustworthy blue" enterprise palette in the West may read differently elsewhere. The
`i18n` skill covers the broader locale surface; color is one dimension of it.

## 6. The gray-test

Desaturate the screenshot (or view it in grayscale). If the hierarchy is still clear, the palette is
working — contrast and luminance are carrying the structure. If it turns to mush, you were relying on
hue alone to create hierarchy, which fails for color-blind users and weakens the design.

```
Color version:  [primary CTA in blue]  [secondary in gray]  → looks fine
Gray-test:      [primary CTA ????]      [secondary ???]       → can't tell them apart? Bad.
```

The gray-test is the fastest color-blindness check: if it passes in grayscale, it passes for most
color-vision deficiencies. Pair with a contrast-ratio check (`palettes.md` WCAG rules) for the full
a11y picture.

## 7. Color temperature

| | Warm | Cool |
|---|---|---|
| **Hues** | Red, orange, yellow | Blue, green, purple |
| **Feel** | Energetic, intimate, advancing | Calm, professional, receding |
| **Use** | CTAs, urgency, warmth in brand | Trust, calm backgrounds, spaciousness |

A palette is usually one temperature dominant. Mixing warm and cool in equal measure creates tension
(sometimes intended, usually accidental). Warm colors appear to "advance" (closer to the viewer); cool
colors "recede" — useful for layering (warm accents on cool backgrounds pop).

## 8. Dark mode color adjustments

Dark mode is not "invert the light palette." Key shifts:

- **Desaturate + lighten accents** — a saturated blue that pops on white looks muddy and vibrates on
  dark. Reduce saturation, raise brightness.
- **Elevation via lighter darks** — raised surfaces are *lighter* darks, not darker (opposite of light
  mode where raised = lighter white).
- **Body text is not pure white** — pure white on pure black vibrates. Use a near-white (slate-50).
- **Shadows are weaker** — on dark backgrounds, shadows barely read; rely on elevation + borders.
- **Reduce font weight by one step** — bold text looks muddy on dark (the `font-pairings.md` rule).

design-principles §6 (consistency from systems) applies: dark mode changes the semantic token layer,
not the atomic layer — the same hue values, different role mappings.

## 9. How this connects to palettes.md

| This file (theory) | `palettes.md` (application) |
|---|---|
| HSB model, hue wheel | Semantic token table with HSL values |
| 5 color schemes | 12 palette directions by product type |
| 70:25:5 proportion | 60/30/10 dominant-surface-accent formula |
| Psychology, temperature | Palette-by-product-type recommendations |
| Gray-test | WCAG contrast ratios (4.5:1 / 3:1) |
| Dark mode shifts | Dark-mode token values per semantic role |

Load `color-theory.md` when choosing *which colors* and *why they work together*. Load `palettes.md`
when implementing them as *tokens with correct contrast*. Both inform the `frontend-design` Step 3
(Apply the color formula).
