# Typography Fundamentals

Depth reference for the `frontend-design` skill. The theory beneath `font-pairings.md`: font anatomy,
optical sizing, vertical rhythm, the modular type-scale ratios, and rendering. Load this when the
question is "why does this font read well/badly"; load `font-pairings.md` when the question is "which
two fonts and what sizes."

## 1. Font anatomy

The parts of a letterform that determine readability and character:

| Part | What | Affects |
|---|---|---|
| **x-height** | Height of lowercase 'x' | High x-height = more readable at small sizes (the letters have more "body") |
| **Ascenders** | Strokes rising above x-height (b, d, f, h, k, l, t) | Distinguish letters; long ascenders add elegance, short add compactness |
| **Descenders** | Strokes dropping below baseline (g, j, p, q, y) | Same; need line-height to accommodate |
| **Counters** | Enclosed negative space (a, e, o, p) | Small counters fill in at small sizes → use fonts with open counters for UI |
| **Terminals** | Ends of strokes | Rounded = friendly; flat = technical; ball = editorial |
| **Stroke contrast** | Variation between thick and thin | High contrast = elegant but fragile at small sizes; low = sturdy, readable |

Why it matters for UI:
- **High x-height + open counters + low contrast** = readable at 12-14px. Inter, system-ui, Roboto.
- **Low x-height + high contrast** = beautiful at display sizes, illegible at body sizes. Serifs like
  Didot. Use for headings only.
- A font that looks gorgeous at 48px and falls apart at 13px is not a UI font — it's a display font.

## 2. Optical sizing

Type is designed for a target size range. The same typeface at 12px and 48px has different optimal
forms:

| At small sizes | At large sizes |
|---|---|
| Larger x-height | More refined x-height |
| Wider counters | Tighter counters |
| Lower stroke contrast | Higher contrast |
| Heavier weight | Lighter weight for same visual weight |
| More generous spacing | Tighter spacing |

**Variable fonts** with an `opsz` (optical size) axis handle this automatically — the typeface reshapes
itself by size. If using non-variable fonts, pick sizes where the font's design works: don't force a
display serif into 12px body text.

**Optical weight:** a 400-weight font at 48px looks lighter than the same 400 at 14px. To match visual
weight across sizes, bump display text up a weight (400 → 500/600 at large sizes). Conversely, in dark
mode, reduce weight by one step — bold strokes look muddy on dark backgrounds (`font-pairings.md`).

## 3. Vertical rhythm

Align text to a baseline grid so spacing feels structured, not arbitrary. The math:

```
Line-height = base unit × N
Spacing between elements = base unit × N
```

With a 4px base unit (the `design-tokens.md` spacing grid):
- Body line-height = 24px (4 × 6) for 16px text → 1.5 ratio
- Heading line-height = 28px (4 × 7) for 32px text → 1.2 ratio (tighter for large text)
- Space after a paragraph = 24px (matches line-height — the grid holds)

| Element | Size | Line-height | Ratio |
|---|---|---|---|
| Body | 16px | 24px | 1.5 |
| H4 | 20px | 28px | 1.4 |
| H3 | 24px | 32px | 1.33 |
| H2 | 28px | 36px | 1.28 |
| H1 | 36px | 44px | 1.22 |

Rules:
- **Body line-height ≥ 1.5** (WCAG recommendation) for readability.
- **Heading line-height 1.2-1.3** — large text needs less leading; extra space breaks the line's unity.
- **Line length 45-75 characters** (desktop), 35-50 (mobile) — longer lines tire the eye; shorter
  disrupts rhythm.
- Everything snaps to the same base unit → the eye perceives "designed," not "assembled."

## 4. Modular type scale

Don't pick sizes arbitrarily — use a ratio. Each step = previous × ratio:

| Ratio | Name | Character |
|---|---|---|
| 1.125 | Major second | Subtle; fine-grained dashboards |
| 1.2 | Minor third | Balanced; common for product UI |
| 1.25 | Major third | Distinct; marketing-ish |
| 1.333 | Perfect fourth | Strong; editorial, landing pages |
| 1.5 | Perfect fifth | Dramatic; hero sections only |

Example with 1.2 ratio, 16px base:
```
16 × 1.2 = 19.2 → 20 (h4)
20 × 1.2 = 24    (h3)
24 × 1.2 = 28.8 → 28 (h2)
28 × 1.2 = 33.6 → 32 (h1)
```

`font-pairings.md` uses a fixed scale (text-xs through text-5xl); this explains *why* those steps are
spaced as they are — a modular ratio produces them. Pick the ratio by content character: dense data UI
= 1.125; marketing = 1.333+.

## 5. Font rendering and subpixel

Screens render type imperfectly. Understanding why helps you choose sizes that don't break:

| Issue | Cause | Mitigation |
|---|---|---|
| **Blurry at small sizes** | Hinting (font's size-specific instructions) weak | Use well-hinted UI fonts (Inter, system-ui) |
| **Color fringing** | Subpixel rendering on LCD | Worse on Windows ClearType; test cross-platform |
| **Thin strokes vanish** | Subpixel at 12px with light weight | Minimum 400 weight at 12-14px |
| **Inconsistent across OS** | macOS, Windows, Linux render differently | Test on all three; can't fully control |

Rules:
- **12px is the floor** — below 12px, rendering breaks and accessibility fails. Use 12px only for
  captions/metadata.
- **Test on Windows** — macOS renders type more generously; Windows is the harsh test. If it reads on
  Windows, it reads everywhere.
- **Antialiasing** — `-webkit-font-smoothing: antialiased` (macOS) darkens text; use for light-on-dark.
  `auto` for dark-on-light.

## 6. Monospace specifics

Code/data benefits from monospace — each glyph same width, aligning columns:

- **Use for:** code blocks, terminal output, tabular data alignment, version strings.
- **Features:** tabular figures (numbers align in columns), ligatures (optional, for code).
- **Recommended:** SF Mono (Apple), JetBrains Mono, Fira Code. `font-pairings.md` catalogs these.
- **Size:** match body text size, or one step smaller (13-14px against 16px body).

## 7. How this connects to font-pairings.md

| This file (theory) | `font-pairings.md` (application) |
|---|---|
| Anatomy (x-height, counters, contrast) | 31 pairings with character notes |
| Optical sizing, weight matching | Weight hierarchy (display 700, heading 600, body 400) |
| Vertical rhythm, baseline grid | Line-height/line-length targets |
| Modular scale ratios | The text-xs → text-5xl scale |
| Rendering, subpixel, hinting | Cross-platform loading tips (font-display, preload) |

Load `typography-fundamentals.md` when choosing *which typeface qualities* fit the use. Load
`font-pairings.md` when picking *specific pairings and sizes*. Both inform `frontend-design` Step 4
(Typography pairing).
