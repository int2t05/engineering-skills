---
name: prototype
description: Use when a design question is best answered by a throwaway prototype — a single shareable HTML file for state/logic, or several toggleable UI variations to compare. Triggers on "prototype", "compare layouts", "validate the interaction", "sketch out", "try this quickly", "build a demo", "原型", "试做", "试这个方案", "搭个快速 demo".
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## When to use

- "Does this logic / state model feel right?" → logic prototype
- "What should this look like?" → UI prototype
- Sanity-check a state machine or data model before committing; explore UI directions before picking one
- Triggers on "prototype", "throwaway", "mockup", "compare layouts", "validate the interaction", "sketch out", "try this quickly", "build a demo", "原型", "试做", "试这个方案", "搭个快速 demo"

**Not for:** production UI implementation (use `frontend-design`); production code (use `implement`).

## Steps

### 1. Pick a branch

The two branches produce very different artifacts; getting this wrong wastes the whole prototype.

- **Logic / state model** → load `references/logic.md`. Single shareable HTML file with free-play
  buttons and tabbed guided walkthroughs a non-developer can drive.
- **What it looks like** → load `references/ui.md`. Several radically different UI variations on one
  route, switchable via `?variant=` and a floating bar.

If the question is ambiguous and the user isn't reachable, default to whichever branch matches the
surrounding code (backend module → logic; page/component → UI) and state the assumption up top.

### 2. Build it throwaway from day one

- Locate it close to where it will be used, but name it so a reader sees it's a prototype
- Trivial to run: one command in the task runner, or a single HTML file double-clicked
- No persistence by default — state in memory; no tests, no abstractions, no polish
- Surface the full relevant state after every action (logic) or variant switch (UI)

### 3. Capture the answer when done

Fold validated decisions into the real code. Capture the prototype itself as a **primary source**:
commit to a throwaway branch (out of main), leave a context pointer on the implementation issue,
and record the verdict + question settled. Main keeps only the validated decision.

**Output:** `docs/design/prototype-findings.md` — the question tested, the verdict, and the validated
decision. The prototype code itself stays on a throwaway branch; only the finding is promoted to main
as a durable record.

## Verify

- [ ] Question being answered stated explicitly at the top of the prototype
- [ ] Correct branch chosen — not silently defaulted
- [ ] Runs from one command or one double-click, no setup required
- [ ] State visible after every action / variant switch
- [ ] Validated decision folded into real code; prototype on a throwaway branch

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (enforce simplicity, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/design-principles.md](${CLAUDE_PLUGIN_ROOT}/references/design-principles.md) — design discipline (hierarchy before decoration, design every state, recognize rather than recall).
- [references/logic.md](references/logic.md) — single-shareable-HTML logic prototype: pure module, free-play + guided walkthroughs
- [references/ui.md](references/ui.md) — toggleable UI variants: sub-shape A (existing page) vs B (throwaway route), floating switcher
