# Product Icon Design

Criterion for generating product icons — the mark that *represents the product* (app icon,
favicon, plugin icon, brand mark). Distinct from UI *glyph* icons (Lucide/Heroicons single-color
stroke glyphs used inside an interface). A product icon is the face of the product; a UI glyph is
a control within it.

> **Grounding rule.** Every design task references real open-source implementations — a concrete
> reference item, never designed from nothing. The table below is the grounding; cite at least one
> before generating.

## The criterion

A product icon must read as a shipped product, not a placeholder. The bar: **not a single primitive
shape with a flat single fill.** A lone circle/square/triangle in one flat color signals
"unfinished / AI-default," not "real product." Depth, layering, and a considered multi-tone palette
are the floor — not optional polish.

## References to study (open-source, nameable)

Each is real OSS — study what it demonstrates; never copy a mark.

| Reference (license) | What it demonstrates |
|---|---|
| **Phosphor Icons** (MIT) — `duotone` weight | Multi-tone layering: base fill + translucent secondary. Depth without complexity. |
| **Material Symbols** (Google, Apache 2.0) | Variable-axis system (weight/grade/optical-size) — scalability + system thinking across sizes. |
| **Fluent UI Icons** (Microsoft, MIT) | Monoline system carrying optical balance and weight tuning. |
| **Remix Icon** / **Tabler Icons** / **Iconoir** (MIT/Apache) | Metaphor vocabulary — breadth to study, not to lift. |
| **Lucide** / **Heroicons** (ISC/MIT) | The UI-glyph boundary: single-color stroke icons are *correct in-app* and *wrong as a product mark*. Cited to prevent the line-icon-as-product-icon anti-pattern. |

For multi-tone depth and gradient beyond what line sets cover, retrieve real product brand icons via
`design-research` (free galleries: Lapa Ninja, Godly, Land-book). Collect 5–10 in the same category
(dev tool, security, voice, luxury, productivity — reuse `imagegen` brand-mode categories); extract
what makes each premium before generating. Match quality and rhythm; never copy a name, logo, or mark.

## Anti-patterns ("simple shapes + simple colors")

- Lone primitive (circle / square / triangle) + one flat fill.
- A 1-color line glyph used as the *product* mark (fine as a UI control).
- Default AI purple→blue gradient dropped on a primitive shape.
- Clipart geometry, random sparkle, generic lightning bolt.

## Premium criteria

- **Depth / dimensionality** — gradient, inner light, soft shadow, considered bevel where the style calls for it.
- **Layered / composite form** — ≥2 visual elements in deliberate relation, not a lone primitive.
- **Considered multi-tone palette** — base + accent(s) + neutrals, on-brand (see [design-principles.md](design-principles.md) CRAP + token tiers).
- **Optical balance** — tuned by eye, not mathematical center (counters, weight, negative space).
- **Scalability** — holds at 16px favicon → 512px store icon; test small sizes.
- **Ownable + connected to brand idea** — reuse `imagegen` brand-mode §3 concept methods (monogram+meaning, product action, metaphor fusion, negative space, construction geometry).
- **Platform adaptation** — squircle / radius per platform, safe area, light + dark variants.

## SVG execution

Vector-first. Palette via gradients and semi-transparent layers, not flat fills. Outline paths; set
`viewBox`; optimize path data. Ship a monochrome variant for dark or monochrome contexts (plugin
chrome, dark-mode tab bar). Structural contrast — technique only, not a real brand mark:

```svg
<!-- primitive (anti-pattern): one circle, one flat fill -->
<svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="#3b82f6"/></svg>

<!-- premium (criterion): gradient surface + layered composite + optical balance -->
<svg viewBox="0 0 64 64">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0ea5e9"/><stop offset="1" stop-color="#6366f1"/>
  </linearGradient></defs>
  <rect x="6" y="6" width="52" height="52" rx="14" fill="url(#g)"/>
  <path d="M22 34l8 8 14-16" stroke="#fff" stroke-width="5" fill="none"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

## Verify

- **Squint test** — blur eyes; still recognizable as the product?
- **16px test** — readable as a favicon?
- **Monochrome test** — holds in one color (dark / monochrome contexts)?
- **On-palette test** — colors are brand tokens, not random?
- **Not-a-primitive test** — more than one shape + one flat fill? If not, it fails the criterion.

## References

- [design-principles.md](design-principles.md) — CRAP, hierarchy before decoration, consistency from systems.
- [engineering-principles.md](engineering-principles.md) — push back, verify don't assume.
- `imagegen` brand-mode ([../skills/03-design/imagegen/references/brand-mode.md](../skills/03-design/imagegen/references/brand-mode.md)) — logo concept methods.
- `design-research` ([../skills/03-design/design-research/SKILL.md](../skills/03-design/design-research/SKILL.md)) — real-icon retrieval from free galleries.
