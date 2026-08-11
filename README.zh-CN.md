# Engineering Skills（工程技能包）

> **语言：** [English](README.md) | 中文

一个统一的 agent 技能包——**33 个工程技能**，按软件开发生命周期组织。以 Claude Code 插件形式发布（每次会话启动自动注入共享工程原则），同时兼容 Codex、Cursor、Cline、Continue、OpenCode 等任何读取 `AGENTS.md` 的 agent。

由三个来源集合合并而成（83 → 33）：24 个个人根技能、[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)（24，MIT）、[mattpocock/skills](https://github.com/mattpocock/skills)（35，MIT）。原始仓库本地保留（已 gitignore）作溯源。

## 安装

**Claude Code（主推——SessionStart 钩子注入环境原则）：**

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

或本地开发用：`claude --plugin-dir /path/to/clone`。

安装后，SessionStart 钩子会把 8 条工程原则（[`references/engineering-principles.md`](references/engineering-principles.md)）作为环境上下文注入——每次会话都自带这套纪律。技能按 `description:` 触发短语自动激活，也可显式按名调用（`/tdd`、`/code-review`、`/brainstorm`）。

**其他 agent 框架（Codex、Cursor、Cline、Continue、OpenCode、Windsurf 等）：**

技能内容是纯 markdown。[`AGENTS.md`](AGENTS.md) 是通用入口——每次会话先读它获取路由 + 原则。两条路线（二选一——Claude Code 插件与文件拷贝互斥）：

```bash
# skills.sh——覆盖最广（70+ agent）；只装内容文件（不含 SessionStart 钩子）
npx skills@latest add int2t05/engineering-skills

# 或手动拷贝：把 skills/ + references/ + AGENTS.md 放进 agent 的指令目录
```

每个技能带一个 `agents/openai.yaml`（Codex 适配器：`display_name`、`short_description`，用户调用型技能还有 `policy.allow_implicit_invocation`），保证两个框架保持同步。规范措辞见 [`.agents/install-block.md`](.agents/install-block.md)。

## 工作方式

- **通用入口：** `AGENTS.md` 给任何 agent 定向——路由表、调用模型、安装。Claude Code 作为插件读取；其他框架会话启动时读取。
- **自动触发：** 31 个技能在任务匹配其 `description:` 触发短语时激活（含中文短语如 "技术选型"、"生成测试"、"性能优化"）。
- **显式调用：** 输入 `/技能名`（如 `/tdd`、`/debugging`）。`brainstorm` 和 `handoff` 仅限显式调用（`disable-model-invocation: true` ↔ `agents/openai.yaml` 的 `allow_implicit_invocation: false`）。
- **路由：** 拿不准用哪个技能？调用 `using-skills`——它把任务映射到对应阶段。
- **规划：** 用各框架内置的 plan mode（Claude Code：`EnterPlanMode`/`ExitPlanMode`），不是自定义技能（原则 §7）。
- **渐进式披露：** 每个 `SKILL.md` 是精简核心；百科式数据放在技能内的 `references/` 按需加载。

## 目录——按阶段分列全部 33 个技能

### meta（元）
**`using-skills`** —— 路由器。把任务映射到 9 个阶段的对应技能。
- 触发：会话开始，或"该用哪个技能"。
- 产出：路由到的技能被激活。

### 01-product（产品）—— 澄清要做什么
**`brainstorm`** —— 一次问一个问题，把模糊想法磨成具体提案。
- 触发："brainstorm"、"grill me"、"interview me"、"refine this idea"。*仅显式调用。*
- 产出：用户确认的提案；可据此写 spec。

**`spec`** —— 写 spec/PRD（目标、结构、命令、代码风格、测试、边界），写代码前先定。
- 触发："write spec"、"create prd"、"spec out"、"to spec"。
- 产出：覆盖 6 个核心领域的规范文档。

**`oss-strategy`** —— 开源战略：商业模式、COSS、open core、商业化、增长。
- 触发："open source strategy"、"OSS 策略"、"DevHunt"、"developer tools directory"。
- 产出：战略决策（不是 GitHub 美化——那是 `oss-polish`）。

### 02-research（调研）—— 动手前先调研
**`research`** —— 深度网络调研，带来源核验，产出带引用的 Markdown 文档。
- 触发："深度调研"、"source-backed investigation"、"cited report"。
- 产出：带引用的 Markdown 文件（`research/YYYY-MM-DD-<slug>.md`）。

**`market-research`** —— 市场规模、竞品对比、投资尽调、行业情报。
- 触发："市场规模"、"竞品分析"、"尽调"。
- 产出：面向决策的研究摘要，带来源归属。

**`tech-selection`** —— 为具体需求选型/对比技术栈、库、框架或仓库。
- 触发："技术选型"、"方案对比"、"选哪个"、"tech stack"、"library comparison"。
- 产出：对比矩阵 + 推荐。

### 03-design（设计）—— 编码前先设计
**`architecture`** —— 高层系统架构：NFR、模式、组件、ADR。
- 触发："系统设计"、"架构设计"、"ADR"、"scalability"。
- 产出：ADR + 架构图。参考：adr-template、architecture-patterns、database-selection、nfr-checklist、system-design。

**`domain-modeling`** —— 构建/锐化领域模型：挑战术语、场景压测、更新 CONTEXT.md + ADR。
- 触发："领域模型"、"统一语言"、"CONTEXT.md"。
- 产出：共享的统一语言文档 + ADR。

**`api-design`** —— API/接口设计：REST/GraphQL 契约、版本、错误模型、易用性。
- 触发："设计 API"、"REST 契约"、"GraphQL schema"。
- 产出：契约规范（应用 Hyrum's Law、One-Version Rule）。

**`codebase-design`** —— 深模块、重构/深化机会、可测试性。
- 触发："深模块"、"重构架构"、"deepening"。
- 产出：深化机会报告；选一个深入处理。

**`frontend-design`** —— 有辨识度的生产级 UI：色彩、字体、布局、交互状态。
- 触发："frontend"、"UI"、"design"、"界面设计"。
- 产出：可用的 UI 代码。参考：styles（18）、palettes（12）、font-pairings（31）、ux-guidelines（232）、apple-hig。

**`prototype`** —— 一次性原型验证设计问题（逻辑用单 HTML，UI 用可切换变体）。
- 触发："原型"、"对比布局"、"验证交互"。
- 产出：一次性 HTML 文件；设计问题得到回答。

### 04-develop（开发）—— 实现
**`implement`** —— 按 spec/ticket 实现：在接缝处 TDD、类型检查、全量测试、code-review、提交。
- 触发："实现"、"build this"、"编码这个功能"。
- 产出：已提交、已测试、已评审的代码。参考：source-verification、doubt-cycle。

**`breakdown`** —— 把 plan/spec 拆成 tracer-bullet ticket（带阻塞边）；大工作用决策地图。
- 触发："拆 ticket"、"分解"、"wayfinder"。
- 产出：带阻塞边的 ticket，或决策地图。

**`context-engineering`** —— 实现前组装正确的文件、定义和先前决策到工作上下文。
- 触发："agent 缺上下文"、"哪些文件重要"。
- 产出：打包好的工作上下文。参考：context-strategies。

### 05-tune（调优）—— 优化
**`performance`** —— 先量后优：profile、定位瓶颈、改进。
- 触发："webperf"、"性能回归"、"慢"、"性能优化"。
- 产出：profile + 针对性修复。参考：bottlenecks、anti-patterns。

**`simplify`** —— 清晰胜过聪明：移除投机性抽象和死复杂度。
- 触发："简化"、"太复杂"、"重构求清晰"。
- 产出：保持行为的更简代码。参考：opportunities。

### 06-test（测试）—— 证明能用
**`tdd`** —— 红绿重构，一次一个垂直切片。
- 触发："tdd"、"测试驱动开发"、"red green refactor"、"红绿重构"。
- 产出：通过的测试 + 行为已验证。参考：test-strategy（测试金字塔、测试替身层级）、mocking、good-tests、testing-anti-patterns。

**`test-generation`** —— 为现有代码或从 spec 生成测试文件（非 TDD 循环——用 tdd）。任意框架。
- 触发："生成测试"、"write tests for"、"create tests"。
- 产出：测试文件 + 覆盖决策矩阵。

**`api-testing`** —— API 测试策略：契约、REST/GraphQL、集成。
- 触发："测 API"、"契约测试"、"集成测试"。
- 产出：测试脚手架 + schema。参考：templates、schemas。

**`e2e-testing`** —— 端到端/浏览器测试：Playwright 流、表单提交、DevTools 驱动。
- 触发："playwright"、"e2e 测试"、"浏览器测试"、"端到端"。
- 产出：E2E 测试文件。参考：playwright-rules。

### 07-verify（验证）—— 合并前评审
**`code-review`** —— 双轴评审：Standards（约定 + 坏味道基线）和 Spec（忠于来源 issue），并行子 agent。
- 触发："评审这个"、"code review"、"合并前"。
- 产出：已核验的问题报告。

**`debugging`** —— 纪律化诊断：建红灯回路 → 最小化 → 假设 → 插桩 → 修复 → 回归测试。
- 触发："调试"、"bug"、"测试失败"、"异常行为"。
- 产出：根因 + 回归测试。参考：hitl-loop-template。

**`security-review`** —— 对待提交变更做安全评审：密钥、认证、注入、访问控制、加固。
- 触发："安全评审"、"查漏洞"。
- 产出：安全问题报告。

### 08-ship（发布）—— 部署
**`shipping`** —— 上线生产：清单、特性开关、分阶段发布、回滚、首小时验证。
- 触发："发布"、"部署"、"上线"、"go live"。
- 产出：带回滚就绪的发布。

**`git-workflow`** —— 提交/分支/合并冲突/守卫/pre-commit。按意图解冲突——绝不 `--abort`。
- 触发："提交"、"合并冲突"、"rebase"、"pre-commit"。
- 产出：干净的提交 / 已解冲突。参考：block-dangerous-git、pre-commit-setup。

**`ci-cd`** —— CI/CD 流水线与自动化：build/test/deploy、流水线设计、策略。
- 触发："CI 流水线"、"GitHub Actions"、"部署策略"。
- 产出：流水线配置 + 策略。

**`deprecation-migration`** —— 弃用旧代码/API 或迁移系统：保持行为的分阶段路径。
- 触发："弃用"、"迁移"、"下线 API"。
- 产出：迁移计划（绞杀者/适配器/扩展-收缩）。

**`oss-polish`** —— 美化开源项目的 GitHub 形象：README、topics、叙事、趋势定位。
- 触发："美化仓库"、"开源项目美化"、"优化项目展示"。
- 产出：精修的 README + topics + 叙事。参考：badges、scripts。

### 09-operate（运维）—— 运行
**`observability`** —— 加日志/指标/告警/插桩；让运行时行为可观测。
- 触发："加日志"、"指标"、"告警"、"插桩"。
- 产出：插桩 + 上线前清单。参考：observability-checklist。

**`documentation-audit`** —— 审计文档漂移；同步 Swagger、功能文档、通用文档到代码。
- 触发："文档过时"、"文档漂移"、"同步文档"。
- 产出：已同步的文档。参考：templates。

**`handoff`** —— 把工作交接给另一个会话/agent：结构化简报（上下文、决策、下一步）。
- 触发："交接"、"handoff"。*仅显式调用。*
- 产出：交接简报（存盘或作为后台 agent 启动）。

## 约定

- **插件布局：** `.claude-plugin/plugin.json` 用 `skills[]` 数组声明全部 33 个技能（嵌套 `./skills/<阶段>/<技能>` 路径——保留 9 阶段分类）。
- **每个技能：** 文件夹 + `SKILL.md`（大写）；frontmatter 为 `name` + `description`（+ 可选 `disable-model-invocation`）；正文按 When to use / Steps / Verify / References 四节。
- **多框架：** `AGENTS.md`（通用入口）+ `.agents/`（调用模型、安装块）+ 每技能 `agents/openai.yaml`（Codex 适配器）。用户调用型技能在 Claude Code（`disable-model-invocation`）和 Codex（`allow_implicit_invocation: false`）两端保持同步——校验器强制这条不变量。
- **共享参考：** 在插件根 `references/`，技能内用 `${CLAUDE_PLUGIN_ROOT}/references/...` 链接（Claude Code 跨项目可移植；其他框架经 `AGENTS.md` 用仓库相对路径读取）。
- **环境原则：** SessionStart 钩子（`hooks/session-start`）每次 Claude Code 会话注入 `engineering-principles.md`；其他框架经 `AGENTS.md` 读取。
- **校验：** `bash scripts/validate-skills.sh`（schema + 清单同步 + Codex 适配器 + 调用同步）。重新生成 Codex 适配器：`python scripts/gen-agents-yaml.py`。

## 溯源

83 → 33 合并自：24 个个人根技能 + [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)（24，MIT）+ [mattpocock/skills](https://github.com/mattpocock/skills)（35，MIT）。原始仓库本地保留在 `archive/`（已 gitignore）。
