# Tech-selection mode

Reference for the `research` skill, **tech-selection** mode. Choosing or comparing a technology
stack, library, framework, open-source project, or repository for a concrete requirement. Produces
a defensible selection backed by GitHub evidence and official docs — not a popularity contest.

## Clarify the requirement

Restate: goal, constraints, platform, language/runtime, scale, budget, deadline, team skill,
must-haves, non-goals. Ask one concise question only if the requirement is too broad to search
usefully; otherwise state assumptions and proceed.

## Split the selection problem

Identify decision dimensions: capability fit, integration cost, maturity, maintenance, license,
ecosystem, performance/scalability, security, deployment complexity, lock-in. Define what "效果如何"
means: expected result, user/business impact, performance, maintainability, delivery speed,
validation plan.

## Source priority

| Priority | Source type | Use |
| --- | --- | --- |
| P0 | GitHub repos, README, docs folder, issues, PRs, releases, commits, license | Main evidence for fit and health |
| P1 | Official docs, blogs, release notes, package registry | Validate capabilities, versions, APIs, support policy |
| P2 | Technical blogs, Stack Overflow, Hacker News, Reddit | Discover adoption friction and operational pain |
| P3 | SEO listicles, marketing pages | Background only; never key evidence |

Final recommendations must be primarily supported by P0 and P1; use P2 to qualify confidence and
surface risks. If P0/P1 evidence is missing, lower confidence and state the gap.

## Search GitHub first

- Multiple angles: requirement keywords, domain terms, language/framework terms, "awesome" lists, example apps, benchmark repos, known alternatives.
- Collect at least five credible candidates before narrowing; if fewer exist, state why and compare the credible set.
- For each candidate: repo URL, description, primary language, license, stars/forks/watchers, latest commit or release date, release cadence, open issue/PR signal, docs/examples quality, package ecosystem, requirement fit.
- Do not rank by stars alone. Penalize stale maintenance, unclear license, missing docs, unresolved critical issues, high integration complexity.

## Validate with official and community sources

- Fetch official docs or release notes for capability claims, version compatibility, support status, limitations.
- Search community sources for recurring operational problems, migration friction, missing features, production stories.
- Prefer recent evidence for fast-moving stacks; use exact dates for releases, commits, version claims.

For weighted scoring, build-vs-buy, TCO, migration-cost estimation, and the long-term-bet vs
commodity distinction — load [references/selection-rubric.md](selection-rubric.md).

## 10-section output template

Default path: `docs/research/competitor.md`. If the file exists, append `-2` or `-HHmmss`;
overwrite only with explicit permission. Trim to fit, keep section order.

```markdown
# [Requirement] 技术选型研究

Generated: YYYY-MM-DD
Scope: [What was researched and excluded]
Output: [Report path]

## 1. 需求理解与假设
[Goal, constraints, assumptions, non-goals.]

## 2. 技术选型结论
Recommendation: [Chosen stack/project]
Confidence: [High/Medium/Low]
[Short rationale with citations.]

## 3. 候选方案总览
| Option | Main Repo | Fit | Maturity | Maintenance | Key Tradeoff |
| --- | --- | --- | --- | --- | --- |
| [Name] | [repo](https://github.com/org/repo) | [fit] | [signal] | [signal] | [tradeoff] |

## 4. GitHub 仓库深度分析
### [Candidate]
- Repository: [org/repo](https://github.com/org/repo)
- License: [license]
- Activity: [latest release/commit, issue/PR signal]
- Strengths: [evidence-backed]
- Weaknesses: [evidence-backed]
- Requirement fit: [analysis]

## 5. 官方文档与生态证据
[Official docs, release notes, package registry, community signals.]

## 6. 与其他技术选型的比较
[Why the chosen option beats specific alternatives for this requirement.]

## 7. 为什么选择这个
[Decision logic: strongest evidence, fit, constraints, tradeoffs.]

## 8. 效果如何
[Expected effect, success metrics, likely improvements, limits.]

## 9. 风险、限制与验证建议
[Risks, mitigations, prototype/benchmark/test plan.]

## 10. Sources
- [Source title](<source-url>) — Accessed: YYYY-MM-DD — Date: [published/updated or not visible] — Reliability: [GitHub/official/community/secondary] — Supports: [claim]
```

## Verify (tech-selection mode)

- No unresolved placeholders (`TBD`, `[Title]`, `<source-url>`, `github.com/org/repo`).
- Every key recommendation, comparison point, repository health claim, and date-sensitive claim has a citation.
- GitHub repository evidence + official documentation present when available; if community sources are low-signal, say so instead of forcing them.
- Stars alone did not drive the recommendation; maintenance, license, issue health, integration cost were weighed.
- No old blog post is treated as current capability evidence.
- Live sources were actually fetched; no "researched" claim when browsing was unavailable.
