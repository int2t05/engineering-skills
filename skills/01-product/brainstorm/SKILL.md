---
name: brainstorm
description: Use before any creative work, or when the ask is underspecified. One-question-at-a-time dialogue that sharpens a vague idea into a concrete proposal. Triggers on "brainstorm", "grill me", "interview me", "refine this idea".
disable-model-invocation: true
---

# Brainstorm

Sharpen a vague idea into a confirmed proposal through one-question-at-a-time dialogue.
The cheapest moment to find ambiguity is before any plan, spec, or code exists — once
building starts, switching costs lock in the wrong thing.

## When to use

- The ask is underspecified — missing who, why, what success looks like, or the binding constraint.
- New feature, project, or "refine this idea" / "stress-test my thinking."
- User says "brainstorm", "grill me", "interview me", or 头脑风暴.
- You're tempted to silently fill ambiguous requirements before a spec exists.

**Not for:** unambiguous asks ("rename this variable"), pure info requests, or when the
user has explicitly asked for speed over verification.

## Steps

1. **Hypothesize with a confidence number.** If in a codebase, explore project context first
   (Glob/Grep/Read for architecture, patterns, constraints) before forming the hypothesis.
   Before asking anything, write your best read of what the user wants in one sentence, plus
   an honest confidence (0–100%):
   ```
   HYPOTHESIS: You want a way to answer "how are we doing?" in standup, and "dashboard" was the convention that came to mind.
   CONFIDENCE: ~30% — missing: who it's for, what "metrics" means, what success looks like
   ```
   Below ~70%, append what's still unresolved. The number forces honesty — if you can't
   predict the user's reaction to the next three questions, the number is wrong.

2. **Ask ONE question, with a guess attached.**
   ```
   Q: <one focused question>
   GUESS: <your hypothesis for the answer, with reasoning>
   ```
   One question per message — never a batch. Batching encourages skim-reading and surface
   answers; the third question often depends on the first. Attach a guess so the user reacts
   to a wrong hypothesis faster than generating from scratch. Be visibly willing to be wrong.

3. **Listen for "want vs. should want."** The most dangerous answers pattern-match
   best-practice talk ("scalable", "clean architecture", "the standard approach") without
   specifics. When you hear these, ask: *"If you didn't have to justify this to anyone,
   what would you actually want?"* That question often does more work than the previous five.

4. **Diverge then converge.** Once intent is clear, generate 3–8 idea variations using
   lenses from `references/techniques.md` (inversion, constraint removal, simplification,
   SCAMPER, first principles). Cluster into 2–3 directions and stress-test each against
   user value, feasibility, and differentiation. Surface hidden assumptions explicitly:
   what you're betting is true, what could kill it, what you're choosing to ignore.

5. **Repeat until ~95% confidence.** The stop test: *can you predict the user's reaction
   to the next three questions you'd ask?* If yes, you have shared understanding. If no,
   ask the next question. If several rounds pass without confidence rising, step back and
   reframe — something foundational is missing. Tell the user.

6. **Self-review the proposal.** Before presenting, scan for placeholders, internal
   contradictions, ambiguity (could any line be read two ways?), and scope (is this one
   proposal or three?). Fix inline. A "Not Doing" list makes trade-offs explicit — focus
   is about saying no to good ideas.

7. **Propose — restate and confirm.** Write back what you now think the user wants, tight
   (5–8 lines), in their language:
   ```
   - Outcome:      <one line>
   - User:         <one line — who benefits>
   - Why now:      <one line — what changed>
   - Success:      <one line — how we know it worked>
   - Constraint:   <one line — the binding limit>
   - Out of scope: <one line — non-negotiable; silent disagreement about non-goals is half of misalignment>
   ```
   The gate is an explicit "yes." "Whatever you think," "sounds good," and silence are
   **not** yes — re-ask with two concrete options framed as a choice. Loop until explicit
   confirmation, then hand off to the `spec` skill.

## Verify

- An explicit hypothesis with a confidence number was stated in the first turn.
- Every confidence below ~70% had a one-line reason attached.
- Questions were asked one at a time, each with a guess attached.
- Multiple directions were explored, not just the first idea.
- A want-vs-should-want probe ran when sophistication-signaling answers appeared.
- A Not-Doing list makes trade-offs explicit.
- A concrete restate (Outcome / User / Why now / Success / Constraint / Out of scope) was written.
- The user confirmed with an explicit yes — not delegation, not ambiguity.
- A spec is writable from the confirmed proposal.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill.
- [references/techniques.md](references/techniques.md) — ideation frameworks (SCAMPER, HMW, first principles, JTBD), decision techniques (design tree, questionnaire handoff), evaluation rubric, and worked examples.
