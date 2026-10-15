# Model Evaluation

Model evaluations exercise real tasks with and without a skill. Task correctness and incremental value are separate: both runs passing means the skill has not demonstrated a benefit on that case, not that the task failed.

## Run

Requires the selected CLI to be installed and authenticated, plus the fixture tooling and Bash for shell-based acceptance commands. Do not include credentials in cases or transcripts.

```bash
python scripts/run-eval.py --backend claude --skill tdd --runs 1
python scripts/run-eval.py --backend codex --case tdd-001 --runs 1
python scripts/run-eval.py --backend claude --case spec-neg-001 --runs 1
```

`--model` selects a model explicitly; otherwise the CLI configuration applies. `--no-baseline` checks correctness only. All required rubric expectations must pass; the pass-rate threshold applies across repeated runs, not to silently dropping rubric items. More runs help reveal variance; a single sample is not statistical assurance.
Codex tasks use an isolated workspace with workspace-write policy; `--workspace-root` can select a host-approved parent directory. Windows sandbox access must be available; permission-denied runs are not evidence of skill quality. Actual tool availability and permissions affect the result. Claude uses its configured tool permissions. Do not bypass failures or ask the grader to assume unavailable work succeeded.

## What is measured

- Actual task behavior and output correctness, with deterministic acceptance commands where applicable.
- Relevant process evidence such as a real failing test before a fix.
- Negative controls: the workflow must not force a spec or extra artifact onto an adjacent small task.
- Baseline comparison for incremental benefit, separate from absolute success.

The with-skill run receives the self-contained installed content and can read its references. The baseline receives the same task without that content. Output paths in the task or acceptance checks are authorized for the isolated experiment.
This injection-based harness does not reproduce every host's automatic discovery or routing. Validate implicit triggering separately with the pack installed in the actual host.

## Cases and artifacts

Cases live at `evals/cases/<skill>.json`, with real fixtures under `evals/fixtures/`. Preserve concrete behavior expectations; do not force a document section count or fixed wording as a substitute for quality.

`grader.type` may be code-based, llm-judge or hybrid. Model grading is fallible: inspect the saved evidence and rerun suspected harness errors before attributing failure to a skill.

Artifacts are saved under `evals/results/<backend>/<case-id>/<with|base>-<n>/`: prompt, transcript, actual workspace and metadata. Summaries use `run-summary-<backend>.json`. These local files are ignored by Git.
Structural and installation tests run in CI. Model runs are on demand because they require access, time and tokens; a green structural check is not behavioral coverage.

## Coverage

The pilot suites cover tdd, spec, code-review and debugging. Other workflows need representative tasks and actual model runs before a behavioral reliability claim.
Use official evaluation patterns and real product tasks. Short descriptions and shared rules should earn their context cost by reducing observed errors or extra work, not by forcing a strong baseline to fail.
