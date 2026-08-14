# Engineering Skills

> Languages: English | [中文](README.zh-CN.md)

[![Build](https://img.shields.io/github/actions/workflow/status/int2t05/engineering-skills/validate.yml?label=build&branch=main)](https://github.com/int2t05/engineering-skills/actions/workflows/validate.yml)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-DA7857?logo=anthropic)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![version](https://img.shields.io/badge/version-2.4.0-blue)](./.claude-plugin/plugin.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

A Claude Code plugin — **43 engineering skills** organized by the software development
lifecycle. Shared engineering principles are injected at every session start, so the
discipline is ambient — not something you have to remember to load. PM and UIUX skills
additionally layer `product-principles.md` / `design-principles.md` as domain discipline.

Doc-producing skills split output into two layers: project-level (`docs/PRD.md` etc.,
concise, on main) and version-level (`docs/vX.Y/prd.md` etc., detailed, on version
branches). See [`docs/skill-outputs.md`](docs/skill-outputs.md) for the full matrix.

## Install

**Claude Code (primary):**

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

**Other agents (Codex, Cursor, Cline, Continue, OpenCode, Windsurf…):**
skill content is plain markdown. See [`.agents/install-block.md`](.agents/install-block.md)
for the canonical install commands.

## How to use

- **Auto-trigger:** skills activate when a task matches their description (English or
  Chinese — e.g. "技术选型", "性能优化", "深度检索").
- **Explicit call:** type `/skill-name` (`/tdd`, `/code-review`, `/debugging`).
- **Not sure which skill?** `/using-skills` routes the task to a phase.
- **Planning:** uses the harness's built-in plan mode, not a custom skill.

## Structure

```
engineering-skills/
├── .claude-plugin/          # plugin.json (manifest) + marketplace.json
├── .github/
│   ├── workflows/validate.yml   # CI: schema + adapter-sync + invocation-sync
│   ├── ISSUE_TEMPLATE/          # bug-report.md
│   └── PULL_REQUEST_TEMPLATE.md
├── skills/                   # 43 skills, 9 SDLC phases + meta
│   ├── meta/using-skills/       # router
│   ├── meta/skill-authoring/    # author + eval skills
│   ├── 01-product/ … 09-operate/
│   └── <skill>/SKILL.md + references/ + agents/openai.yaml
├── references/               # engineering / product / design principles (shared)
├── scripts/                  # validate-skills.sh, gen-agents-yaml.py
├── docs/                     # skill-outputs.md, workflow-prompts.md
├── AGENTS.md                 # universal entry for non-Claude agents
└── LICENSE                   # MIT
```

## Catalog — 43 skills by phase

| Phase | Skills |
|---|---|
| meta | using-skills, skill-authoring |
| 01-product | brainstorm, spec, oss-strategy |
| 02-research | research (general/market/tech-selection modes) |
| 03-design | architecture, api-design, frontend-design, schema-design, prompt-engineering, domain-modeling, prototype, codebase-design, image-to-code, imagegen, design-research |
| 04-develop | implement, multi-agent-orchestration, breakdown, context-engineering, i18n |
| 05-tune | performance, simplify, refactoring |
| 06-test | tdd, test-generation, api-testing, e2e-testing, load-testing |
| 07-verify | code-review, debugging, security-review, linting |
| 08-ship | shipping, git-workflow, ci-cd, deprecation-migration, oss-polish |
| 09-operate | observability, documentation-audit, incident-response, handoff |

> Triggers + routing: [`AGENTS.md`](AGENTS.md) · Product matrix: [`docs/skill-outputs.md`](docs/skill-outputs.md)

Validate the collection: `bash scripts/validate-skills.sh`

## Reporting Issues

Bugs and suggestions: [github.com/int2t05/engineering-skills/issues](https://github.com/int2t05/engineering-skills/issues)

## License

MIT — see [LICENSE](LICENSE).

## Provenance

Original skill concepts adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) and [mattpocock/skills](https://github.com/mattpocock/skills). This pack is a ground-up rewrite fusing those concepts with systematic PM/UIUX principles.
