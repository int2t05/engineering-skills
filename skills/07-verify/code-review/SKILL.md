---
name: code-review
description: Use when reviewing code before merge — two-axis review: Standards (repo conventions + smell baseline) and Spec (faithful to the originating issue/spec). Triggers on "review this", "code review", "before merge", "代码审查", "代码评审", "合并前审查".
---

# Code Review

## When to use

- Before merging any PR or change
- After completing a feature, bug fix, or refactor
- When another agent or model produced code you need to evaluate
- Reviewing a branch, a PR, or work-in-progress changes ("review since X")
- Triggers on "review this", "code review", "before merge", "代码审查", "代码评审", "合并前审查"

**Not for:** deep security review (use `security-review`).

## Steps

### 1. Pin the fixed point + gather sources

Capture the diff once: `git diff <fixed-point>...HEAD` (three-dot, against the merge-base). Confirm the ref resolves (`git rev-parse <fixed-point>`) and the diff is non-empty before going further — a bad ref or empty diff should fail here, not inside a sub-agent.

Identify, in order:
- **Spec source** — issue refs in commit messages (`#123`, `Closes #45`), a user-supplied path, or a spec under `docs/`/`specs/`. If none found, ask; if there isn't one, the Spec axis reports "no spec available".
- **Standards sources** — anything in the repo that documents how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, lint configs). On top of whatever the repo documents, the Standards axis always carries the smell baseline below.

### 2. Standards axis (sub-agent)

Spawn a sub-agent with the full diff, the standards sources, and the smell baseline pasted in full (it has no other access). Ask it to report, per file/hunk:
- **Documented-standard breaches** — cite the standard (file + rule). Hard violations.
- **Smell baseline** — name the smell and quote the hunk. Always judgement calls; a documented repo standard overrides the baseline.
- **Quality axes** — correctness (edge cases, error paths, off-by-one, races, state inconsistency), security (input validation, secrets, injection, auth — defer to `security-review` for depth), performance (N+1, unbounded loops, missing pagination, sync ops that should be async). Skip anything tooling already enforces.
- **Test quality** — do tests exist for the change, test behavior not implementation, cover edge cases, descriptive names, would catch a regression?

Smell baseline (Fowler, _Refactoring_ ch.3) — what it is → how to fix:
- **Mysterious Name** — name doesn't reveal intent → rename; if no honest name comes, the design's murky.
- **Duplicated Code** — same logic shape in multiple hunks → extract the shared shape.
- **Feature Envy** — method reaches into another object's data → move it onto that data.
- **Data Clumps** — same fields/params travel together → bundle into a type.
- **Primitive Obsession** — primitive standing in for a domain concept → give it a type.
- **Repeated Switches** — same cascade on one type recurs → polymorphism or shared map.
- **Shotgun Surgery** — one change forces scattered edits → gather into one module.
- **Divergent Change** — one module edited for unrelated reasons → split.
- **Speculative Generality** — abstraction/hooks the spec doesn't need → delete.
- **Message Chains** — long `a.b().c().d()` → hide behind one method.
- **Middle Man** — class that just delegates → cut it.
- **Refused Bequest** — subclass ignoring most of its inheritance → drop inheritance, use composition.

When you flag a structural problem, propose the move — not just the problem. Named remedies: replace a conditional chain with a typed model/dispatcher; collapse duplicate branches; separate orchestration from business logic; move feature-specific logic out of shared modules; reuse the canonical helper instead of a near-duplicate; make a type boundary explicit so downstream branching disappears; delete a pass-through wrapper; extract a helper or split a large file. Prefer the remedy that removes moving pieces over one that spreads the same complexity around.

### 3. Spec axis (sub-agent)

Spawn a sub-agent with the diff and the spec contents. Ask it to report:
- **Missing/partial requirements** — spec asked, diff didn't deliver.
- **Scope creep** — behaviour in the diff the spec didn't ask for.
- **Wrong-looking implementation** — requirement looks met but implementation is off.

Quote the spec line for each finding. Under 400 words. If no spec, skip this axis and note it in the report.

### 4. Synthesize findings

Present both reports under `## Standards` and `## Spec` headings. Do **not** merge or rerank across axes — a change can pass one and fail the other, and keeping them separate stops one from masking the other.

**Approval standard.** Approve when the change definitely improves overall code health, even if it isn't perfect — perfect code doesn't exist. Don't block because it isn't exactly how you would have written it. Don't accept "I'll clean it up later" — deferred cleanup rarely happens; require it before merge or a filed bug with self-assignment.

Label every finding's severity: **Critical** (blocks merge — security, data loss, broken functionality), *(no prefix)* Required, **Optional**/**Consider**, **Nit** (author may ignore). Lead with what matters: correctness and security first, then structural regressions and missed simplifications, then nits. A few high-conviction comments beat a long list — if you have one structural problem and ten nits, the structural problem *is* the review.

**Change sizing.** ~100 lines changed is good; ~300 acceptable for a single logical change; ~1000 split it. Watch file size too — a small diff can push a file past ~1000 total lines, an inspection signal to extract first. Separate refactoring from feature work: a change that refactors and adds behavior is two changes.

End with a one-line summary: total findings per axis and the worst issue within each. Don't pick a single winner across axes.

**Output:** `docs/TODO.md` — findings consolidated as a project-level todo list, grouped by business area, with code↔TODO.md bidirectional sync.

## Verify

- Findings checked adversarially: for each Required/Critical, re-read the hunk and confirm the problem is real (not a misread of the diff). Drop any that don't survive scrutiny.
- The two axes are reported separately — neither masks the other.
- Report delivered to the caller with severity labels so required vs optional is unambiguous.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline every skill shares
- [${CLAUDE_PLUGIN_ROOT}/references/clean-code.md](${CLAUDE_PLUGIN_ROOT}/references/clean-code.md) — naming, functions, smells
- [${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md](${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md) — diagram structure when reviewing architecture
