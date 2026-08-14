# Brainstorm Techniques

Ideation frameworks, evaluation rubric, and worked examples. Use selectively — pick the
lens that fits the idea, don't run every framework mechanically.

## Contents

- [Ideation Frameworks](#ideation-frameworks)
- [Decision Techniques](#decision-techniques)
- [Evaluation Rubric](#evaluation-rubric)
- [Worked Example](#worked-example)
- [What to Notice in This Example](#what-to-notice-in-this-example)

## Ideation Frameworks

### Divergent Lenses

Use these in Step 4 (Diverge) to generate 3–8 idea variations from a confirmed intent.

- **Inversion:** "What if we did the opposite?" Charge the customer instead of the merchant;
  async instead of sync; pickup instead of delivery.
- **Constraint removal:** "What if budget/time/tech weren't factors?" Then walk back to what's
  essential.
- **Audience shift:** "What if this were for [different user]?" Regulars instead of new
  customers; the quiet team members instead of the loud ones.
- **Combination:** "What if we merged this with [adjacent idea]?" Retro + experimentation;
  ordering + retention automation.
- **Simplification:** "What's the version that's 10x simpler?" One action item instead of
  twenty; SMS instead of an app.
- **10x version:** "What would this look like at massive scale?" AI-mediated collaboration
  instead of manual conflict resolution.
- **Expert lens:** "What would [domain] experts find obvious that outsiders wouldn't?"
  Facilitators know safety is the #1 retro killer, not format.

**Best for:** Generating diverse variations from a confirmed intent during the diverge phase.

### SCAMPER

Structured transformation of an existing idea. Best for improving or reimagining existing
products, less useful for greenfield ideas.

- **Substitute:** Swap a component, technology, audience, or business model.
- **Combine:** Merge with another product, service, or idea.
- **Adapt:** Borrow from other industries, domains, or time periods.
- **Modify (Magnify/Minimize):** 10x bigger, 10x smaller, exaggerate one feature, strip to minimum.
- **Put to other uses:** Who else could use this? What other problems could it solve?
- **Eliminate:** Remove a feature entirely. Zero configuration. Half the steps.
- **Reverse/Rearrange:** Opposite order. User does the work instead of the system.

### How Might We (HMW)

Reframe problems as opportunities. Start with an observation, reframe as "How might we
[desired outcome] for [specific user] without [key constraint]?"

- **Good:** Narrow enough to be actionable, broad enough to allow creative solutions, contains
  a tension that forces creativity. ("...help new users find relevant content in their first
  5 minutes")
- **Bad:** Too broad ("make users happy"), too narrow ("add a sidebar"), or solution-embedded
  ("build a chatbot").

**Best for:** Reframing stuck thinking. When someone is anchored on a solution, pull them back to the problem.

### First Principles Thinking

Break the idea to fundamental truths, then rebuild:

1. What do we know is **true** (not assumed, not conventional)?
2. What are we **assuming**? List every assumption, even the obvious ones.
3. Which assumptions can we **challenge**? "Is this a law of physics, or just how it's been done?"
4. **Rebuild** from the truths alone.

Best for breaking out of incremental thinking when every idea feels like a small improvement
on the status quo.

### Jobs to Be Done (JTBD)

Focus on what the user is trying to accomplish, not what they say they want:

- **Functional job:** What task are they completing?
- **Emotional job:** How do they want to feel?
- **Social job:** How do they want to be perceived?

Format: "When I [situation], I want to [motivation], so I can [expected outcome]."
Key insight: people hire products to do a job. Netflix competes with sleep, not just other
streaming services.

**Best for:** Understanding the real problem. When you're not sure if you're solving the right thing.

### Constraint-Based Ideation

Deliberately impose constraints to force creative solutions: time ("1 day to build"),
feature ("only one feature"), tech ("can't use the obvious technology"), cost ("free
forever"), audience ("never used a computer"), scale ("1 billion users" vs "just 10").

**Best for:** Cutting through complexity. When the idea is growing too large or too vague.

### Pre-mortem

Imagine the idea has already failed. Work backwards:

1. It's 12 months from now. The project shipped and flopped. What went wrong?
2. List every plausible reason for failure — technical, market, team, timing.
3. For each failure mode: Is this preventable? Is it a signal the idea needs to change?
4. Which failure modes are you willing to accept? Which ones would kill the project?

**Best for:** Stress-testing ideas that feel good but haven't been pressure-tested.

### Analogous Inspiration

Look at how other domains solved similar problems:

- What industry has already solved a version of this problem?
- What would this look like if [specific company/product] built it?
- What natural system works this way?
- What historical precedent exists?

Find *structural* similarities, not surface-level ones. "Uber for X" is surface-level.
"A two-sided marketplace that solves a trust problem between strangers" is structural.

**Best for:** Generating variations that feel genuinely different from the obvious approach.

## Decision Techniques

Alternatives to one-question-at-a-time dialogue for specific situations.

### Design Tree / Frontier

Map decisions as a **design tree**: every decision branches into the decisions that hang off it.
Work the **frontier** — every decision whose prerequisites are already settled (the questions you
can ask now without guessing at answers you haven't heard yet). Ask the whole frontier in one round:
number each question and give your recommended answer. Then wait for answers before the next round.

Each round of answers reshapes the tree — settled decisions push the frontier outward and unblock
dependent questions. A question whose answer depends on another still-open question belongs to a
later round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the
environment (filesystem, tools, etc.), dispatch a sub-agent to find it — don't ask the user for
anything you could look up yourself. Don't block on it: a running exploration is an unsettled
prerequisite, so only the questions downstream of it wait for the sub-agent to report — ask the
rest of the frontier now. The _decisions_ are the user's — put each to them and wait.

**Best for:** Complex multi-decision plans where questions have dependencies. Complements
one-question-at-a-time — use when the decision graph is wide and shallow, not deep and narrow.

### Questionnaire Handoff

Turn a decision you can't fully answer into a **questionnaire** for a third party who holds
knowledge you lack. Write it as a Markdown document they fill in async or walk through together.

Interview the user only about the *send* (who it goes to, what they need back) — never grill them
about the subject they can't answer. The questions in the document target the gap between what the
recipient knows and what the user needs. Order questions most-important-first (async may be one
pass), one idea per question, never compound.

**Best for:** When a decision requires expertise the user doesn't have (domain knowledge,
infrastructure details, stakeholder constraints) and an async handoff is more practical than a
live session.

## Evaluation Rubric

Use during convergence to stress-test 2–3 clustered directions.

### 1. User Value (most important)

**Painkiller vs. Vitamin:**
- **Painkiller:** Acute, frequent problem. Users actively seek it. They'll switch. Signs:
  emotional descriptions, existing workarounds, willingness to pay.
- **Vitamin:** Nice to have. Marginal improvement. Users nod politely, don't change behavior.

**Questions:**
- Can you name 3 specific people who have this problem right now?
- What are they doing today instead? (The real competitor is always the current workaround.)
- Would they switch? What would make them switch?
- How often? (Daily > monthly.)
- Is this "pull" (users asking) or "push" (you think they should want it)?

**Red flags:** "Everyone could use this" (no specific user); "like X but better" (marginal);
real but rare (high intensity, low frequency).

### 2. Feasibility

- Does the core technology exist and work reliably?
- What's the hardest technical problem? Known-hard or novel?
- Dependencies on third parties, APIs, or data you don't control?
- Minimum team/effort for MVP? Specialized expertise needed?
- How quickly can you get something in front of users? (Days/weeks, not months.)

**Red flags:** "We just need to solve [very hard research problem] first"; multiple
dependencies that all need to work simultaneously; MVP requires months.

### 3. Differentiation

Not better — *different*. What's the one thing this does that nothing else does?

**Types (strongest to weakest):**
1. New capability (previously impossible)
2. 10x improvement on a key dimension
3. New audience (brings capability to the excluded)
4. New context (works where existing solutions fail)
5. Better UX (dramatically simpler)
6. Cheaper (weakest — easily competed away)

**Red flags:** differentiation is entirely technology, not experience; "faster/cheaper/prettier"
without a structural reason; the differentiating feature isn't the one users care most about.

### Assumption Audit

For every direction, list assumptions in three categories:

- **Must be true (dealbreakers):** If wrong, the idea dies. Validate before building.
  Example: "Users will share their data with us."
- **Should be true (important):** Significantly impacts success but doesn't kill the idea.
  Adjust the approach if wrong. Example: "Users prefer self-serve over talking to a person."
- **Might be true (nice to have):** Secondary features or optimizations. Don't validate until
  core is proven. Example: "Users will share results with teammates."

### Decision Framework

When choosing between directions, rank on this matrix:

|                    | High Feasibility | Low Feasibility |
|--------------------|------------------|-----------------|
| **High Value**     | Do this first    | Worth the risk  |
| **Low Value**      | Only if trivial  | Don't do this   |

Use differentiation as the tiebreaker between options in the same quadrant.

### MVP Scoping

1. **One job, done well.** Not three jobs done partially.
2. **Riskiest assumption first.** The MVP's purpose is to test the assumption most likely wrong.
3. **Time-box, not feature-list.** "What can we build and test in [timeframe]?"
4. **The "Not Doing" list is mandatory.** Explicitly name what you're cutting and why.
5. **If it's not embarrassing, you waited too long.** The first version should feel incomplete.

## Worked Example

**User invokes:** "I want to help small local restaurants compete with the big delivery platforms."

### Phase 1: Understand & Expand

**Skill restates:** How might we give independent restaurants the reach and convenience
customers expect from delivery platforms, without forcing them into a model that erodes
their margins and brand?

**Sharpening questions (one at a time):** Which part of "compete" — acquisition, logistics,
UX, retention, or margin pressure? Who are you building for — the owner or the diner?
What's the constraint — software, cooperative, physical?

**User clarifies:** Restaurant owners. The core pain is 25-30% commission to delivery apps
but they can't opt out because that's where customers are. Thinking software.

**Skill generates 6 variations:**
1. **Direct Channel Toolkit** — branded ordering to move existing customers off-platform.
2. **Inversion** — charge the customer, not the restaurant; "support your local spot."
3. **Constraint removal** — pickup-only, no delivery; restaurants keep 100%.
4. **Combination** — restaurant collective, shared platform, cross-promotion.
5. **Audience shift** — build exclusively for existing regulars; "your usual?" one-tap reorder.
6. **Expert lens** — owners are in the kitchen; the tool must run itself (auto-texts, auto-reorders).

### Phase 2: Evaluate & Converge

User picks 1 + 5 + 6. Skill clusters into two directions:

**Direction A: The "Regulars Engine" (5 + 6 fused)** — retention tool for existing repeat
customers, zero management.
- User value: high. Every direct reorder saves 25-30% commission. 50 regulars = $20K/year.
- Feasibility: medium. Ordering tech is commodity; hard part is identifying regulars without
  manual work.
- Differentiation: high for the niche. Too small for DoorDash to care — exactly why it's a wedge.
- Hidden assumptions: regulars will use a new ordering method (most likely to be wrong);
  owners will share customer contact info; direct ordering won't cannibalize dine-in.
- What could kill it: customers won't switch channels. Habit is powerful.

**Direction B: Direct Channel + Retention Hybrid (1 + 5)** — branded ordering plus retention.
- Higher ceiling, but building two products. Each piece individually has competitors.
- Hidden assumption: bundling is better than partnering with existing tools.
- What could kill it: scope. Two things well is exponentially harder than one.

**Honest read:** Direction A is the sharper bet. The biggest risk is channel-switching —
SMS-based reorder (no app install) might crack it.

### Phase 3: Sharpen & Ship

The output is a one-pager: Problem Statement, Recommended Direction, Key Assumptions to
Validate, MVP Scope, Not Doing (and why), Open Questions.

**MVP Scope:** SMS-based reordering for self-identified regulars. 15-minute setup. Customer
receives "want your usual Thursday order?" text, confirms, pays via link. Pickup only. No
discovery, no marketplace, no app.

**Not Doing:** delivery logistics (expensive, not the core problem); customer acquisition
(that's the platform's game); branded apps/websites (commodity — Square and Toast do this);
menu management/POS integration (scope creep); analytics dashboards (owner is in the kitchen).

## What to Notice in This Example

1. **The restatement changes the frame.** "Compete" becomes "retain existing customers."
2. **Questions diagnose before prescribing.** Each question determines which type of problem
   this actually is.
3. **Variations have reasons.** Each explains *why* it exists (what lens generated it).
4. **The skill has opinions.** "I'd push you toward A." It tells you what it thinks.
5. **Phase 2 is honest.** Ideas get called out for low differentiation or high complexity.
6. **The "Not Doing" list does real work.** Specific and reasoned — things you might *want*
   to do but shouldn't yet.
