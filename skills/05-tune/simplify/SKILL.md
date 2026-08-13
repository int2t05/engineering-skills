---
name: simplify
description: Use when the code is too complex — clarity over cleverness, removes speculative abstractions, dead complexity, and earns-its-cost structures. Triggers on "simplify", "too complex", "refactor for clarity", "简化", "太复杂", "重构求清晰". Not for cross-module structural changes (use refactoring) or architecture audit (use codebase-design) — single-file clarity stays here.
---

# Code Simplification

Simplify code by reducing complexity while preserving exact behavior. The goal is not fewer lines — it's code that is easier to read, understand, modify, and debug. Every simplification must pass one test: "Would a new team member understand this faster than the original?"

## When to use

- After a feature works and tests pass, but the implementation feels heavier than it needs to be
- During code review when readability or complexity issues are flagged
- When you encounter deeply nested logic, long functions, or unclear names
- After merging changes that introduced duplication or inconsistency
- Triggers on "simplify", "too complex", "refactor for clarity"

**Not for:** code you don't fully understand yet — comprehend before you simplify. Performance-critical code where the "simpler" version would be measurably slower. Throwaway code about to be rewritten entirely. Cross-module structural changes — extracting/moving modules, redrawing dependency boundaries, splitting or merging files → use `refactoring`. Designing where a seam or deep module should go (producing an audit, not executing) → use `codebase-design`. Single-file clarity stays here: naming, nesting, dead code.

## Steps

### 1. Understand before touching (Chesterton's Fence)

Before changing or removing anything, understand why it exists. If you see a fence across a road and don't understand why it's there, don't tear it down.

- What is this code's responsibility? What calls it, what does it call?
- What are the edge cases and error paths? Are there tests defining expected behavior?
- Why might it have been written this way — performance? platform constraint? historical reason? Check `git blame` for the original context.

If you can't answer these, you're not ready. Read more context first.

### 2. Identify simplification opportunities

Scan for concrete signals — each is a specific pattern, not a vague smell. The full tables (structural complexity, naming, redundancy) with examples are in `references/opportunities.md`. Summary:

- **Structural:** deep nesting (3+ levels), long functions (50+ lines), nested ternaries, boolean parameter flags, repeated conditionals.
- **Naming:** generic names (`data`, `temp`, `result`), abbreviations (`usr`, `cfg`), misleading names, comments restating "what" instead of "why".
- **Redundancy:** duplicated logic, dead code, unnecessary abstractions, over-engineered patterns (factory-for-a-factory), redundant type assertions.

### 3. Apply the five principles

1. **Preserve behavior exactly.** Same output for every input, same error behavior, same side effects and ordering, all existing tests pass without modification. If you're not sure a simplification preserves behavior, don't make it.
2. **Follow project conventions.** Read CLAUDE.md; study how neighboring code handles similar patterns. Simplification that breaks project consistency is churn, not simplification.
3. **Prefer clarity over cleverness.** Explicit code beats compact code when the compact version requires a mental pause to parse. A 1-line nested ternary is not simpler than a 5-line if/else.
4. **Maintain balance.** Over-simplification is a failure mode: inlining too aggressively (removing a concept's name), combining unrelated logic into one complex function, removing abstractions that exist for extensibility or testability, optimizing for line count.
5. **Scope to what changed.** Default to recently modified code. Avoid drive-by refactors of unrelated code unless explicitly asked to broaden scope — unscoped simplification creates noisy diffs and risks regressions.

### 4. Apply changes incrementally

One simplification at a time. Run the test suite after each change. **Submit refactoring changes separately from feature or bug fix changes** — a PR that refactors and adds a feature is two PRs; split them.

- Make the change → run the suite → pass: continue to the next; fail: revert and reconsider.
- Avoid batching multiple simplifications into one untested change. If something breaks, you need to know which simplification caused it.
- **Rule of 500:** if a refactoring would touch more than 500 lines, invest in automation (codemods, sed scripts, AST transforms) rather than manual edits. Manual edits at that scale are error-prone and exhausting to review.

### 5. Verify the result

Step back and evaluate the whole. Compare before and after:

- Is the simplified version genuinely easier to understand?
- Did you introduce any patterns inconsistent with the codebase?
- Is the diff clean and reviewable? Would a teammate approve?

If the "simplified" version is harder to understand or review than the original, revert. Not every simplification attempt succeeds.

## Verify

- [ ] All existing tests pass without modification
- [ ] Build succeeds with no new warnings; linter/formatter passes (no style regressions)
- [ ] Each simplification is a reviewable, incremental change; the diff is clean — no unrelated changes mixed in
- [ ] Simplified code follows project conventions (checked against CLAUDE.md or equivalent)
- [ ] No error handling removed or weakened; no dead code left behind (unused imports, unreachable branches)
- [ ] The "simplified" code is genuinely easier to understand than the original

**Red flags:** simplification that requires modifying tests to pass (you likely changed behavior); "simplified" code that is longer and harder to follow than the original; renaming to match personal preferences rather than project conventions; removing error handling because "it makes the code cleaner"; simplifying code you don't fully understand; batching many simplifications into one hard-to-review commit; refactoring outside the current task's scope without being asked.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (enforce simplicity, surgical scope, verify don't assume)
- [${CLAUDE_PLUGIN_ROOT}/references/clean-code.md](${CLAUDE_PLUGIN_ROOT}/references/clean-code.md) — meaningful names, small functions, comments, error handling (Uncle Bob)
- [references/opportunities.md](references/opportunities.md) — full simplification-opportunities tables (structural / naming / redundancy) + language-specific examples (TypeScript, Python, React/JSX)
