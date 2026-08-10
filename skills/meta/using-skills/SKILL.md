---
name: using-skills
description: Use when starting a session or deciding which skill applies. Maps incoming work to the right skill across the 9 SDLC phases (product → research → design → develop → tune → test → verify → ship → operate).
---

# Using Skills

A router. Identify the SDLC phase of the incoming work, then activate the matching
skill. Every skill in this collection lives under one of nine phases.

## When to use

- Start of a session, before any response or action.
- Unsure which skill fits the task at hand.
- A task spans multiple phases and you need to sequence them.

## Steps

1. Pick the phase, then activate the entry-point skill it lists.
   - **01-product** — `brainstorm` · `spec` · `oss-strategy`
   - **02-research** — `research` · `market-research` · `tech-selection`
   - **03-design** — `architecture` · `domain-modeling` · `api-design` · `codebase-design` · `frontend-design` · `prototype`
   - **04-develop** — `implement` · `breakdown` · `context-engineering`
   - **05-tune** — `performance` · `simplify`
   - **06-test** — `tdd` · `test-generation` · `api-testing` · `e2e-testing`
   - **07-verify** — `code-review` · `debugging` · `security-review`
   - **08-ship** — `shipping` · `git-workflow` · `ci-cd` · `deprecation-migration` · `oss-polish`
   - **09-operate** — `observability` · `documentation-audit` · `handoff`

2. Disambiguate with three questions:
   - *Building new, or fixing what exists?* New → start at `01-product` (`brainstorm` / `spec`), not `04-develop`. Fixing → `07-verify` (`debugging`), then `06-test` (`tdd`) to lock the fix.
   - *Process question or implementation question?* Process skills (`brainstorm`, `debugging`, `code-review`) run before implementation skills (`frontend-design`, `api-design`).
   - *About to ship?* Run `08-ship` in order: `git-workflow` → `ci-cd` → `shipping`.

3. Sequence multi-phase work in phase order; finish one skill before starting the next. A full feature may run product → design → develop → test → verify → ship. A bug fix may be just `debugging` → `tdd` → `code-review` → `git-workflow`.

4. Skills are **rigid** (TDD, debugging — follow exactly) or **flexible** (patterns — adapt to context). The skill's own body tells you which.

5. For the full decision tree — every branch routed to its skill — see `references/phase-tree.md`.

## Verify

The routed skill's `## When to use` matches the task, and the skill activates via the Skill tool without a mismatch signal. If the skill's triggers don't fit the work, re-route — don't force-fit.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill in this collection.
- [references/phase-tree.md](references/phase-tree.md) — full ASCII decision tree by phase and task shape.

External skill discovery (`npx skills find/add`) is out of scope — this router maps tasks to this collection's 33 internal skills only.
