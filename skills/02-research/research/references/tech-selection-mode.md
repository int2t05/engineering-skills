# Technology Selection

Choose a library, framework, service or repository for concrete requirements. Present the decision using [report-spine.md](report-spine.md).

## Inputs

Identify must-have behavior, platform, actual runtime, deployment constraints, scale, team capacity and migration cost. Inspect existing dependencies first.
Ask when a missing constraint changes the choice; do not silently choose requirements for the user.

## Evidence

- Official documentation and releases establish supported behavior, compatibility and lifecycle.
- Actual source, tests, examples, issues and licenses establish implementation fit and maintenance constraints.
- Community reports reveal operational friction and questions to verify, not conclusive capability facts.
- Popularity and marketing claims are context, not decision criteria by themselves.

Select credible candidates that address the same requirement. Do not force a minimum count or clone repositories without a decision they inform.
Record relevant repository commits and files. Read the license and current compatibility guidance rather than relying on remembered categories.

## Comparison

Compare fit, integration effort, failure behavior, operating complexity, security, data ownership, license and reversibility as relevant.
Show which criteria are hard constraints and which are preferences. Use weighted scoring only when the weights and uncertain inputs are meaningful; it must not disguise a subjective choice as measured precision.
For detailed cost and migration comparisons, load [selection-rubric.md](selection-rubric.md).

## Decision

Recommend the simplest candidate meeting actual constraints. Explain the strongest rejected alternative, remaining uncertainty and an experiment that could overturn the recommendation.
Update the existing owner of the question at its approved path; do not create timestamped duplicates merely because a file already exists.

## Verify

- Recommendations rely on actually read primary or implementation evidence.
- Comparisons use the same requirements and show material constraints.
- Missing capability claims are limited to what was checked; unsupported absence claims remain unverified.
- Integration and migration risks are explained; no unrun benchmark is treated as measured evidence.
