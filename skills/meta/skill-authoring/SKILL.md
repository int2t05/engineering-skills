---
name: skill-authoring
description: Use when creating, editing, or evaluating a skill in this collection — writes SKILL.md frontmatter and four sections, generates the Codex adapter, runs the validator, and tunes description triggering. The authoring half of using-skills (which routes/consumes). Triggers on "write a skill", "edit skill", "skill eval", "tune triggers", "写技能", "改技能", "技能评估". Not for routing to an existing skill (use using-skills) or building an MCP server (use mcp-builder if added).
---

# Skill Authoring

Create, edit, and evaluate skills in this collection. Every skill conforms to the anatomy in
`references/skill-anatomy.md` and passes `scripts/validate-skills.sh`. This skill is the authoring
half — `using-skills` routes work to existing skills; this one makes new ones or fixes existing ones.

## When to use

- Creating a new skill (new SDLC phase gap, repeated task worth a skill)
- Editing an existing skill's frontmatter, steps, or references
- Tuning a skill's description triggers (false positives, false negatives, collision with another skill)
- Evaluating a skill — does it fire when it should, stay distinct from neighbors, change agent behavior?
- Triggers on "write a skill", "edit skill", "skill eval", "tune triggers", "写技能", "改技能", "技能评估"

**Not for:** routing a task to an existing skill (use `using-skills`); designing an MCP server (out of scope, see official mcp-builder docs); writing project docs like PRD/README (use `spec`/`oss-polish`).

## Steps

### 1. Check the anatomy before writing

Load [${CLAUDE_PLUGIN_ROOT}/references/skill-anatomy.md](${CLAUDE_PLUGIN_ROOT}/references/skill-anatomy.md) — the folder layout, frontmatter rules (name + description + optional disable-model-invocation only), the four body sections (When to use / Steps / Verify / References), the `**Output:**` convention, progressive disclosure (15-150 line SKILL.md, depth in `references/`), and the description hybrid format (`Use when…` + `Triggers on…` + exclusions, ≤1024 chars, no cross-skill phrase collisions).

### 2. Place the skill and wire the backbone

- **Phase** — pick the phase by output type + consumer, not by method. A skill producing a design artifact for design consumers goes in 03-design even if it reuses research methods (see `design-research`). Method does not set phase; output and consumers do.
- **Backbone** — every skill links `engineering-principles.md`. PM-side skills also link `product-principles.md`; UIUX skills also link `design-principles.md`. The validator enforces these (see `scripts/validate-skills.sh` `pm_skills`/`uiux_skills` lists — add the new skill there if it's PM or UIUX).
- **Path** — `skills/<phase>/<name>/SKILL.md` (kebab-case name, uppercase SKILL.md).

### 3. Write the description for routing, not features

- **Name actions, not tools.** "Use when retrieving real design references" not "Use WebFetch on galleries." The model routes on user intent, not on the tool the skill happens to run.
- **Hybrid format:** `Use when [intent]. [One sentence: what]. Triggers on "phrase1", "phrase2", "中文1" — also when user says "[natural cue]". Not for [exclusion] → use [other-skill].`
- **No collision.** Quoted trigger phrases must be unique across all skills — the validator's collision check flags any shared phrase. Before finalizing, grep the phrase across `skills/`.
- **Keep "Triggers on" literal** — the validator requires it; `gen-agents-yaml.py` cuts the description at that clause for the Codex adapter.

### 4. Write the four sections

- **When to use** — 2-4 conditions + a `**Not for:**` boundary naming the adjacent skills (prevents routing collisions). This is load-bearing: every boundary pair in this pack was deliberate.
- **Steps** — numbered, each independently verifiable. Push encyclopedic data into `references/<x>.md` loaded on demand (progressive disclosure). Reference files over 100 lines get a `## Contents` ToC (see the anatomy's progressive-disclosure rule).
- **Verify** — concrete evidence (file exists, no placeholders, count met), not "looks right".
- **References** — `engineering-principles.md` (+ domain backbone) + skill-specific `references/`. Every `references/` link must resolve (dead-link check).
- **Output** — declare `**Output:** <path>` only if the skill produces a doc/artifact. Behavior-only skills (implement, tdd, debugging) omit it. Every declared path must appear in `docs/skill-outputs.md` (validator syncs).

### 5. Generate the adapter + run the validator

```bash
python scripts/gen-agents-yaml.py   # generate agents/openai.yaml for every skill
bash scripts/validate-skills.sh      # schema + manifest-sync + collision + dead-links + domain-principles + Output-sync
```

Fix every FAIL before considering the skill done. The validator is the gate — a skill that doesn't
pass doesn't ship.

### 6. Sync the discovery surface

A new or renamed skill touches: `.claude-plugin/plugin.json` skills[] (the source), `docs/skill-outputs.md`
(if the skill produces a doc), `AGENTS.md` routing table, `skills/meta/using-skills/SKILL.md` phase list,
`skills/meta/using-skills/references/phase-tree.md`, and the `README.md` + `README.zh-CN.md` catalogs.
The catalog ordering and the `research (general/market/tech-selection modes)` suffix are human-curated,
so these are maintained by hand — but the validator now enforces them: the **presence check** fails if a
manifest skill is missing from any of the five routing surfaces, and the **dynamic Output scan** fails if
a declared `**Output:` path is missing from `docs/skill-outputs.md` (no hardcoded dict to update). A rename
is a breaking change (the old invocation name disappears) — bump the version and call it out in the commit.

### 7. Evaluate — does it actually work?

Three tiers (adapted from established skill-eval practice):

- **Structural** (free, CI) — validator green. Already done in Step 5.
- **Trigger & routing** (free, CI) — does the description fire on the right prompts and not collide? The collision check is the automated subset. For deeper routing eval, write ~3 positive + ~2 negative trigger prompts per skill and check the model routes correctly (defer to a later run, like the Tier 2 framework).
- **Behavioral** (tokens, on demand) — does an agent following the skill satisfy its `## Verify`? `bash scripts/run-eval.sh --skill <name>` runs the skill against real tasks with and without the skill loaded (RED-GREEN baseline) and grades the output. Every skill should have ≥3 cases (2 positive + 1 negative control) in `evals/cases/<name>.json` before it's trusted. This is the real test; do it before trusting the skill.

If a skill passes structural but fails behavioral, the SKILL.md is wrong even if the validator is green. Fix the skill, not the test.

## Verify

- [ ] `scripts/validate-skills.sh` green (count, manifest-sync, collision, dead-links, domain-principles, Output-sync)
- [ ] `gen-agents-yaml.py` generated the adapter with no drift
- [ ] Description follows the hybrid format; quoted phrases unique across the pack (grep-confirmed)
- [ ] Four sections present; `**Not for:**` names adjacent skills; `**Output:**` declared iff doc-producing
- [ ] All discovery surface files synced (plugin.json, validator lists, skill-outputs, AGENTS, phase-tree, using-skills, README×2)
- [ ] At least one behavioral check run against a real task (not just structural green); ≥3 eval cases in `evals/cases/<name>.json` for skills that gate real work

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline for every skill (surface assumptions, verify don't assume, surgical scope).
- [${CLAUDE_PLUGIN_ROOT}/references/skill-anatomy.md](${CLAUDE_PLUGIN_ROOT}/references/skill-anatomy.md) — the anatomy this skill enforces: folder layout, frontmatter, four sections, Output convention, progressive disclosure, description hybrid format, superset-of-official-spec note.
- [references/eval-tiers.md](references/eval-tiers.md) — the three eval tiers (structural / trigger-routing / behavioral) in detail, with the prompt-template for routing eval.
