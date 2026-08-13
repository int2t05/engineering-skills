# Dispatch Patterns

Reference for the `multi-agent-orchestration` skill. When to fan out vs sequence, how to construct
subagent context, review-checkpoint patterns, and the failure modes to watch for.

## When to fan out (parallel) vs sequence (plan-driven)

| Signal | Mode | Why |
|---|---|---|
| Tasks share no data | Parallel | No dependency → concurrency is free |
| Task N's output is task N+1's input | Sequence | Can't start N+1 until N verifies |
| Each task touches a disjoint file set | Parallel | No merge conflict |
| Tasks touch the same files | Sequence | Concurrent edits race |
| Tasks are each >1 context window | Sequence (plan-driven) | Each needs full context for its slice |
| Tasks are small and few (2-3) | Neither — do inline | Orchestration overhead exceeds the work |
| One slow task unblocks others | Parallel, then sequence | Start the slow one early, do fast ones while it runs |

**The test for "independent":** if task A's output changes what task B would do, they're not
independent — sequence them. If A and B produce outputs that only meet at synthesis, they're
independent — parallelize.

## Context-construction template

A subagent's prompt is its entire world. It has no access to your conversation, your prior
decisions, or files you've read unless you put them in the prompt. Construct deliberately:

```
## Goal
[One sentence: the verifiable outcome this subagent must produce.]

## Inputs
- [File path + what to read in it, or quote the relevant section inline]
- [Spec excerpt: paste the acceptance criteria or constraints directly]
- [Prior decision: "We decided X because Y" — don't make it re-derive]

## Boundaries
- In scope: [exactly what to do]
- Out of scope: [what not to touch — adjacent code, config, tests beyond the target]
- Ask me if: [decisions you shouldn't make autonomously]
- Decide autonomously if: [implementation details within the stated boundaries]

## Verify target
[The exact check that defines done: "tests in test/foo.test.ts pass", "file docs/X.md exists with
sections 1-7 and no TBD placeholders", "output matches this schema: ..."]

## Isolation note
You have no access to any prior session or conversation. This prompt is your entire context. Don't
assume state, files, or decisions not stated above. If something is missing, ask — don't guess.
```

**Common context-construction mistakes:**
- "See the PRD" — it can't see the PRD. Paste the relevant section.
- "You know what to do" — it doesn't. State the goal as a verifiable outcome.
- "Fix the bug" — which bug? Where? What's the expected behavior? Quote the failing test.
- Omitting the verify target — without it, "done" is subjective and the review step can't check.

## Review-checkpoint patterns (plan-driven)

After each implementer-subagent returns, before launching the next:

1. **Read the full result** — not just the summary line. Look at what it claims it did.
2. **Run the verify target** — if it said "tests pass", run the tests. If it said "file exists", check the file. Don't trust the claim; check the evidence.
3. **Check scope** — did it touch files outside the boundaries? Did it invent work? Revert out-of-scope changes.
4. **Check downstream fit** — does the output match what the next task expects as input? If task 1 was "build the schema" and task 2 is "build the API on the schema", does the schema have the fields the API needs?
5. **Decide: accept, re-dispatch, or fix-inline** — accept if it meets the target; re-dispatch with a corrected prompt if it's structurally wrong; fix inline if the gap is small and you can do it faster than re-explaining.

**Never auto-advance past an unverified step.** The plan-driven sequence's value is the checkpoint;
skipping it collapses to an unreviewed single-context implementation with extra overhead.

## Failure modes

| Failure | Cause | Fix |
|---|---|---|
| Race condition | Dispatched dependent tasks as parallel | Sequence them; check the independence test |
| Context-starved subagent | Prompt said "see X" instead of quoting X | Construct full context (template above) |
| Unverified seam | Advanced plan-driven sequence without checking prior step | Enforce the review checkpoint |
| Inconsistent assumptions | Parallel agents made different guesses about the same ambiguity | State the decision in each prompt, or sequence them |
| Orchestration overhead > work | Dispatched 2 tiny tasks that'd take 1 minute inline | Do small/few tasks inline; reserve orchestration for scale/isolation |
| Subagent scope creep | Boundaries were vague | State out-of-scope explicitly; revert out-of-scope changes at review |
| "It passed" but didn't | Trusted the subagent's self-reported verify without running it | Always run the verify check yourself at the review step |

## End-to-end verify (after synthesis)

Per-piece passing ≠ whole passing. After all subagents complete:

- Run the **original goal's** verify (the thing the user asked for), not just each subagent's sub-goal.
- Check **seams**: do subagent outputs agree on naming, types, conventions? Isolated contexts produce isolated assumptions — reconcile at the seam.
- Audit the **trace**: what was done by subagents vs inline? If something is wrong, you need to know which subagent produced it.
