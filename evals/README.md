# Behavioral Eval Harness

Tests whether a skill actually changes agent behavior — not just whether it's
well-authored (the structural validator covers that). Implements the **RED-GREEN
pattern**: every case runs twice, with-skill and without-skill (baseline). A case
passes only when the with-skill run satisfies the expectations *and* the baseline
does not — proving the skill itself made the difference.

## Run

```bash
# All pilot skills (tdd, spec, code-review, debugging)
bash scripts/run-eval.sh

# One skill
bash scripts/run-eval.sh --skill tdd

# One case, 3 runs (statistical confidence)
bash scripts/run-eval.sh --case tdd-001 --runs 3

# Skip baselines (faster, but can't prove the skill changes behavior)
bash scripts/run-eval.sh --no-baseline

# Pin a model
bash scripts/run-eval.sh --model claude-sonnet-5
```

Exit code = number of failed cases (matches `validate-skills.sh` convention).

## When to run

- **On demand** — before trusting a skill in production, after a SKILL.md rewrite.
- **Weekly CI schedule** — catches regressions from model updates
  (`.github/workflows/eval-behavioral.yml`).
- **NEVER as a CI gate** — behavioral evals are slow (5-10 min/case),
  non-deterministic, and token-costly. Tier 1 (`validate-skills.sh`) remains the
  CI gate.

## Directory structure

```
evals/
  cases/<skill>.json    # one JSON array per skill, each element is one eval case
  fixtures/             # shared input files (starter repos, buggy diffs, failing tests)
  agents/grader.md      # the LLM-judge grader prompt
  results/              # gitignored run outputs (transcripts, grading.json, summary)
```

## Eval case format

Each case is a JSON object in `cases/<skill>.json`:

```json
{
  "id": "tdd-001",
  "skill_under_test": "skills/06-test/tdd",
  "task_prompt": "Implement parseDuration(s) ... Use TDD.",
  "negative_control": false,
  "fixture": "evals/fixtures/tdd-starter",
  "grader": {
    "type": "hybrid",
    "code_check": {
      "command": "npm test",
      "cwd": "{workspace}",
      "pass_condition": "exit_code == 0"
    },
    "llm_judge": {
      "agent": "evals/agents/grader.md",
      "expectations": [
        "A test file was written before the implementation file",
        "The agent ran the test and observed it fail (RED phase)",
        "..."
      ]
    }
  },
  "runs": 1,
  "timeout_seconds": 300
}
```

**Key fields:**
- `id` — `<skill>-<NNN>` (positive) or `<skill>-neg-<NNN>` (negative control)
- `skill_under_test` — path to the skill directory (runner reads SKILL.md)
- `task_prompt` — exactly what the agent receives. Real user phrasing.
- `negative_control` — `true` = the skill should NOT activate. Grader checks
  absence of the skill's workflow, not presence. Tests precision, not just recall.
- `fixture` — directory copied to a temp workspace per run. `null` if none.
- `grader.type` — `code-based` (run a command, check exit code), `llm-judge`
  (rubric scoring via grader subagent), or `hybrid` (both; pass = code AND judge).
- `grader.code_check` — deterministic check: command, cwd, pass condition.
- `grader.llm_judge.expectations` — verifiable statements the grader scores
  PASS/FAIL against the transcript + output files.
- `runs` — repetitions (1 for MVP, 3 for CI confidence). A case passes if
  pass_rate >= 0.67 (2/3).
- `timeout_seconds` — per-run wall-clock timeout.

## Grader types

- **code-based** — runs a command (`npm test`, `pytest`), checks exit code + file
  existence. Fast, deterministic. For code-producing skills (tdd, implement,
  test-generation, api-testing, e2e-testing, etc.).
- **llm-judge** — a grader subagent reads the transcript + output files, scores
  each expectation PASS/FAIL with evidence. For doc/behavior skills (spec,
  architecture, code-review, debugging, etc.).
- **hybrid** — both. Code check (tests pass) + LLM-judge (process followed).
  Most code-producing pilot skills use hybrid.

## RED-GREEN baseline

Every case runs with-skill AND without-skill. The with-skill prompt includes the
full SKILL.md content; the baseline omits it. A case is **discriminating** when
with-skill passes and baseline fails. If both pass, the case doesn't prove the
skill adds value (flagged as "non-discriminating" in the summary, not a failure).

## Negative controls

Every skill's eval suite should include at least one negative control — a task
where the skill should NOT activate. This tests precision (the skill doesn't
over-trigger), not just recall. A negative control passes when the agent does NOT
invoke the skill's workflow for a task outside its scope.

## Writing new cases

1. Pick a skill and a realistic task a user would actually phrase that way.
2. Write 3-5 positive cases covering the skill's core workflow.
3. Write 1-2 negative controls (tasks the skill's `**Not for:**` excludes).
4. For code-producing skills, prefer `hybrid` graders (deterministic check +
   process judge). For doc/behavior skills, use `llm-judge`.
5. Expectations should be verifiable from the transcript or output files — not
   subjective ("good quality"). Quote what evidence would satisfy each.
6. Run `bash scripts/run-eval.sh --skill <name> --runs 3` and iterate until
   with-skill reliably beats baseline.

See `skills/meta/skill-authoring/references/eval-tiers.md` for the full tier
methodology (structural / trigger-routing / behavioral).
