---
name: performance
description: Use when optimizing performance — measure before you optimize: profile, identify bottlenecks, then improve. Triggers on "webperf", "performance regression", "慢", "性能优化", "性能调优" — also when user says "太慢了" / "卡顿".
---

# Performance Optimization

Measure before optimizing. Performance work without measurement is guessing — and guessing leads to premature optimization that adds complexity without improving what matters. Profile first, identify the actual bottleneck, fix it, measure again. Optimize only what measurements prove matters.

## When to use

- Performance requirements exist in the spec (load time budgets, response time SLAs)
- Users or monitoring report slow behavior, or Core Web Vitals are below thresholds
- You suspect a change introduced a regression
- Building features that handle large datasets or high traffic
- Triggers on "webperf", "performance regression", "慢", "性能优化"

**Not for:** Don't optimize before you have evidence of a problem. Premature optimization adds complexity that costs more than the performance it gains. Diagnosing a bug (use `debugging`).

## Steps

### 1. Measure — establish a baseline with real data

Two complementary approaches — use both:

- **Synthetic** (Lighthouse, DevTools Performance tab): controlled, reproducible. Best for CI regression detection and isolating specific issues.
- **RUM** (`web-vitals` library, CrUX): real user data in real conditions. Required to validate that a fix actually improved user experience.

Use the same command, same conditions, same fixed budget (wall-clock, sample count, or request count) every time. A baseline taken on a cold cache against a result taken on a warm one measures the cache, not your change.

### 2. Identify the actual bottleneck (not assumed)

Profile before proposing a fix. Let the symptom tell you where to look — the symptom→cause decision tree and per-category investigation tables (frontend LCP/CLS/INP, backend N+1/memory/CPU/latency) are in `references/bottlenecks.md`. Core Web Vitals "Good" thresholds (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) and performance budgets are there too.

### 3. Fix the specific bottleneck

Address what measurements proved matters. Common anti-patterns and their fixes — N+1 queries, unbounded data fetching, missing image optimization, unnecessary re-renders, large bundle size, missing caching — are cataloged with code in `references/anti-patterns.md`.

**Change one thing at a time.** Three optimizations landed together produce one number, and you cannot attribute it. If they must ship together, measure each in isolation first.

### 4. Verify — re-measure, keep or revert

A fix is a hypothesis until you re-measure. Re-measure the way you measured the baseline. Beat the noise, not just the mean: repeat the measurement and compare the delta against run-to-run variance. A 3% gain inside ±5% variance is not a gain; it is a different sample.

| Result vs. baseline | Action |
|---|---|
| Past the threshold, tests green | **Keep.** Commit with before/after numbers in the message. |
| Within noise (no measurable change) | **Revert.** |
| Worse | **Revert.** |
| Improved, but a test went red | **Revert.** A regression wearing a win's clothing. |

**"Neutral" is a revert, not a keep.** The change is already written, throwing it away feels wasteful, so it lands unmeasured, and the codebase accretes complexity that never bought anything. Code you keep, you maintain forever — make it pay for itself.

**Correctness gates the metric.** An "optimization" that wins by dropping work the product needed (skipping a validation, caching something that must be fresh, removing a load-bearing `await`) is a regression, not a win.

### 5. Guard against regression

Log every attempt — kept and reverted alike — so a dead idea isn't re-run next quarter. Reverted work leaves no trace in git history, which is exactly why the same dead idea gets tried again. A short ledger in the PR description or a `PERF.md` works:

| Idea | Baseline → Result | Verdict | Why |
|---|---|---|---|
| Memoize the row component | INP 240ms → 235ms | reverted | Inside noise (±15ms). Rows weren't the bottleneck. |
| Virtualize the list | INP 240ms → 90ms | kept | Long tasks gone from the trace. |

Then add monitoring or a regression test so the gain doesn't erode. If a performance budget is configured, enforce it in CI.

## Verify

- [ ] Before and after measurements exist (specific numbers, same command and conditions)
- [ ] Improvement exceeds run-to-run variance, not just the mean
- [ ] Changes that didn't beat the baseline were reverted, not kept as neutral
- [ ] Attempts logged — kept and reverted alike — so a dead idea isn't re-run
- [ ] Specific bottleneck identified and addressed; Core Web Vitals within "Good" thresholds
- [ ] No N+1 queries in new data fetching code; bundle size hasn't increased significantly
- [ ] Existing tests still pass (optimization didn't break behavior)

**Red flags:** optimization without profiling data to justify it; N+1 patterns or unpaginated list endpoints in new code; images without dimensions / lazy loading / responsive sizes; `React.memo` / `useMemo` sprayed everywhere (overusing is as bad as underusing); a "win" that required a test to be changed, skipped, or deleted; several optimizations bundled into one unattributable measurement; the same failed optimization attempted again because nobody recorded the first attempt.

**Output:** `PERF.md` (optional) — attempt ledger of performance changes (kept + reverted), so a dead idea isn't re-run next quarter. Mirrors `COST.md` in cost-optimization.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (verify don't assume, enforce simplicity, surgical scope)
- [references/bottlenecks.md](references/bottlenecks.md) — symptom→cause decision tree, frontend/backend bottleneck tables, Core Web Vitals targets, performance budgets
- [references/anti-patterns.md](references/anti-patterns.md) — N+1, unbounded fetching, image optimization, re-renders, bundle splitting, caching (with code examples)
- [references/database-performance.md](references/database-performance.md) — DB-specific: EXPLAIN plan reading, index maintenance, slow-query analysis, N+1 detection, query anti-patterns, connection pooling
