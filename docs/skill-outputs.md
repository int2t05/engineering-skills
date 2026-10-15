# 产物选择

路径是建议，生成、移动或重命名前须人工确认；用户已给出路径或确认的产物表可直接执行，不重复询问。
按决策、契约、运行操作或可复用知识选择产物，不要求每个项目具备同一套文档。

## 选择规则

| 情况 | 建议 |
|---|---|
| 小改动、简单解释、普通测试结果 | 聊天说明目标与验证，通常不新增文档 |
| 需求或重大方案需要人工审计 | 更新其权威 PRD/TECH；风险决定审计项数量 |
| 任务需要跨会话协调 | 保留 PLAN；短任务用内联计划 |
| API 或数据契约已有机器定义 | 维护权威源，避免另写相同内容 |
| 独立发布范围需长期维护 | 再考虑版本目录，不默认复制三份文档 |
| 调研、审计、设计、事故记录 | 根据证据和后续消费者保留，不因上线机械删除 |
| 仓库展示 | README 承担入口；不默认生成摘要、故事或 Wiki |

## 技能声明

以下为速查视图，与各 SKILL.md 的 `**Output:**` 对应。人类接受与技术检查遵循 [human-audit](../references/human-audit.md)。

| 技能 | 建议产物与条件 |
|---|---|
| `brainstorm` | `ROADMAP.md`; `docs/research/interview.md` only for actual interviews. |
| `oss-strategy` | `docs/research/strategy.md` when durable strategy is requested. |
| `spec` | `docs/PRD.md`; optionally `docs/vX.Y/prd.md` for separately maintained release scope. |
| `research` | `docs/research/YYYY-MM-DD-<slug>.md`, `docs/research/market.md` or `docs/research/competitor.md`; prefer its existing owner. |
| `api-design` | `docs/API/*.md` or the authoritative machine-readable contract. |
| `architecture` | `docs/TECH.md`; optionally `docs/vX.Y/tech.md` and `docs/design/adr/NNNN-slug.md`. |
| `codebase-design` | `docs/design/codebase-audit.md` when a durable decision is needed. |
| `design-research` | `docs/design/references.md` when a durable board is needed. |
| `domain-modeling` | `CONTEXT.md`; optionally `docs/design/adr/NNNN-slug.md`. |
| `frontend-design` | `docs/design/DESIGN.md`, `docs/design/frontend-audit.md` or `docs/research/ux-research.md` only for corresponding requested work. |
| `prompt-engineering` | `docs/design/PROMPT.md` for a maintained workflow. |
| `prototype` | `docs/design/prototype-findings.md` when conclusions need persistence. |
| `schema-design` | `docs/design/SCHEMA.md` if useful beyond schema source. |
| `breakdown` | `docs/PLAN.md`; optionally `docs/vX.Y/plan.md` for separate release planning. |
| `cost-optimization` | `COST.md` only for a useful continuing ledger. |
| `load-testing` | `docs/CAPACITY.md` for durable capacity decisions. |
| `a11y-review` | `docs/a11y-report.md` when durable findings are requested. |
| `code-review` | `docs/TODO.md` only for agreed durable tracking; otherwise conversation. |
| `security-review` | `docs/security-report.md` when durable findings are requested. |
| `oss-polish` | `README.md`; extra contribution or website artifacts need agreed purpose and paths. |
| `shipping` | `docs/launch/rollback-plan.md` when a separate recovery document is useful. |
| `documentation-audit` | `docs/audit/YYYY-MM-DD-documentation.md` at the approved path alongside corrected docs. |
| `incident-response` | `docs/postmortem/YYYY-MM-DD-<slug>.md` at the approved path. |
| `purity-audit` | `docs/audit/YYYY-MM-DD-purity.md` at the approved path. |

## 其他按需产物

- `docs/FLOW/*.md`：复杂业务调用链或数据流需要长期维护时。
- `docs/FRONT.md`：前端结构需要独立说明时；否则合并到 TECH。
- `FEATURES.md`：确有独立功能目录消费者时；否则由 PRD 管理。
- `AGENTS.md`、`CLAUDE.md`：实际项目上下文入口，不复制通用纪律。
- 原型、图片、代码、测试、配置是其任务本身的产物，不为它们自动附加报告。

具体任务和文档写作偏好见 [提示词手册](workflow-prompts.md)。
