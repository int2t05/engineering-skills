---
name: code-review
description: Use when reviewing code — pre-merge two-axis review (Standards + Spec), in-flight adversarial doubt, evidence-before-done verification, or receiving review feedback. Triggers on "review this", "code review", "before merge", "代码审查", "合并前审查", "帮我看看这代码", "能合并吗", "are you sure", "verify before done", "收到评审意见". Not for machine-detectable lint (use linting) or runtime bugs (use debugging).
---

# Code Review

Four review modes, each a different moment and posture. Pick by when the review happens and who's
giving vs receiving it.

## When to use

- **pre-merge** (default) — before merging a PR/change: two-axis review, Standards (repo conventions + smell baseline) and Spec (faithful to the originating issue/spec)
- **in-flight** — during implementation, before a decision stands: adversarial cross-examination biased to disprove, not approve
- **evidence-gate** — before claiming a task done/fixed/passing: produce fresh verification evidence, not assertion
- **receiving** — when review feedback arrives: verify the feedback is correct before acting on it; technical rigor over performative agreement
- Triggers on "review this", "code review", "before merge", "代码审查", "合并前审查", "帮我看看这代码", "能合并吗", "are you sure", "verify before done", "收到评审意见"

**Not for:** deep security review (use `security-review`); machine-detectable lint/style (use `linting`); runtime behavior bugs (use `debugging`).

## Steps

### 1. Pick the mode

- Merging a PR / evaluating a diff → **pre-merge** (Step 2)
- Mid-implementation, a non-trivial decision is about to stand → **in-flight** (load [references/review-modes.md](references/review-modes.md) §in-flight)
- About to claim "done" / "fixed" / "passing" → **evidence-gate** (load [references/review-modes.md](references/review-modes.md) §evidence-gate)
- Review feedback just arrived and you're deciding whether to act on it → **receiving** (load [references/review-modes.md](references/review-modes.md) §receiving)

### 2. Pre-merge review (default mode)

#### 2a. Pin the fixed point + gather sources

Capture the diff once: `git diff <fixed-point>...HEAD` (three-dot, against the merge-base). Confirm
the ref resolves (`git rev-parse <fixed-point>`) and the diff is non-empty before going further.

Identify, in order:
- **Spec source** — issue refs in commit messages (`#123`, `Closes #45`), a user-supplied path, or a spec under `docs/`/`specs/`. If none found, ask; if there isn't one, the Spec axis reports "no spec available".
- **Standards sources** — anything documenting how code should be written (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, lint configs). On top of repo docs, the Standards axis always carries the smell baseline below.

#### 2b. Standards axis (sub-agent)

Spawn a sub-agent with the full diff, the standards sources, and the smell baseline pasted in full
(it has no other access). Ask it to report, per file/hunk:
- **Documented-standard breaches** — cite the standard (file + rule). Hard violations.
- **Smell baseline** — name the smell and quote the hunk. Always judgement calls; a documented repo standard overrides the baseline.
- **Quality axes** — correctness (edge cases, error paths, off-by-one, races, state inconsistency), security (input validation, secrets, injection, auth — defer to `security-review` for depth), performance (N+1, unbounded loops, missing pagination, sync ops that should be async). Skip anything tooling enforces.
- **Test quality** — do tests exist for the change, test behavior not implementation, cover edge cases, descriptive names, would catch a regression?

Smell baseline (Fowler, _Refactoring_ ch.3) — what it is → how to fix:
- **Mysterious Name** → rename; if no honest name comes, the design's murky.
- **Duplicated Code** → extract the shared shape.
- **Feature Envy** → move the method onto the data it envies.
- **Data Clumps** → bundle the traveling fields into a type.
- **Primitive Obsession** → give the domain concept a type.
- **Repeated Switches** → polymorphism or shared map.
- **Shotgun Surgery** → gather scattered edits into one module.
- **Divergent Change** → split the module edited for unrelated reasons.
- **Speculative Generality** → delete the unused abstraction.
- **Message Chains** → hide `a.b().c().d()` behind one method.
- **Middle Man** → cut the pure delegator.
- **Refused Bequest** → drop inheritance, use composition.

When you flag a structural problem, propose the move — not just the problem. Named remedies:
replace a conditional chain with a typed model/dispatcher; collapse duplicate branches; separate
orchestration from business logic; move feature-specific logic out of shared modules; reuse the
canonical helper; make a type boundary explicit; delete a pass-through wrapper; extract a helper or
split a large file. Prefer the remedy that removes moving pieces.

#### 2c. Spec axis (sub-agent)

Spawn a sub-agent with the diff and the spec contents. Ask it to report:
- **Missing/partial requirements** — spec asked, diff didn't deliver.
- **Scope creep** — behaviour in the diff the spec didn't ask for.
- **Wrong-looking implementation** — requirement looks met but implementation is off.

Quote the spec line for each finding. Under 400 words. If no spec, skip this axis and note it.

#### 2d. Synthesize findings

Present both reports under `## Standards` and `## Spec` headings. Do **not** merge or rerank across
axes — a change can pass one and fail the other; keeping them separate stops one from masking the other.

**Approval standard.** Approve when the change definitely improves overall code health, even if
imperfect. Don't block because it isn't exactly how you'd write it. Don't accept "I'll clean it up
later" — deferred cleanup rarely happens; require it before merge or a filed bug with self-assignment.

Label every finding's severity: **Critical** (blocks merge — security, data loss, broken
functionality), *(no prefix)* Required, **Optional**/**Consider**, **Nit**. Lead with what matters:
correctness and security first, then structural regressions and missed simplifications, then nits.
A few high-conviction comments beat a long list.

**Change sizing.** ~100 lines good; ~300 acceptable for one logical change; ~1000 split it. Watch
file size — a small diff can push a file past ~1000 total lines, a signal to extract first. Separate
refactoring from feature work (§9, engineering-principles.md).

End with a one-line summary: total findings per axis and the worst issue within each.

### 3. In-flight / evidence-gate / receiving modes

These three modes run at different moments than pre-merge and have distinct postures. Load
[references/review-modes.md](references/review-modes.md) for the full workflow of each:

- **in-flight** — adversarial cross-examination of a non-trivial decision *before it stands*, while
  course-correction is cheap. Biased to disprove, not approve. Not a substitute for pre-merge review.
- **evidence-gate** — before claiming done/fixed/passing: identify the proving command, run it, read
  the full output, confirm. No completion claim without fresh evidence.
- **receiving** — when review feedback arrives: before implementing suggestions, verify the feedback
  is technically correct. Reject performative agreement and blind implementation; push back on
  unclear or questionable feedback with evidence.

**Output:** `docs/TODO.md` — pre-merge findings consolidated as a project-level todo list, grouped by
business area, with code↔TODO.md bidirectional sync. (In-flight/evidence-gate/receiving produce
behavior, not a doc.)

## Verify

- **pre-merge:** findings checked adversarially (for each Required/Critical, re-read the hunk and confirm the problem is real — drop any that don't survive scrutiny); two axes reported separately; severity labels clear; `docs/TODO.md` on disk with code↔TODO.md sync.
- **in-flight:** the decision was cross-examined before standing, not after; the disprove-bias was applied.
- **evidence-gate:** the proving command was actually run and its output read — not asserted; the claim matches the evidence.
- **receiving:** each piece of feedback was verified before action; feedback rejected with evidence where wrong; no blind implementation.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline every skill shares (verify don't assume, push back when warranted, §9 behavior-preserving change).
- [${CLAUDE_PLUGIN_ROOT}/references/clean-code.md](${CLAUDE_PLUGIN_ROOT}/references/clean-code.md) — naming, functions, smells.
- [${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md](${CLAUDE_PLUGIN_ROOT}/references/mermaid-diagrams.md) — diagram structure when reviewing architecture.
- [references/review-modes.md](references/review-modes.md) — the three non-default modes in full: in-flight adversarial doubt, evidence-gate verification, receiving review feedback.
- [references/tech-debt-register.md](references/tech-debt-register.md) — upgrade TODO.md to a prioritized register: interest/principal/risk/effort, paydown cadence, accepted-debt decisions.
