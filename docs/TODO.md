# 项目待办 — 技能包改进

> **来源：** 2026-08-14 对 workbuddy 三 marketplace 的 191 个 SDLCx skill 做全量调研，以 7 维度
> （覆盖缺口 / 解剖结构 / 元层路由 / 验证安全 / 编排 / 内容器件 / 技能创作法）交叉比对当前 45-skill 包。
> 本文件是过滤后的可执行清单；原始收割物与子 agent 报告为本地研究材料，未发布。
>
> **原则：** 本包主动"去胖"（v2.0.0 合并技能、多次 purity audit、CLAUDE.md 明令不得臆测增项）。
> 调研约 60% 印证当前设计正确，约 25% 该跳过，仅约 15% 真正值得改。下列按执行顺序排。
>
> **与 code-review 契约的关系：** `docs/TODO.md` 是项目级待办（见 `docs/skill-outputs.md`）。
> code-review 在 pre-merge 时把代码发现写入此处并做代码↔TODO 双向校验；本改进清单是同源不同来源的
> 项目级待办，两者共存。code-review 写入时按业务区合并，不覆盖本清单的改进条目。

## 执行顺序总览

1. **Tier A 加固** — 一个 PR，纯 `validate-skills.sh` + `using-skills` 改动，零新 skill，零 discovery-surface 同步
2. **⚠️ description 捷径陷阱抽测** — 决定是否精修 hybrid 格式（先于 Tier C）
3. **Tier B 扩展现有 skill** — 按需逐个 ref 文件
4. **Tier C 新增 skill** — 3 个，各独立 PR，走全流程
5. **Tier D 解剖学指引** — 写入 `references/skill-anatomy.md`

---

## Tier A — 立即采纳（高价值 / 低成本 / 契合哲学）

### A1 验证器：安全内容扫描

当前 `scripts/validate-skills.sh` 约 22 项检查，**全部结构/元数据，零安全扫描**。包经 marketplace 安装，
一旦引入第三方贡献 skill，藏在 `scripts/install.sh` 里的恶意载荷会绕过所有现有检查。收割的 `skill-vetter` /
`skills-security-check` 给出完整 grep 检查目录。

- [ ] 把扫描循环从 `SKILL.md` 扩到 `find "$skill_dir" -type f`（覆盖 scripts/、references/、**所有**伴生文件）—— 一行架构改动解锁下面全部
- [ ] prompt-injection 短语模板（`⚠️ CRITICAL REQUIREMENT`、`必须先执行`、`THE SKILL WILL NOT WORK`）
- [ ] 混淆执行：`base64 -d | bash`、`curl | bash`、`wget | sh`
- [ ] 裸 IP URL（`http://123.45.67.89`）
- [ ] 云凭证路径（`~/.ssh`、`~/.aws`、`~/.kube`、`~/.gnupg`、`~/.netrc`）
- [ ] 持久化/后门（`.bashrc`、`.zshrc`、`crontab`、`authorized_keys`、`systemctl`、`launchctl`）
- [ ] 反向 shell（`nc -e`、`/dev/tcp/`、`mkfifo`、`socat`）
- [ ] 数据外送（`curl -d`、`wget --post-data`）
- [ ] 全局包安装（`pip install`、`npm i -g`、`brew install` 等）+ 非官方源（`--index-url`、`--registry`、`git+https`）
- [ ] 破坏性操作（`rm -rf`、`shutil.rmtree`）带**项目本地 vs 系统级路径区分**：`rm -rf ./dist` 放行，`rm -rf /` 或 `~/*` 失败
- [ ] 隐蔽标志（`--quiet`、`--silent`、`2>/dev/null`、`nohup`）
- [ ] 硬编码凭证前缀（`sk-`、`ghp_`、`AKIA`、`-----BEGIN.*PRIVATE KEY-----`）
- [ ] 可疑域名（`pastebin`、`ngrok`、`bit.ly`、`tinyurl`）

**Cost:** 低（纯 bash grep） · **Value:** 高 · **Verify:** 构造含上述模式的样本 skill 文件，CI 拦截且 `Total errors: 0` 在干净 skill 上仍成立。

### A2 验证器：结构漂移检查

收割的 `quick_validate.py` 做了几件当前验证器没做的：

- [ ] `name:` == 目录名（防 frontmatter/目录名漂移）
- [ ] description ≤ 1024 字符强制（anatomy 说了，验证器没查）
- [ ] kebab-case 目录名强制（regex `/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/`）

**Cost:** 低（awk/grep） · **Value:** 中高 · **Verify:** 构造 `name:` 与目录名不符 / 超 1024 字符的样本，被 CI 拦截。

### A3 路由器："无技能命中"降级链

`skills/meta/using-skills/SKILL.md` 的失败处理只有一句"re-route — don't force-fit"，无具体降级。
收割的 `find-skills` 给出三步。

- [ ] 加入三步降级：承认缺口 → 用通用能力直接帮 → 建议用 `skill-authoring` 创建（包内自然降级，不引入外部发现）

**Cost:** 低（几行） · **Value:** 高 · **Verify:** using-skills SKILL.md 更新 + `validate-skills.sh` 绿。

### A4 路由器：反合理化红旗表

当前路由器主动邀请跳过："Not for: tasks where the right skill is already obvious"。收割的 `using-superpowers`
给出 12 行借口→现实对照表。

- [ ] 在 using-skills 加精简红旗表（"This is just a simple question" → "Questions are tasks. Check for skills." 等约 6 条）
- [ ] 收紧"Not for"措辞，避免鼓励跳过路由

**Cost:** 低 · **Value:** 中高 · **Verify:** using-skills 更新 + validator 绿。契合 engineering-principles §1-3（浮现假设/管理困惑/反弹）。

### A5 落实评估闭环（系统性最强）

`skills/meta/skill-authoring/SKILL.md` 定义三级评估，明言 behavioral eval 是"the real test; do it before
trusting the skill"——但磁盘上零评估用例（deferred to "实战"）。收割给了具体方法论。

- [ ] 为刚性纪律 skill 物化评估，优先 4 个：`tdd`、`debugging`、`code-review`、`implement`
- [ ] 每个物化 2-3 个压力测试场景文件（`test-pressure-N.md`，组合 3+ 压力类型：时间/沉没成本/权威/经济/疲劳/社交/务实，强制 A/B/C 选择）
- [ ] 跑 TDD-for-skills：RED（无 skill 跑基线）→ GREEN（有 skill 看合规）→ REFACTOR（堵漏洞）
- [ ] 评估断言要"判别性"——弱断言上的及格比无用更糟（制造虚假信心）；查内容不只查文件名存在

**Cost:** 中（跑 behavioral eval 花 token） · **Value:** 高（兑现包自己定的标准） · **Verify:** 4 个 skill 各有 ≥2 场景文件，跑通且行为合规。

---

## ⚠️ 调查项 — description "捷径陷阱"（先于 Tier C）

收割的 `writing-skills` 给出**有证据的警告**：description 里若含"what it does"概述，Claude 会按 description
走捷径，不读 skill 正文。实测案例：description 写"code review between tasks"→ Claude 只做 1 次审查，而 skill
流程图要求 2 次。

当前 hybrid 格式恰恰包含 `[One sentence: what it does]`（`references/skill-anatomy.md` 描述写作节）。

- [ ] 对多模式 skill（`code-review`/`implement`/`debugging`/`tdd`）做行为抽测：看 description 是否在诱发捷径
- [ ] 若是：把"what it does"句移入 `## When to use` 正文，description 只留触发条件 + 排除项
- [ ] 若否（当前表现良好）：记录抽测结论，不改

**Cost:** 中（抽测） · **Verify:** 抽测记录归档 `docs/audit/`；若改，hybrid 格式定义同步更新且 validator 绿。

---

## Tier B — 扩展现有 skill（外科手术式覆盖，不增 skill 数）

对每个"缺口"先问能否加 `references/x.md` 到现有 skill，而非新建。下列均不触发 discovery-surface 同步。

| 缺口 | 扩展目标 | 加什么 | Cost | Verify |
|---|---|---|---|---|
| SQL/EXPLAIN 优化 | `performance` + `references/sql-optimization.md` | EXPLAIN 读法、索引策略、N+1、游标分页、物化视图、分区 | 低 | ref 存在 + validator 死链检查绿 |
| 设计系统审计 | `frontend-design` + `references/design-system-audit.md` | token 覆盖/硬编码值审计、组件变体/状态/a11y 文档化、系统性扩展 | 低 | 同上（已有 16 ref，加 1 自然） |
| OpenAPI spec 生命周期 | `api-design` + `references/openapi-lifecycle.md` | design-first vs code-first、Spectral/Redocly lint、openapi-generator SDK gen | 低 | 同上 |
| Changelog / 发布说明 | `shipping` 或 `documentation-audit` + ref | commit 史→分类（feature/fix/breaking/security）→用户语言发布说明 | 低 | 同上 |
| SLO 实现深度 | `observability` + 更深 ref | Prometheus recording/alerting 规则、燃尽告警、复盘节奏 | 低 | 同上（已引 `slo-methodology.md`） |
| On-call 班次交接 | `handoff` + `references/on-call-shift.md` 模式 | 活跃事件/进行中调查/最近变更/已知问题/升级触发 + 班前中后清单 | 低 | 同上（与现有 dev-work handoff 模式区分） |

- [ ] 逐个按需实现（每条独立 commit，便于回滚）

---

## Tier C — 新增 skill（仅 3 个，有充分理由）

门槛：无现有 skill 拥有该域 + 高价值 + 可泛化。clear 了这关的只有 3 个。每个走全流程：
anatomy + validator + 5 处 discovery-surface 同步（plugin.json/AGENTS/phase-tree/using-skills/README×2）+ version bump。

| 新 skill | 阶段 | 理由 | Cost |
|---|---|---|---|
| `auth-implementation` | 04-develop | 无 skill 指导**正确实现**认证；`security-review` 只审查漏洞。认证是工程师引入安全洞的 #1 位置，几乎每个应用都需要。模式（JWT/session/OAuth2、RBAC、refresh-token 轮换、密码哈希）语言无关 | 中 |
| `error-handling` | 04-develop | 横切关注点（熔断/重试/Result type/优雅降级）无主人；`debugging` 诊断 bug，不设计错误传播策略。多语言、框架中立 | 中 |
| `accessibility-review` | 07-verify | 07-verify 有 code-review/debugging/security-review/linting 但无 a11y。法律要求、常被跳过、WCAG 标准框架中立、干净缺口 | 低-中 | **已发布为 `a11y-review`（v2.6.0）** |

- [ ] `auth-implementation` — 先写 spec/触发词，跑 collision 检查，再写 4 段 + ref
- [ ] `error-handling` — 同上
- [x] `accessibility-review` — 已发布为 `a11y-review`（v2.6.0）
- [ ] 每个：`gen-agents-yaml.py` + `validate-skills.sh` 绿 + 5 处 surface 同步 + version bump + CHANGELOG

**边界情况 — RAG/LLM-app：** 倾向**扩展** `prompt-engineering` 加 `references/rag-architecture.md`（向量库/embedding/分块/rerank/eval），而非新建——收割版 LangChain 锁定严重，新建成本高且偏离纯 markdown。

---

## Tier D — 解剖学指引（写入 `references/skill-anatomy.md`）

框架中立的内容器件，作为**指引**纳入 anatomy，非强制：

- [ ] **压力测试场景文件** — 伴生 `test-pressure-N.md`，逼模型在真实压力下违反规则（配合 A5）
- [ ] **合理化借口→现实表** — 出现在 3+ 收割 skill，任何纪律 skill 受益
- [ ] **参考文件只深一级** — 不嵌套（Claude 会 `head -100` 部分读，嵌套致信息缺失）；当前包已基本遵守，显式化
- [ ] **"按需加载"参考表** — SKILL.md 内置 `文件→何时加载` 表，利多 ref skill（如 frontend-design 16 个）
- [ ] **CREATION-LOG.md**（可选）— 记录提取决策/来源/结构理由，利维护

**明确不采纳：** scripts/templates/data/CSV 伴生结构——违反纯 markdown 可移植性（`AGENTS.md` 明言"skill content is plain markdown"）。

---

## Tier E — 明确不做（及理由）

记录以防未来重复建议：

| 不做 | 理由 |
|---|---|
| 加权评分路由 + 结构化 metadata（keywords/tags/category 入 frontmatter） | 对 45 skill 过度工程；加 frontmatter 字段（validator 明令禁止）；违反纯 markdown；phase-tree 在此规模足够 |
| scripts/templates/data 伴生文件 | 破坏跨 agent 可移植性 |
| MCP builder / MCP integration skill | 包是 skill 包非 plugin-dev 包；README 明言 out of scope |
| CloudBase/Godot/Tencent/Next.js/LangChain/FastAPI 等 vendor 技能 | 不可泛化 |
| monorepo / Helm / K8s 打包 / secrets 基础设施 | 工具/vendor 特定；implement/breakdown/ci-cd/security-review 已在正确高度覆盖概念 |
| UX copy / roadmap / test-case design | PM/QA 侧，与现有 skill 部分重叠，边际价值低 |
| 第三人称改写 45 个 description | 风格偏好非缺陷；当前第二人称祈使一致且有效；churn 巨大不值 |
| 行数预算放宽到 500 行 | 当前 15-150 行**更严**，契合反臃肿哲学，保持 |

---

## 完成判定

- Tier A 全绿：验证器含安全扫描 + 漂移检查；路由器含降级链 + 红旗表；4 个纪律 skill 有物化评估
- ⚠️ 抽测有归档结论（改或不改均有记录）
- Tier B/C/D 按 PR 推进，每个独立可回滚，validator 始终绿
- Tier E 的"不做"清单在本文件留存，未来再提同类建议时直接引用
