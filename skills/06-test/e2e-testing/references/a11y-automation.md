# Accessibility Test Automation

Depth reference for the `e2e-testing` skill. How to automate a11y testing in CI — axe-core,
Lighthouse CI, Storybook a11y addon. Design-time a11y rules are in `frontend-design`'s
`ux-guidelines.md` (the 15-rule checklist) and `design-foundations.md` §Usability Heuristics (Nielsen #1, #4, #6); the
`shipping` skill's pre-launch checklist checks for "no axe-core / Lighthouse a11y warnings." This
reference teaches how to install and configure those tools so the checklist can pass.

## Contents

- [1. Why automate a11y testing](#1-why-automate-a11y-testing)
- [2. axe-core — the standard engine](#2-axe-core--the-standard-engine)
- [3. Lighthouse CI](#3-lighthouse-ci)
- [4. Storybook a11y addon](#4-storybook-a11y-addon)
- [5. What to test (the a11y test surface)](#5-what-to-test-the-a11y-test-surface)
- [6. CI integration rules](#6-ci-integration-rules)
- [7. How this connects](#7-how-this-connects)

## 1. Why automate a11y testing

Manual a11y testing (keyboard navigation, screen reader, contrast check) is essential but slow and
expert-dependent. Automated testing catches the mechanical violations — missing alt text, contrast
failures, invalid ARIA, missing labels — on every PR, before a human ever looks at the UI.

| What automated catches | What automated misses |
|---|---|
| Missing alt text, labels, landmarks | Whether the alt text is meaningful |
| Contrast ratio below threshold | Whether the reading order makes sense |
| Invalid ARIA roles/states | Whether ARIA is used appropriately |
| Keyboard traps (focus can't escape) | Whether keyboard flow is logical |
| Missing focus styles | Whether focus order matches visual order |
| Duplicate IDs | Whether the page is usable with a screen reader |

Automated testing catches ~30-50% of a11y issues (the mechanical ones). The rest requires manual
testing. Both are needed; automation is the floor, not the ceiling.

## 2. axe-core — the standard engine

axe-core is the a11y test engine used by most tools (Lighthouse, browser DevTools, Storybook). It
runs WCAG 2.1 AA checks against the DOM and reports violations.

### Integration patterns

| Pattern | When | Tool |
|---|---|---|
| **In E2E tests** | Catch a11y regressions in full-page flows | `@axe-core/playwright` (or Cypress axe) |
| **On components** | Catch a11y issues per component in isolation | Storybook a11y addon |
| **In CI / pre-deploy** | Catch a11y issues on built pages | Lighthouse CI |
| **In dev (browser)** | Catch issues while developing | axe DevTools browser extension |

### E2E integration (Playwright + axe)

```js
import { AxeBuilder } from '@axe-core/playwright';

test('page has no a11y violations', async ({ page }) => {
  await page.goto('/dashboard');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

### Per-page vs per-component
- **Per-page (E2E)**: test the full rendered page including layout, nav, content. Catches issues
  that only appear when components compose (e.g. a modal trap inside a nav).
- **Per-component (Storybook)**: test each component in isolation. Catches issues at the source;
  faster feedback; but misses composition issues.

Use both: Storybook a11y in dev (fast, per-component), axe in E2E (comprehensive, per-page).

## 3. Lighthouse CI

Lighthouse includes a11y audits (powered by axe) alongside performance/SEO. Lighthouse CI runs
Lighthouse on every PR and fails the build if the a11y score drops below a threshold.

```yaml
# .github/workflows/lighthouse.yml
- uses: treosh/lighthouse-ci-action@v11
  with:
    urls: |
      http://localhost:3000/
      http://localhost:3000/dashboard
    budgetPath: ./lighthouse-budget.json
    uploadArtifacts: true
```

### Budget file (assert thresholds)
```json
{
  "assertions": {
    "categories:accessibility": ["error", { "minScore": 0.9 }]
  }
}
```

- `minScore: 0.9` — fail if a11y score < 90. Tune to your baseline; start at 0.8, raise over time.
- `error` — fail the build (vs `warn` which only reports).

### Lighthouse a11y score caveats
- **Score is a sample, not exhaustive** — Lighthouse runs a subset of axe checks. A 100 score
  doesn't mean a11y is perfect; it means the checked rules pass.
- **Headless Chrome differs from real users** — Lighthouse runs headless; some a11y issues (focus
  behavior, screen reader interaction) only surface in a real browser.
- **Test authenticated pages** — the public homepage is usually clean; the authenticated app (where
  the real UI complexity lives) is where violations hide. Lighthouse CI needs auth setup to test
  these.

## 4. Storybook a11y addon

Tests each story in isolation, in dev (instant feedback) and in CI (regression catch).

```bash
npm install --save-dev @storybook/addon-a11y
```

```js
// .storybook/main.js
addons: ['@storybook/addon-a11y'];
```

The addon panel shows violations per story, with the failing element highlighted. Devs fix a11y
before the story is merged, not after.

### Storybook a11y in CI
```bash
npm run build-storybook
npx storybook a11y-report  # or per-story checks in test-runner
```

## 5. What to test (the a11y test surface)

| Surface | What to test | Tool |
|---|---|---|
| Every page/route | Full-page a11y | axe in E2E |
| Every component | Component-level a11y | Storybook addon |
| Every interactive state | Modal open, dropdown expanded, form errored | axe after state change in E2E |
| Keyboard navigation | Focus order, no traps, focus visible | Manual + axe (partial) |
| Color contrast | All text/UI against backgrounds | axe + Lighthouse |
| Dynamic content | After AJAX/render updates | axe re-run after the update |

The "every interactive state" row is the most-missed: a page can pass a11y in its default state
and fail when a modal opens (focus trap, ESC behavior, background scroll-lock). Re-run axe after
state changes.

## 6. CI integration rules

- **Fail the build on a11y violations** — `error`, not `warn`. A warning is ignored; an error is
  fixed. (Start with `warn` to establish baseline, then switch to `error` once clean.)
- **Test the built app, not just source** — some a11y issues (missing alt from CMS content, ARIA
  injected by third-party scripts) only appear after build/runtime.
- **Test authenticated pages** — set up CI auth (login session) so the real app is tested, not just
  the marketing page.
- **Track the score over time** — a11y score trending down across PRs means regressions are
  sneaking in; the CI catches the cliff, not the drift.
- **Don't exclude rules without a documented reason** — axe lets you disable rules (`disable: ['color-contrast']`).
  Each disable is a conscious decision; an undocumented disable is a silent acceptance.

## 7. How this connects

- **Design rules**: `frontend-design`/`ux-guidelines.md` (15 a11y rules) and
  `design-foundations.md` §Usability Heuristics (Nielsen heuristics) — what to build.
- **Pre-launch check**: `shipping` skill checks for "no axe-core / Lighthouse a11y warnings."
- **This reference**: how to install/configure axe-core, Lighthouse CI, Storybook a11y so the
  pre-launch check can pass — and so regressions are caught per-PR, not at launch.

Load this when setting up a11y test automation. Load `ux-guidelines.md` when designing a component.
The design rules say what good a11y looks like; this reference automates checking that the code
meets them.
