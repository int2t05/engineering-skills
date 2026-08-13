# Engineering Skills

> **语言：** [English](README.md) | 中文

一个 Claude Code 插件——**42 个工程技能**，按软件开发生命周期组织。从打磨模糊想法到上线运行，技能按阶段归类。

共享工程原则在每次会话启动时注入，纪律是环境性的——不必刻意加载。PM 侧与 UIUX 技能额外链接 `product-principles.md` / `design-principles.md` 作为领域纪律层。

文档型技能产物分两层：项目级（`docs/PRD.md` 等，简洁，main 分支）+ 版本级（`docs/vX.Y/prd.md` 等，详细，版本分支）。单版本项目回退 `docs/` 根。完整产物矩阵见 `docs/skill-outputs.md`。

## 安装

**Claude Code（首选）：**

```
/plugin marketplace add https://github.com/int2t05/engineering-skills
/plugin install engineering-skills@int2t05
```

本地开发用：`claude --plugin-dir /path/to/clone`。

**其他 agent（Codex、Cursor、Cline、Continue、OpenCode、Windsurf 等）：**

技能内容是纯 markdown。[`AGENTS.md`](AGENTS.md) 是通用入口——每次会话先读它。

```bash
npx skills@latest add int2t05/engineering-skills
# 或手动拷贝：把 skills/ + references/ + AGENTS.md 放进 agent 的指令目录
```

## 使用方式

- **自动触发：** 任务匹配技能 description 时自动激活（中英文皆可——如"技术选型"、"性能优化"、"深度检索"）。
- **显式调用：** 输入 `/技能名`（`/tdd`、`/code-review`、`/debugging`）。
- **拿不准用哪个技能？** `/using-skills` 把任务路由到对应阶段。
- **规划：** 用框架内置的 plan mode，不是自定义技能。

## 目录——按阶段分列全部 42 个技能

### meta

**`using-skills`** —— 路由器。把任务映射到 9 个阶段的对应技能。

- 触发："which skill should I use", "route this task", "用哪个技能", "路由".

### 01-product —— 澄清要做什么

**`brainstorm`** —— 一次问一个问题，把模糊想法磨成具体提案。

- 触发："brainstorm", "grill me", "interview me", "refine this idea", "头脑风暴", "帮我打磨想法", "盘问我". *仅限用户调用.*

**`spec`** —— 写 spec/PRD（目标、结构、命令、代码风格、测试、边界），写代码前先定。

- 触发："write spec", "create prd", "spec out", "写需求文档", "写规格", "需求文档".

**`oss-strategy`** —— 开源战略：商业模式、COSS、open core、商业化、增长。

- 触发："open source strategy", "OSS 策略", "DevHunt", "开源策略", "开源商业模式".

### 02-research —— 动手前先调研

**`research`** —— 深度网络调研，带来源核验，产出带引用的 Markdown 文档。

- 触发："deep research", "source-backed investigation", "cited report", "深度调研", "深度检索", "调研报告", "调研转文档".

**`market-research`** —— 市场规模、竞品对比、投资尽调、行业情报。

- 触发："market sizing", "competitor analysis", "due diligence", "市场调研", "市场规模", "竞品分析".

**`tech-selection`** —— 为具体需求选型/对比技术栈、库、框架或仓库。

- 触发："技术选型", "方案对比", "选哪个", "tech stack", "library comparison", "技术对比".

### 03-design —— 编码前先设计

**`architecture`** —— 高层系统架构：NFR、模式、组件、ADR。

- 触发："system design", "架构设计", "ADR", "scalability", "系统设计", "架构决策".

**`domain-modeling`** —— 构建/锐化领域模型：挑战术语、场景压测、更新 CONTEXT.md + ADR。

- 触发："domain model", "ubiquitous language", "CONTEXT.md", "领域模型", "统一语言", "领域建模".

**`api-design`** —— API/接口设计：REST/GraphQL 契约、版本、错误模型、易用性。

- 触发："design API", "REST contract", "GraphQL schema", "接口设计", "API 契约", "API 设计".

**`codebase-design`** —— 深模块、重构/深化机会、可测试性。

- 触发："deep modules", "refactor architecture", "deepening", "深化模块", "重构架构", "代码库设计".

**`frontend-design`** —— 有辨识度的生产级 UI：色彩、字体、布局、交互状态。

- 触发："frontend", "UI", "design", "界面设计", "前端设计".

**`image-to-code`** —— 图片优先的前端管线——先生成设计参考图，深度分析，再实现代码忠实还原。

- 触发："image to code", "设计图转代码", "图片实现", "从设计图实现".

**`brandkit`** —— 品牌识别图生成——logo 概念、身份板、配色、字体、mockup，面向高端品牌系统。

- 触发："brand kit", "品牌识别", "logo 设计", "品牌系统".

**`imagegen-web`** —— 网站设计参考图生成——每个 section 一张横向图，面向落地页和营销站的高端艺术方向。只出图，不写代码。

- 触发："web design image", "website mockup", "landing page image", "section image", "网站设计图", "网页参考图", "落地页配图".

**`imagegen-mobile`** —— 移动端 app 屏幕与流程图生成——iOS/Android/跨平台概念，带手机 mockup 框。只出图，不写代码。

- 触发："mobile design image", "app screen image", "mobile mockup", "app flow", "移动端设计图", "app 屏幕图", "手机界面图", "移动端流程图".

**`schema-design`** —— 数据模型设计——实体、关系、范化、索引、约束、分区，面向新功能或限界上下文。

- 触发："data model", "schema design", "database design", "ER model", "数据模型", "表结构设计", "数据库设计".

**`prompt-engineering`** —— 设计提示词、评测或 LLM 驱动特性——prompt 架构、模型选型、guardrails、eval 体系。

- 触发："prompt engineering", "LLM feature", "eval harness", "prompt design", "提示词工程", "LLM 特性", "prompt 设计".

**`prototype`** —— 一次性原型验证设计问题（逻辑用单 HTML，或可切换 UI 变体对比）。

- 触发："prototype", "compare layouts", "validate the interaction", "sketch out", "try this quickly", "build a demo", "原型", "试做", "试这个方案", "搭个快速 demo".

### 04-develop —— 实现

**`implement`** —— 按 spec/ticket 实现：在接缝处 TDD、类型检查、全量测试、code-review、提交。也覆盖轻量改动（小编辑、重命名、搭骨架）。

- 触发："implement", "build this", "code the feature", "实现", "编码", "改这个配置", "重命名", "搭项目骨架".

**`breakdown`** —— 把 plan/spec 拆成带阻塞边的 tracer-bullet ticket；大工作用决策地图。

- 触发："break into tickets", "decompose", "wayfinder", "拆解任务", "拆票", "任务分解".

**`context-engineering`** —— 实现前组装正确的文件、定义和先前决策到工作上下文，或解释现有代码。

- 触发："agent lacks context", "what files matter", "解释这段代码", "这个模块怎么工作", "带我过一遍代码库".

**`i18n`** —— 国际化——消息提取、ICU/MessageFormat、locale 路由、RTL 布局、复数、本地化格式。

- 触发："i18n", "localization", "l10n", "RTL", "国际化", "本地化", "多语言".

### 05-tune —— 优化

**`performance`** —— 先量后优：profile、定位瓶颈、改进。

- 触发："webperf", "performance regression", "慢", "性能优化", "性能调优".

**`simplify`** —— 清晰胜过聪明：移除投机性抽象和死复杂度。

- 触发："simplify", "too complex", "refactor for clarity", "简化", "太复杂", "重构求清晰".

### 06-test —— 证明能用

**`tdd`** —— 红绿重构，一次一个垂直切片。

- 触发："tdd", "test-driven", "red green refactor", "测试驱动开发", "红绿重构", "测试驱动".

**`test-generation`** —— 为现有代码或从 spec 生成测试文件（非 TDD 循环——用 tdd）。任意框架。

- 触发："generate tests", "write tests for", "生成测试", "生成测试代码", "补测试".

**`api-testing`** —— API 测试策略：契约、REST/GraphQL、集成。

- 触发："test API", "contract testing", "integration test", "API 测试", "接口测试", "契约测试".

**`e2e-testing`** —— 端到端/浏览器测试：用户旅程、表单提交、运行时 UI 验证（默认 Playwright，或等价方案）。

- 触发："playwright", "e2e test", "browser test", "end-to-end", "端到端测试", "浏览器测试".

**`load-testing`** —— 容量验证——生成真实与对抗流量，找破坏点，刻画饱和度，验证自动伸缩。

- 触发："load test", "stress test", "capacity", "k6", "Locust", "压测", "压力测试", "容量测试".

### 07-verify —— 合并前评审

**`code-review`** —— 双轴评审：Standards（约定 + 坏味道基线）和 Spec（忠于来源 issue），并行子 agent。

- 触发："review this", "code review", "before merge", "代码审查", "代码评审", "合并前审查".

**`debugging`** —— 纪律化诊断：建红灯回路 → 最小化 → 假设 → 插桩 → 修复 → 回归测试。也覆盖日志排查。

- 触发："debug", "bug", "test failure", "unexpected behavior", "调试", "排查 bug", "读日志", "排查错误日志".

**`security-review`** —— 对待提交变更做安全评审：密钥、认证、注入、访问控制、加固。

- 触发："security review", "check for vulnerabilities", "安全审查", "安全审计", "漏洞检查".

### 08-ship —— 部署

**`shipping`** —— 上线生产：清单、特性开关、分阶段发布、回滚、首小时验证。

- 触发："ship", "deploy", "launch", "go live", "上线", "发布", "部署到生产".

**`git-workflow`** —— 提交/分支/合并冲突/守卫/pre-commit。按意图解冲突——绝不 `--abort`。

- 触发："commit", "merge conflict", "rebase", "pre-commit", "提交", "合并冲突", "分支管理".

**`ci-cd`** —— CI/CD 流水线与自动化：build/test/deploy、流水线设计、策略。

- 触发："CI pipeline", "GitHub Actions", "deployment strategy", "CI/CD", "流水线", "持续集成", "部署策略".

**`deprecation-migration`** —— 弃用旧代码/API、迁移系统或升级依赖：保持行为的分阶段路径。

- 触发："deprecate", "migrate", "sunset API", "弃用", "迁移", "升级依赖", "更新这个库", "upgrade dependency".

**`oss-polish`** —— 美化开源项目的 GitHub 形象：README、topics、叙事、趋势定位。

- 触发："polish my repo", "开源项目美化", "优化项目展示".

### 09-operate —— 运行

**`observability`** —— 加日志/指标/告警/插桩；让运行时行为可观测。

- 触发："add logging", "metrics", "alerting", "instrumentation", "加日志", "可观测性", "监控告警".

**`documentation-audit`** —— 同步漂移文档到代码，或从零写新文档。

- 触发："docs out of date", "documentation drift", "sync docs", "写文档", "写 README", "文档化这个功能", "文档同步".

**`handoff`** —— 把工作交接给另一个会话/agent：结构化简报（上下文、决策、下一步）。

- 触发："handoff", "hand over", "交接", "移交工作". *仅限用户调用.*

**`incident-response`** —— 生产事故响应——严重度分级、遏制、沟通、回滚 vs 修复决策、无指责复盘。

- 触发："incident", "on-call", "page", "postmortem", "事故响应", "线上故障", "复盘".

## 校验

```bash
bash scripts/validate-skills.sh          # schema + manifest-sync + adapter-sync + invocation-sync
python scripts/gen-agents-yaml.py        # 重新生成 Codex 适配器（编辑 frontmatter 后）
```

MIT.

## 来源

原始技能概念改编自 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 与 [mattpocock/skills](https://github.com/mattpocock/skills)，本地保留于 `archive/`（已 gitignore）供查阅。本包是在其概念基础上融合系统性 PM/UIUX 原理的重新撰写。
