# Review Modes

The three non-default modes of the `code-review` skill. The default (pre-merge two-axis review) is
in SKILL.md; these run at different moments with distinct postures. Adapted from established
practice (addyosmani's doubt-driven-development, obra's verification-before-completion and
receiving-code-review).

## §in-flight — adversarial doubt before a decision stands

**When:** during implementation, when a non-trivial decision is about to become load-bearing
(an architectural choice, a data-model shape, a public API signature, a state-management approach).
**Not** a substitute for pre-merge review — this is earlier, while course-correction is cheap.

**Posture:** biased to *disprove*, not approve. The goal is to find the decision wrong before it
propagates, not to validate it. A decision that survives a genuine disprove attempt is trustworthy;
one that only survives approval is not.

### Workflow

1. **State the decision precisely.** Write it as a claim: "We will use X for Y because Z." Vague
   decisions can't be doubted — make it specific enough to attack.
2. **Generate the strongest counter-argument.** What's the best case for this being wrong? What
   assumption, if false, collapses the decision? What scale, constraint, or edge case breaks it?
   Don't generate a strawman — generate the attack you'd respect.
3. **Run the counter fresh.** Cross-examine in a fresh context (subagent or a clean prompt) so prior
   commitment doesn't bias the doubt. Ask: "Given this decision and this counter-argument, is the
   decision still right? What evidence would change your mind?"
4. **Decide.** If the counter holds, revise the decision before it stands. If it fails, the decision
   survives — proceed, noting the attack it survived.
5. **Record the survivor.** Brief note: the decision, the attack considered, why it held. This
   becomes the defense if a future review questions it.

### What this is not

- Not pre-merge review (that reviews a diff; this reviews a decision before it's implemented deeply).
- Not generic skepticism ("is this a good idea?") — it requires a specific counter-argument.
- Not analysis paralysis — if you can't generate a strong counter in one pass, the decision is
  probably safe; move on.

## §evidence-gate — before claiming done

**When:** the moment before you say "done", "fixed", "passing", "works", "ready to merge". The claim
is the gate; evidence is the key.

**Posture:** no completion claim without fresh verification evidence. "Seems right" / "should work"
/ "I'm pretty sure" are not evidence — they're assertions. The bar is: identify the proving command,
run it, read the full output, confirm it proves the claim.

### Workflow

1. **Identify the proving command.** What command, run against what input, would prove the claim?
   - "Done" (feature works) → the acceptance test / e2e that exercises the user path.
   - "Fixed" (bug gone) → the regression test that reproduces the bug, now passing.
   - "Passing" (tests green) → `npm test` / `pytest` / `go test` full suite, not a subset.
   - "Works on mobile" → ran on a mobile viewport/device, not assumed from desktop.
2. **Run it.** Actually invoke the command. Don't rely on a prior run — run it now, against the
   current state. If the command needs setup (server running, DB migrated, env vars), do the setup.
3. **Read the full output.** Not just the last line ("All tests passed"). Read the full output —
   failures hide in the middle, warnings matter, skipped tests are not passing tests. A green summary
   with 40 skipped tests is not "passing".
4. **Confirm the evidence matches the claim.** Does the output actually prove what you claimed? "The
   build succeeded" is not "the feature works". "Tests pass" is not "the bug is fixed" (unless the
   test reproduces the bug). Match the evidence to the specific claim.
5. **Report with the evidence.** "Done — `test/auth.test.ts` passes, including the regression case
   for #123. Output: [paste]." Not "Done."

### What this is not

- Not "run the tests" generically — the proving command must match the specific claim.
- Not a one-time gate — every completion claim gets evidence, every time.
- Not optional when "it obviously works" — that's exactly when the gate earns its keep.

## §receiving — when review feedback arrives

**When:** review feedback (from a human, another agent, or a CI bot) has arrived and you're deciding
whether and how to act on it.

**Posture:** technical rigor over performative agreement. Don't blindly implement feedback ("they
said so"), and don't perform gratitude instead of evaluating it. Verify the feedback is correct
before acting; push back with evidence where it's wrong.

### Workflow

1. **Restate the feedback precisely.** What exactly is being claimed/suggested? Vague feedback
   ("this could be cleaner") can't be evaluated — restate it as a specific claim ("function X does
   too much; extract Y").
2. **Verify the claim.** Is the feedback technically correct?
   - Does the problem it describes actually exist? (Read the code it points at.)
   - Is the suggested fix correct? (Does it actually fix the problem without introducing a worse one?)
   - Is the underlying reasoning sound, or is it a style preference dressed as a defect?
3. **Decide per-item, not per-reviewer.** Don't accept all feedback from a trusted reviewer or reject
   all from a harsh one. Evaluate each item on its technical merits. A senior reviewer can be wrong
   about a specific point; a junior reviewer can be right.
4. **Respond with evidence, not deference.**
   - If correct → implement it, say why it's right (not just "fixed").
   - If wrong → push back with the evidence. "I checked — the function doesn't do X because [code
     reference / test output]. The suggestion would break Y." Don't soften a correct pushback to seem
     cooperative.
   - If unclear → ask for the specific case/repro that motivates it, don't guess and implement.
5. **Record the outcome.** What was accepted, what was rejected and why. A review where everything
   was "addressed" is suspicious; a review with reasoned accept/reject is trustworthy.

### What this is not

- Not defensiveness — verify, don't dismiss. Genuine pushback requires evidence, not preference.
- Not blanket compliance — implementing all feedback blindly is as wrong as rejecting all feedback.
- Not a social exchange — the goal is correct code, not making the reviewer feel heard.
