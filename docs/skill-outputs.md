# Skill 产物矩阵

> 每个产出 markdown 文档的 skill 的固定产物路径。产物路径在各 skill 的 SKILL.md 里声明
>（`**Output:**` 标记或 Steps 散文）；本表是速查视图。
>
> 命名规则：**全大写** = 项目级正式文档（docs/ 根，单文件）；**全大写目录** = 多文件集合
>（docs/ 根）；**阶段目录** = 中间产物按阶段归类（`docs/research/`、`docs/design/`），
> 目录内全大写=该阶段主文档、小写=中间产物。

## 文档型 skill（产 md）

| skill | 阶段 | 产物 | 路径 | 命名 | 作用 |
|---|---|---|---|---|---|
| `spec` | 01-product | 需求文档 | `docs/PRD.md` | 大写 | 项目级需求，shared source of truth |
| `architecture` | 03-design | 架构总览 | `docs/TECH.md` | 大写 | 系统架构图、组件、NFR、数据层 |
| `architecture` | 03-design | 决策记录 | `docs/design/adr/NNNN-slug.md` | 阶段目录 | 每项重大架构决策的 ADR |
| `domain-modeling` | 03-design | 统一语言 | `CONTEXT.md` | 大写 | 项目术语表（根目录） |
| `domain-modeling` | 03-design | 决策记录 | `docs/design/adr/NNNN-slug.md` | 阶段目录 | 领域建模产生的 ADR（共享 design/adr/） |
| `api-design` | 03-design | API 契约 | `docs/API/*.md` | 大写目录 | 每端点组一份，请求/响应/错误/示例 |
| `frontend-design` | 03-design | UIUX 设计报告 | `docs/design/DESIGN.md` | 阶段目录 | 从零设计：设计系统/信息架构/交互/组件规划 |
| `frontend-design` | 03-design | 前端审计 | `docs/design/frontend-audit.md` | 阶段目录 | 审计现有前端的优化建议 |
| `schema-design` | 03-design | 数据模型文档 | `docs/design/SCHEMA.md` | 阶段目录 | ER 图 + 实体/索引/约束/分区规划 |
| `prompt-engineering` | 03-design | 提示词设计文档 | `docs/design/PROMPT.md` | 阶段目录 | prompt 架构 + 模型选型 + eval + guardrails |
| `breakdown` | 04-develop | 实现计划 | `docs/PLAN.md` | 大写 | ticket 拆解作章节，blocking edges |
| `code-review` | 07-verify | 待办清单 | `docs/TODO.md` | 大写 | 代码↔TODO 双向校验的项目级待办 |
| `security-review` | 07-verify | 安全报告 | `docs/security-report.md` | 小写 | 按严重度的安全发现 + 修复/接受理由 |
| `incident-response` | 09-operate | 复盘报告 | `docs/postmortem/YYYY-MM-DD-<slug>.md` | 阶段目录 | 无指责复盘：时间线/影响/根因/行动项 |
| `tech-selection` | 02-research | 技术对比 | `docs/research/competitor.md` | 阶段目录 | 技术选型对比矩阵 + 推荐（PRD 输入） |
| `market-research` | 02-research | 市场调研 | `docs/research/market.md` | 阶段目录 | 用户原话/竞品/行业情报（PRD 输入） |
| `research` | 02-research | 调研档案 | `docs/research/YYYY-MM-DD-<slug>.md` | 阶段目录 | 带引用的深度调研，累积存档 |
| `oss-polish` | 08-ship | README | `README.md` | 大写 | 开源展示面 |
| `oss-polish` | 08-ship | 仓库摘要 | `REPOSITORY_SUMMARY.md` | 大写 | 架构/组件/技术/数据流 |
| `oss-polish` | 08-ship | 叙事史 | `THE_STORY_OF_THIS_REPO.md` | 大写 | commit 历史叙事 |
| `performance` | 05-tune | 性能台账 | `PERF.md`（可选） | 大写 | 尝试记录（kept + reverted），防重复踩坑 |
| `load-testing` | 06-test | 容量报告 | `docs/CAPACITY.md`（可选） | 大写 | 容量上限/瓶颈/自动伸缩验证/行动项 |
| `documentation-audit` | 09-operate | 同步现有 5 类 | 不产新文件 | — | 把 prd/tech/todo/api/flow 同步到代码 |
| `handoff` | 09-operate | 交接简报 | OS 临时目录 | — | 给下一会话的 context/决策/下一步 |
| `brainstorm` | 01-product | 产品路线图 | `ROADMAP.md` | 大写 | 产品定位/多版本/验收项 |
| `brainstorm` | 01-product | 用户访谈记录 | `docs/research/interview.md` | 阶段目录 | discovery 访谈发现（PRD 输入） |
| `oss-strategy` | 01-product | 商业策略 | `docs/research/strategy.md` | 阶段目录 | 商业模式/定价/GTM（PRD 输入） |
| `frontend-design` | 03-design | 用户研究 | `docs/research/ux-research.md` | 阶段目录 | persona/journey/可用性测试（DESIGN 输入） |
| `prototype` | 03-design | 原型验证结论 | `docs/design/prototype-findings.md` | 阶段目录 | 测试问题/结论/验证决策 |
| `codebase-design` | 03-design | 代码库审计 | `docs/design/codebase-audit.md` | 阶段目录 | 深化机会/选定候选/grill 结论 |

## 正式文档（docs/ 只保留这 5 类）

| 文档 | 产出 skill | 风格 |
|---|---|---|
| `docs/PRD.md` | spec | mermaid 为主，文字简洁 |
| `docs/TECH.md` | architecture | mermaid 为主，文字简洁 |
| `docs/API/*.md` | api-design | 详细请求/响应 |
| `docs/FLOW/*.md` | 跨任务产物 | mermaid 流程 + 详细数据流描述 |
| `docs/TODO.md` | code-review | 按业务合并 |

## 跨任务产物（非 skill 直接产出，工作流约定）

| 产物 | 路径 | 产出方式 |
|---|---|---|
| 业务流程文档 | `docs/FLOW/*.md` | 按 workflow-prompts 的 FLOW 提示词 |
| 前端结构审计 | `docs/FRONT.md` | 按 workflow-prompts 的 FRONT 提示词 |
| 用户可见功能 | `FEATURES.md` | 按 workflow-prompts 的 FEATURES 提示词 |
| AI 上下文指令 | `CLAUDE.md` | `/init` 或 workflow-prompts 的 CLAUDE.md 生成提示词 |
| 忽略规则 | `.gitignore` | 按 workflow-prompts 的 .gitignore 提示词 |

## 图片型 skill（产图片，不写代码）

| skill | 阶段 | 产物 | 作用 |
|---|---|---|---|
| `brandkit` | 03-design | 品牌识别图 | logo 概念/身份板/配色/字体/mockup |
| `imagegen-web` | 03-design | 网站设计参考图 | 每 section 一张横向图，落地页/营销站艺术方向 |
| `imagegen-mobile` | 03-design | 移动端屏幕/流程图 | iOS/Android 屏幕图 + 流程，带手机 mockup 框 |

## 不产 md 的 skill（产物是代码/行为）

`implement` · `tdd` · `test-generation` · `api-testing` · `e2e-testing` · `debugging` ·
`simplify` · `shipping` · `git-workflow` · `ci-cd` · `deprecation-migration` ·
`observability` · `context-engineering` · `using-skills` · `image-to-code` · `i18n`

这些 skill 的产物是代码、测试、提交、配置或行为变更，不强行加 md 产物。
