# WCAG 2.2 AA Checklist — Mapped to axe-core + Manual Checks

The criterion-by-criterion checklist for an a11y review. WCAG 2.2 AA is the default
target (it covers 2.1 AA plus new criteria). Each criterion notes whether axe-core
catches it automatically or it requires a manual check.

## Perceivable

| Criterion | What to check | axe? |
|---|---|---|
| 1.1.1 Non-text content | Every meaningful image has `alt`; decorative images have `alt=""`; complex images have a text alternative nearby | auto |
| 1.3.1 Info & relationships | Form fields have `<label>` (or `aria-label`/`aria-labelledby`); tables use `<th scope>`; lists use semantic `<ul>/<ol>`; headings use `<h1>`–`<h6>` | auto + manual |
| 1.3.2 Meaningful sequence | DOM order matches visual reading order (flex/grid reorder can break this) | manual |
| 1.4.1 Use of color | Information/action not conveyed by color alone (errors have text/icon, not just red) | manual |
| 1.4.3 Contrast (minimum) | Text contrast ≥ 4.5:1 (large text ≥ 3:1) against its background | auto |
| 1.4.11 Non-text contrast | UI component boundaries and state indicators ≥ 3:1 contrast | auto |
| 1.4.13 Content on hover/focus | Hover/focus content is dismissible, hoverable, persistent | manual |

## Operable

| Criterion | What to check | axe? |
|---|---|---|
| 2.1.1 Keyboard | Every interactive element is operable via keyboard alone | manual |
| 2.1.2 No keyboard trap | Focus doesn't get stuck (modals must trap and release correctly) | manual |
| 2.4.1 Bypass blocks | Skip-link or landmarks (`<main>`, `<nav>`) to jump past repeated content | auto + manual |
| 2.4.3 Focus order | Tab order follows the logical reading/interaction order | manual |
| 2.4.7 Focus visible | Every focusable element has a visible focus indicator | manual |
| 2.5.3 Label in name | The accessible name contains the visible label text (buttons/links) | auto |
| 2.4.11 Focus not obscured (2.2 new) | Focused element isn't fully hidden by sticky headers/overlays | manual |

## Understandable

| Criterion | What to check | axe? |
|---|---|---|
| 3.2.1 On focus | Focus doesn't trigger an unexpected context change (no auto-submit on focus) | manual |
| 3.2.2 On input | Changing a form field doesn't auto-change context without warning | manual |
| 3.3.1 Error identification | Errors are text, not just color; `aria-describedby` links field to message | auto + manual |
| 3.3.2 Labels or instructions | Form fields have visible labels/instructions | auto |
| 3.3.3 Error suggestion | Errors tell the user how to fix it, not just that it's wrong | manual |

## Robust

| Criterion | What to check | axe? |
|---|---|---|
| 4.1.2 Name, role, value | Custom widgets have correct ARIA `role`, `name`, `state`; native elements use native semantics | auto |
| 4.1.3 Status messages | `aria-live` (polite/assertive) on dynamic updates, errors, success — so AT announces them | manual |

## axe-core rule tags

axe tags rules by WCAG criterion (`wcag2a`, `wcag2aa`, `wcag21aa`, `wcag22aa`) and by
category (`cat.color`, `cat.forms`, `cat.keyboard`, etc.). When triaging axe findings,
the tag tells you the severity level and the criterion. Rules tagged `best-practice`
are not WCAG-mandated — triage them lower.

The ~30–40% axe catches are the deterministic class (contrast, missing labels, invalid
ARIA, duplicate IDs, empty buttons). The other ~60–70% — keyboard order, focus
management, reading-order vs visual-order, live-region announcements, color-independence
— require the manual walkthrough in Step 3–4 of the skill. A clean axe run is the floor,
not the finish line.
