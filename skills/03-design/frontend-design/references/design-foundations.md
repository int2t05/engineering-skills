# Design Foundations

Condensed from the former cognitive-laws, color-theory, gestalt-and-hierarchy, typography-fundamentals, usability-heuristics, and information-architecture references.

The psychology, theory, and evaluation frameworks beneath a usable interface: how the brain groups and perceives elements, how users decide and remember, how color and type carry meaning, how hierarchy directs the eye, how heuristics surface flaws, and how content organization makes things findable. Each principle below has a concrete UI consequence — not abstract theory, but constraints on component and layout decisions.

## Contents

- [Perception & Gestalt](#perception--gestalt)
- [Cognitive Laws](#cognitive-laws)
- [Color](#color)
- [Typography](#typography)
- [Hierarchy & Layout](#hierarchy--layout)
- [Usability Heuristics](#usability-heuristics)
- [Information Architecture](#information-architecture)

## Perception & Gestalt

The brain groups elements before it reads them. Use grouping to imply structure without drawing it. Related things go close and look similar; unrelated things go far and look different. Most "messy" layouts violate proximity (everything equidistant) or similarity (inconsistent styling for the same role).

| Principle | Rule | UI application |
|---|---|---|
| **Proximity** | Elements close together are seen as related | Group form field + label; space sections apart |
| **Similarity** | Elements that look alike are seen as related | Same button style = same action type; same color = same category |
| **Continuity** | Elements on a line or curve are seen as a group | Aligned columns; a progress bar reads as one path |
| **Closure** | The mind completes incomplete shapes | A card with a gap still reads as a card; don't over-border |
| **Common fate** | Elements moving together are seen as related | A staggered list reveal animates as one group |
| **Figure-ground** | The eye separates a focal element from its background | Contrast the active element against the field; modal scrim |

## Cognitive Laws

The psychology laws that govern how fast and accurately users perceive and act on an interface.

### Hick's Law
**Decision time grows with the number and complexity of choices.** Every additional option adds cognitive cost; similar options cost less to parse than dissimilar ones.

- Menus with 4 items + progressive disclosure beat 12-item menus.
- Settings chunked into sections beat one long list.
- A primary CTA + secondary link beats 3 equal-weight buttons.
- Sensible filter defaults reduce the decision space.

Reduce options, group related ones, default the common path. When you can't reduce, make the common option obvious (default selected, visually prominent).

### Fitts's Law
**Time to reach a target = f(distance, size). Closer and bigger = faster.** `MT = a + b·log₂(D/W + 1)` — time grows with distance, shrinks with width.

- Touch targets ≥ 44pt (Apple HIG) / 48dp (Material) — small targets are slow and miss-prone.
- Primary buttons are large and span the reachable zone on mobile.
- Destructive actions placed *far* from common ones (distance as safety).
- Edge/corner targets are effectively infinite-size on desktop (cursor stops at screen edge) — put menus there.

Enlarge important targets, shorten the path to them, use distance deliberately to protect against accidental destructive clicks.

### Miller's 7±2
**Working memory holds about 7 (±2) chunks at once.** "Chunks" are grouped units — a 10-digit phone number is 3 chunks (3-3-4), not 10.

- Navigation with 7±2 top-level items; deeper items go in submenus.
- Long forms chunked into steps (3 steps of 4 fields beat 12 at once).
- Phone/credit-card numbers formatted with separators, not one bare string.
- Dashboards show 5-7 KPIs at the top level; the rest drill down.

Chunk everything serial. If a user must remember more than ~7 things to complete a task, the interface is holding the memory for them — show state, don't hide it.

### Tesler's Law (complexity conservation)
**Every application has irreducible complexity. You can only decide who bears it.** The choice: the user (more steps, decisions) or the system (more code, defaults, automation).

| Decision | User bears | System bears |
|---|---|---|
| Date entry | Types format | Parses natural language, shows a picker |
| Setup | Configures 20 options | Ships sane defaults, surfaces advanced later |
| Error handling | Reads error, decides fix | Auto-recovers, logs transparently |

Move complexity to the system when routine and predictable; leave it to the user when it's a genuine judgment only they can make. Hiding complexity behind "magic" that fails opaquely is worse than surfacing it.

### Von Restorff effect
**The item that differs from its surroundings is the one remembered.** In a list, the visually distinct item is recalled — why a single accent color on a neutral palette directs attention.

- One primary CTA in the accent color; secondary actions neutral.
- The selected/active state is visually distinct from inactive siblings.
- A critical warning stands out from routine UI.
- Over-use kills the effect: if everything is highlighted, nothing is.

Reserve visual distinction for the one thing that matters most per screen. The 60/30/10 color formula (below) is Von Restorff operationalized — the 10% accent is the remembered element.

### Serial position effect
**First and last items in a sequence are recalled best; the middle is forgotten.**

| Position | Recall |
|---|---|
| **Primacy** (first) | Strong — the anchor, the expectation-setter |
| **Recency** (last) | Strong — the most recent, the action-taken |
| **Middle** | Weak — blurred into "the rest" |

- Put the most important nav item first; least critical in the middle.
- End a flow on a clear success state (recency shapes the memory of the whole flow).
- Form steps: front-load the easy/important, end on confirmation.

First and last positions are premium real estate. Don't waste the first nav slot on "Home" if a deeper action matters more; don't end a flow on a blank state.

### Cognitive load — three types

| Type | Source | Reduction strategy |
|---|---|---|
| **Intrinsic** | The task itself is hard | Can't remove it; chunk it, provide guidance, accept slower completion |
| **Extraneous** | The interface adds friction the task doesn't need | **Kill this.** The only load fully in your control |
| **Germane** | Effort spent understanding/learning the system | Reduce when possible, but some is necessary for capable tools |

Extraneous load is the design's fault: inconsistent patterns, unclear labels, hidden state, decorative noise. Every extraneous load reduction frees cognitive budget for the task itself.

### Progressive disclosure (and other load-reduction patterns)

Show the common path; hide the advanced. Reveal complexity only when the user signals they need it.

```
Default view:  [ common options, the 80% path ]
                    ↓ (user clicks "Advanced")
Expanded view: [ common + advanced options ]
```

Rules:
- **Default to the common case** — pre-select the option 80% of users need.
- **Surface the advanced, don't bury it** — "Advanced" is visible, not three levels deep.
- **Never hide critical actions behind disclosure** — disclosure is for options, not the primary path.
- **Pair with chunking** — 30 fields with disclosure becomes 5 + 25 advanced, not 30 with a toggle.

Other load-reduction patterns:
- **Defaults** — pre-fill what you can correctly infer; a pre-filled default removes a decision.
- **Remove distractions** — one primary action per screen; secondary actions subordinate.
- **Recognition over recall** — show options as visible choices, not commands to remember.
- **Grouping** — related fields together reduce scan cost (Gestalt proximity).

## Color

### HSB model
Work in HSB (Hue, Saturation, Brightness), not RGB — it maps to how humans perceive color.

| Channel | Range | Controls |
|---|---|---|
| **Hue (H)** | 0-360° | The color itself (red 0°, yellow 60°, green 120°, cyan 180°, blue 240°, magenta 300°) |
| **Saturation (S)** | 0-100% | How intense (0% = gray, 100% = full color) |
| **Brightness (B)** | 0-100% | How light (0% = black, 100% = full) |

Why HSB over RGB: to make a palette "lighter," change Brightness; "muted," change Saturation; shift hue, change Hue. RGB mixes these — adjusting "lighter" in RGB changes all three channels unpredictably. HSB separates the dimensions the way you actually think about color.

### Five color schemes
Pick hues from the wheel by relationship:

| Scheme | How | Best for |
|---|---|---|
| **Monochromatic** | One hue, vary S/B | Most stable; low-risk; single-tone brand |
| **Analogous** | Adjacent hues (±30°) | Harmonious; natural; calm palettes |
| **Complementary** | Opposite hues (180°) | Strongest contrast; use sparingly (one accent) |
| **Triadic** | Three equidistant (120°) | Lively; balanced; needs careful proportion |
| **Split-complementary** | One + two adjacent to its opposite | Softer than complementary; contrast without tension |

Rules:
- **Complementary is for accents, not pairs** — red text on green vibrates and is exhausting. Use as one accent against neutral.
- **Triadic needs proportion discipline** — three equal colors fight; pick one dominant, one secondary, one accent.
- **Analogous rarely clashes** — safest scheme; hard to make ugly, easy to make bland.

### The 70:25:5 rule
Color proportion, not just choice. Three great colors in equal thirds look noisy; the same three in 70/25/5 look designed.

| Role | Proportion | Hue role |
|---|---|---|
| **Neutral** | 70% | Backgrounds, large surfaces — near-white or near-black, low-saturation |
| **Primary** | 25% | Brand color — secondary surfaces, headings, key UI |
| **Accent** | 5% | The single sharp color — CTAs, critical alerts, the one thing per screen (Von Restorff) |

If two things share the accent color, neither stands out. The finer 60/30/10 split (dominant/surface/accent) expresses the same principle.

### Color psychology
Hue carries emotional association — not absolute (culture and context modulate), but with stable tendencies in a given market:

| Hue | Common association | Typical use |
|---|---|---|
| **Red** | Urgency, danger, passion | Errors, destructive actions, alerts |
| **Orange** | Energy, warmth, affordability | CTAs, enthusiasm, budget brands |
| **Yellow** | Optimism, caution | Warnings, highlights, cheerful accents |
| **Green** | Success, growth, go | Confirmations, positive states, finance |
| **Blue** | Trust, calm, competence | Enterprise, finance, security, tech |
| **Purple** | Creativity, luxury, mystery | Premium, creative tools, AI |
| **Pink/Magenta** | Playful, modern, bold | Consumer, lifestyle, bold brands |
| **Neutral** | Professional, minimal, timeless | Default for serious tools |

Rules:
- **Psychology is a tendency, not a law** — a red CTA works if the brand is red; context overrides defaults.
- **Don't rely on hue alone for meaning** — red = error is meaningless to a color-blind user. Always pair with an icon, word, or shape.
- **Semantic colors are non-negotiable** — error/success/warning/info each get a dedicated hue, used consistently.

### Cultural variance
Color meaning shifts across cultures — critical for i18n products:

| Color | West | East |
|---|---|---|
| **Red** | Danger, stop | Luck, prosperity, celebration (China) |
| **White** | Purity, weddings | Mourning, funerals (parts of Asia) |
| **Green** | Safety, money | Religion (Islam), infidelity (China, historically) |
| **Blue** | Corporate, male | Immortality, heaven (parts of Middle East) |

Research the target market's associations before locking the palette.

### The gray-test
Desaturate the screenshot (view in grayscale). If the hierarchy is still clear, the palette is working — contrast and luminance carry the structure. If it turns to mush, you relied on hue alone, which fails for color-blind users and weakens the design.

The gray-test is the fastest color-blindness check: if it passes in grayscale, it passes for most color-vision deficiencies. Pair with a WCAG contrast-ratio check (4.5:1 / 3:1) for the full a11y picture.

### Color temperature

| | Warm | Cool |
|---|---|---|
| **Hues** | Red, orange, yellow | Blue, green, purple |
| **Feel** | Energetic, intimate, advancing | Calm, professional, receding |
| **Use** | CTAs, urgency, warmth in brand | Trust, calm backgrounds, spaciousness |

A palette is usually one temperature dominant. Mixing warm and cool equally creates tension (sometimes intended, usually accidental). Warm colors appear to "advance"; cool "recede" — useful for layering (warm accents on cool backgrounds pop).

### Dark mode color adjustments
Dark mode is not "invert the light palette." Key shifts:
- **Desaturate + lighten accents** — a saturated blue that pops on white looks muddy and vibrates on dark. Reduce saturation, raise brightness.
- **Elevation via lighter darks** — raised surfaces are *lighter* darks, not darker (opposite of light mode).
- **Body text is not pure white** — pure white on pure black vibrates. Use a near-white (slate-50).
- **Shadows are weaker** — on dark backgrounds, shadows barely read; rely on elevation + borders.
- **Reduce font weight by one step** — bold text looks muddy on dark.

## Typography

### Font anatomy
The parts of a letterform that determine readability and character:

| Part | What | Affects |
|---|---|---|
| **x-height** | Height of lowercase 'x' | High x-height = more readable at small sizes |
| **Ascenders** | Strokes rising above x-height (b, d, f, h, k, l, t) | Distinguish letters; long = elegant, short = compact |
| **Descenders** | Strokes dropping below baseline (g, j, p, q, y) | Need line-height to accommodate |
| **Counters** | Enclosed negative space (a, e, o, p) | Small counters fill in at small sizes → open counters for UI |
| **Terminals** | Ends of strokes | Rounded = friendly; flat = technical; ball = editorial |
| **Stroke contrast** | Variation between thick and thin | High = elegant but fragile at small sizes; low = sturdy, readable |

For UI: **high x-height + open counters + low contrast** = readable at 12-14px (Inter, system-ui, Roboto). **Low x-height + high contrast** = beautiful at display sizes, illegible at body sizes (Didot) — headings only. A font that looks gorgeous at 48px and falls apart at 13px is a display font, not a UI font.

### Optical sizing
Type is designed for a target size range. The same typeface reshapes itself by size:

| At small sizes | At large sizes |
|---|---|
| Larger x-height | More refined x-height |
| Wider counters | Tighter counters |
| Lower stroke contrast | Higher contrast |
| Heavier weight | Lighter weight for same visual weight |
| More generous spacing | Tighter spacing |

**Variable fonts** with an `opsz` (optical size) axis handle this automatically. With non-variable fonts, pick sizes where the font's design works — don't force a display serif into 12px body.

**Optical weight:** a 400-weight font at 48px looks lighter than the same 400 at 14px. To match visual weight across sizes, bump display text up a weight (400 → 500/600 at large sizes). In dark mode, reduce weight by one step — bold strokes look muddy on dark.

### Vertical rhythm
Align text to a baseline grid so spacing feels structured, not arbitrary. With a 4px base unit:
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
- **Body line-height ≥ 1.5** (WCAG) for readability.
- **Heading line-height 1.2-1.3** — large text needs less leading; extra space breaks the line's unity.
- **Line length 45-75 characters** (desktop), 35-50 (mobile) — longer lines tire; shorter disrupts rhythm.
- Everything snaps to the same base unit → the eye perceives "designed," not "assembled."

### Modular type scale
Don't pick sizes arbitrarily — use a ratio. Each step = previous × ratio:

| Ratio | Name | Character |
|---|---|---|
| 1.125 | Major second | Subtle; fine-grained dashboards |
| 1.2 | Minor third | Balanced; common for product UI |
| 1.25 | Major third | Distinct; marketing-ish |
| 1.333 | Perfect fourth | Strong; editorial, landing pages |
| 1.5 | Perfect fifth | Dramatic; hero sections only |

Example with 1.2 ratio, 16px base: `16 → 20 → 24 → 28 → 32`. Pick the ratio by content character: dense data UI = 1.125; marketing = 1.333+.

### Font rendering and subpixel

| Issue | Cause | Mitigation |
|---|---|---|
| **Blurry at small sizes** | Weak hinting (font's size-specific instructions) | Use well-hinted UI fonts (Inter, system-ui) |
| **Color fringing** | Subpixel rendering on LCD | Worse on Windows ClearType; test cross-platform |
| **Thin strokes vanish** | Subpixel at 12px with light weight | Minimum 400 weight at 12-14px |
| **Inconsistent across OS** | Different renderers per OS | Test on all three; can't fully control |

Rules:
- **12px is the floor** — below, rendering breaks and accessibility fails. Use 12px only for captions/metadata.
- **Test on Windows** — macOS renders type more generously; Windows is the harsh test. If it reads on Windows, it reads everywhere.
- **Antialiasing** — `-webkit-font-smoothing: antialiased` (macOS) darkens text; use for light-on-dark. `auto` for dark-on-light.

### Monospace
Code/data benefits from monospace — each glyph same width, aligning columns.
- **Use for:** code blocks, terminal output, tabular data alignment, version strings.
- **Features:** tabular figures (numbers align in columns), ligatures (optional, for code).
- **Recommended:** SF Mono (Apple), JetBrains Mono, Fira Code.
- **Size:** match body text, or one step smaller (13-14px against 16px body).

## Hierarchy & Layout

### Visual hierarchy — four techniques
Hierarchy is established through four levers, in roughly this priority:

| Technique | How | Strongest when |
|---|---|---|
| **Size** | Larger = more important | Heading vs body; primary CTA vs secondary |
| **Contrast** | Darker/bolder/saturated = more important | Primary text vs muted helper text |
| **Spacing** | More space around = more importance | Hero section breathes; dense lists compress |
| **Position** | Top-left (LTR) = first seen | Primary action placement; nav order |

Three tiers are usually enough: **Primary** (large, bold, high-contrast — the main action or content), **Secondary** (medium, medium-weight, medium-gray — supporting info), **Auxiliary** (small, light, low-contrast — metadata, timestamps, hints).

Color is *not* in the list — color alone is the weakest hierarchy lever (fails for color-blind users and on low-contrast displays). Use color to *reinforce* hierarchy established by size/contrast/spacing, never to carry it alone.

### Reading patterns
The eye doesn't scan evenly; it follows predictable paths depending on layout type.

**F-pattern** (dense, text-heavy pages — dashboards, tables, articles): users scan the left edge vertically, dropping horizontal sprints where something catches attention. Put important content on the left; use subheadings and bold leads to pull the horizontal sprints deeper.

**Z-pattern** (sparse, visual pages — landing pages, heroes, login screens): top-left → top-right → bottom-left → bottom-right. Logo top-left, primary CTA top-right or bottom-right, diagonal flow between.

Choose by content density, not preference. An F-pattern landing page buries the CTA; a Z-pattern dashboard wastes the scan.

### Squint test
Blur your eyes (or literally squint) until text is unreadable. What remains visible is the hierarchy a glance perceives:
- If the primary action and headline still stand out → hierarchy holds.
- If everything blurs to equal weight → no hierarchy; decoration carries nothing.
- If the wrong element stands out (a decorative gradient over the CTA) → hierarchy is inverted.

A layout that fails the squint test cannot be rescued by color or copy. Fix the size/contrast/spacing hierarchy first.

### 5-second test
Show the screen to someone for 5 seconds, then hide it and ask: What is this for? What's the main thing you'd do here? If they can't answer both, the hierarchy isn't communicating the page's purpose. The 5-second test measures whether the *primary* signal cuts through — it doesn't test details, and that's the point.

### CRAP principles
Robin Williams' four principles — the root of visual organization. Each traces to a Gestalt law.

**Contrast** — Different things must look *visibly* different, not "slightly" different. A 14px body and 15px subheading have no contrast; a 14px body and 20px bold heading do. Contrast is binary in effect: either the eye sees a difference or it doesn't. When in doubt, increase the gap, not narrow it. *Anti-pattern:* 5 shades of gray users can't tell apart.

**Repetition** — Same things must look the same — consistency. Every primary button uses the same color, radius, padding, typography. Repetition is what makes a design *system* rather than a collection of one-offs. *Anti-pattern:* three different "primary button" styles across the app because each page was styled independently.

**Alignment** — Every element aligns to another along a visible or invisible line. Nothing floats arbitrarily. Alignment creates the invisible structure the eye reads as "designed" vs "assembled." *Anti-pattern:* centering everything (the default of people unsure what else to do); labels misaligned to their inputs.

**Proximity** — Related elements close; unrelated far. The space *between* groups is as meaningful as the space *within* them. Proximity is the cheapest, most powerful grouping tool — cheaper than borders, boxes, or color. *Anti-pattern:* a form where every field is equidistant so sections don't read as sections; a sidebar where nav items are crammed with no group separation.

## Usability Heuristics

### Nielsen's 10 usability heuristics (1994)
The standard framework for heuristic evaluation. Each with a concrete UI example:

1. **Visibility of system status** — The system shows what's happening, so users trust it and can predict outcomes. Loading bars, skeleton screens, "Saved 2 seconds ago" indicators, progress steps (1 of 4).
2. **Match between system and real world** — Use language and concepts the user knows, not internal jargon. "Shopping cart" not "transactional item buffer"; "That email doesn't match an account" not "AUTH_USER_NOT_FOUND." Organize information the way the user thinks, not the way the database is structured.
3. **User control and freedom** — Users make mistakes; give them an escape hatch. Undo/redo, "Cancel" on every multi-step flow, easy exit from modals/drawers/fullscreen (Esc, backdrop click, explicit close).
4. **Consistency and standards** — Same action = same style, same word, same location. One primary-button style across the app; "Delete" everywhere (not "Remove" here and "Delete" there). Follow platform conventions (Apple HIG / Material) — don't invent gestures users already know.
5. **Error prevention** — Prevent errors before they happen — better than good error messages. Confirm destructive actions, disable submit until required fields valid, inline validation as the user types, constrain input (date picker, not free-text date that must be parsed).
6. **Recognition rather than recall** — Show options and state visibly; don't force users to remember. Visible menu items not CLI-style commands, selected state persists visibly across navigation, recently-used items surfaced.
7. **Flexibility and efficiency of use** — Serve both novices and experts. Keyboard shortcuts for frequent actions (⌘K command palette, j/k navigation), templates and "duplicate" for repeated workflows, customizable density/defaults for power users without confusing novices.
8. **Aesthetic and minimalist design** — Only what's needed. Every extra unit of information competes with the useful. One primary action per screen, remove decoration that carries no meaning, white space is hierarchy (Gestalt proximity) not waste. "Minimal" ≠ stark; it means nothing extraneous.
9. **Help users recognize, diagnose, and recover from errors** — Plain language, the problem's cause, and a next step — not error codes. "We couldn't save your changes. Your connection dropped — retry?" State what went wrong, suggest the fix or offer the recovery action.
10. **Help and documentation** — Accessible when needed, focused on the task, with concrete steps. Contextual help (tooltips, "learn more" next to the relevant field), organized by task not feature, searchable with common tasks first.

### Heuristic Evaluation method
Expert review: walk the interface against the 10 heuristics, note violations, rate severity.

**Severity scale (Nielsen):**

| Rating | Meaning |
|---|---|
| 0 | Not a problem |
| 1 | Cosmetic — fix if time |
| 2 | Minor — low priority |
| 3 | Major — important to fix |
| 4 | Catastrophic — must fix before release |

**Procedure:** Walk each screen/flow 2-3 times independently → for each heuristic, list violations → assign severity → triage (fix all 3-4 first, then 2s, then 1s).

Heuristic evaluation is fast (a few hours for a medium app) and catches the structural issues user testing won't (users won't articulate "this violates consistency" — they'll just feel something's off). It doesn't replace user testing; it precedes it.

### Don Norman — emotional design (three levels)
Usability is necessary but not sufficient. Products are experienced at three levels:

| Level | What it addresses | Design implication |
|---|---|---|
| **Visceral** | The immediate, pre-cognitive reaction to appearance | First impression matters: color, proportion, motion create the gut response |
| **Behavioral** | Usability and pleasure of use | Does it work, feel smooth, give feedback? (the heuristics above) |
| **Reflective** | The user's conscious assessment — self-image, meaning, story | Does using this make the user feel competent / professional / part of something? |

A product that's usable (behavioral) but ugly (visceral) or meaningless (reflective) still loses. All three levels shape whether users return.

### Dieter Rams' 10 principles
The benchmark for "good design" — a check on whether what you've made is actually good, not just shipped:

1. **Innovative** — not derivative; uses technology meaningfully.
2. **Useful** — serves a purpose; no decoration without function.
3. **Aesthetic** — well-made objects affect well-being; ugly tools wear on users.
4. **Understandable** — the product explains itself; structure is clear.
5. **Unobtrusive** — neutral, leaving room for self-expression; not decor.
6. **Honest** — doesn't pretend to be more innovative/powerful than it is.
7. **Long-lasting** — avoids trends; lasts in perception, not just durability.
8. **Thorough down to the last detail** — care and accuracy show respect for the user.
9. **Environmentally friendly** — minimal footprint in production and lifecycle.
10. **As little design as possible** — less, but better. Pure, focused.

Rams' last principle is the purest expression of the design ethic this collection follows: focus on the essential, remove the rest.

**How the three frameworks connect:**
- **Nielsen** is the *evaluation* framework — walk the interface, find violations, fix by severity.
- **Norman** is the *experience* framework — usable is necessary, but visceral and reflective levels also determine whether users return.
- **Rams** is the *quality* framework — the check on whether the design is actually good, not just functional.

## Information Architecture

IA is the skeleton beneath the visual layer — get it wrong and no amount of polish rescues the "I can't find anything" feeling. IA decisions are made before visual decisions: a beautifully styled menu with the wrong items in the wrong order is still a bad menu.

### The four IA elements

| Element | Question it answers | Output |
|---|---|---|
| **Grouping** | What belongs together? | Sections, categories, cards |
| **Hierarchy** | What's under what? | Tree (parent→child), depth, order |
| **Labeling** | What do we call it? | Nav labels, section titles, button text |
| **Journey** | How does a user move through it? | Flows, sequences, next-steps |

An interface with bad grouping feels scattered; bad hierarchy feels flat; bad labeling feels confusing; bad journey feels like a maze. Each fails differently — diagnose which element is broken before restructuring.

### Tree vs network structure

| | Tree | Network |
|---|---|---|
| **Shape** | One-to-many (parent → children) | Many-to-many (any node links to any) |
| **Example** | Sidebar menu, file system | Wiki, linked docs, web of content |
| **Best for** | Wayfinding, administration, predictable nav | Exploration, cross-referencing, non-linear reading |
| **Risk** | Rigid — items don't fit one parent | Lost — no clear "where am I" |
| **Navigation state** | Current location is clear (breadcrumbs, active item) | Current location is fuzzy; needs wayfinding aids |

Most apps are a tree with network pockets: the nav is a tree, but content within links cross-wise. Decide the primary structure (usually tree for apps, network for content/knowledge tools), then add cross-links as enhancement, not replacement.

### Card sorting
Validate IA with real users rather than guessing how they group things.

| Mode | How | When |
|---|---|---|
| **Open** | Users group pre-labeled cards into categories they name themselves | Early — discovering mental models, no existing structure |
| **Closed** | Users sort cards into categories you've defined | Validating an existing/revised structure |

Procedure: write each content item/feature on a card (40-60 manageable) → have 5-8 target users sort independently → look for agreement (grouped together by most = belong together) → disagreement signals a confusing label or genuinely ambiguous item.

Card sorting reveals the *user's* taxonomy, which frequently differs from the *team's* internal taxonomy. Users group by task; teams group by feature/module. Prefer the user's.

### Navigation depth — the 3-click myth
The "everything within 3 clicks" rule is a myth — research shows users will click happily if each click feels like progress toward their goal. The real measure is **predictability**, not click count: at each step, can the user confidently predict what the next click will show? Is the path to any goal obvious, even if it's 5 clicks deep?

| Too shallow | Too deep |
|---|---|
| Top-level menu with 20 items (scanning cost > click cost) | 6-level nesting where users lose their place |
| Broad-and-flat overwhelms | Narrow-and-deep disorients |

Target 2-3 levels for primary navigation; deeper is fine for genuinely hierarchical content (settings, file trees) as long as breadcrumbs and the active state keep the user oriented.

### Labeling systems
Labels are the IA's user-facing surface. Bad labels make good structure unusable.

| Principle | Bad | Good |
|---|---|---|
| **User's language** | "Transactional persistence layer" | "Orders" |
| **Mutually exclusive** | "Tools" + "Utilities" (overlap) | "Tools" + "Settings" (distinct) |
| **Collective, not singular** | "Button" / "Form" (item-level) | "Components" / "Forms" (category-level) |
| **Consistent voice** | Mix of nouns and verbs | One voice (usually nouns for nav, verbs for actions) |
| **Scannable length** | "Configurations and preferences management" | "Settings" |

Test labels by asking a new user to predict what's behind each one. If they guess wrong, the label fails — regardless of how accurate it is internally.

### User journey maps
The journey element made explicit — a user's path through the product to accomplish a goal:

```
Stage      Awareness →  Consideration →  Signup →  First use →  Habitual use →  Churn-risk
Action     lands       compares          signs up  onboarding      daily task      hasn't logged in
Emotion    curious     skeptical         hopeful   confused→abled  smooth          indifferent
Pain       none        "is this real?"   friction  too many steps  none            "forgot it exists"
Opportunity strong hero social proof     reduce    guide first key  power features  re-engagement
```

Journey maps surface where emotion drops and pain spikes — the points that need design attention. They connect IA (where things are) to flow (how users move) to feeling (whether they return).
