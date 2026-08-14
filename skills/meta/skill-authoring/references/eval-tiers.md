# Skill Evaluation Tiers

How to evaluate a skill beyond the structural validator. Three tiers, ascending in cost and
conviction. Adapted from established skill-eval practice (addyosmani's three-tier model + the
anthropics skill-creator eval pattern).

## Contents

- [Tier 1 — Structural (free, CI)](#tier-1--structural-free-ci)
- [Tier 2 — Trigger & routing (free, CI-safe)](#tier-2--trigger--routing-free-ci-safe)
- [Tier 3 — Behavioral (tokens, on demand)](#tier-3--behavioral-tokens-on-demand)
- [Tier 3 Implementation — the behavioral eval harness](#tier-3-implementation--the-behavioral-eval-harness)
- [When to run each tier](#when-to-run-each-tier)

## Tier 1 — Structural (free, CI)

What `scripts/validate-skills.sh` already checks:

- Frontmatter: `name` + `description` (+ optional `disable-model-invocation`); no disallowed fields.
- `description` contains `Triggers on` / `触发`. (The ≤1024-char limit is documented in `skill-anatomy.md` but not yet enforced by the validator — tracked as TODO A2.)
- Four sections present: When to use (with `Not for`), Steps, Verify, References.
- `engineering-principles.md` linked; PM skills link `product-principles.md`; UIUX skills link `design-principles.md`.
- `agents/openai.yaml` exists with required fields (`interface`, `display_name`, `short_description`) and invocation-sync (`disable-model-invocation` / `allow_implicit_invocation`). Full regeneration sync via `gen-agents-yaml.py` is a separate CI step in `validate.yml`.
- `plugin.json` skills[] matches on-disk skills; count correct.
- No dead `references/` links; no cross-skill trigger-phrase collisions.
- `**Output:**` paths match `docs/skill-outputs.md`.
- Discovery-surface presence: every manifest skill appears in all 5 routing surfaces (README×2, AGENTS.md, phase-tree.md, using-skills/SKILL.md).
- WARN (non-blocking): reference files >100 lines without a `## Contents` ToC; SKILL.md files >150 lines.

**A skill passing Tier 1 is structurally valid, not behaviorally correct.** It can still fail to
fire, collide semantically, or not change agent behavior. Tier 1 is the floor.

## Tier 2 — Trigger & routing (free, CI-safe)

Does the description fire on the right prompts and stay distinct from neighbors?

- **Positive prompts** — 3 prompts that *should* trigger this skill. Does the model route to it
  top-k? Write them as real user phrasings, not keyword tests.
- **Negative prompts** — 2 prompts that *should not* trigger this skill, each tagged with the skill
  that *should* own it (`owner`). Does this skill stay out of the top-k?
- **Collision check** — the validator's literal-phrase collision check is the automated subset. For
  semantic collision (two descriptions near-collide on meaning but not exact phrases), write prompts
  that could route to either and check which wins.

Prompt template (one per skill, stored for re-runs):

```json
{
  "skill_name": "<name>",
  "trigger": {
    "positive": [
      { "prompt": "<real user phrasing that should fire this skill>", "top_k": 3 }
    ],
    "negative": [
      { "prompt": "<phrasing that should fire a different skill>", "owner": "<other-skill>" }
    ]
  }
}
```

**A Tier-2 failure usually means fix the description, not the eval.** Missing vocabulary → add the
phrase users actually say. Over-broad → narrow the `Use when…` or sharpen the `Not for`.

> The full Tier 2 prompt set (~5 per skill × 45 = ~225 prompts) is deferred to实战 — prompts should
> target the final descriptions after a refactor, not be written prematurely. This reference defines
> the shape so the work is ready when prioritized.

## Tier 3 — Behavioral (tokens, on demand)

Does an agent following the skill actually satisfy its `## Verify` checklist?

- Run the skill against a **real task** (not a toy). Materialize real project inputs if needed.
- Read the **full execution trace** — tool calls, outputs, decisions — not just the final reply.
- Judge against the skill's own `## Verify` items: did each check pass? Did the agent cut corners the
  skill forbids?
- Include **pressure cases** — time pressure, sunk-cost pressure, authority pressure — to verify the
  workflow holds when the prompt argues for skipping it.

**A skill passing Tier 1 + Tier 2 but failing Tier 3 has a wrong SKILL.md** — the description routes
correctly but the body doesn't change behavior. Fix the body (steps, verify, references), not the
eval. This is the real test; a skill untested at Tier 3 is a hypothesis, not a shipped skill.

## Tier 3 Implementation — the behavioral eval harness

> **Status: experimental / not-yet-proven.** The harness runs and persists artifacts (transcripts,
> grading.json, workspace snapshots), but formal RED-GREEN runs on GLM-5.2 have not yet
> achieved discrimination — a strong model passes the current cases without the skill loaded.
> The tuning roadmap (pressure cases, analyzer pass, multi-run variance, dual-gate grading)
> lives in `docs/TODO.md` (section A5). There is no CI workflow; evals run locally on demand.

The harness lives in `evals/` and runs via `scripts/run-eval.sh`. It implements the
**RED-GREEN pattern**: every case runs twice (with-skill and without-skill/baseline) to
prove the skill changes behavior, not just that the agent can do the task. If the
baseline also passes, the case is flagged "non-discriminating" (the task doesn't
exercise the skill's value) — not a failure, but a signal to harden the case.

### Directory structure

- `evals/cases/<skill>.json` — one file per skill, JSON array of eval cases
- `evals/fixtures/` — shared input files (starter repos, buggy diffs, failing tests)
- `evals/agents/grader.md` — the LLM-judge grader prompt
- `evals/results/` — gitignored run outputs (transcripts, grading.json, summary)

### Eval case format

Each case: `id`, `skill_under_test`, `task_prompt` (real user phrasing), `negative_control`
(bool), `fixture`, `grader` (type: code-based / llm-judge / hybrid), `runs`, `timeout_seconds`.
`expectations` nests inside `grader` — under `grader.llm_judge.expectations` for hybrid,
or `grader.expectations` for flat llm-judge. See `evals/README.md` for the full schema.

### Grader types

- **code-based** — runs a command (`npm test`, `pytest`), checks exit code. Fast, deterministic.
  For code-producing skills (tdd, implement, test-generation, api-testing, e2e-testing, etc.).
- **llm-judge** — a grader subagent reads transcript + outputs, scores each expectation
  PASS/FAIL with evidence. For doc/behavior skills (architecture, code-review, etc.).
- **hybrid** — both. Used when both outcome (tests pass) and process (discipline followed)
  matter: the current pilots tdd, spec, debugging all use hybrid; code-review uses llm-judge.

### Running evals

```bash
bash scripts/run-eval.sh                      # all pilot skills
bash scripts/run-eval.sh --skill tdd          # one skill
bash scripts/run-eval.sh --case tdd-001 --runs 3   # one case, 3 runs (statistical confidence)
bash scripts/run-eval.sh --no-baseline        # faster, but can't prove the skill changes behavior
```

Exit code = number of failed cases (matches `validate-skills.sh`). A case passes when its
pass-rate ≥ 0.67 (2/3 by default).

### Negative controls

Every skill's eval suite should include at least one negative control — a task where the skill
should NOT activate (drawn from its `**Not for:**` boundary). This tests precision (the skill
doesn't over-trigger), not just recall. A negative control passes when the agent does NOT invoke
the skill's workflow for a task outside its scope.

### When to run

- On demand (manual, local) — before trusting a skill in production, after a SKILL.md rewrite.
- **NEVER as a CI gate** — behavioral evals are slow (5-10 min/case), non-deterministic, and
  token-costly. Tier 1 (`validate-skills.sh`) remains the CI gate. There is no CI workflow.

### Pilot skills

`tdd`, `spec`, `code-review`, `debugging` — 2-5 cases each, including negative controls. See
`evals/cases/`. The pattern is proven on these four; expanding to all 45 skills is mechanical
case-writing once a skill's grader type and expectations are defined.

## When to run each tier

| Tier | When | Cost | What it proves |
|---|---|---|---|
| 1 | Every change (CI) | Free | The skill is structurally valid |
| 2 | After a description rewrite or new skill | Free | The description routes correctly |
| 3 | Before trusting a skill in production | Tokens | The skill changes agent behavior as promised |

Most skills ship after Tier 1 + a spot-check Tier 2. Tier 3 is for skills that gate real work
(debugging, code-review, tdd, security-review) — run behavioral eval before relying on them.
