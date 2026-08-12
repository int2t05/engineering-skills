# Information Architecture

Depth reference for the `frontend-design` skill. How to organize content so users find what they need:
the four IA elements, tree vs network structures, card sorting, navigation depth, labeling systems, and
journey maps. IA is the skeleton beneath the visual layer — get it wrong and no amount of polish
rescues the "I can't find anything" feeling.

## 1. The four IA elements

| Element | Question it answers | Output |
|---|---|---|
| **Grouping** | What belongs together? | Sections, categories, cards |
| **Hierarchy** | What's under what? | Tree (parent→child), depth, order |
| **Labeling** | What do we call it? | Nav labels, section titles, button text |
| **Journey** | How does a user move through it? | Flows, sequences, next-steps |

An interface with bad grouping feels scattered; bad hierarchy feels flat; bad labeling feels confusing;
bad journey feels like a maze. Each fails differently — diagnose which element is broken before
restructuring.

## 2. Tree vs network structure

| | Tree | Network |
|---|---|---|
| **Shape** | One-to-many (parent → children) | Many-to-many (any node links to any) |
| **Example** | Sidebar menu, file system | Wiki, linked docs, web of content |
| **Best for** | Wayfinding, administration, predictable nav | Exploration, cross-referencing, non-linear reading |
| **Risk** | Rigid — items don't fit one parent | Lost — no clear "where am I" |
| **Navigation state** | Current location is clear (breadcrumbs, active item) | Current location is fuzzy; needs wayfinding aids |

Most apps are a tree with network pockets: the nav is a tree, but content within links cross-wise.
Decide the primary structure (usually tree for apps, network for content/knowledge tools), then add
cross-links as enhancement, not replacement.

## 3. Card sorting

Validate IA with real users rather than guessing how they group things.

| Mode | How | When |
|---|---|---|
| **Open** | Users group pre-labeled cards into categories they name themselves | Early — discovering mental models, no existing structure |
| **Closed** | Users sort cards into categories you've defined | Validating an existing/revised structure |

Procedure:
1. Write each content item / feature on a card (40-60 is manageable).
2. Have 5-8 target users sort independently.
3. Look for agreement: items grouped together by most users belong together.
4. Disagreement signals either a confusing label or a genuinely ambiguous item — sharpen or split.

Card sorting reveals the *user's* taxonomy, which frequently differs from the *team's* internal
taxonomy. Users group by task; teams group by feature/module. Prefer the user's.

## 4. Navigation depth — the 3-click myth

The "everything within 3 clicks" rule is a myth — research shows users will click happily if each click
feels like progress toward their goal. The real measure is **predictability**, not click count:

- At each step, can the user confidently predict what the next click will show?
- Is the path to any goal obvious, even if it's 5 clicks deep?

| Too shallow | Too deep |
|---|---|
| Top-level menu with 20 items (scanning cost > click cost) | 6-level nesting where users lose their place |
| Broad-and-flat overwhelms | Narrow-and-deep disorients |

Target 2-3 levels for primary navigation; deeper is fine for genuinely hierarchical content (settings,
file trees) as long as breadcrumbs and the active state keep the user oriented.

## 5. Labeling systems

Labels are the IA's user-facing surface. Bad labels make good structure unusable.

| Principle | Bad | Good |
|---|---|---|
| **User's language** | "Transactional persistence layer" | "Orders" |
| **Mutually exclusive** | "Tools" + "Utilities" (overlap) | "Tools" + "Settings" (distinct) |
| **Collective, not singular** | "Button" / "Form" (item-level) | "Components" / "Forms" (category-level) |
| **Consistent voice** | Mix of nouns and verbs | One voice (usually nouns for nav, verbs for actions) |
| **Scannable length** | "Configurations and preferences management" | "Settings" |

Test labels by asking a new user to predict what's behind each one. If they guess wrong, the label
fails — regardless of how accurate it is internally.

## 6. User journey maps

The journey element made explicit — a user's path through the product to accomplish a goal:

```
Stage      Awareness →  Consideration →  Signup →  First use →  Habitual use →  Churn-risk
Action     lands       compares          signs up  onboarding      daily task      hasn't logged in
Emotion    curious     skeptical         hopeful   confused→abled  smooth          indifferent
Pain       none        "is this real?"   friction  too many steps  none            "forgot it exists"
Opportunity strong hero social proof     reduce    guide first key  power features  re-engagement
```

Journey maps surface where emotion drops and pain spikes — the points that need design attention. They
connect IA (where things are) to flow (how users move) to feeling (whether they return).

## 7. How this connects to the skill

`frontend-design` Step 1 (Define element + context) and the `docs/design/DESIGN.md` output call for
"information architecture." This reference is the method behind that deliverable:

- **Grouping + hierarchy** → the nav structure and page layout.
- **Labeling** → every nav item, section title, and button.
- **Journey** → the user flows (cross-references `docs/FLOW/*.md` from the `breakdown`/flow skills).

IA decisions are made before visual decisions — a beautifully styled menu with the wrong items in the
wrong order is still a bad menu. Load this reference when the question is "what goes where and what do
we call it," before "what does it look like."
