# Engineering Skills

[English](README.md) · [MIT](LICENSE) · [CI](https://github.com/int2t05/engineering-skills/actions/workflows/validate.yml)

面向 Claude Code、Codex 与其他 Agent Skills 宿主的软件工程技能包。
按任务提供需求、设计、开发、验证与运维工作流；通用规则保持简洁，文档支持人工审计。

## 安装

**Claude Code**

```text
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

**Codex** — 原生插件：

```bash
codex plugin marketplace add https://github.com/int2t05/engineering-skills.git
codex plugin add engineering-skills@int2t05
```

更新时先执行 `codex plugin marketplace upgrade int2t05`，再执行 `codex plugin add engineering-skills@int2t05` 刷新安装副本。必要时重启 Codex。

**独立技能 / 其他宿主** — 需要 Python 3.10 或以上，支持 Windows：

```bash
git clone https://github.com/int2t05/engineering-skills.git
cd engineering-skills
python scripts/install-skills.py
```

默认安装到 `~/.agents/skills`。每个技能包含所需共享资源，不依赖插件环境变量或符号链接。
只装部分技能可加 `--skill implement --skill debugging`。更新、冲突保护及其他宿主见[安装说明](.agents/install-block.md)。同一宿主避免重复安装。

## 使用

Claude Code 输入 `/implement`；Codex 插件输入 `$engineering-skills:implement`，独立安装输入 `$implement`。支持自动发现的宿主也可根据意图选择技能。
`brainstorm` 与 `handoff` 需显式调用。路由不确定时用 `using-skills`，简单任务不必重复路由。

从实际任务进入，明确的小改动不走完整生命周期。新建、移动、重命名文档前确认路径；重大需求与方案供人工审计，技术验证不代签人工确认。

[任务提示词](docs/workflow-prompts.md) · [技能路由](AGENTS.md) · [产物选择](docs/skill-outputs.md) · [通用准则](references/engineering-principles.md)

## 技能目录

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

## 验证与贡献

```bash
python scripts/gen-agents-yaml.py
bash scripts/validate-skills.sh
python -m unittest discover -s test -v
```

CI 检查结构、目录、产物声明、适配器漂移与真实安装。模型行为评估单独按需运行，格式和安装通过不代表模型效果已证实。
见[评估说明](evals/README.md)。通过 [GitHub Issues](https://github.com/int2t05/engineering-skills/issues) 提交可复现的问题；Issue/PR 模板记录范围与证据。贡献技能遵循[编写规范](references/skill-anatomy.md)。

## 结构

- `skills/`：按阶段组织的工作流、引用资料与 Codex 适配器。
- `references/`：共享工程、产品、设计与人工审计规则。
- `scripts/`、`test/`：验证、安装和真实文件系统检查。
- `.claude-plugin/`、`hooks/`：Claude Code 集成。
- `docs/`：任务提示词、产物说明与项目协调文档。

## 参考来源

参考 [OpenAI skills](https://github.com/openai/skills)、[Anthropic skills](https://github.com/anthropics/skills)、[Superpowers](https://github.com/obra/superpowers)、[Addy Osmani](https://github.com/addyosmani/agent-skills)、[Matt Pocock](https://github.com/mattpocock/skills) 的实际工作流与资源组织，按本包的任务边界和人工确认方式重新组织。参考仓库不是运行依赖。
