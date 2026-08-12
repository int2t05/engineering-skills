# Material Design

Depth reference for the `frontend-design` skill. Google's Material Design 3 (M3) — the counterpart to
`apple-hig.md` for Android and Google-ecosystem products. This file summarizes the M3 system and routes
to official sources for depth; it is not a substitute for the M3 spec.

## 1. When to use Material vs Apple HIG vs custom

| System | Use when |
|---|---|
| **Material 3** | Android-native apps; Google-ecosystem products; cross-platform apps wanting a neutral, well-documented system |
| **Apple HIG** | iOS/iPadOS/macOS/tvOS/visionOS/watchOS native apps (`apple-hig.md`) |
| **A custom system** | A distinctive brand identity that intentionally diverges; products where Material/HIG would look generic |

Rule: when designing for a platform, default to that platform's system. Material on iOS feels wrong;
HIG on Android feels wrong. Cross-platform: pick one and apply consistently, or build a custom system
that respects both platforms' interaction norms (gestures, navigation patterns).

## 2. M3 core principles

Material 3 (Material You) is dynamic, personal, and role-based:

| Principle | Meaning |
|---|---|
| **Dynamic color** | Color system derives from a source color (brand or user wallpaper), generating a full tonal palette |
| **Role-based color** | Colors are assigned *roles* (primary, secondary, tertiary, error, surface) not fixed hex |
| **Large shape variety** | Shapes (corner radius) vary by component and emphasis, not one global radius |
| **Motion as meaning** | Motion communicates hierarchy and state, not decoration |
| **Accessibility-first** | Contrast and touch targets are built into the color and type systems |

## 3. M3 color roles

M3 generates a tonal palette (tones 0-100) from a source color, then assigns roles:

| Role | Use |
|---|---|
| **Primary** | Highest-emphasis buttons, active states, key UI |
| **On-primary** | Text/icon on primary surfaces |
| **Primary container** | Filled containers less prominent than primary |
| **On-primary-container** | Text/icon on primary container |
| **Secondary** | Less prominent components |
| **Tertiary** | Accent, contrasting accents |
| **Error** | Errors, destructive actions |
| **Surface** | Backgrounds, cards |
| **On-surface** | Text on surfaces |
| **Surface variant** | Elevated/alternative surfaces |
| **Outline** | Borders, dividers |

The pattern: every role has a pair (color + "on-color" for content on it). This guarantees contrast by
construction — you never pick a text color and background independently and hope they pass WCAG.

`palettes.md` semantic tokens (text-primary, bg-surface, accent-primary) map to these roles. M3 is the
theory; the tokens are the implementation.

## 4. M3 type roles

M3 type scale is role-based (not numeric H1-H6):

| Role | Size (dp) | Weight | Use |
|---|---|---|---|
| **Display** | 57 / 45 / 36 | 400 | Hero, top-level numbers |
| **Headline** | 32 / 28 / 24 / 22 | 400 | Section headings |
| **Title** | 22 / 16 / 14 | 500 | Card titles, section labels |
| **Body** | 16 / 14 / 12 | 400 | Default text |
| **Label** | 14 / 12 / 11 | 500 | Buttons, labels, overlines |

Each role has large/medium/small variants. The scale is larger and rounder than M2 — M3 favors legible,
prominent type. Compare to `font-pairings.md` scale (text-xs 12 → text-5xl 48) — same intent, M3's
naming is role-based, the skill's is scale-based.

## 5. M3 elevation (5 levels)

Elevation in M3 is layered surfaces with tonal + shadow differences:

| Level | Elevation | Example |
|---|---|---|
| **0** | 0dp | Flat surface (page background) |
| **1** | 1dp | Card on a flat surface |
| **2** | 3dp | FAB, raised button (resting) |
| **3** | 6dp | App bar (scrolled), dialog |
| **4** | 8dp | Navigation drawer, modal |
| **5** | 12dp | Scrolled FAB, popover |

In dark mode, elevation uses *tonal overlay* (lighter surface tones) instead of shadows — shadows
don't read on dark backgrounds (same as `color-theory.md` §8).

## 6. M3 state layers

Every interactive component has a state layer — a semi-transparent overlay communicating its state:

| State | Overlay opacity | When |
|---|---|---|
| **Hover** | 8% (on-content color) | Cursor over (desktop) |
| **Focused** | 10% | Keyboard focus |
| **Pressed** | 10% | Active press |
| **Dragged** | 16% | Being dragged |

The state layer sits *above* the content, using the "on-color" at low opacity. This is more systematic
than ad-hoc hover/focus styles — `component-anatomy.md` variant axes operationalize the same idea
(orthogonal state × variant × size axes mapped to tokens).

## 7. M3 vs M2

| | Material 2 | Material 3 (Material You) |
|---|---|---|
| **Color** | Fixed primary/secondary palette | Dynamic, tonal, role-based |
| **Type** | Numeric scale (H1-H6) | Role-based (display/headline/title/body/label) |
| **Shape** | Consistent per-component radius | Varied shape scale (full, large, medium, small) |
| **Elevation** | Shadow-based | Tonal + shadow (tonal in dark mode) |
| **Personalization** | None | Dynamic color from user source |

M3 is the current system (2021+). New projects use M3; M2 is legacy. The M3 Web implementation
(Material Web Components) and the Tailwind/Radix ecosystem carry M3 patterns into web.

## 8. Official sources

For full specs, route to the official M3 documentation:

- **M3 Design Kit (Figma)** — the canonical components, tokens, color tooling.
- **m3.material.io** — color tool, type tool, shape tool, component specs, accessibility guidance.
- **Material Web Components** — the web implementation (`github.com/material-components/material-web`).

The `brief-inference.md` design-system selection map includes Material Web + M3 as the choice when the
brief signals Google-ecosystem or Android conventions. Load `apple-hig.md` symmetrically when the brief
signals Apple platforms.

## 9. How this connects

- **M3 color roles** ↔ `palettes.md` semantic tokens (role pairs guarantee contrast).
- **M3 type roles** ↔ `font-pairings.md` type scale (role-based vs scale-based naming, same intent).
- **M3 elevation** ↔ `design-tokens.md` elevation/shadow scale + `color-theory.md` dark-mode rules.
- **M3 state layers** ↔ `component-anatomy.md` variant axes (state as a systematic axis, not ad-hoc).
- **M3 shape variety** ↔ `design-tokens.md` radius scale (varied, not one global radius).

Material 3 is a complete, opinionated system. For Android/Google-ecosystem products, adopt it rather
than recreating it — install the official Material Web Components, don't hand-roll Material-styled CSS
(`brief-inference.md` honesty rule). For custom-brand products, borrow M3's *structure* (role-based
color, systematic state layers) without its *look*.
