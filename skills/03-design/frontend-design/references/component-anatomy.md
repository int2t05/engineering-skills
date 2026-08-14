# Component Anatomy

How to decompose a component into parts, variants, and states. This reference defines
the structural patterns for building composable, variant-rich components. Load when
designing a new component from scratch or refactoring an existing one into parts.

## Contents

- [When to load this](#when-to-load-this)
- [Part-based design (compound components)](#part-based-design-compound-components)
- [Slot architecture](#slot-architecture)
- [Variant architecture](#variant-architecture)
- [Component composition patterns](#component-composition-patterns)
- [Accessibility anatomy](#accessibility-anatomy)
- [Anti-patterns](#anti-patterns)
- [Verify](#verify)

## When to load this

- Designing a compound component (Card with Header/Body/Footer, Modal with Title/Content/Actions).
- Defining a variant architecture (a Button with size/variant/state axes).
- Refactoring a monolithic component into composable parts.

## Part-based design (compound components)

A compound component exposes sub-parts as named children. The parent owns layout; the
parts own their content. This lets callers compose freely without prop drilling.

```
<Card>
  <Card.Header>
    <Card.Title>Dashboard</Card.Title>
    <Card.Action>Settings</Card.Action>
  </Card.Header>
  <Card.Body>
    Content here.
  </Card.Body>
  <Card.Footer>
    <Button>Save</Button>
  </Card.Footer>
</Card>
```

Rules:
- **The parent owns layout** (flex direction, gap, padding). Parts don't set their own
  margins — the parent's gap handles spacing.
- **Parts own their content and states** (hover, focus, disabled), not layout.
- **Slots, not props** — `Card.Header` is a slot, not a `headerText` prop. Props are for
  configuration; slots are for composition.
- **Context for shared state** — if Header needs to know the Card's variant (e.g.,
  `bordered`), use React Context, not prop drilling.

## Slot architecture

A slot is a designated region in a component's layout that accepts content. Define slots
explicitly:

| Slot pattern | When | Example |
|---|---|---|
| **Named child** | Fixed set of regions, caller composes | `Card.Header`, `Card.Body` |
| **Render prop** | Region's content depends on parent state | `renderHeader={(user) => <Avatar src={user.img} />}` |
| **Pass-through** | Caller provides the whole element | `<Card header={<MyHeader />}>` |

Default to named children (most composable). Use render props only when the slot needs
parent state. Use pass-through when the caller already has a built element.

## Variant architecture

Variants are orthogonal axes. A Button has `variant` (primary/secondary/ghost),
`size` (sm/md/lg), and `state` (default/hover/focus/disabled/loading). Each axis is
independent — 3 variants × 3 sizes × 5 states = 45 combinations, but you define 3+3+5,
not 45.

### Defining variants

| Axis | Values | Token driver |
|---|---|---|
| `variant` | primary / secondary / ghost / destructive | `color-*` tokens (bg, text, border per variant) |
| `size` | sm / md / lg | `spacing-*` (padding) + `typography-size-*` (font size) |
| `state` | default / hover / focus / active / disabled / loading | opacity, shadow, cursor tokens |

Rules:
- **Each axis maps to tokens, not hardcoded values.** Variant primary →
  `color-accent-primary` token, not `#3b82f6`.
- **States are CSS, not JS** — hover/focus/active are `:hover`/`:focus`/`:active`
  selectors, not conditional classes. Disabled and loading are props (JS-driven state).
- **Document the matrix** — list the axes and their values in the component's doc
  comment. A 45-combination matrix that's really 3+3+5 must read as 3+3+5.

## Component composition patterns

### As child (polymorphic)

A component that renders as a different element (Button as `<a>`, Card as `<button>`):

```tsx
<Button as="a" href="/docs">Read docs</Button>
```

Use when the visual component needs to be a different semantic element. The `as` prop
swaps the root element; all other props (variant, size) still apply.

### Forwarded refs

Every composable component forwards refs:

```tsx
const Button = forwardRef<HTMLButtonElement, ButtonProps>(({ variant, ...props }, ref) => (
  <button ref={ref} className={variants(variant)} {...props} />
));
```

Without ref forwarding, callers can't focus, measure, or animate the component from
outside.

### Class merging (cn / clsx)

When a component accepts a `className` prop, merge it with the component's own classes:

```tsx
<button className={cn(baseStyles, variantStyles[variant], className)} />
```

The caller's `className` wins (appended last) — they can override without fighting the
component's defaults.

## Accessibility anatomy

Every interactive component has an accessibility contract:

| Part | Role | Requirement |
|---|---|---|
| Root | `button` / `link` / `tab` | Correct semantic element or ARIA role |
| Label | text content or `aria-label` | Accessible name present |
| State | `aria-disabled` / `aria-busy` | Reflects JS-driven state (disabled, loading) |
| Focus | `:focus-visible` | Visible focus ring (never `outline: none` without replacement) |

A component is not done until its accessibility contract is documented and verified.
See `ux-guidelines.md` Category 1 for the full a11y rule set.

## Anti-patterns

- **Monolithic component** — one giant component with 20 props for layout, content, and
  state. Split into parts.
- **Prop drilling variant** — passing `variant` through 5 levels of children. Use Context.
- **Hardcoded values in variants** — `if (variant === 'primary') return '#3b82f6'`. Use
  tokens.
- **CSS-in-JS state conditions** — `isHovered && styles.hover`. Use `:hover` selector.
- **Missing ref forwarding** — caller can't control focus or measurement.

## Verify

- Parts are named children (slots), not prop-drilled configuration.
- Variant axes are orthogonal and each maps to tokens.
- States use CSS selectors where possible (`:hover`), props only for JS-driven state.
- Refs are forwarded on every composable component.
- `className` is merged with `cn()` / `clsx`, caller wins.
- Accessibility contract documented (role, label, state, focus).
