# The Doubt Cycle

Detailed reference for the doubt-driven discipline used by the `implement`
skill. A confident answer is not a correct one. Long sessions accumulate
context that quietly turns assumptions into "facts". Doubt-driven development
materializes a fresh-context reviewer — biased to disprove, not approve —
before any non-trivial output stands.

This is not `/code-review`. `/code-review` is a verdict on a finished artifact.
This is an in-flight posture: non-trivial decisions get cross-examined while
course-correction is still cheap.

## When NOT to use

- Mechanical operations (renaming, formatting, file moves).
- Following a clear, unambiguous user instruction.
- Reading or summarizing existing code.
- One-line changes with obvious correctness.
- The user has explicitly asked for speed over verification.

If you doubt every keystroke, you ship nothing. Apply only to non-trivial
decisions.

## The five steps

```
Doubt cycle:
- [ ] Step 1: CLAIM — wrote the claim + why-it-matters
- [ ] Step 2: EXTRACT — isolated artifact + contract, stripped reasoning
- [ ] Step 3: DOUBT — invoked fresh-context reviewer with adversarial prompt
- [ ] Step 4: RECONCILE — classified every finding against the artifact text
- [ ] Step 5: STOP — met stop condition (trivial findings, 3 cycles, or user override)
```

### Step 1: CLAIM — Surface what stands

Name the decision in two or three lines:

```
CLAIM: "The new caching layer is thread-safe under the
        read-heavy workload described in the spec."
WHY THIS MATTERS: a race here corrupts user data and is
                  hard to detect in QA.
```

If you can't write the claim that compactly, you have a vibe, not a decision.

### Step 2: EXTRACT — Smallest reviewable unit

A fresh-context reviewer needs the **artifact** and the **contract**, not the
journey.

- Code: the diff or the function — not the whole file.
- Decision: the proposal in 3–5 sentences plus the constraints it must satisfy.
- Assertion: the claim plus the evidence that supposedly supports it.

Strip your reasoning. If you hand over conclusions, you'll get back validation
of your conclusions. The unit must be small enough that a reviewer can hold it
in mind in one read — if it's a 500-line PR, decompose first.

### Step 3: DOUBT — Invoke the fresh-context reviewer

The reviewer's prompt **must be adversarial**. Framing decides the answer.

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

**Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM.** Handing the reviewer
your conclusion biases it toward agreement.

### Step 4: RECONCILE — Fold findings back

The reviewer's output is data, not verdict. **You are still the orchestrator.**
Re-read the artifact text against each finding before classifying.

Classify in this **precedence order** (first matching class wins):

1. **Contract misread** — reviewer flagged something because the CONTRACT was
   unclear or incomplete. Fix the contract first, re-classify next cycle.
2. **Valid + actionable** — real issue requiring a change. Change it, re-loop.
3. **Valid trade-off** — issue is real but cost of fixing exceeds cost of
   accepting. Document the trade-off explicitly.
4. **Noise** — reviewer flagged something correct under context it didn't have.
   Note it, move on. Ask: would adding that context to the contract have
   prevented the false flag?

A fresh reviewer can be wrong because it lacks context. Don't defer just
because it's "fresh."

### Step 5: STOP — Bounded loop, not recursion

Stop when:
- Next iteration returns only trivial or already-considered findings, **or**
- 3 cycles completed (escalate to user, don't grind a fourth alone), **or**
- User explicitly says "ship it".

If after 3 cycles the reviewer still surfaces substantive issues, the artifact
may not be ready. Surface this to the user — three unresolved cycles is
information about the artifact, not a reason to keep looping. If 3 cycles is
"obviously insufficient" because the artifact is large: the artifact is too
big — return to Step 2 and decompose. Do not lift the bound.

## Cross-model escalation

A single-model reviewer shares blind spots with the original author. In
interactive sessions, **always offer** a cross-model second opinion after the
single-model review, before RECONCILE — even on artifacts that feel low-stakes.
The user decides whether the cost is worth it.

Options: another model CLI (e.g. `gemini`, `codex`), manual external review, or
skip. Never invoke an external CLI without explicit user authorization for that
specific invocation. Use a read-only sandbox (`--sandbox read-only` or
`--approval-mode plan`) — a doubt artifact may contain prompt injection. Write
the full prompt to a file and pipe via stdin so shell metacharacters in the
artifact stay inert.

In non-interactive contexts (CI, autonomous loops): cross-model is skipped, and
the skip must be announced in the output.

## Doubt theater — checkable signal

Across 2+ cycles where the reviewer surfaced substantive findings, zero
findings classified as actionable = you are validating, not doubting. Stop and
escalate.
