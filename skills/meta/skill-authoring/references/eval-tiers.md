# Skill Evaluation Tiers

How to evaluate a skill beyond the structural validator. Three tiers, ascending in cost and
conviction. Adapted from established skill-eval practice (addyosmani's three-tier model + the
anthropics skill-creator eval pattern).

## Tier 1 — Structural (free, CI)

What `scripts/validate-skills.sh` already checks:

- Frontmatter: `name` + `description` (+ optional `disable-model-invocation`); no disallowed fields.
- `description` contains `Triggers on` / `触发`; ≤1024 chars.
- Four sections present: When to use (with `Not for`), Steps, Verify, References.
- `engineering-principles.md` linked; PM skills link `product-principles.md`; UIUX skills link `design-principles.md`.
- `agents/openai.yaml` exists and is in sync (`gen-agents-yaml.py`).
- `plugin.json` skills[] matches on-disk skills; count correct.
- No dead `references/` links; no cross-skill trigger-phrase collisions.
- `**Output:**` paths match `docs/skill-outputs.md`.

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

> The full Tier 2 prompt set (~5 per skill × 43 = ~215 prompts) is deferred to实战 — prompts should
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

## When to run each tier

| Tier | When | Cost | What it proves |
|---|---|---|---|
| 1 | Every change (CI) | Free | The skill is structurally valid |
| 2 | After a description rewrite or new skill | Free | The description routes correctly |
| 3 | Before trusting a skill in production | Tokens | The skill changes agent behavior as promised |

Most skills ship after Tier 1 + a spot-check Tier 2. Tier 3 is for skills that gate real work
(debugging, code-review, tdd, security-review) — run behavioral eval before relying on them.
