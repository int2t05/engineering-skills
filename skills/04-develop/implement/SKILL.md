---
name: implement
description: Use when implementing the work described by a spec or tickets — drives TDD within each slice, runs typechecks and tests regularly, and closes with code-review before committing. Also covers lightweight changes (small edits, mechanical renames, project scaffolding) that don't need a full spec. Triggers on "implement", "build this", "code the feature", "实现", "编码", "改这个配置", "重命名", "搭项目骨架" — also when user says "改一下这个" / "加个功能". Not for pure test-driven exploration with no spec (use tdd).
---

# Implement

Execute the work described by a spec or tickets in thin vertical slices. Each
slice cuts a complete path through every layer (schema, API, UI, tests) and
lands green. Drive TDD within each slice; verify framework-specific patterns
against official docs; subject non-trivial decisions to a fresh-context doubt
cycle before they stand.

## When to use

- Implementing work described by a spec, plan, or set of tickets.
- Multi-file changes that should land one vertical slice at a time.
- Framework-specific code where current docs determine correct patterns.
- High-stakes or unfamiliar code where correctness matters more than speed.
- Lightweight changes that don't need a spec — small config edits, mechanical renames/moves, project scaffolding (see `references/lightweight-changes.md`).

**Not for:** changes needing design decisions (use `spec`); system architecture (use `architecture`); pure test-driven exploration or bugfix-via-test with no spec — red-green-refactor as the whole task (use `tdd`). Have a spec and want slice-by-slice implementation? That stays here, with TDD driven within each slice.

## Steps

1. **Read the spec or tickets.** Orient on what "done" means. Note any
   pre-agreed TDD seams — integration points where tests must exist before code
   lands. If versions are missing or ambiguous, ask; the version determines
   which patterns are correct.

2. **Slice the work vertically.** One demoable end-to-end path per slice, sized
   to a single fresh context. Keep it compilable between slices. Wide refactors
   (one mechanical change fanning across the codebase) are the exception —
   sequence them as expand–contract, never force them into a tracer bullet.

3. **For each slice, implement via TDD at the seams:**
   - Write the failing test first (red), then the code (green), then refactor.
   - For framework-specific code: detect the stack and exact versions from the
     dependency file; fetch the relevant official docs page (not the homepage);
     follow the documented pattern and cite the source URL in a code comment.
     Flag anything you cannot verify as `UNVERIFIED`. When docs conflict with
     existing code, surface the conflict — don't silently pick one. See
     [references/source-verification.md](references/source-verification.md).
   - Run the typecheck and the affected test file(s) after each slice. Don't
     repeat a command on unchanged code — it adds no information.

4. **Run a doubt cycle for non-trivial decisions.** A decision is non-trivial
   when it introduces branching logic, crosses a module boundary, asserts a
   property the type system can't verify (thread safety, idempotence, ordering),
   or has irreversible blast radius (production deploy, data migration, public
   API change). Name the claim, extract the artifact + contract (not your
   reasoning), spawn a fresh-context adversarial reviewer, reconcile each
   finding against the artifact text, and stop on trivial findings / 3 cycles /
   user override. See [references/doubt-cycle.md](references/doubt-cycle.md).

5. **Commit the slice** with a descriptive message. Each slice is independently
   revertable. Don't mix concerns — feature, refactor, and config changes go in
   separate commits (see §9, behavior-preserving change discipline, in engineering-principles.md).

6. **After all slices: run the full test suite once.** Not per slice — once, at
   the end. If it fails, localize with the debugging skill; don't re-run blind.

7. **Run `/code-review` on the diff.** Address blocking findings before
   committing final state.

8. **Commit final state to the current branch** (if not already committed per
   slice).

## Verify

- Full test suite passes.
- Typecheck clean.
- `/code-review` returned no blocking findings.
- Framework-specific patterns carry source citations (or explicit `UNVERIFIED`
  flags); no deprecated APIs used.
- Non-trivial decisions survived at least one fresh-context doubt cycle.
- Work committed to the current branch.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill.
- [${CLAUDE_PLUGIN_ROOT}/references/clean-code.md](${CLAUDE_PLUGIN_ROOT}/references/clean-code.md) — code-quality bar for the implementation.
- [references/source-verification.md](references/source-verification.md) — source hierarchy, citation rules, retrieval safety.
- [references/doubt-cycle.md](references/doubt-cycle.md) — the five-step doubt cycle and cross-model escalation.
- [references/lightweight-changes.md](references/lightweight-changes.md) — small edits, renames, scaffolding that don't need a spec
