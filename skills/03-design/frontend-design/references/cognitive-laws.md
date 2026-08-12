# Cognitive Laws

Depth reference for the `frontend-design` skill. The psychology laws that govern how fast and accurately
users perceive and act on an interface. Each law has a concrete UI consequence — not abstract theory,
but constraints on component and layout decisions.

## 1. Hick's Law

**Decision time grows with the number and complexity of choices.**

Every additional option adds cognitive cost. The cost isn't linear — similar options (3 plans that
differ in one field) cost less to parse than dissimilar ones (3 unrelated actions).

| UI consequence |
|---|
| Menus with 12 items slow users vs 4-item menus with progressive disclosure |
| Settings pages chunked into sections beat one long list |
| A primary CTA + secondary link beats 3 equal-weight buttons |
| Filter facets with sensible defaults reduce the decision space |

Apply: reduce options, group related options, default the common path. When you can't reduce options,
structure them so the common one is obvious (default selected, visually prominent).

## 2. Fitts's Law

**Time to reach a target = f(distance, size). Closer and bigger = faster.**

The math: `MT = a + b·log₂(D/W + 1)` — time grows with distance to the target and shrinks with target
width. The practical extracted rules:

| UI consequence |
|---|
| Touch targets ≥ 44pt (Apple HIG) / 48dp (Material) — small targets are slow and miss-prone |
| Primary buttons are large and span the reachable zone on mobile |
| Destructive actions are placed *far* from common actions (distance as a safety mechanism) |
| Edge/corner targets are effectively infinite-size on desktop (cursor stops at screen edge) — put menus there |

Apply: enlarge important targets, shorten the path to them, and use distance deliberately to protect
against accidental destructive clicks.

## 3. Miller's 7±2

**Working memory holds about 7 (±2) chunks at once.**

People can't hold a long list in their head. "Chunks" are grouped units — a 10-digit phone number is
3 chunks (3-3-4), not 10.

| UI consequence |
|---|---|
| Navigation with 7±2 top-level items; deeper items go in submenus |
| Long forms chunked into steps (3 steps of 4 fields beat 12 fields at once) |
| Phone/credit-card numbers formatted with separators, not one bare string |
| Dashboards show 5-7 KPIs at the top level; the rest drill down |

Apply: chunk everything serial. If a user would have to remember more than ~7 things to complete a
task, the interface is holding the memory for them — show state, not hide it (design-principles §8).

## 4. Tesler's Law (complexity conservation)

**Every application has an irreducible amount of complexity. You can only decide who bears it.**

You can't eliminate complexity; you can move it. The choice: the user bears it (more steps, more
decisions) or the developer/system bears it (more code, more defaults, more automation).

| Decision | User bears | System bears |
|---|---|---|
| Date entry | User types format | System parses natural language, shows a picker |
| Setup | User configures 20 options | System ships sane defaults, surfaces advanced later |
| Error handling | User reads error, decides fix | System auto-recovers, logs transparently |

Apply: move complexity to the system when it's routine and predictable; leave it to the user when it's
a genuine judgment only they can make. Hiding complexity behind "magic" that fails opaquely is worse
than surfacing it.

## 5. Von Restorff effect

**The item that differs from its surroundings is the one remembered.**

The "isolation effect": in a list, the visually distinct item is recalled. This is why a single accent
color on a neutral palette directs attention.

| UI consequence |
|---|
| One primary CTA in the accent color; secondary actions neutral |
| The selected/active state is visually distinct from inactive siblings |
| A critical warning stands out from routine UI |
| Over-use kills the effect: if everything is highlighted, nothing is |

Apply: reserve visual distinction for the one thing that matters most per screen. The 60/30/10 color
formula (`palettes.md`) is Von Restorff operationalized — 10% accent is the remembered element.

## 6. Serial position effect

**First and last items in a sequence are recalled best; the middle is forgotten.**

| Position | Recall |
|---|---|
| **Primacy** (first) | Strong — the anchor, the expectation-setter |
| **Recency** (last) | Strong — the most recent, the action-taken |
| **Middle** | Weak — blurred into "the rest" |

| UI consequence |
|---|
| Put the most important nav item first; the least critical in the middle |
| End a flow on a clear success state (recency shapes the memory of the whole flow) |
| In a long list, the first and last options are chosen disproportionately |
| Form steps: front-load the easy/important, end on confirmation |

Apply: first and last positions are premium real estate. Don't waste the first nav slot on "Home" if a
deeper action matters more; don't end a flow on a blank state.

## 7. Cognitive load — three types

| Type | Source | Reduction strategy |
|---|---|---|
| **Intrinsic** | The task itself is hard | You can't remove it; chunk it, provide guidance, accept slower completion |
| **Extraneous** | The interface adds friction the task doesn't need | **Kill this.** This is the only load fully in your control |
| **Germane** | Effort spent understanding/learning the system | Reduce when possible, but some is necessary for capable tools |

Extraneous load is the design's fault: inconsistent patterns, unclear labels, hidden state, decorative
noise. Every extraneous load reduction frees cognitive budget for the task itself.

## 8. Progressive disclosure (the load-reduction pattern)

Show the common path; hide the advanced. Reveal complexity only when the user signals they need it.

```
Default view:  [ common options, the 80% path ]
                    ↓ (user clicks "Advanced")
Expanded view: [ common + advanced options ]
```

Rules:
- **Default to the common case** — pre-select the option 80% of users need.
- **Surface the advanced, don't bury it** — "Advanced" is visible, not hidden in a menu three levels
  deep.
- **Never hide critical actions behind disclosure** — disclosure is for options, not for the primary
  path.
- **Pair with chunking** — a 30-field form with progressive disclosure becomes 5 fields + 25 advanced,
  not 30 fields with a toggle.

## 9. Other load-reduction patterns

- **Defaults** — pre-fill what you can correctly infer. A pre-filled default removes a decision.
- **Remove distractions** — one primary action per screen; secondary actions visually subordinate.
- **Recognition over recall** — show options as visible choices, not commands to remember
  (design-principles §8).
- **Grouping** — related fields together reduce the scan cost (Gestalt proximity).

The combined effect: a user who would face 12 decisions on a flat form faces 3 + "show advanced" — the
same capability, a fraction of the cognitive cost.
