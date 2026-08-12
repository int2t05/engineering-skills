# Gestalt and Visual Hierarchy

Depth reference for the `frontend-design` skill. The principles behind *why* a layout works: Gestalt
grouping laws, the four hierarchy techniques, reading-pattern models, the squint and 5-second tests,
and the CRAP principles expanded. This is the theory layer beneath `palettes.md`, `font-pairings.md`,
and `anti-tells.md` (the application layer).

## 1. Gestalt principles

The brain groups elements before it reads them. Use grouping to imply structure without drawing it.

| Principle | Rule | UI application |
|---|---|---|
| **Proximity** | Elements close together are seen as related | Group form field + label; space sections apart |
| **Similarity** | Elements that look alike are seen as related | Same button style = same action type; same color = same category |
| **Continuity** | Elements on a line or curve are seen as a group | Aligned columns; a progress bar reads as one path |
| **Closure** | The mind completes incomplete shapes | A card with a gap still reads as a card; don't over-border |
| **Common fate** | Elements moving together are seen as related | A staggered list reveal animates as one group |
| **Figure-ground** | The eye separates a focal element from its background | Contrast the active element against the field; modal scrim |

The practical takeaway: related things go close and look similar; unrelated things go far and look
different. Most "messy" layouts violate proximity (everything equidistant) or similarity (inconsistent
styling for the same role).

## 2. Visual hierarchy — four techniques

Hierarchy is established through four levers, in roughly this priority:

| Technique | How | Strongest when |
|---|---|---|
| **Size** | Larger = more important | Heading vs body; primary CTA vs secondary |
| **Contrast** | Darker/bolder/saturated = more important | Primary text vs muted helper text |
| **Spacing** | More space around = more importance | Hero section breathes; dense lists compress |
| **Position** | Top-left (LTR) = first seen | Primary action placement; nav order |

Three tiers are usually enough:

| Tier | Treatment |
|---|---|
| **Primary** | Large, bold, dark/high-contrast — the main action or content |
| **Secondary** | Medium, medium-weight, medium-gray — supporting info |
| **Auxiliary** | Small, light, low-contrast — metadata, timestamps, hints |

Color is *not* in the list — color alone is the weakest hierarchy lever (fails for color-blind users and
on low-contrast displays). Use color to *reinforce* hierarchy established by size/contrast/spacing,
never to carry it alone.

## 3. Reading patterns

The eye doesn't scan evenly; it follows predictable paths depending on layout type.

**F-pattern** (dense, text-heavy pages — dashboards, tables, articles):
```
████████████████████
████████████
████████████████████
████████
████████████████████
```
Users scan the left edge vertically, dropping horizontal sprints where something catches attention.
Design implication: put important content on the left; use subheadings and bold leads to pull the
horizontal sprints deeper.

**Z-pattern** (sparse, visual pages — landing pages, heroes, login screens):
```
1──────────────────2
                    │
                    │
3──────────────────4
```
Top-left → top-right → bottom-left → bottom-right. Design implication: logo top-left, primary CTA
top-right or bottom-right, diagonal flow between.

Choose the pattern by content density, not preference. An F-pattern landing page buries the CTA; a
Z-pattern dashboard wastes the scan.

## 4. Squint test

Blur your eyes (or literally squint) until text is unreadable. What remains visible is the hierarchy a
glance perceives:

- If the primary action and headline still stand out → hierarchy holds.
- If everything blurs to equal weight → there is no hierarchy; decoration is carrying nothing.
- If the wrong element stands out (a decorative gradient over the CTA) → hierarchy is inverted.

A layout that fails the squint test cannot be rescued by color or copy. Fix the size/contrast/spacing
hierarchy first.

## 5. 5-second test

Show the screen to someone for 5 seconds, then hide it and ask:

- What is this for?
- What's the main thing you'd do here?

If they can't answer both, the hierarchy isn't communicating the page's purpose. The 5-second test
measures whether the *primary* signal cuts through — it doesn't test details, and that's the point.

## 6. CRAP principles (expanded)

Robin Williams' four principles — the root of visual organization (design-principles §1). Each traces
to a Gestalt law:

### Contrast
Different things must look *visibly* different — not "slightly" different. A 14px body and 15px
subheading have no contrast; a 14px body and 20px bold heading do. Contrast is binary in effect: either
the eye sees a difference or it doesn't. When in doubt, increase the gap, not narrow it.

**Anti-pattern:** 5 shades of gray in a palette where users can't tell which is which.

### Repetition
Same things must look the same — consistency. Every primary button uses the same color, radius, padding,
and typography. Repetition is what makes a design *system* rather than a collection of one-offs. Tokens
(`design-tokens.md`) exist to make repetition mechanical, not manual.

**Anti-pattern:** three different "primary button" styles across the app because each page was styled
independently.

### Alignment
Every element aligns to another element along a visible or invisible line. Nothing floats arbitrarily.
Alignment creates the invisible structure the eye reads as "designed" vs "assembled."

**Anti-pattern:** centering everything (the default of people unsure what else to do); labels misaligned
to their inputs.

### Proximity
Related elements close; unrelated far. The space *between* groups is as meaningful as the space *within*
them. Proximity is the cheapest, most powerful grouping tool — cheaper than borders, boxes, or color.

**Anti-pattern:** a form where every field is equidistant from the next, so sections don't read as
sections; or a sidebar where nav items are crammed with no group separation.

## 7. How this connects

- **Gestalt** explains *why* grouping works → apply via **proximity and similarity**.
- **Hierarchy** decides *what stands out* → apply via **size/contrast/spacing/position** (not color).
- **Reading patterns** predict *where the eye goes* → apply via **F or Z layout** by content type.
- **Squint + 5-second tests** verify the hierarchy *actually communicates* → run before shipping.
- **CRAP** is the checklist for visual organization → contrast, repetition, alignment, proximity.

These are theory; `palettes.md` (color), `font-pairings.md` (type), `design-tokens.md` (system), and
`anti-tells.md` (forbidden patterns) are the application. Load theory first when the question is "why
does this look off"; load application when the question is "what values do I use."
