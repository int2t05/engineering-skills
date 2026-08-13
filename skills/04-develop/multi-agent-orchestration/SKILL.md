---
name: multi-agent-orchestration
description: Use when executing work through subagents — dispatching independent tasks to parallel isolated-context agents, or driving a plan as a sequence of implementer-subagents with review checkpoints. Scales beyond a single context window. Triggers on "parallel agents", "subagent execution", "dispatch tasks", "fan out", "并行 agent", "子代理执行", "派发任务". Not for breaking a plan into tickets (use breakdown) or doing the implementation yourself (use implement).
---

# Multi-Agent Orchestration

Execute work through subagents instead of a single context. Two modes: **parallel dispatch**
(independent tasks to concurrent isolated-context agents) and **plan-driven execution** (a plan as a
sequence of implementer-subagents, each reviewed before the next). Use when the work exceeds one
context window, or when isolation prevents cross-task contamination.

## When to use

- A plan/ticket set is too large for one session — drive it as sequenced implementer-subagents
- 2+ independent tasks that don't share state — dispatch them concurrently to isolated contexts
- A task needs a fresh context to avoid prior-session bias or context bloat
- Reviewing one task's output before starting the next (plan-driven checkpoint)
- Triggers on "parallel agents", "subagent execution", "dispatch tasks", "fan out", "并行 agent", "子代理执行", "派发任务"

**Not for:** breaking a plan into tickets (use `breakdown` — this skill *executes* the tickets, it doesn't decompose them); doing the implementation yourself in one context (use `implement`); single-task work that fits one session (just do it — orchestration has overhead).

## Steps

### 1. Decide: parallel dispatch or plan-driven execution?

- **Parallel dispatch** — the tasks are independent (no data dependency between them). Run them concurrently. Use when: lint-fixing N files, researching N competitors, generating N independent components.
- **Plan-driven execution** — the tasks have an order (each informs or gates the next). Run them sequentially with review between. Use when: a feature spans schema → API → UI → tests, or when task N's output must be verified before task N+1 starts.

If tasks are independent but few (2-3) and each is small, don't orchestrate — do them inline. Orchestration earns its overhead only when isolation or scale matters.

### 2. Construct the context for each subagent

A subagent has no access to your conversation — its context is only what you put in its prompt. Construct it deliberately:

- **Goal** — what the subagent must produce (a verifiable outcome, not "work on X").
- **Inputs** — the files, specs, decisions, and constraints it needs. Quote the relevant spec section; don't say "see the PRD" (it can't).
- **Boundaries** — what's in scope, what's out, what to ask about vs. decide autonomously.
- **Verify target** — the exact check that defines done (tests pass, file exists with N sections, output matches schema).
- **Isolation note** — tell it not to assume state from any prior session; its prompt is its entire world.

### 3. Dispatch (parallel) or sequence (plan-driven)

- **Parallel** — launch all subagents in one message (multiple Agent tool calls). Wait for all; collect results. Don't start the next phase until all return, unless a slow one unblocks others.
- **Plan-driven** — launch one implementer-subagent for task 1. When it returns, **review its output** (read the result, run its verify check, confirm it's correct) before launching task 2's implementer. The review is the checkpoint — never auto-advance to the next task without verifying the prior.

### 4. Review each subagent's output

For every subagent result, before consuming it:

- Did it meet the verify target from its prompt? (Run the check; don't trust the claim.)
- Did it stay in scope, or invent work outside the boundaries?
- Is the output consistent with what downstream tasks expect?
- If it failed or drifted — either re-dispatch with a corrected prompt, or fix inline if the gap is small. Don't build on a broken foundation.

### 5. Synthesize and verify the whole

After all subagents complete (parallel) or the plan finishes (plan-driven):

- Does the integrated result meet the original goal? Run the end-to-end verify, not just each piece.
- Are there seams between subagent outputs — inconsistencies in naming, style, assumptions? Reconcile them; isolated contexts produce isolated assumptions.
- State what was done by subagents vs. inline, so the trace is auditable.

## Verify

- [ ] Each subagent had a constructed context (goal + inputs + boundaries + verify target) — not a vague "do X"
- [ ] Parallel tasks were genuinely independent (no hidden data dependency that serialized them)
- [ ] Plan-driven tasks were reviewed before advancing — no auto-advance past an unverified step
- [ ] Each subagent's output met its verify target (checked, not claimed)
- [ ] The integrated whole meets the original goal (end-to-end verify, not just per-piece)
- [ ] Seams between subagent outputs reconciled (naming, style, assumptions)

**Red flags:** dispatching tasks that share state as if independent (race condition); auto-advancing a plan-driven sequence without reviewing the prior step; a subagent prompt that says "see the conversation" or "you know what to do" (it doesn't — its context is only its prompt); skipping the end-to-end verify because each piece "passed"; treating subagent output as trusted without checking.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, verify don't assume, goal-driven execution, surgical scope).
- [references/dispatch-patterns.md](references/dispatch-patterns.md) — when to fan out vs sequence, context-construction templates, review-checkpoint patterns, common failure modes (race conditions, context-starved subagents, unverified seams).
