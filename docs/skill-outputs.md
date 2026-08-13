# Skill 产物矩阵

> 每个产出 markdown 文档的 skill 的固定产物路径。产物路径在各 skill 的 SKILL.md 里声明
>（`**Output:**` 标记或 Steps 散文）；本表是速查视图。
>
> 排序与 [workflow-prompts.md](workflow-prompts.md) 一致——按生命周期阶段 0→9，每阶段内
> **前置参考在前、最重要产物最后**（产物越重要顺序越往后）。
>
> 命名规则：**全大写** = 项目级正式文档（docs/ 根，单文件）；**全大写目录** = 多文件集合
>（docs/ 根）；**阶段目录** = 中间产物按阶段归类（`docs/research/`、`docs/design/`、
> `docs/audit/`、`docs/postmortem/`），目录内全大写=该阶段主文档、小写=中间产物。

## 文档型 skill（产 md）

| 阶段 | skill | 产物 | 路径 | 命名 | 作用 |
|---|---|---|---|---|---|
| **0 产品调研** | `brainstorm` | 用户访谈记录 | `docs/research/interview.md` | 阶段目录 | discovery 访谈发现（PRD 输入）；可由 workflow-prompts 用户访谈提示词独立产出 |
| | `research` | 调研档案 | `docs/research/YYYY-MM-DD-<slug>.md` | 阶段目录 | 带引用的深度调研，累积存档 |
| | `market-research` | 市场调研 | `docs/research/market.md` | 阶段目录 | 用户原话/竞品/行业情报（PRD 输入） |
| | `tech-selection` | 技术对比 | `docs/research/competitor.md` | 阶段目录 | 技术选型对比矩阵 + 推荐（PRD 输入） |
| | `oss-strategy` | 商业策略 | `docs/research/strategy.md` | 阶段目录 | 商业模式/定价/GTM（PRD 输入） |
| | `brainstorm` | **产品路线图** | `ROADMAP.md` | 大写 | 产品定位/多版本/验收项（本阶段最重要产物） |
| **1 需求与设计** | `frontend-design` | 用户研究 | `docs/research/ux-research.md` | 阶段目录 | persona/journey/可用性测试（DESIGN 输入） |
| | `prototype` | 原型验证结论 | `docs/design/prototype-findings.md` | 阶段目录 | 测试问题/结论/验证决策 |
| | `codebase-design` | 代码库审计 | `docs/design/codebase-audit.md` | 阶段目录 | 深化机会/选定候选/grill 结论 |
| | `domain-modeling` | 统一语言 | `CONTEXT.md` | 大写 | 项目术语表（根目录） |
| | `domain-modeling` | 决策记录 | `docs/design/adr/NNNN-slug.md` | 阶段目录 | 领域建模产生的 ADR（共享 design/adr/） |
| | `prompt-engineering` | 提示词设计文档 | `docs/design/PROMPT.md` | 阶段目录 | prompt 架构 + 模型选型 + eval + guardrails |
| | `schema-design` | 数据模型文档 | `docs/design/SCHEMA.md` | 阶段目录 | ER 图 + 实体/索引/约束/分区规划 |
| | `api-design` | API 契约 | `docs/API/*.md` | 大写目录 | 每端点组一份，请求/响应/错误/示例 |
| | `frontend-design` | UIUX 设计报告 | `docs/design/DESIGN.md` | 阶段目录 | 从零设计：设计系统/信息架构/交互/组件规划 |
| | `frontend-design` | 前端审计 | `docs/design/frontend-audit.md` | 阶段目录 | 审计现有前端的优化建议 |
| | `architecture` | 决策记录 | `docs/design/adr/NNNN-slug.md` | 阶段目录 | 每项重大架构决策的 ADR（跨版本共享） |
| | `spec` | **需求文档** | `docs/PRD.md`（项目级，简洁，main）+ `docs/vX.Y/prd.md`（版本级，详细，版本分支） | 大写+小写 | 项目级 shared source of truth；版本级详细 PRD |
| | `architecture` | **架构总览** | `docs/TECH.md`（项目级，简洁，main）+ `docs/vX.Y/tech.md`（版本级，详细，版本分支） | 大写+小写 | 系统架构图、组件、NFR、数据层（由 PRD 驱动） |
| **2 实现计划** | `documentation-audit` | 审计报告 | `docs/audit/YYYY-MM-DD-documentation.md` | 阶段目录 | 同步五类正式文档到代码 + 产审计报告 |
| | `breakdown` | **实现计划** | `docs/PLAN.md`（项目级，简洁，main）+ `docs/vX.Y/plan.md`（版本级，详细，版本分支） | 大写+小写 | ticket 拆解作章节，blocking edges（本阶段最重要产物） |
| **4 优化重构** | `performance` | 性能台账 | `PERF.md`（可选） | 大写 | 尝试记录（kept + reverted），防重复踩坑 |
| **5 测试** | `load-testing` | 容量报告 | `docs/CAPACITY.md`（可选） | 大写 | 容量上限/瓶颈/自动伸缩验证/行动项 |
| **6 审查调试** | `security-review` | 安全报告 | `docs/security-report.md` | 小写 | 按严重度的安全发现 + 修复/接受理由 |
| | `code-review` | **待办清单** | `docs/TODO.md` | 大写 | 代码↔TODO 双向校验的项目级待办（本阶段最重要产物） |
| **8 运行维护** | `documentation-audit` | 审计报告 | `docs/audit/YYYY-MM-DD-documentation.md` | 阶段目录 | 同步五类正式文档到代码 + 产审计报告 |
| | `incident-response` | **复盘报告** | `docs/postmortem/YYYY-MM-DD-<slug>.md` | 阶段目录 | 无指责复盘：时间线/影响/根因/行动项 |
| | `handoff` | 交接简报 | OS 临时目录 | — | 给下一会话的 context/决策/下一步 |
| **9 开源上线** | `oss-polish` | **README** | `README.md` | 大写 | 开源展示面（本阶段最重要产物） |
| | `oss-polish` | 仓库摘要 | `REPOSITORY_SUMMARY.md` | 大写 | 架构/组件/技术/数据流 |
| | `oss-polish` | 叙事史 | `THE_STORY_OF_THIS_REPO.md` | 大写 | commit 历史叙事 |

## 正式文档（docs/ 只保留这 5 类）

| 文档 | 产出 skill | 风格 |
|---|---|---|
| `docs/PRD.md`（+ `docs/vX.Y/prd.md`） | spec | 项目级简洁多 mermaid（main）；版本级详细（版本分支） |
| `docs/TECH.md`（+ `docs/vX.Y/tech.md`） | architecture | 项目级简洁多 mermaid（main）；版本级详细（版本分支） |
| `docs/API/*.md` | api-design | 详细请求/响应（跨版本共享） |
| `docs/FLOW/*.md` | 跨任务产物 | mermaid 流程 + 详细数据流描述（跨版本共享） |
| `docs/TODO.md` | code-review | 按业务合并（项目级） |

> **版本分层规则**：ROADMAP.md 是项目全局视图（简洁，多版本+验收项，main）。
> PRD/TECH/PLAN 分两层——大写项目级（`docs/PRD.md` 等，简洁多 mermaid，main 分支）+
> 小写版本级（`docs/vX.Y/prd.md` 等，详细，版本分支）。单版本项目自动回退 `docs/` 根，
> 不建版本目录。API/FLOW/TODO/research 跨版本共享，不重复。

## 跨任务产物（非 skill 直接产出，工作流约定）

| 阶段 | 产物 | 路径 | 产出方式 |
|---|---|---|---|
| 横切（任意阶段） | 业务流程文档 | `docs/FLOW/*.md` | 按 workflow-prompts 的 FLOW 提示词 |
| 横切（任意阶段） | 前端结构审计 | `docs/FRONT.md` | 按 workflow-prompts 的 FRONT 提示词 |
| 1 需求与设计 | 用户可见功能 | `FEATURES.md` | 按 workflow-prompts 的 FEATURES 提示词 |
| 2 实现计划 | AI 上下文指令 | `CLAUDE.md` | `/init` 或 workflow-prompts 的 CLAUDE.md 生成提示词 |
| 2 实现计划 | 忽略规则 | `.gitignore` | 按 workflow-prompts 的 .gitignore 提示词 |

## 图片型 skill（产图片，不写代码）

| 阶段 | skill | 产物 | 作用 |
|---|---|---|---|
| 1 需求与设计 | `brandkit` | 品牌识别图 | logo 概念/身份板/配色/字体/mockup |
| 1 需求与设计 | `imagegen-web` | 网站设计参考图 | 每 section 一张横向图，落地页/营销站艺术方向 |
| 1 需求与设计 | `imagegen-mobile` | 移动端屏幕/流程图 | iOS/Android 屏幕图 + 流程，带手机 mockup 框 |

## 不产 md 的 skill（产物是代码/行为）

| 阶段 | skill | 产物 |
|---|---|---|
| 3 写代码 | `implement` · `tdd` · `context-engineering` · `i18n` | 源码 / test/ |
| 3 写代码 | `image-to-code` | 前端代码 |
| 4 优化重构 | `simplify` | 重构后代码 |
| 5 测试 | `test-generation` · `api-testing` · `e2e-testing` | 测试代码 |
| 6 审查调试 | `debugging` | 修复 + 回归测试 |
| 7 上线发布 | `shipping` · `git-workflow` · `ci-cd` · `deprecation-migration` | 提交 / 流水线 / 部署 |
| 8 运行维护 | `observability` | 插桩代码 |
| meta | `using-skills` | 路由（无产物） |

这些 skill 的产物是代码、测试、提交、配置或行为变更，不强行加 md 产物。
