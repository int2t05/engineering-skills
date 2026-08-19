# Engineering Skills

> 语言：[English](README.md) | 中文

[![Build](https://img.shields.io/github/actions/workflow/status/int2t05/engineering-skills/validate.yml?label=build&branch=main)](https://github.com/int2t05/engineering-skills/actions/workflows/validate.yml)
[![Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-DA7857?logo=anthropic)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![version](https://img.shields.io/badge/version-2.8.1-blue)](./.claude-plugin/plugin.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

一个 Claude Code 插件——**47 个工程技能**，按软件开发生命周期组织。工程原则在每次会话
启动时注入，纪律成为环境上下文而非需要记住加载的东西。PM 与 UIUX 技能额外叠加
`product-principles.md` / `design-principles.md` 作为领域纪律层。

文档型技能的产物分两层：项目级（`docs/PRD.md` 等，简洁，main 分支）+ 版本级
（`docs/vX.Y/prd.md` 等，详细，版本分支）。完整矩阵见 [`docs/skill-outputs.md`](docs/skill-outputs.md)。

## 安装

**Claude Code（主要）：**

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

**其他 agent（Codex、Cursor、Cline、Continue、OpenCode、Windsurf…）：**
技能内容是纯 markdown。标准安装命令见 [`.agents/install-block.md`](.agents/install-block.md)。

## 使用方式

- **自动触发**：任务匹配技能描述时自动激活（中英文均可，如"技术选型"、"性能优化"、"深度检索"）。
- **显式调用**：输入 `/技能名`（如 `/tdd`、`/code-review`、`/debugging`）。
- **不知用哪个技能？** `/using-skills` 路由到对应阶段。
- **规划**：用内置 plan 模式，不是某个技能。

## 结构

```
engineering-skills/
├── .claude-plugin/          # plugin.json（清单）+ marketplace.json
├── .github/
│   ├── workflows/validate.yml   # CI：schema + adapter-sync + invocation-sync
│   ├── ISSUE_TEMPLATE/          # bug-report.md
│   └── PULL_REQUEST_TEMPLATE.md
├── skills/                   # 47 个技能，9 个 SDLC 阶段 + meta
│   ├── meta/using-skills/       # 路由
│   ├── meta/skill-authoring/    # 写 + 评估技能
│   ├── 01-product/ … 09-operate/
│   └── <skill>/SKILL.md + references/ + agents/openai.yaml
├── references/               # engineering / product / design 原则（共享）
├── scripts/                  # validate-skills.sh, gen-agents-yaml.py, run-eval, check-routing-overlap.py
├── docs/                     # skill-outputs.md, workflow-prompts.md
├── AGENTS.md                 # 非 Claude agent 的通用入口
└── LICENSE                   # MIT
```

## 目录——按阶段分列全部 47 个技能

| 阶段 | 技能 |
|---|---|
| meta | using-skills, skill-authoring |
| 01-product | brainstorm, spec, oss-strategy |
| 02-research | research（general/market/tech-selection 模式） |
| 03-design | architecture, api-design, frontend-design, schema-design, prompt-engineering, domain-modeling, prototype, codebase-design, image-to-code, imagegen, design-research |
| 04-develop | implement, multi-agent-orchestration, breakdown, context-engineering, i18n, auth-implementation, error-handling |
| 05-tune | cost-optimization, performance, simplify, refactoring |
| 06-test | tdd, test-generation, api-testing, e2e-testing, load-testing |
| 07-verify | a11y-review, code-review, debugging, security-review, linting |
| 08-ship | shipping, git-workflow, ci-cd, deprecation-migration, oss-polish |
| 09-operate | observability, documentation-audit, incident-response, handoff |

> 触发词与路由：[`AGENTS.md`](AGENTS.md) · 产物矩阵：[`docs/skill-outputs.md`](docs/skill-outputs.md)

校验本集合：`bash scripts/validate-skills.sh`

## 报告问题

Bug 与建议：[github.com/int2t05/engineering-skills/issues](https://github.com/int2t05/engineering-skills/issues)

## 许可证

MIT —— 见 [LICENSE](LICENSE)。

## 来源

原始技能概念改编自 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 与 [mattpocock/skills](https://github.com/mattpocock/skills)。本包是在其概念基础上融合系统性 PM/UIUX 原理的重新撰写。
