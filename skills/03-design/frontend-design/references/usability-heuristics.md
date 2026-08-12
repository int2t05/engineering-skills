# Usability Heuristics

Depth reference for the `frontend-design` skill. The authoritative frameworks for evaluating whether an
interface is usable: Nielsen's 10 heuristics (with UI examples), the Heuristic Evaluation method, Don
Norman's emotional-design levels, and Dieter Rams' principles. This is the evaluation layer atop
`ux-guidelines.md` (the 232-rule checklist) — the *why* behind the rules.

## 1. Nielsen's 10 usability heuristics (1994)

Jakob Nielsen's heuristics — the standard framework for heuristic evaluation. Each with a concrete UI
example:

### 1. Visibility of system status
The system shows what's happening, so users trust it and can predict outcomes.
- Loading bars and skeleton screens (not silent waits).
- "Saved 2 seconds ago" indicators in editors.
- Progress steps in a multi-step flow (1 of 4).

### 2. Match between system and real world
Use language and concepts the user knows, not internal jargon.
- "Shopping cart" not "transactional item buffer."
- Error: "That email doesn't match an account" not "AUTH_USER_NOT_FOUND."
- Organize information the way the user thinks about it, not the way the database is structured.

### 3. User control and freedom
Users make mistakes; give them an escape hatch.
- Undo/redo for destructive or editable actions.
- "Cancel" on every multi-step flow (not just "Submit").
- Easy exit from modals, drawers, and fullscreen modes (Esc, backdrop click, explicit close).

### 4. Consistency and standards
Same action = same style, same word, same location. Users shouldn't have to wonder if different words
mean the same thing.
- One primary-button style across the app.
- "Delete" everywhere (not "Remove" here and "Delete" there for the same action).
- Follow platform conventions (Apple HIG / Material) — don't invent gestures users already know.

### 5. Error prevention
Prevent errors before they happen — better than good error messages.
- Confirm destructive actions (delete, discard).
- Disable submit until required fields are valid.
- Inline validation as the user types, not only on submit.
- Constrain input (date picker, not free-text date that must be parsed).

### 6. Recognition rather than recall
Show options and state visibly; don't force users to remember.
- Visible menu items, not CLI-style commands.
- Selected state persists visibly across navigation.
- Recently-used items surfaced (recent files, recent searches).
- See design-principles §8.

### 7. Flexibility and efficiency of use
Serve both novices and experts. Shortcuts accelerate the experienced without burdening the new.
- Keyboard shortcuts for frequent actions (⌘K command palette, j/k navigation).
- Templates and "duplicate" for repeated workflows.
- Customizable density/defaults for power users, without confusing novices.

### 8. Aesthetic and minimalist design
Only what's needed. Every extra unit of information competes with the useful.
- One primary action per screen.
- Remove decorative elements that don't carry meaning.
- White space is not wasted space — it's hierarchy (Gestalt proximity).
- "Minimal" ≠ stark; it means nothing extraneous.

### 9. Help users recognize, diagnose, and recover from errors
Plain language, the problem's cause, and a next step — not error codes.
- "Wrong: Error 500." "Right: 'We couldn't save your changes. Your connection dropped — retry?'"
- State what went wrong, in plain words.
- Suggest the fix or offer the action to recover (retry, restore, contact support).

### 10. Help and documentation
Accessible when needed, focused on the task, with concrete steps.
- Contextual help (tooltips, "learn more" next to the relevant field).
- Documentation organized by task, not by feature.
- Searchable, with the most common tasks first.

## 2. Heuristic Evaluation method

Expert review: walk the interface against the 10 heuristics, note violations, rate severity.

**Severity scale (Nielsen):**
| Rating | Meaning |
|---|---|
| 0 | Not a problem |
| 1 | Cosmetic — fix if time |
| 2 | Minor — low priority |
| 3 | Major — important to fix |
| 4 | Catastrophic — must fix before release |

**Procedure:**
1. Walk each screen/flow 2-3 times independently.
2. For each heuristic, list where the interface violates it.
3. Assign severity to each violation.
4. Triage: fix all 3-4 first, then 2s, then 1s.

Heuristic evaluation is fast (a few hours for a medium app) and catches the structural issues user
testing won't (users won't articulate "this violates consistency" — they'll just feel something's off).
It doesn't replace user testing; it precedes it.

## 3. Don Norman — emotional design (three levels)

Usability is necessary but not sufficient. Products are experienced at three levels:

| Level | What it addresses | Design implication |
|---|---|---|
| **Visceral** | The immediate, pre-cognitive reaction to appearance | First impression matters: color, proportion, motion create the gut response |
| **Behavioral** | Usability and pleasure of use | The heuristics above; does it work, feel smooth, give feedback? |
| **Reflective** | The user's conscious assessment — self-image, meaning, story | Does using this make the user feel competent / professional / part of something? |

A product that's usable (behavioral) but ugly (visceral) or meaningless (reflective) still loses. All
three levels shape whether users return. The `frontend-design` Steps (pick a bold direction, apply color
formula, specify states) address visceral + behavioral; the product's positioning (spec, brainstorm)
addresses reflective.

## 4. Dieter Rams' 10 principles

The benchmark for "good design" — a check on whether what you've made is actually good, not just
shipped:

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

Rams' last principle is the purest expression of the purity ethic this collection follows: focus on the
essential, remove the rest.

## 5. How these connect

- **Nielsen** is the *evaluation* framework — walk the interface, find violations, fix by severity.
- **Norman** is the *experience* framework — usable is necessary, but visceral and reflective levels
  also determine whether users return.
- **Rams** is the *quality* framework — the check on whether the design is actually good, not just
  functional.

Use Nielsen in the `frontend-design` Verify step and the `frontend-audit` flow. Use Norman when
choosing aesthetic direction (Step 1-2). Use Rams as the final "is this actually good?" gut check before
shipping. `ux-guidelines.md` operationalizes Nielsen into 232 concrete rules; this file is the framework
behind them.
