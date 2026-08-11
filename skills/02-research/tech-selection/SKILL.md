---
name: tech-selection
description: Use when choosing or comparing a technology stack, library, framework, open-source project, or repository for a concrete requirement. Triggers on "技术选型", "方案对比", "选哪个", "tech stack", "library comparison", "技术对比".
---

## When to use

- Choosing or comparing a technology stack, library, framework, open-source project, or GitHub repository for a concrete requirement.
- User says "技术选型", "方案对比", "选哪个", "tech stack", "library comparison".
- Need a defensible selection backed by GitHub evidence and official docs, not a popularity contest.

**Not for:** market sizing or competitor business analysis (use `market-research`); cited deep research report (use `research`).

## Steps

1. **Clarify the requirement.**
   - Restate goal, constraints, platform, language/runtime, scale, budget, deadline, team skill, must-haves, and non-goals.
   - Ask one concise question only if the requirement is too broad to search usefully; otherwise state assumptions and proceed.

2. **Split the selection problem.**
   - Identify decision dimensions: capability fit, integration cost, maturity, maintenance, license, ecosystem, performance/scalability, security, deployment complexity, lock-in.
   - Define what "效果如何" means: expected result, user/business impact, performance, maintainability, delivery speed, validation plan.

3. **Search GitHub first.**
   - Use multiple angles: requirement keywords, domain terms, language/framework terms, "awesome" lists, example apps, benchmark repos, known alternatives.
   - Collect at least five credible candidates before narrowing; if fewer exist, state why and compare the credible set.
   - For each candidate, collect: repo URL, description, primary language, license, stars/forks/watchers, latest commit or release date, release cadence, open issue/PR signal, docs/examples quality, package ecosystem, requirement fit.
   - Do not rank by stars alone. Penalize stale maintenance, unclear license, missing docs, unresolved critical issues, high integration complexity.

4. **Validate with official and community sources.**
   - Fetch official docs or release notes for capability claims, version compatibility, support status, limitations.
   - Search community sources for recurring operational problems, migration friction, missing features, production stories.
   - Prefer recent evidence for fast-moving stacks; use exact dates for releases, commits, version claims.

5. **Compare candidates.**
   - Build a short matrix comparing the recommended option against meaningful alternatives.
   - Explain why the winner fits this requirement better, not just why it is popular.
   - Separate evidence from inference; mark uncertain claims as inference.

6. **Assess expected effect.**
   - State what the selected technology should improve: delivery speed, reliability, UX, performance, maintainability, cost, ecosystem leverage.
   - State tradeoffs and residual risks.
   - Give a practical validation plan: prototype scope, success metrics, tests/benchmarks, migration spike, or production trial.

7. **Write the cited Markdown report.**
   - Default path: `docs/competitor.md` in the workspace. If the file exists, append `-2` or
     `-HHmmss`; overwrite only with explicit permission.
   - Inline-cite where claims appear, plus a source appendix.
   - Use the template below (trim to fit, keep section order):

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

8. **Deliver a short chat summary.**
   - Report path, recommended option and confidence, top 3 reasons, main tradeoff or risk, source count by source class and any access limitations.
   - If live browsing was unavailable or forbidden, do not present the result as researched — explain the limitation and offer an offline-only draft or ask to proceed with live research.

**Source priority.**

| Priority | Source type | Use |
| --- | --- | --- |
| P0 | GitHub repos, README, docs folder, issues, PRs, releases, commits, license | Main evidence for fit and health |
| P1 | Official docs, blogs, release notes, package registry | Validate capabilities, versions, APIs, support policy |
| P2 | Technical blogs, Stack Overflow, Hacker News, Reddit | Discover adoption friction and operational pain |
| P3 | SEO listicles, marketing pages | Background only; never key evidence |

Final recommendations must be primarily supported by P0 and P1; use P2 to qualify confidence and surface risks. If P0/P1 evidence is missing, lower confidence and state the gap.

## Verify

- The report file exists and contains no unresolved placeholders (`TBD`, `[Title]`, `<source-url>`, `github.com/org/repo`).
- Every key recommendation, comparison point, repository health claim, and date-sensitive claim has a citation.
- The source set includes GitHub repository evidence and official documentation when available; if community sources are unavailable or low-signal, say so instead of forcing them.
- Stars alone did not drive the recommendation; maintenance, license, issue health, and integration cost were weighed.
- No old blog post is treated as current capability evidence.
- Live sources were actually fetched; no "researched" claim is made when browsing was unavailable or forbidden.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md)
