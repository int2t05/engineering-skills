# Font Pairings

Typography pairing catalog by personality, the type scale, weight hierarchy, and Google Fonts
selection. Pair a distinctive display font with a refined body font — avoid generic defaults (Arial,
Inter, Roboto, system fonts). Vary between generations; never converge on the same choice every
time.

## Pairing rules

- **Match heading/body personalities** — a brutalist display font needs a body font that can carry
  it; a delicate serif display needs a quiet body font.
- **Contrast, not clash** — pair fonts that differ enough to create hierarchy (serif display +
  sans body, or vice versa) but share an underlying tone.
- **Avoid generic fonts** — Arial, Inter, Roboto, system-ui as defaults signal "AI slop." Reach for
  distinctive, characterful choices.
- **One display + one body** — don't use three or four fonts. Two is enough; one (with weight
  variation) works for minimalist styles.
- **License check** — confirm the font's license covers your use (web embedding, app bundling).
  Google Fonts (OFL) is safe for most projects.

## Type scale

Use a consistent modular scale. Don't invent arbitrary sizes:

| Token | Size | Use |
|-------|------|-----|
| `text-xs` | 12px | Labels, captions, badges |
| `text-sm` | 14px | Secondary text, table cells |
| `text-base` | 16px | Body text (minimum on mobile — avoids iOS auto-zoom) |
| `text-lg` | 18px | Lead paragraph, emphasis |
| `text-xl` | 20–24px | Subsection headings |
| `text-2xl` | 24–28px | Section headings |
| `text-3xl` | 30–32px | Page subheadings |
| `text-4xl` | 36–40px | Page headings |
| `text-5xl` | 48px+ | Display / hero |

- **Don't skip heading levels** (h1 → h2 → h3, no jumps).
- **Don't use heading styles for non-heading content.**
- **Line-height**: 1.5–1.75 for body; 1.1–1.3 for headings.
- **Line length**: 65–75 chars desktop; 35–60 chars mobile.
- **Letter-spacing**: respect platform defaults; avoid tight tracking on body text. Slight positive
  tracking on uppercase labels is fine.

## Weight hierarchy

| Role | Weight | Use |
|------|--------|-----|
| Display / hero | 700–800 | Hero headings, large display type |
| Heading | 600–700 | Section/subsection headings |
| Body | 400 | Default body text |
| Label / emphasis | 500 | Buttons, labels, table headers, nav |
| Light (use sparingly) | 300 | Large display only, never body |

Use font-weight to reinforce hierarchy. Don't use color alone to distinguish heading levels.

## Specialized figures

- **Tabular/monospaced figures** for data columns, prices, timers — prevents layout shift when
  numbers change.
- **Ligatures** — enable for serif body text if the font supports them; disable for monospace data.

## Pairing catalog by personality

### Elegant / Luxury
Display serif + quiet sans body. Refined, generous whitespace.
- **Playfair Display** + Source Sans 3
- **Cormorant Garamond** + Inter (if you must use Inter, pair it with a strong display)
- **DM Serif Display** + DM Sans
- **Fraunces** + Inter

### Playful / Friendly
Rounded display + warm body. Approachable, bouncy.
- **Fraunces** (soft) + Nunito
- **Bricolage Grotesque** + Nunito Sans
- **Caprasimo** + Mulish
- **Quicksand** + Source Sans 3

### Professional / Corporate
Clean sans + structured sans. Trustworthy, readable.
- **Manrope** + Source Sans 3
- **Sora** + Inter (pair with a distinctive display to avoid generic)
- **Bricolage Grotesque** + Manrope
- **Archivo** + Archivo Narrow (same family, different widths)

### Modern / Tech
Geometric sans + mono accents. Sharp, technical.
- **Space Grotesk** + JetBrains Mono (overused — vary)
- **Sora** + IBM Plex Mono
- **Outfit** + Space Mono
- **Geist** + Geist Mono

### Editorial / Magazine
Serif display + serif or sans body. Print-inspired, content-first.
- **Fraunces** + Source Serif 4
- **Playfair Display** + Source Sans 3
- **Newsreader** + Inter
- **Lora** + Karla

### Brutalist / Raw
Monospace or chunky display + monospace body. Unpolished, structural.
- **Space Mono** + JetBrains Mono
- **Archivo Black** + Space Mono
- **Anybody** + JetBrains Mono

### Minimalist / Refined
One font family with weight variation. Restrained, precise.
- **Inter** (all weights) — but vary away from this default
- **Manrope** (all weights)
- **Sora** (all weights)
- **Geist** (all weights)

### Retro-Futuristic / Cyberpunk
Display monospace + neon glow + mono body. Electric, technical.
- **VT323** + JetBrains Mono
- **Major Mono Display** + Space Mono
- **Orbitron** + Rajdhani

### Organic / Natural
Humanist serif/sans + warm body. Flowing, earthy.
- **Fraunces** (soft optical) + Lora
- **Crimson Pro** + Karla
- **Spectral** + Work Sans

### Industrial / Utilitarian
Monospace + condensed sans. Dense, functional.
- **JetBrains Mono** + Archivo Narrow
- **IBM Plex Mono** + IBM Plex Sans Condensed

## Google Fonts selection tips

- **Variable fonts** — prefer variable fonts (one file, many weights/widths) for performance.
- **Preload critical fonts** — only the display + body weights actually used above the fold.
- **font-display: swap** — avoid FOIT (flash of invisible text); show fallback immediately.
- **Reserve space** — set `size-adjust` on the fallback font to reduce layout shift (CLS).
- **Don't over-preload** — only critical fonts, not every variant.
- **Self-host vs Google CDN** — self-host for production performance; Google CDN for prototyping.

## Avoid (generic AI defaults)

- **Inter / Roboto / Arial / system-ui** as the only font — too generic.
- **Space Grotesk** used every time — it's become the AI default for "modern."
- **Purple gradient text** on display fonts — overused AI aesthetic.
- **More than two font families** — creates noise.
- **Skipping the body font** ("I'll just use the system font for body") — the body font carries
  readability; choose it deliberately.
