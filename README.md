# Engineering Skills

[中文](README.zh-CN.md) · [MIT](LICENSE) · [CI](https://github.com/int2t05/engineering-skills/actions/workflows/validate.yml)

Engineering workflows for Claude Code, Codex and other agents that read Agent Skills.
Use task-specific guidance for requirements, design, implementation, verification and operation, with concise shared rules and human-auditable documents.

## Install

**Claude Code**

```text
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

**Codex** — managed plugin:

```bash
codex plugin marketplace add https://github.com/int2t05/engineering-skills.git
codex plugin add engineering-skills@int2t05
```

Update with `codex plugin marketplace upgrade int2t05`, then `codex plugin add engineering-skills@int2t05` to refresh the installed copy. Restart Codex if needed.

**Standalone skills / other hosts** — Python 3.10 or later, including Windows:

```bash
git clone https://github.com/int2t05/engineering-skills.git
cd engineering-skills
python scripts/install-skills.py
```

Installs self-contained skill folders into `~/.agents/skills`. Shared resources are bundled; no plugin root variable or symlink is needed.
Use `--skill implement --skill debugging` for a selection. [Installation and updates](.agents/install-block.md) covers conflicts, local edits and other destinations.
Avoid duplicate installations in the same host.

## Use

Claude Code: `/implement`. Codex plugin: `$engineering-skills:implement`; standalone: `$implement`. Supported hosts may also select skills from matching intent.
`brainstorm` and `handoff` require explicit invocation. Use `using-skills` when routing is uncertain, not before every simple task.

Start at the task that needs solving; a clear edit does not need a full lifecycle.
Confirm document paths before creation, movement or renaming. Significant requirements and design remain reviewable; human acceptance is separate from technical checks.

[Task prompts](docs/workflow-prompts.md) · [Routing](AGENTS.md) · [Output choices](docs/skill-outputs.md) · [Shared rules](references/engineering-principles.md)

## Catalog

| Phase | Skills |
|---|---|
| 01-product | brainstorm, oss-strategy, spec |
| 02-research | research |
| 03-design | api-design, architecture, codebase-design, design-research, domain-modeling, frontend-design, image-to-code, imagegen, prompt-engineering, prototype, schema-design |
| 04-develop | auth-implementation, breakdown, context-engineering, error-handling, i18n, implement, multi-agent-orchestration |
| 05-tune | cost-optimization, performance, refactoring, simplify |
| 06-test | api-testing, e2e-testing, load-testing, tdd, test-generation |
| 07-verify | a11y-review, code-review, debugging, linting, security-review |
| 08-ship | ci-cd, deprecation-migration, git-workflow, oss-polish, shipping |
| 09-operate | documentation-audit, handoff, incident-response, observability, purity-audit |
| meta | skill-authoring, using-skills |

## Verify and contribute

```bash
python scripts/gen-agents-yaml.py
bash scripts/validate-skills.sh
python -m unittest discover -s test -v
```

CI checks schema, catalogs, output declarations, adapter drift and self-contained installation. Behavioral model evaluation is separate and on demand; these checks do not prove model quality.
See [evaluation guidance](evals/README.md). Report a reproducible problem via [GitHub Issues](https://github.com/int2t05/engineering-skills/issues); the issue and PR templates identify scope and evidence. Follow [skill anatomy](references/skill-anatomy.md) when contributing a workflow.

## Layout

- `skills/`: phase-organized workflows, references and generated Codex adapters.
- `references/`: shared engineering, product, design and human-audit guidance.
- `scripts/` and `test/`: validation, installation and real filesystem checks.
- `.claude-plugin/` and `hooks/`: Claude Code integration.
- `docs/`: task prompts, output guidance and project coordination.

## Sources

Workflow comparisons: [OpenAI skills](https://github.com/openai/skills), [Anthropic skills](https://github.com/anthropics/skills), [Superpowers](https://github.com/obra/superpowers), [Addy Osmani](https://github.com/addyosmani/agent-skills) and [Matt Pocock](https://github.com/mattpocock/skills).
Instructions are adapted to this pack's task boundaries and approval model; reference projects are not runtime dependencies.
