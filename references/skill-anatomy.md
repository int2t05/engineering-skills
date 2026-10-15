# Skill Anatomy

Skills add task-specific knowledge and reliable decision boundaries. They are not encyclopedias or mandatory itineraries.

## Layout

`skills/<phase>/<name>/SKILL.md` contains the lean workflow; `references/` carries depth loaded on demand. `agents/openai.yaml` is generated Codex metadata.
Use source-relative Markdown links. Shared resources are linked relative to the skill directory; the installer copies and rewrites external dependencies into a self-contained skill. Never require a host-specific root variable.

## Frontmatter

Required: `name` and `description`. Optional: `disable-model-invocation: true` for intentionally user-invoked workflows.
Names match kebab-case directories. Describe the specific intent in one short sentence, followed by a small `Triggers on` list including a relevant Chinese phrase.
Do not enumerate all methods or broaden triggers to every task in the domain. Quoted trigger phrases are unique across the pack; semantic overlap still needs real routing evaluation.
Descriptions must fit the host limit; favor about one hundred characters over filling the entire allowance.

## Body

- `## When to use`: intent and a `**Not for:**` boundary naming adjacent workflows.
- `## Steps`: practical actions, inputs and consequential choices. No repeated general principles or knowledge the model already supplies.
- `## Verify`: observable evidence corresponding to the actions. Make unavailable checks explicit.
- `## References`: shared engineering principles and relevant task references, with brief load conditions.

Target 15–150 lines; move depth into references. Long references include a `## Contents` map. Keep skill-owned references one level deep where practical; generated distribution resources may preserve their source hierarchy.
A reference listed as optional must not silently introduce mandatory subagents, commits, output files or approvals contrary to the main workflow.

## Outputs and human review

Use `**Output:**` for useful durable artifacts; behavior-only skills omit it.
Paths are suggestions, not automatic authorization. Confirm document purpose and path under [human-audit.md](human-audit.md), then preserve that authorization across the task.
Keep output declarations and [the matrix](../docs/skill-outputs.md) aligned.

PRD, TECH and PLAN normally use one project-level owner. Separate release detail under `docs/vX.Y/` only when independent scopes need maintaining; do not duplicate documents by default or force a branch layout.
Do not generate a fixed document set, pad audit item counts or require human approval to claim that author checks passed. Human acceptance and technical verification are separate states.

## Domain references

Every skill links [engineering-principles.md](engineering-principles.md). Product skills also link product-principles; UI design skills link design-principles. Artifact-producing skills link human-audit.
English skill instructions support cross-platform use; Chinese trigger phrases and reader-oriented outputs support the personal workflow.

## Maintenance and verification

1. Compare real neighboring implementations and define representative tasks.
2. Update metadata, workflow and necessary references, keeping names stable unless a change is explicitly intended.
3. When names or outputs change, synchronize plugin manifest, AGENTS routing, phase tree, router catalog, README catalogs and output matrix.
4. Generate adapters with `python scripts/gen-agents-yaml.py` and run `bash scripts/validate-skills.sh`.
5. Run `python -m unittest discover -s test -v` to exercise actual self-contained installation and conflict handling.
6. Evaluate real agent runs against a baseline; record task completion, routing, unnecessary work, time and cost separately. Structural and installer tests do not prove model benefit.

The base Agent Skills format requires a folder and SKILL.md metadata; these additional conventions keep this pack coherent without coupling it to one host.
