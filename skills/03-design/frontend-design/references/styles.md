# UI Styles Catalog

18 visual styles with characteristics, when-to-use, and effect specs (shadows, blur, radius).
Pick one style per project and apply it consistently — don't mix flat and skeuomorphic randomly.

## Contents

- [Style selection rules](#style-selection-rules)
- [Styles](#styles)
- [Anti-patterns (all styles)](#anti-patterns-all-styles)

## Style selection rules

- **Match style to product type** — a fintech dashboard and a playful consumer app need different styles.
- **Consistency** — use the same style across all pages. Don't vary by screen.
- **Effects match style** — shadows, blur, and radius must align with the chosen style (glass = blur+transparency; flat = no shadows; clay = inflated rounded shapes).
- **Dark-mode pairing** — design light/dark variants together to keep brand, contrast, and style consistent.
- **Elevation consistent** — use a consistent shadow/elevation scale for cards, sheets, modals; avoid random shadow values.
- **Icon style consistent** — one icon set/visual language (stroke width, corner radius) across the product. SVG only (Lucide, Heroicons), never emoji as structural icons.
- **Platform-adaptive** — respect platform idioms (iOS HIG vs Material): navigation, controls, typography, motion. See [apple-hig.md](apple-hig.md).
- **Primary action** — each screen has only one primary CTA; secondary actions are visually subordinate.
- **State clarity** — hover/pressed/disabled states must be visually distinct while staying on-style.
- **System controls** — prefer native/system controls over fully custom ones; customize only when branding requires it.

## Styles

### Glassmorphism
- **Characteristics**: Frosted-glass transparency, background blur, subtle borders, layered depth.
- **When to use**: Media-rich apps, dashboards, iOS/macOS-native feel, overlays on imagery.
- **Effects**: `backdrop-filter: blur(12px)` · semi-transparent surfaces (rgba 0.65–0.85) · 1px subtle light border · soft diffuse shadow.
- **Radius**: 12–20px.
- **Avoid**: Blurring everything (blur = background dismissal, not decoration); low-contrast text on glass.

### Claymorphism
- **Characteristics**: Soft 3D inflated shapes, rounded corners, dual shadows (dark below, light above) for a clay/putty feel.
- **When to use**: Playful consumer apps, toy-like UIs, children's products, friendly onboarding.
- **Effects**: Inset + drop shadow combo · `box-shadow: 0 8px 16px rgba(0,0,0,0.15), inset 0 -4px 8px rgba(255,255,255,0.3)` · saturated pastel colors.
- **Radius**: 16–28px, heavily rounded.

### Minimalism
- **Characteristics**: Maximum whitespace, restrained color, content-first, few elements, strong typography.
- **When to use**: Editorial sites, portfolios, SaaS landing pages, content-heavy products, luxury brands.
- **Effects**: No shadows or very subtle ones · flat surfaces · thin or no borders · monochrome or limited palette.
- **Radius**: 0–8px, subtle.
- **Avoid**: Over-decorating; every element must earn its place.

### Brutalism
- **Characteristics**: Raw, unpolished, heavy borders, monospace fonts, high contrast, exposed structure, intentionally "ugly."
- **When to use**: Developer tools, creative agencies, indie projects, counter-culture brands.
- **Effects**: Thick black borders (2–4px) · no shadows · no blur · harsh color blocks · visible grid lines.
- **Radius**: 0, sharp corners.
- **Avoid**: Softening it — brutality is the point.

### Neumorphism
- **Characteristics**: Soft extruded plastic, monochromatic, dual inset/outset shadows making elements appear carved from the surface.
- **When to use**: Calculator-style UIs, compact tool panels, single-purpose apps. Use sparingly — poor contrast accessibility.
- **Effects**: `box-shadow: 6px 6px 12px rgba(0,0,0,0.15), -6px -6px 12px rgba(255,255,255,0.8)` · surface color = background color · no hard borders.
- **Radius**: 12–20px.
- **Avoid**: Low-contrast states; neumorphism fails accessibility checks for disabled/active states.

### Bento Grid
- **Characteristics**: Modular grid of varied-size cards (like a Japanese bento box), each cell a self-contained module, rounded corners, gaps between cells.
- **When to use**: Dashboards, feature showcases, product landing pages, Apple-style presentations.
- **Effects**: Subtle shadows per cell · gap 12–24px · varied cell sizes within the grid.
- **Radius**: 16–24px per cell.

### Dark Mode
- **Characteristics**: Dark surfaces (slate/near-black), light text, desaturated accent colors, reduced eye strain in low-light.
- **When to use**: Code editors, media apps, gaming, always-on displays. Design alongside light mode, never bolt on.
- **Effects**: True black (#000) for OLED · or slate (slate-900/950) for softer feel · elevation via lighter dark layers (slate-800 over slate-900).
- **Avoid**: Inverted colors (don't just flip); use desaturated lighter tonal variants; test contrast independently.

### Skeuomorphism
- **Characteristics**: Real-world metaphors, textures, realistic shadows, physical affordances (knobs, switches, leather, wood).
- **When to use**: Specialized pro tools (audio mixers, instrument apps), retro games, brand-specific products. Use sparingly — modern UIs favor flat.
- **Effects**: Multi-layer shadows · gradients for depth · texture overlays · beveled edges.
- **Radius**: Varied, matching the real-world object.

### Flat Design
- **Characteristics**: Solid color blocks, no shadows or gradients, clean typography, geometric shapes, bold colors.
- **When to use**: Information-dense apps, Microsoft-style enterprise UI, fast-loading mobile apps.
- **Effects**: No shadows · no blur · solid fills · clear color hierarchy.
- **Radius**: 0–4px, minimal.
- **Avoid**: Too-flat interactive states — use color/opacity shifts, not nothing.

### Retro-Futuristic
- **Characteristics**: Neon gradients, cyberpunk grids, glitch effects, monospace + display fonts, dark backgrounds with electric accents.
- **When to use**: Gaming, crypto/Web3, tech demos, creative tech brands.
- **Effects**: Glow shadows (`box-shadow: 0 0 20px rgba(0,255,255,0.5)`) · gradient meshes · scanline overlays · neon borders.
- **Radius**: 0–8px.

### Organic / Natural
- **Characteristics**: Flowing curves, earth tones, hand-drawn elements, asymmetry, botanical/natural textures.
- **When to use**: Wellness, sustainability, food, beauty, health products.
- **Effects**: Soft shadows · organic SVG shapes · paper/grain textures · warm muted palette.
- **Radius**: Irregular, organic curves (SVG paths, not uniform radius).

### Luxury / Refined
- **Characteristics**: Generous whitespace, serif typography, muted metallic accents (gold, bronze), high-quality imagery, restrained animation.
- **When to use**: Fashion, jewelry, hospitality, premium brands, real estate.
- **Effects**: Subtle shadows · thin metallic borders · serif headings · muted jewel-tone palette.
- **Radius**: 0–4px, sharp and precise.

### Playful / Toy-like
- **Characteristics**: Bright saturated colors, rounded shapes, bouncy animations, illustrated characters, large friendly type.
- **When to use**: Children's apps, education, casual games, consumer onboarding.
- **Effects**: Bouncy spring animations · bold shadows · sticker-style elements.
- **Radius**: 20–full, very rounded.

### Editorial / Magazine
- **Characteristics**: Strong grid, large imagery, serif display fonts, column-based layout, pull quotes, print-inspired hierarchy.
- **When to use**: Publications, blogs, news, content-first brands.
- **Effects**: Minimal shadows · thin rules/borders · drop caps · column-based layout.
- **Radius**: 0–2px, print-like.

### Art Deco / Geometric
- **Characteristics**: Symmetry, geometric patterns, gold/black/cream palette, bold lines, sunburst/fan motifs, luxury feel.
- **When to use**: Event sites, luxury hospitality, vintage-themed brands.
- **Effects**: Gold foil accents · geometric SVG patterns · strong vertical lines.
- **Radius**: 0, sharp geometry.

### Soft / Pastel
- **Characteristics**: Light muted colors, soft shadows, rounded shapes, gentle gradients, friendly and calm.
- **When to use**: Baby/parenting apps, mental health, beauty, lifestyle.
- **Effects**: Soft diffuse shadows · pastel gradients · rounded everything.
- **Radius**: 16–full.

### Industrial / Utilitarian
- **Characteristics**: Monospace fonts, dense data, terminal-green/amber accents, minimal decoration, function over form.
- **When to use**: DevOps dashboards, monitoring tools, CLI-companion apps, IoT.
- **Effects**: No shadows · thin borders · monospace data · status-color accents.
- **Radius**: 0–2px.

### Maximalist
- **Characteristics**: High density, overlapping elements, mixed media, bold color clashes, layered transparencies, controlled chaos.
- **When to use**: Creative agencies, art showcases, music/culture sites, event promotions.
- **Effects**: Layered shadows · gradient meshes · noise textures · overlap and diagonal flow.
- **Radius**: Mixed, intentionally varied.

### Soft / Agency
- **Characteristics**: Haptic depth, cinematic spatial rhythm, obsessive micro-interactions, premium "expensive" feel. Double-Bezel nested card architecture (outer shell + inner core with concentric radius). Fluid island navigation (floating glass pill). Massive whitespace (`py-24` to `py-40`). Spring-physics motion.
- **When to use**: Premium consumer brands, lifestyle/real estate, high-end agency portfolios, Awwwards-tier landing pages.
- **Effects**: `backdrop-blur-2xl` · hairline borders (`ring-1 ring-white/10`) · inset highlights (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`) · diffused ambient shadows · `ease-[cubic-bezier(0.32,0.72,0,1)]` motion.
- **Radius**: Large and nested — outer `rounded-[2rem]`, inner `rounded-[calc(2rem-0.375rem)]` for concentric curves.
- **Fonts**: Geist, Clash Display, PP Editorial New, Plus Jakarta Sans (never Inter/Roboto/Arial).
- **Icons**: Phosphor Light, Remix Line (ultra-thin strokes only).

### Editorial Minimalist
- **Characteristics**: Clean document-style interfaces, warm monochrome palette, typographic contrast, flat bento grids, muted pastel accents. No gradients, no heavy shadows. Notion/Linear-tier workspace aesthetic.
- **When to use**: Workspace tools, documentation, SaaS dashboards, developer tools, editorial blogs.
- **Effects**: No shadows (or ultra-diffuse < 0.05 opacity) · thin borders (`1px solid #EAEAEA`) · subtle navbar blur only.
- **Radius**: Crisp — 8px or 12px maximum. No `rounded-full` for containers.
- **Palette**: Warm bone/off-white canvas (`#F7F6F3`), off-black text (`#111111`), spot pastels for semantic accents (pale red/blue/green/yellow).
- **Fonts**: 3-tier — sans-serif body (SF Pro Display, Geist Sans, Switzer), editorial serif headings (Lyon Text, Newsreader, Instrument Serif), monospace metadata (Geist Mono, JetBrains Mono).
- **Icons**: Phosphor Bold/Fill, Radix UI Icons.

### Industrial Brutalist
- **Characteristics**: Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects (halftone, CRT scanlines, dithering).
- **When to use**: Data-heavy dashboards, portfolios, editorial sites that need to feel like declassified blueprints or tactical telemetry.
- **Effects**: Halftone filters · CRT scanlines · bitmap dithering · visible grid compartments · zero border-radius · ASCII framing (brackets, crosshairs, registration marks).
- **Radius**: 0 — zero border-radius, uncompromising.
- **Two modes** (pick one, never mix): Swiss Industrial Print (light mode, heavy sans-serif, newsprint substrate, aviation red accent) or Tactical Telemetry (dark mode, monospace dominance, phosphor glow, terminal green).
- **Fonts**: Macro — Neue Haas Grotesk Black, Archivo Black (massive scale, tight tracking, uppercase). Micro — JetBrains Mono, IBM Plex Mono (small, generous tracking, uppercase). Textural — Playfair Display/EB Garamond sparingly, degraded.

## Anti-patterns (all styles)

- Mixing flat and skeuomorphic randomly within one product
- Emoji as structural icons (use SVG)
- Random shadow values not on a scale
- Defining interaction states for one theme (light/dark) only
- Hardcoded per-screen hex values instead of semantic tokens
- One icon family with mixed stroke widths
- Blur used as decoration instead of background dismissal
