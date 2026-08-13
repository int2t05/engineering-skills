---
name: refactoring
description: Use when restructuring code without changing behavior — extract modules, move classes, redraw dependency boundaries, split or merge files. Behavior-preserving structural changes that make the codebase easier to evolve, distinct from single-file clarity cleanup. Triggers on "refactor structure", "extract module", "move class", "split file", "change dependency", "重构结构", "提取模块", "拆分文件", "改依赖图". Not for single-file clarity cleanup (use simplify), architecture audit producing a design doc (use codebase-design), or lint/style fixes (use linting).
---

# Refactoring

Restructure code while preserving exact behavior — extract a module, move a class to its better
home, redraw a dependency boundary, split or merge files. The goal is a codebase that is easier to
evolve, not fewer lines or prettier names. Every move is behavior-preserving and test-pinned.

## When to use

- Extracting a module or class from inline code to redraw a boundary
- Moving a function/class to where it has the most context (Feature Envy fix at structure level)
- Splitting one oversized file/module into cohesive units, or merging near-duplicates into one
- Changing a dependency direction — inverting, decoupling, replacing a concrete dep with an interface
- Preparing a codebase for a feature by reshaping it first (then implement separately)
- Triggers on "refactor structure", "extract module", "move class", "split file", "change dependency", "重构结构", "提取模块", "拆分文件", "改依赖图"

**Not for:** single-file clarity cleanup — renaming, nesting, dead-code removal (use `simplify`); producing an architecture audit or design doc without executing the change (use `codebase-design`); machine-detectable lint/style issues (use `linting`).

## Steps

### 1. Pin behavior before moving anything

Refactoring is behavior-preserving by definition — if behavior can shift, you're not refactoring,
you're rewriting. Pin it first:

- Run the test suite; it must be green. If it isn't, stop — fix the breakage or establish the baseline separately.
- If the area has weak coverage, add **characterization tests** that capture current behavior (inputs → observed outputs) before you touch structure. You're not testing what it *should* do; you're pinning what it *does* do so the refactor can't silently change it.
- Note any behavior you suspect is accidental (a bug tests currently encode). Don't fix it here — refactoring preserves behavior, bugs included. File it; fix it in a separate change.

### 2. Name the structural move

State the move in one sentence before executing. The catalog:

- **Extract** — pull a cohesive responsibility out into its own module/class/function behind a named interface.
- **Move** — relocate a function/class to where it has the most context (where its data lives).
- **Split** — break an oversized file/module along a cohesive seam into smaller units.
- **Merge** — fold near-duplicates into one canonical implementation.
- **Change dependency** — invert a dependency, decouple via interface, or replace a concrete dependency with a port.

If you can't name it as one of these, it's probably clarity cleanup (→ `simplify`) or a design question (→ `codebase-design`).

### 3. Plan the move as the smallest behavior-preserving steps

Decompose the move into steps small enough that each one leaves the codebase green. "Extract module"
is not one step — it's: create the empty module → move one responsibility → update callers → run
tests → move the next. Large structural moves done in one pass are where regressions hide.

- At scale (touching >500 lines), prefer automation — codemods, AST transforms, IDE refactors — over manual edits. Manual structural edits at scale are error-prone and exhausting to review.
- Keep each step independently revertible. If step 4 breaks, you revert to step 3, not to the start.

### 4. Execute incrementally — test after every step

One step, then the full suite, then the next step. Never batch structural changes into one untested
commit.

- Make the move → run the suite → pass: continue; fail: revert the step and reconsider.
- Submit refactoring changes separately from feature or bug-fix changes. A PR that refactors *and* changes behavior is two PRs — split them. Reviewers cannot judge behavior preservation against a diff that also changes behavior.

### 5. Verify the structure improved

Step back and compare before and after:

- Is the boundary cleaner? Do callers depend on less?
- Did the move concentrate complexity (good) or just relocate it (no gain)?
- Is the diff reviewable as a pure structural change — no behavior drift mixed in?

If the "refactored" structure is not clearly better, or the diff entangles behavior changes, revert. Not every refactor improves things.

## Verify

- [ ] Test suite green before and after, with no test modifications (modified tests mean behavior changed)
- [ ] Each step is an independently revertible, behavior-preserving change; the diff is purely structural
- [ ] The structural move is named (extract / move / split / merge / change-dependency) and the result concentrates complexity rather than relocating it
- [ ] No behavior change mixed in — bugs observed during the refactor are filed, not silently fixed
- [ ] Refactoring submitted separately from feature/bug-fix work
- [ ] At scale (>500 lines), automation used instead of manual edits

**Red flags:** tests modified to pass after the move (behavior shifted); a "refactor" PR that also fixes a bug or adds a feature; large structural change in one untested pass; moving code without pinning behavior first; a refactor that leaves complexity merely relocated, not reduced.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, surgical scope, enforce simplicity)
