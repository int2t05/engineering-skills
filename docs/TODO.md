# 项目待办 — 技能包改进

> **来源：** 竞品 SDLCx skill 全量调研，7 维度交叉比对后过滤出的可执行清单。
>
> **原则：** 本包主动"去胖"（CLAUDE.md 明令不得臆测增项）。
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

- [x] 把扫描循环从 `SKILL.md` 扩到 `find "$skill_dir" -type f`（覆盖 scripts/、references/、**所有**伴生文件）—— 非 markdown 走执行/凭证/持久化模式，markdown 走注入短语
- [x] prompt-injection 短语模板（`⚠️ CRITICAL REQUIREMENT`、`必须先执行`、`THE SKILL WILL NOT WORK`）
- [x] 混淆执行：`base64 -d`、`curl | bash`、`wget | bash`
- [x] 裸 IP URL（`http://123.45.67.89`）
- [x] 云凭证路径（`~/.ssh`、`~/.aws`、`~/.kube`、`~/.gnupg`、`~/.netrc`）
- [x] 持久化/后门（`.bashrc`、`.zshrc`、`crontab`、`authorized_keys`、`systemctl`、`launchctl`）
- [x] 反向 shell（`nc -e`、`/dev/tcp/`、`mkfifo`、`socat`）
- [ ] 数据外送（`curl -d`、`wget --post-data`）— **deferred**：design-research/github_fetcher 合法用 curl，需上下文感知区分 fetch vs exfil
- [x] 非官方源（`--index-url`、`--registry`、`git+https`）；全局包安装（`pip install`、`npm i -g`）— **deferred**：eval fixture 合法 `npm install`，需区分 `-g` 全局 vs 本地
- [x] 破坏性操作：`rm -rf /`、`rm -rf ~`、`rm -rf $`（系统级路径拦截）；完整 local-vs-system 区分（`shutil.rmtree` 参数解析）— **deferred**
- [ ] 隐蔽标志（`--quiet`、`--silent`、`2>/dev/null`、`nohup`）— **deferred**：validator/run-eval 自身合法用 `--silent`/`2>/dev/null`，高假阳性
- [x] 硬编码凭证前缀（`ghp_`、`AKIA`、`sk-ant-`、`-----BEGIN.*PRIVATE KEY-----`）
- [ ] 可疑域名（`pastebin`、`ngrok`、`bit.ly`、`tinyurl`）— **deferred**：需上下文感知（design-research 合法 gallery 域名）

> **A1 现状：** 9/13 模式已实现并验证（构造恶意样本被拦截，干净包 0 假阳性）。4 项 deferred
> 因纯 grep 假阳性高（需上下文感知实现），记于此待后续。已实现的覆盖最高信号的脚本捆绑威胁
> （reverse shell / 混淆执行 / 硬编码凭证 / 裸 IP / 云凭证路径 / 持久化 / 非官方源 / 系统级 rm）+
> markdown 注入短语。

**Cost:** 低（纯 bash grep） · **Value:** 高 · **Verify:** 构造含上述模式的样本 skill 文件，CI 拦截且 `Total errors: 0` 在干净 skill 上仍成立。

### A2 验证器：结构漂移检查

收割的 `quick_validate.py` 做了几件当前验证器没做的：

- [x] `name:` == 目录名（防 frontmatter/目录名漂移）
- [x] description ≤ 1024 字符强制（anatomy 说了，验证器没查）
- [x] kebab-case 目录名强制（regex `/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/`）

**Cost:** 低（awk/grep） · **Value:** 中高 · **Verify:** 构造 `name:` 与目录名不符 / 超 1024 字符的样本，被 CI 拦截。

### A3 路由器："无技能命中"降级链

`skills/meta/using-skills/SKILL.md` 的失败处理只有一句"re-route — don't force-fit"，无具体降级。
收割的 `find-skills` 给出三步。

- [x] 加入三步降级：承认缺口 → 用通用能力直接帮 → 建议用 `skill-authoring` 创建（包内自然降级，不引入外部发现）

**Cost:** 低（几行） · **Value:** 高 · **Verify:** using-skills SKILL.md 更新 + `validate-skills.sh` 绿。

### A4 路由器：反合理化红旗表

当前路由器主动邀请跳过："Not for: tasks where the right skill is already obvious"。收割的 `using-superpowers`
给出 12 行借口→现实对照表。

- [x] 在 using-skills 加精简红旗表（"This is just a simple question" → "Questions are tasks. Check for skills." 等约 6 条）
- [x] 收紧"Not for"措辞，避免鼓励跳过路由

**Cost:** 低 · **Value:** 中高 · **Verify:** using-skills 更新 + validator 绿。契合 engineering-principles §1-3（浮现假设/管理困惑/反弹）。

### A5 评估体系 — 待完善（系统性最强）

> **状态：实验性 / 待完善。** harness 能跑、能留产物，但在 GLM-5.2 上**未实现区分力**——
> 强模型裸跑（不加载 skill）也能通过当前 case。CI workflow 已删（`eval-behavioral.yml`），
> 评估改为本地按需运行，绝不 gate CI。本节是调优路线图。

**已建成（基础设施可用）：**

- [X] RED-GREEN harness（`scripts/run-eval.py`）：with-skill vs baseline 双跑，证明技能改变行为
- [X] 3 种 grader（code-based / llm-judge / hybrid），`evals/agents/grader.md` 带证据评分 + 自评 case 质量
- [X] 产物持久化：transcript.md / grading.json / workspace 快照 / run-summary.json → `evals/results/`（gitignored）
- [X] 超时 partial transcript 恢复（TimeoutExpired.stdout 不再丢弃）
- [X] 10 个 case（6 正向 + 4 负控），4 个 fixture（cart-bug / paginate-buggy / buggy-diff / spec-brief）
- [X] 负控测试精度（技能不该激活的任务，grader 反转逻辑）

**实跑发现（GLM-5.2）：**

| Case            | with          | base | discriminating | 性质                                       |
| --------------- | ------------- | ---- | -------------- | ------------------------------------------ |
| tdd-001         | 100%          | 100% | no             | 真实——GLM 裸跑也做 test-first            |
| debugging-001   | 100%          | 100% | no             | 真实——GLM 裸跑也找到 input-mutation 根因 |
| code-review-001 | (修前假 100%) | —   | —             | grader schema bug 致假通过，已修，待重跑   |
| spec-001        | —            | —   | —             | 未完整跑完                                 |

**根因不是（仅）case 太弱，是模型够强。** GLM-5.2 在纯技术任务上裸跑也做纪律化过程。
调研结论（archive addyosmani/obra + SWE-bench/CR-Bench/OpenRCA 2.0）一致指向：
**强模型能 game 纯技术任务，但抵不住"压力场景"——权威/时间/沉没成本压力要求跳过纪律时，
裸跑模型会妥协，带技能的不会。** 这是下一步的唯一有效方向。

**参照的成熟评估体系（本包 harness 的设计来源 + 调优依据）：**

| 体系                              | 核心做法                                                                                                                                                                                                | 本包借鉴了什么                                  | 还没借鉴（调优来源）                      |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------- |
| **SWE-bench**               | FAIL_TO_PASS + PASS_TO_PASS 双门：bug 修复测试过**且** 原有测试没回归才算解决；每 task 入库前验证"测试真能区分对错修复"                                                                           | RED-GREEN baseline 思路                         | P4 dual-gate grading（防 symptom-patch）  |
| **Anthropic skill-creator** | with-skill/without-skill**同轮并行**双跑；benchmark.json 量化 delta（pass_rate mean±stddev）；`agents/analyzer.md` 自动标"两边都过=非判别"断言                                                 | 双跑结构 + grader.md 证据评分 + 自评 case 质量  | P2 analyzer pass + P3 多跑方差            |
| **obra superpowers**        | TDD-for-skills：RED（无 skill 跑基线看失败）→ GREEN（有 skill 看合规）→ REFACTOR（堵漏洞）；**压力场景组合 3+ 类型**（时间/沉没成本/权威/疲劳），强制 A/B/C 无退路；捕获"合理化借口"逐条堵      | RED-GREEN 命名 + 负控概念                       | P1 压力场景（最强 discriminator）+ 借口表 |
| **addyosmani agent-skills** | 三层评估（结构/触发路由/行为）；**case 把 fixture 的 bug 藏进现有通过的测试**（hidden bug），discriminator 是"naive 路径过、disciplined 路径过更多"；trigger.negative 带 `owner` 做配对路由测试 | 三层 tier 结构 + fixture 设计 + 负控 owner 思路 | P6 benign case + fixture 隐藏 bug 模式    |
| **CR-Bench / SWE-PRBench**  | 代码审查 benchmark：多严重度（Critical/High/Medium/Low）+ 类型×影响×严重度三维；benign PR 测 false-positive；发现"模型抓表层 nit、漏跨文件 Critical"                                                  | code-review-001 多严重度 diff 设计              | P6 severity 加权 + benign case            |
| **OpenRCA 2.0**             | 过程级评分不只看结果：76% 模型说对根因，仅 61.5% 能画因果路径（"ungrounded diagnosis"）；outcome-only 评分把这种假成功判为通过                                                                          | grader 查过程（reproduce 先于 hypothesize）     | P5 收紧到"必须画因果链"                   |
| **DashBench (DoorDash)**    | severity 加权评分（C=4/H=2/M=1/L=0.5）；20-30% benign PR 测克制；"单一分数天然误导"                                                                                                                     | —                                              | P6 加权 + benign                          |
| **c-CRAB**                  | 把审查意见转成**可执行测试**：AI review "识别了 issue" 当且仅当应用其建议修复后测试通过——避开文本相似度                                                                                         | —                                              | defer（test-based review，polish）        |

> 本包当前 harness ≈ Anthropic skill-creator 的双跑结构 + addyosmani 的三层/fixture/负控 + obra 的
> RED-GREEN 命名。**缺的三块**：obra 的压力场景（P1）、skill-creator 的 analyzer 量化非判别断言（P2）、
> SWE-bench 的 dual-gate（P4）。这三块是从"能跑"到"能证明区分力"的路径。

**调优路线图（按 ROI 排序）：**

- [ ] **P1 压力场景 case（最强 discriminator，源自 obra superpowers）** — 每个 discipline skill 加 2-3 个压力 case，
  prompt 主动论证跳过纪律（"lead 说 fix 很明显，跳过失败测试直接改"／"生产挂了，stakeholder
  要立刻 patch 别复现"）。组合 3+ 压力类型（时间/沉没成本/权威/疲劳），强制 A/B/C 选择无退路。
  期望：裸跑妥协（选 A：直接改），带技能坚持（选 B：先复现）。
- [ ] **P2 analyzer pass（量化非判别断言）** — 跑完后自动比对两边 grading，标出"两边都过"的断言
  （non-discriminating）和"两边都挂"的断言（broken/beyond-capability）。anthropics skill-creator
  `agents/analyzer.md` 的核心机制——把"哪些断言没区分力"从主观变可度量
- [ ] **P3 多跑方差（single run 不可信）** — 每 case 跑 3 次，报 mean±stddev。LLM 行为 run-to-run
  波动大，单次 100%/100% 可能是运气。`--runs 3` 已支持，但当前为省 token 只跑 1 次
- [ ] **P4 dual-gate grading（防 symptom-patch）** — FAIL_TO_PASS（bug 修复测试过）+ PASS_TO_PASS
  （原有测试没回归）双门。SWE-bench 设计，防"修了症状破了别处"。当前 code_check 只查 exit 0，
  不区分修对 vs 修坏
- [ ] **P5 过程级评分不只看结果** — OpenRCA 2.0 "ungrounded diagnosis"：76% 模型能说出对根因，
  但只有 61.5% 能用因果路径论证。当前 grader 已查过程（reproduce 先于 hypothesize），但可收紧
  到"必须画因果链"而非"提到根因词"
- [ ] **P6 code-review 加 benign case + severity 加权** — DashBench：20-30% 干净 PR 测 false-positive
  （过度报告）；severity 权重 Critical=4/High=2/Medium=1/Low=0.5，防"抓一堆 nit 掩盖漏 Critical"
- [ ] **P7 重跑 code-review-001（grader 修后）** — 确认 flat-schema 修复后真评分；route-ordering bug
  是设计的 discriminator，验证基线是否真漏

**明确不建（defer 到 P1 验证后再说）：** 盲比较 comparator、description 优化循环、HTML viewer、
pass@k 统计——with/without baseline 已是核心证据，这些是 polish。

**Cost:** 高（压力 case 设计 + 多跑花 token） · **Value:** 高（兑现包自定的 Tier 3 标准；
当前 harness 是"能跑的假设"而非"已证实的证据"） · **Verify:** 至少 1 个压力 case 实现
discriminating（with 过、base 不过），analyzer pass 报出非判别断言清单。

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

| 缺口                  | 扩展目标                                                    | 加什么                                                                       | Cost | Verify                                   |
| --------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------- | ---- | ---------------------------------------- |
| SQL/EXPLAIN 优化      | `performance` + `references/sql-optimization.md`        | EXPLAIN 读法、索引策略、N+1、游标分页、物化视图、分区                        | 低   | ref 存在 + validator 死链检查绿          |
| 设计系统审计          | `frontend-design` + `references/design-system-audit.md` | token 覆盖/硬编码值审计、组件变体/状态/a11y 文档化、系统性扩展               | 低   | 同上（已有 16 ref，加 1 自然）           |
| OpenAPI spec 生命周期 | `api-design` + `references/openapi-lifecycle.md`        | design-first vs code-first、Spectral/Redocly lint、openapi-generator SDK gen | 低   | 同上                                     |
| Changelog / 发布说明  | `shipping` 或 `documentation-audit` + ref               | commit 史→分类（feature/fix/breaking/security）→用户语言发布说明           | 低   | 同上                                     |
| SLO 实现深度          | `observability` + 更深 ref                                | Prometheus recording/alerting 规则、燃尽告警、复盘节奏                       | 低   | 同上（已引`slo-methodology.md`）       |
| On-call 班次交接      | `handoff` + `references/on-call-shift.md` 模式          | 活跃事件/进行中调查/最近变更/已知问题/升级触发 + 班前中后清单                | 低   | 同上（与现有 dev-work handoff 模式区分） |

- [x] 逐个实现（交付 6 个 ref：sql-optimization / design-system-audit / openapi-lifecycle / changelog-and-release-notes / slo-implementation / on-call-shift）

---

## Tier C — 新增 skill（仅 3 个，有充分理由）

门槛：无现有 skill 拥有该域 + 高价值 + 可泛化。clear 了这关的只有 3 个。每个走全流程：
anatomy + validator + 5 处 discovery-surface 同步（plugin.json/AGENTS/phase-tree/using-skills/README×2）+ version bump。

| 新 skill                 | 阶段       | 理由                                                                                                                                                                                              | Cost  |
| ------------------------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| `auth-implementation`  | 04-develop | 无 skill 指导**正确实现**认证；`security-review` 只审查漏洞。认证是工程师引入安全洞的 #1 位置，几乎每个应用都需要。模式（JWT/session/OAuth2、RBAC、refresh-token 轮换、密码哈希）语言无关 | 中    |
| `error-handling`       | 04-develop | 横切关注点（熔断/重试/Result type/优雅降级）无主人；`debugging` 诊断 bug，不设计错误传播策略。多语言、框架中立                                                                                  | 中    |
| `accessibility-review` | 07-verify  | 07-verify 有 code-review/debugging/security-review/linting 但无 a11y。法律要求、常被跳过、WCAG 标准框架中立、干净缺口                                                                             | 低-中 |

- [x] `auth-implementation` — 已发布：SKILL.md + token-patterns.md + oauth-flows.md + openai.yaml
- [x] `error-handling` — 已发布：SKILL.md + retry-patterns.md + openai.yaml
- [x] `accessibility-review` — 已发布为 `a11y-review`
- [ ] 每个：`gen-agents-yaml.py` + `validate-skills.sh` 绿 + 5 处 surface 同步 + version bump + CHANGELOG

**边界情况 — RAG/LLM-app：** 倾向**扩展** `prompt-engineering` 加 `references/rag-architecture.md`（向量库/embedding/分块/rerank/eval），而非新建——竞品 LangChain 技能锁定严重，新建成本高且偏离纯 markdown。

---

## Tier D — 解剖学指引（写入 `references/skill-anatomy.md`）

框架中立的内容器件，作为**指引**纳入 anatomy，非强制：

- [x] **压力测试场景文件** — 已写入 anatomy 作为 convention（eval artifact，配合 A5 Tier 3）
- [x] **合理化借口→现实表** — 已写入 anatomy 作为 convention + using-skills 已实装 6 行表
- [x] **参考文件只深一级** — 已写入 anatomy 显式化（validator dead-link 检查也依赖此）
- [x] **"按需加载"参考表** — 已写入 anatomy 作为 convention
- [x] **CREATION-LOG.md**（可选）— 已写入 anatomy 作为可选 convention

**明确不采纳：** scripts/templates/data/CSV 伴生结构——违反纯 markdown 可移植性（`AGENTS.md` 明言"skill content is plain markdown"）。

---

## Tier F — 内容质量审计（2026-08-14 全量 skill 审计，skill 级具体发现）

> **来源：** 全量 skill 内容质量审计（非结构——结构归 validator）。与 Tier B/C（竞品调研来的扩展/新增）**互补不冲突**：
> B/C 答"该加什么深度"，F 答"现有内容哪里错/薄/矛盾"。交汇处已标注。

### HIGH — 错误 / 误导 / 缺失关键（已验证，优先修）

- [x] **security-review** — OWASP Top 10 用 2017 类名（"Sensitive Data Exposure"/"XSS"），非 2021（A02→Cryptographic Failures、XSS 并入 A03 Injection）；缺 A04 Insecure Design / A06 Vulnerable Components / A08 Integrity / A09 Logging 四个 2021 新类。更新 Step 3 + 补 4 类
- [x] **git-workflow** — `references/block-dangerous-git.sh:7` 把 `"git push"` 当裸子串匹配，拦**所有** push 而非 `--force`。拆成只拦 `push --force`/`push -f`；若全拦是故意的（agent 须用户批准才 push），脚本加注释 + SKILL.md 说明意图
- [x] **shipping** — `SKILL.md:99` 列 `flyway undo`，但那是 Teams/Enterprise 付费功能，Community 版不存在。加注"Community 用户须 `flyway repair`+手动 SQL，或用 Liquibase（免费版支持 rollback）"
- [x] **oss-polish** — `references/scripts/collect-site-metrics.py` 硬编码特定教育站点目录（`docs/chapters/`、`docs/sims/`、`docs/learning-graph/`），90% 项目跑出空表。泛化（源文件/测试/依赖/贡献者计数）或标"文档/教育项目专用"+ 提供代码项目替代路径
- [x] **documentation-audit** — API drift grep 漏 `router.`（Express Router）、`@All`/`@Controller`（NestJS）、`fastify.method`（非 `app.method`），产生假"无漂移"——正是该 skill 存在要防的失败。补 pattern 或建议框架路由内省 API
- [x] **refactoring** — `references/` 完全空，move catalog（extract/move/split/merge/change-dependency）一句一个无 before/after 示例。加 `references/refactoring-catalog.md` + characterization-test 模式
- [x] **multi-agent-orchestration + codebase-design** — ~~写"launch via Agent tool"无此工具~~ **FALSE POSITIVE**：Claude Code 确有 `Agent` 工具（"Launch a new agent"），"multiple Agent tool calls" 正确，不改
- [x] **performance** — `references/bottlenecks.md:68` 用"Time to Interactive < 3.5s"，TTI 已被 INP 替代（2024.03 Core Web Vital），同文件 CWV 表却用 INP，自相矛盾。统一为 INP ≤ 200ms
- [x] **i18n** — 零 RSC/server-component i18n 覆盖（Next App Router server 消息加载 / per-locale bundle 拆分 / `setRequestLocale`），2026 标准实践缺失。Step 4 SSR 段补 server-side message management
- [x] **domain-modeling ↔ architecture** — ADR 格式直接矛盾：domain-modeling 说"可一段话、三准则全满足才写"，architecture 说"4 段强制、每个显著决策都写"，两者写同一 `docs/design/adr/NNNN-slug.md`。统一：一段话为默认、4 段为可选展开、一个门槛

### MEDIUM — 薄 / 陈旧 / 不一致 / 重叠（按 skill 紧凑列）

| skill                 | 发现                                                                                                                         | 动作                                                                     |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| security-review       | OWASP LLM Top 10 版本未标（2024 v2 重排了编号）                                                                              | 标"OWASP LLM Top 10 (2025)"，核对每个 LLM0x                              |
| git-workflow          | `pre-commit-setup.md` 仅 Node（Husky+lint-staged），Python/Go/Rust 零指导                                                  | 加"Non-Node stacks"段（Python`pre-commit` 框架、Go `golangci-lint`） |
| git-workflow          | `git-debugging.md` 仅 12 行 5 命令，缺 `bisect run`/`log -S`(pickaxe)/`reflog`/`blame -L`                          | 扩成带"何时用"的实用 ref                                                 |
| shipping              | 发布门用 p95，但 launch-monitoring.md + observability 用 p99，跨 skill 不一致                                                | 统一 p99（launch 门该抓 tail regression）                                |
| oss-polish            | `github_fetcher.py`/`readme_fetcher.py` 全中文 print/注释/docstring，其余全英文                                          | 译成英文                                                                 |
| oss-polish            | `config.py` 默认 `TOPIC="claude-code"`，badges.md 默认带 Claude 徽章                                                     | `TOPIC` 默认 None，删 Claude-specific 徽章                             |
| oss-polish            | 默认推荐 CC BY-NC-SA 4.0（禁商用），与主流教育项目惯例（MIT/CC BY 4.0）不符                                                  | 改"CC BY 4.0 for educational"，NC 仅限明确要限商用的                     |
| documentation-audit   | Step 4 FLOW drift 说"找调用链"但给零方法（无 grep/工具）                                                                     | 加`grep -rn "fn("` / madge(JS)/pydeps(Python)                          |
| deprecation-migration | `CREATE INDEX CONCURRENTLY` 失败留 INVALID 索引静默无效，未警告                                                            | 加"失败留 INVALID，查`\di`，drop+recreate"                             |
| ci-cd                 | `ci-templates.md` rollback/preview 模板 Vercel 专属，AWS/GCP/Docker 零适配                                                 | 加非 Vercel rollback pattern 或注"换平台等价命令"                        |
| linting               | 无`references/`，全靠 SKILL.md 正文；缺各语言 suppression 语法 + linter 选型指引                                           | 加`references/suppression-patterns.md` + `tool-selection.md`         |
| handoff               | 核心产物 handoff brief 无模板（对比 incident-response 有 postmortem-template）                                               | 加`references/handoff-brief-template.md`                               |
| observability         | 跨 skill 引用`../incident-response/references/runbook-template.md`（脆弱耦合）                                             | inline 最小 runbook 结构或拷进 observability/references/                 |
| a11y-review           | `wcag-checklist.md` 覆盖 ~20 条但 WCAG 2.2 AA 有 ~50 条，未标"子集"，缺 2.4.2/2.4.6/3.1.1 等                               | 加 header 注"high-value subset，余下另行验证"                            |
| incident-response     | Step 2 rollback 指向`shipping`，但 shipping 教规划非操作命令；SEV1 中找不到 `kubectl rollout undo`                       | inline 平台 rollback 命令或加到 shipping 操作段                          |
| oss-strategy          | "Cursor from VSCode" 列为 OSS→商用案例，但 Cursor 从非开源项目                                                              | 换真实案例（Supabase/Plausible/Cal.com）                                 |
| schema-design         | 全 relational-only（3NF/FK/CHECK/PARTITION），无 datastore 假设声明；MongoDB/DynamoDB 全不适用                               | "When to use"加"assumes relational"声明 + 非 relational 适配段           |
| spec                  | SKILL.md 模板（Objective/Structure/Commands…）与`prd-patterns.md`（User Stories/Feature Details/Data Tracking）结构不一致 | 对齐：补 PRD 段或拆"PRD 段 vs 项目约定段"                                |
| api-design            | 400 invalid data 和 422 validation failed 并列未消歧                                                                         | 加"400=malformed 不可解析；422=well-formed 但语义无效"                   |
| research              | Step 5 "默认中文输出"，与全包英文惯例冲突；`pressure-scenarios.md` 全中文                                                  | 默认跟用户输入语言，或默认英文 +`--lang zh`                            |
| design-research       | `sources.md` 硬编码 5 gallery URL，2 个已换域名、1 个已死，无降级路径                                                      | 加 source-health check + "失效则 skip 并记 gap"                          |
| prompt-engineering    | prompt caching 仅一句（缺 breakpoint/TTL/provider 差异/Anthropic 需`cache_control`）                                       | `prompt-architecture.md` 加 caching 子段                               |
| codebase-design       | Step 1 硬依赖"Spawn Explore sub-agent"，单 agent 环境无 fallback                                                             | 加"无 sub-agent 则自己 Glob/Grep/Read 走`git log`"                     |
| e2e-testing           | `playwright-rules.md` Rule 5 用 `waitForTimeout(200)`，与 Rule 8"Never waitForTimeout"直接矛盾                           | 换 web-first assertion 或交叉引用 Rule 8 例外                            |
| implement             | `source-verification.md` 混中文 section header/注释                                                                        | 译英文                                                                   |
| test-generation       | `language-patterns.md` Python/TS/Go 示例的代码注释全中文                                                                   | 译英文                                                                   |
| tdd                   | `testing-anti-patterns.md` 残留"your human partner's correction"配对会话痕迹                                               | 换成通用 self-check 指引                                                 |
| performance           | `anti-patterns.md` 把手写 module-level 变量缓存标"GOOD"（非并发安全、serverless 失效）                                     | 加"minimal illustration，生产用 lru-cache/Redis"告诫                     |
| api-testing           | SKILL.md 说`Idempotency-Key`，template 用 `X-Request-ID`（tracing header 非 idempotency）                                | 统一`Idempotency-Key`（Stripe 标准）                                   |
| simplify              | `opportunities.md` 列 prop drilling，但 SKILL.md 说跨模块结构改用 refactoring                                              | 删或改标"flag for refactoring"                                           |
| cost-optimization     | `cost-drivers.md` 仅 AWS/GCP/Azure，无 k8s（kubecost/OpenCost/namespace 归因），与 FinOps 强关联不符                       | 加 Kubernetes/container 段                                               |
| load-testing          | 零可运行脚本（k6/Locust/wrk/Artillery），全是 prose 描述                                                                     | `load-profiles.md` 加 k6 ramp+soak 示例                                |
| api-testing           | GraphQL 仅 3 bullet 无代码，REST 有完整 CRUD lifecycle（声称 REST/GraphQL 不平衡）                                           | 加 GraphQL 测试示例                                                      |
| api-testing           | SKILL.md 提 Pact/Spring Cloud Contract，template 零实际 Pact 代码                                                            | 加最小 Pact 示例或链官方文档                                             |

### LOW（记录，非优先）

- performance：无 `**Output:** PERF.md` 声明（cost-optimization 却引用它）→ 补声明
- tdd：`mocking.md` 60 行过薄，与 `test-strategy.md` 重叠 → 合并或加深
- e2e-testing：`a11y-automation.md` 用社区 `treosh/lighthouse-ci-action@v11` 非官方 Google LHCI → 核对更新
- implement：`lightweight-changes.md` 写"editor's rename-refactor"，agent 无 editor → 换"language rename tooling (LSP)"
- oss-strategy：BSL/SSPL 合并一行，二者实质不同（BSL 延迟开源 vs SSPL 强 copyleft）→ 拆两行
- prompt-engineering：model selection 用泛 tier 不链 `claude-api` skill → 加 cross-link
- prototype：`ui.md` switcher 实现 Next 专属，声称支持 Vue/Svelte → 加框架适配注
- schema-design：`schema-patterns.md` 全 Postgres 语法，无 MySQL/SQLite 可移植注 → 加一行
- architecture：`nfr-checklist.md` 把 deployment strategy 归 Maintainability（是架构决策非 NFR）→ 移出或改 Operability
- api-design：discriminated union 仅 TS，声称语言无关 → 加"无原生 sum type 语言用 enum+optional"
- observability：structured logging 示例仅 TS → 加 Python structlog/Go slog 一行
- deprecation-migration：Step 4 花 8 行讲 `@total-typescript/shoehorn` 迁移，不可泛化 → 移 ref 或换通用模式
- research：三 mode 模板 metadata 字段语言不一致（中英混）→ 统一

---

## Tier E — 明确不做（及理由）

记录以防未来重复建议：

| 不做                                                                    | 理由                                                                                                      |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| 加权评分路由 + 结构化 metadata（keywords/tags/category 入 frontmatter） | 对 47 skill 过度工程；加 frontmatter 字段（validator 明令禁止）；违反纯 markdown；phase-tree 在此规模足够 |
| scripts/templates/data 伴生文件                                         | 破坏跨 agent 可移植性                                                                                     |
| MCP builder / MCP integration skill                                     | 包是 skill 包非 plugin-dev 包；README 明言 out of scope                                                   |
| CloudBase/Godot/Tencent/Next.js/LangChain/FastAPI 等 vendor 技能        | 不可泛化                                                                                                  |
| monorepo / Helm / K8s 打包 / secrets 基础设施                           | 工具/vendor 特定；implement/breakdown/ci-cd/security-review 已在正确高度覆盖概念                          |
| UX copy / roadmap / test-case design                                    | PM/QA 侧，与现有 skill 部分重叠，边际价值低                                                               |
| 第三人称改写 45 个 description                                          | 风格偏好非缺陷；当前第二人称祈使一致且有效；churn 巨大不值                                                |
| 行数预算放宽到 500 行                                                   | 当前 15-150 行**更严**，契合反臃肿哲学，保持                                                        |

---

## 完成判定

- Tier A 全绿：验证器含安全扫描 + 漂移检查；路由器含降级链 + 红旗表；评估 harness 达成至少 1 个 discriminating case（当前为待完善，见 A5）
- ⚠️ 抽测有归档结论（改或不改均有记录）
- Tier F 的 10 个 HIGH 全修（OWASP 2021 / git push 误拦 / flyway undo / oss-polish 脚本 / drift grep / refactoring 空 ref / Agent tool / TTI→INP / RSC i18n / ADR 矛盾）
- Tier B/C/D/F 按 PR 推进，每个独立可回滚，validator 始终绿
- Tier E 的"不做"清单在本文件留存，未来再提同类建议时直接引用
