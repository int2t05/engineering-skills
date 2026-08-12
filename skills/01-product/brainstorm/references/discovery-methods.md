# Discovery Methods

Depth reference for the `brainstorm` skill. Methods for validating whether a problem is real and worth
solving — the problem-space track that runs before and alongside delivery. Complements `techniques.md`
(ideation lenses for generating variations); this file is for verifying which problem is true.

## 1. The Mom Test

Interview users about their past behavior, not their future opinions. Stated future intent predicts
nothing; past behavior predicts everything (product-principles §2).

**Rules:**
- Talk < 20% of the time; the user talks 80%.
- Ask about a specific, recent past event — not hypotheticals.
- Never ask "would you use this?" — ask "when did you last do [the task]?"
- Listen for emotion and energy; flat answers mean low pain.

**Bad → good questions:**

| Bad (future opinion) | Good (past behavior) |
|---|---|
| "Would you use a tool that...?" | "How did you handle [task] last week?" |
| "Do you think this is a good idea?" | "Walk me through the last time you did this." |
| "How much would you pay?" | "What did this cost you (time/money) last time?" |
| "What features do you want?" | "What was the hardest part of doing it?" |

**5-step interview:**
1. Segment the user (who exactly — role, context, frequency).
2. Ask for a recent, specific experience with the problem.
3. Ask about goals and obstacles in that experience.
4. Ask about alternatives — what did they do instead? (The workaround is your real competitor.)
5. Validate willingness to pay real resources — time, money, data — not stated intent.

## 2. JTBD switching interview

Jobs to be Done, used as an *interview method* (not just an ideation lens). When a user switched to or
from your product, the *forces of progress* tell you what job they hired it for:

```
Push (current situation is bad)   ──┐
Pull (new solution is better)     ──┼──> Switch happens when push + pull > anxiety + habit
Anxiety (new thing is scary)      ──┤
Habit (old way is familiar)       ──┘
```

Ask about a real switching moment:
- **Push** — what was frustrating about the old way?
- **Pull** — what drew you to the new way?
- **Anxiety** — what worried you about switching?
- **Habit** — what made the old way hard to leave?

The insight: people don't buy your feature set — they hire your product to make progress on a job. The
switching interview surfaces the job, not the feature requests.

## 3. Opportunity-solution tree

Teresa Torres' continuous-discovery framework. Keeps discovery tied to outcomes, not features:

```
Outcome (the business/user result you want)
   └── Opportunity (a problem blocking that outcome — from interviews)
        └── Solution (one way to address the opportunity)
            └── Experiment (how you test if the solution works)
```

Rules:
- Opportunities come from user interviews (Mom Test), not brainstorming in a room.
- Each opportunity can have many solutions; each solution can have many experiments.
- The tree prevents solution-first thinking — you don't pick a solution until you've named the
  opportunity it serves and the outcome that opportunity advances.

## 4. Working backwards (PR-FAQ)

Amazon's method: start from the end state and write backwards. Before any code, write:

1. **Press release** — the announcement you'd make at launch, written for a real customer. Forces you
   to state the customer problem, the benefit, and the differentiation in plain language. If you can't
   write a compelling PR, the product isn't compelling.
2. **FAQ** — the questions customers and stakeholders will ask, with answers. Surfaces the hard
   questions before they become hard problems.
3. **Then** the spec, then the code.

Working backwards kills "we built it and couldn't explain why" failures — if the PR reads flat, the
product is flat, and you find out before investing in implementation.

## 5. Problem sources and evaluation funnel

Three sources of problems to discover:

- **Pain points (痛点)** — acute, frequent, actively resented. Strongest signal.
- **Desires (痒点)** — aspirational, lower urgency. Validated only if behavior follows.
- **Trends (趋势)** — emerging shifts that change what's possible. Weak alone, strong combined with pain.

**Evaluation funnel:** `Frequency × Pain intensity × Willingness to pay`

A problem scoring high on all three is a painkiller; high on one is a vitamin. Don't ask "what can I
make?" — ask "who is suffering from what problem?" (product-principles §5).

## 6. User-Problem-Value triangle

Positioning must align at all three corners or it collapses:

```
        User (specific, nameable)
       /    \
      /      \
 Problem     Value (what they save/earn/avoid)
```

- **User** — name 3 specific people, not "everyone."
- **Problem** — the job they can't do well today.
- **Value** — the concrete outcome (save time, earn money, avoid risk), not the feature.

If any corner is vague ("all developers" / "make them productive" / "better tooling"), the triangle
collapses. Sharpen the vague corner before proceeding.

## 7. Lean Canvas

A one-page business-model snapshot for pressure-testing an idea fast:

| Problem | Solution | Unique value proposition | Unfair advantage | Customer segments |
|---|---|---|---|---|
| (top 3 problems) | (top 3 features, one per problem) | (one clear sentence) | (can't be easily copied) | (target users) |

| Cost structure | Revenue streams | Key metrics | Channels |
|---|---|---|---|

The canvas forces every assumption into a box. An empty box is an unexamined assumption. "Unfair
advantage" is the hardest box — if you can't fill it, you're competing on execution alone, which is fine
but should be a conscious choice.

## 8. MVP validation loop

```
Hypothesis (riskiest assumption) → Minimal version → Measure → Learn → Continue / Pivot
```

- The MVP tests **one hypothesis** — the assumption most likely to be wrong. Not a feature list.
- **Time-box, not feature-list** — "what can we build and test in [timeframe]?" defines scope.
- **Measure before building** — decide which metric proves/disproves the hypothesis before the test
  runs.
- **Continue or pivot** — pre-commit to the decision rule. "If activation < 30%, we pivot" decided
  before the test beats "well, the numbers are ambiguous" after.

Classic case: Dropbox's 3-minute demo video validated demand before the syncing code existed. The MVP
was a video, not software — because the riskiest assumption was "do people want this," not "can we
build the sync."
