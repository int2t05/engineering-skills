# Design System Audit

Depth reference for the `frontend-design` skill. How to audit an existing design system
for consistency: token coverage vs hardcoded values, component variant/state/a11y
documentation completeness, and systematic extension patterns. The skill's
`references/design-tokens.md` covers token definition; this covers auditing an existing
implementation for drift from those tokens.

## Contents

- [1. Token coverage vs hardcoded values](#1-token-coverage-vs-hardcoded-values)
- [2. Component variant and state documentation](#2-component-variant-and-state-documentation)
- [3. Accessibility documentation](#3-accessibility-documentation)
- [4. Systematic extension patterns](#4-systematic-extension-patterns)
- [5. Audit checklist](#5-audit-checklist)

## 1. Token coverage vs hardcoded values

A design system's value collapses the moment components bypass tokens. Audit for
hardcoded values that should reference tokens.

### What to scan for

| Pattern | Find it | Fix |
|---|---|---|
| Raw hex colors | `grep -rn '#[0-9a-fA-F]\{3,6\}' src/` | Replace with `var(--color-*)` |
| Hardcoded spacing | `padding: 16px` instead of token | Replace with `var(--space-*)` |
| Magic radii | `border-radius: 8px` scattered | Replace with `var(--radius-*)` |
| Inline font sizes | `font-size: 14px` | Replace with type-scale token |
| Fixed z-index | `z-index: 999` | Replace with `var(--z-*)` tier |
| Hardcoded shadows | `box-shadow: 0 2px 4px rgba(...)` | Replace with `var(--elevation-*)` |

### Coverage metric

```
Token coverage = (values via token) / (total style values) × 100%
```

Target: ≥ 90% of colors, spacing, radii, and typography come from tokens. The remaining
10% is one-off values that genuinely don't fit a scale (documented with a comment
explaining why).

### Drift detection in CI

Run the scan in CI so regressions fail the build. A new `#3b82f6` in a component is a
review blocker — either it's a new token (add it to the system) or it's drift (use the
existing token). Stylelint with a custom rule, or a grep-based script, catches this
before review.

## 2. Component variant and state documentation

Every component must document its variant axes and interaction states. An undocumented
variant is an inconsistency waiting to happen.

### Variant axes

For each component, list the axes along which it varies:

| Component | Variant axes |
|---|---|
| Button | size (sm/md/lg), variant (primary/secondary/ghost), destructive (true/false) |
| Input | size, invalid (true/false), disabled |
| Card | elevation (flat/raised), padding (compact/default) |

Each axis maps to a token or a set of style differences. If a component has a variant
that isn't in this table, it's an ad-hoc addition — either formalize it or remove it.

### State matrix

Every interactive component must define all six states. Audit for missing ones:

| State | How to verify |
|---|---|
| **Default** | Rendered without interaction |
| **Hover** | Mouse over; pointer appears |
| **Focus** | Tab to it; focus ring visible (never `outline: none` without replacement) |
| **Pressed** | Mouse down; visual feedback |
| **Disabled** | `disabled` attr; reduced opacity; not clickable |
| **Loading** | Skeleton or spinner; button shows loading state |

A component missing focus or pressed state is an accessibility and polish bug. Document
the missing state, then implement it.

## 3. Accessibility documentation

Each component must document its a11y contract — not just "it's accessible" but the
specific patterns used.

| Concern | Document |
|---|---|
| **Role** | What ARIA role, if any (e.g. `dialog`, `tablist`) |
| **Keyboard** | Which keys operate it (Enter, Space, Escape, arrows) |
| **Focus management** | Where focus goes on open, close, and after action |
| **Screen reader** | What `aria-label` / `aria-describedby` is needed |
| **Color contrast** | Token pairs that meet 4.5:1 (text) / 3:1 (large, UI components) |
| **Motion** | `prefers-reduced-motion` behavior documented |

### Audit method

1. Tab through every component — can you operate it without a mouse?
2. Run axe-core / Lighthouse on a page using the component.
3. Test with a screen reader (NVDA, VoiceOver) — does it announce correctly?
4. Verify `prefers-reduced-motion` disables non-essential animation.

## 4. Systematic extension patterns

When a new need arises, extend the system — don't add a one-off. The pattern:

### Add a token, not a value

Need a new spacing? Add `--space-5` to the scale, don't hardcode `48px` in one component.
The scale stays coherent; every component can use the new token.

### Add a variant, not a new component

Need a "danger button"? Add `variant: 'destructive'` to the existing Button, don't create
a `DangerButton`. The component API stays unified; the variant is discoverable.

### Deprecate, don't delete

When replacing a token or variant, deprecate the old one with a clear migration path.
A sudden removal breaks every consumer; a deprecation gives teams time to migrate.

| Extension type | Wrong approach | Right approach |
|---|---|---|
| New color | Hardcode hex in component | Add to palette, create semantic token |
| New spacing | Magic number | Extend the spacing scale |
| New component variant | Copy-paste a new component | Add variant axis to existing component |
| New icon size | Arbitrary pixel value | Add to icon-size scale |

## 5. Audit checklist

- [ ] Token coverage ≥ 90% (colors, spacing, radii, typography, elevation, z-index)
- [ ] CI scan blocks new hardcoded values
- [ ] Every component has a documented variant-axis table
- [ ] Every interactive component defines all six states (default/hover/focus/pressed/disabled/loading)
- [ ] Every component documents its a11y contract (role, keyboard, focus, SR, contrast, motion)
- [ ] No `outline: none` without an accessible focus replacement
- [ ] Extensions follow the add-token/add-variant pattern, not one-off values
- [ ] Deprecated tokens/variants have a migration path and a removal date
