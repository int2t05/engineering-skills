# Playwright Rules — Consolidated Reference

Eight rules across six categories. Load this reference when writing or reviewing
Playwright E2E tests, choosing locator strategies, setting up authentication,
or debugging flaky tests.

## Contents

- [Quick Reference](#quick-reference)
- [1. Prefer Role-Based Locators](#1-prefer-role-based-locators)
- [2. Handle Strict Mode Violations](#2-handle-strict-mode-violations)
- [3. Reuse Authentication with Storage State](#3-reuse-authentication-with-storage-state)
- [4. Use Web-First Assertions](#4-use-web-first-assertions)
- [5. Handle React Controlled Date and Time Inputs](#5-handle-react-controlled-date-and-time-inputs)
- [6. Handle Custom Checkbox Components](#6-handle-custom-checkbox-components)
- [7. Mirror Route Structure in Test Organization](#7-mirror-route-structure-in-test-organization)
- [8. Never Use Arbitrary waitForTimeout](#8-never-use-arbitrary-waitfortimeout)

## Quick Reference

| # | Category | Rule | Impact |
|---|----------|------|--------|
| 1 | Locators | Prefer role-based locators | CRITICAL |
| 2 | Locators | Handle strict mode violations | CRITICAL |
| 3 | Authentication | Reuse auth with storage state | CRITICAL |
| 4 | Assertions | Use web-first assertions | HIGH |
| 5 | Forms | Handle React controlled date/time inputs | HIGH |
| 6 | Forms | Handle custom checkbox components | HIGH |
| 7 | Organization | Mirror route structure in test organization | MEDIUM |
| 8 | Reliability | Never use arbitrary waitForTimeout | MEDIUM |

---

## 1. Prefer Role-Based Locators

**Impact: CRITICAL (test resilience to UI changes)**

Use `getByRole`, `getByLabel`, and `getByText` over CSS selectors or test IDs.
Role-based locators mirror how users and assistive technology interact with the
page, making tests resilient to refactoring.

**Incorrect:**

```javascript
// Bad: CSS selectors break when classes change
await page.locator('.btn-primary').click();
await page.locator('#submit-form').click();
await page.locator('div > form > button:nth-child(2)').click();

// Bad: data-testid couples tests to implementation
await page.locator('[data-testid="login-button"]').click();
```

- CSS classes are styling concerns, not behavior contracts
- Selectors break on every UI redesign
- Tests don't verify accessibility (screen readers can't find `.btn-primary`)
- `data-testid` adds noise to production HTML

**Correct:**

```javascript
// Good: Role-based — mirrors user interaction
await page.getByRole('button', { name: 'Sign In' }).click();
await page.getByRole('tab', { name: 'Network' }).click();
await page.getByRole('heading', { name: 'Dashboard' }).toBeVisible();

// Good: Label-based — matches form field labels
await page.getByLabel('Email').fill('user@example.com');

// Good: Text-based — for non-interactive content
await expect(page.getByText('Welcome back')).toBeVisible();

// Good: Use exact when text is ambiguous
await page.getByRole('button', { name: 'Verified', exact: true });
```

**Priority order:**

1. `getByRole` — buttons, tabs, headings, links, checkboxes
2. `getByLabel` — form inputs with labels
3. `getByText` — static content, with `{ exact: true }` when needed
4. `locator('#id')` — for inputs without labels (e.g., `#password`)
5. CSS selectors — last resort for complex DOM structures

---

## 2. Handle Strict Mode Violations

**Impact: CRITICAL (prevents test failures from ambiguous selectors)**

Playwright runs in strict mode by default — locators that match multiple
elements throw an error. Handle this proactively with `{ exact: true }`,
`.first()`, or scoped locators.

**Incorrect:**

```javascript
// Bad: "Verified" also matches "Unverified"
await page.getByRole('button', { name: 'Verified' }).click();

// Bad: "POS Demo" appears in heading AND breadcrumb
await expect(page.getByText('POS Demo')).toBeVisible();

// Bad: "Convert" matches tab name AND submit button
await page.getByRole('button', { name: /convert/i }).click();
```

- Strict mode throws: "resolved to 2 elements"
- Different elements have the same visible text

**Correct:**

```javascript
// Good: exact match prevents substring matching
await page.getByRole('button', { name: 'Verified', exact: true }).click();

// Good: use role to disambiguate heading vs breadcrumb
await expect(page.getByRole('heading', { name: 'POS Demo' })).toBeVisible();

// Good: scope to a specific container
await expect(page.locator('.form-section').getByText('Item Type')).toBeVisible();

// Good: use .first() when you know the first match is correct
await page.getByText('Dashboard').first().click();

// Good: filter with parent context
await page.locator('button').filter({ hasText: 'Arif Azmi' }).first().click();
```

**Strategies (in order of preference):**

1. `{ exact: true }` — prevents "Verified" matching "Unverified"
2. `getByRole('heading', ...)` — disambiguates heading from breadcrumb/sidebar
3. Scoped locator — `container.getByText(...)` limits search area
4. `.first()` — when the first match is always correct
5. `.filter({ hasText: ... })` — combine with other locators

---

## 3. Reuse Authentication with Storage State

**Impact: CRITICAL (eliminates login overhead and rate-limit failures)**

Log in once per role in a setup project, save browser state to JSON files, and
reuse via `storageState` in all tests. Never log in per-test.

**Incorrect:**

```javascript
// Bad: Logging in at the start of every test
test('dashboard shows data', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.locator('#password').fill('password');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.waitForURL('**/dashboard');
    // Now the actual test...
    await expect(page.getByText('Welcome')).toBeVisible();
});
```

- Each test wastes 1-2 seconds on login
- Login rate limits (429) block the entire suite after ~5 tests
- Login failures cascade — every test fails, not just auth tests

**Correct:**

```javascript
// auth/auth.setup.js — runs once before all tests
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const AUTH_DIR = path.join(import.meta.dirname, '..', '.auth');

const users = [
    { name: 'customer', file: 'customer.json', email: 'customer@example.com' },
    { name: 'admin', file: 'admin.json', email: 'admin@example.com' },
];

for (const user of users) {
    setup(`authenticate as ${user.name}`, async ({ page }) => {
        await page.goto('/login');
        await page.getByLabel('Email').fill(user.email);
        await page.locator('#password').fill('password');
        await page.getByRole('button', { name: 'Sign In' }).click();
        await page.waitForURL('**/dashboard');
        await page.context().storageState({ path: path.join(AUTH_DIR, user.file) });
    });
}
```

```javascript
// fixtures/test.js — custom fixture for role-based auth
import { test as base } from '@playwright/test';
import path from 'path';

const AUTH_DIR = path.join(import.meta.dirname, '..', '.auth');

export const test = base.extend({
    role: ['customer', { option: true }],
    authedPage: async ({ browser, role }, use) => {
        const context = await browser.newContext({
            storageState: path.join(AUTH_DIR, `${role}.json`),
        });
        const page = await context.newPage();
        await use(page);
        await context.close();
    },
});
```

```javascript
// specs/dashboard.spec.js — tests get pre-authenticated pages
import { test, expect } from '../fixtures/test.js';

test.describe('Dashboard', () => {
    test.use({ role: 'customer' });
    test('shows welcome message', async ({ authedPage: page }) => {
        await page.goto('/dashboard');
        await expect(page.getByText('Welcome')).toBeVisible();
    });
});
```

```javascript
// playwright.config.js — setup project runs first
export default defineConfig({
    projects: [
        { name: 'auth-setup', testMatch: /auth\.setup\.js$/, testDir: './auth' },
        { name: 'chrome', use: { ...devices['Desktop Chrome'] }, dependencies: ['auth-setup'] },
    ],
});
```

- Login happens once per role (3 logins for 90+ tests)
- No rate-limit issues even with strict throttling
- Role switching is a simple `test.use({ role: 'admin' })`

---

## 4. Use Web-First Assertions

**Impact: HIGH (eliminates flaky timing-dependent tests)**

Playwright's `expect(locator)` assertions auto-retry until the condition is met
or timeout. Never use manual waits or DOM queries followed by manual checks.

**Incorrect:**

```javascript
// Bad: Manual DOM query — no auto-retry, race condition
const button = await page.$('.submit-btn');
expect(button).not.toBeNull();

// Bad: Using waitForTimeout — arbitrary delay, still flaky
await page.waitForTimeout(2000);
const text = await page.textContent('.status');
expect(text).toBe('Success');

// Bad: isVisible() returns immediately — no retry
const visible = await page.locator('.toast').isVisible();
expect(visible).toBe(true);
```

- `page.$()` returns null if element hasn't rendered yet
- `waitForTimeout` wastes time on fast environments, still flaky on slow ones
- `isVisible()` is a snapshot — doesn't wait for animations or lazy rendering

**Correct:**

```javascript
// Good: Web-first assertions auto-retry with configurable timeout
await expect(page.getByText('Success')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('button')).toBeDisabled();
await expect(page.getByRole('dialog')).toBeVisible();
await expect(page.getByRole('dialog')).not.toBeVisible();

// Good: Custom timeout for slow operations
await expect(page.getByText('Uploaded')).toBeVisible({ timeout: 10_000 });

// Good: Text content assertions
await expect(page.getByRole('heading')).toHaveText('Dashboard');
await expect(page.locator('#balance')).toContainText('RM');

// Good: Attribute assertions
await expect(page.locator('input')).toHaveValue('100');
await expect(page.locator('html')).toHaveClass(/dark/);

// Good: URL assertion after navigation
await expect(page).toHaveURL(/\/dashboard/);
```

**Common assertions:** `toBeVisible()` / `toBeHidden()`, `toBeEnabled()` /
`toBeDisabled()`, `toHaveText()` / `toContainText()`, `toHaveValue()`,
`toHaveAttribute()`, `toHaveURL()`, `toHaveClass()`.

---

## 5. Handle React Controlled Date and Time Inputs

**Impact: HIGH (prevents silent form state desync)**

Playwright's `fill()` sets the DOM value but does not always trigger React's
`onChange` for date and time inputs. The HTML value updates but React state
stays empty, causing form validation to fail silently.

**Incorrect:**

```javascript
// Bad: fill() updates DOM but React state stays empty
await page.locator('#date').fill('2026-04-14');
await page.locator('#time').fill('10:00');

// The submit button remains disabled because React state is:
// { preferred_date: '', preferred_time: '' }
// Even though the inputs visually show the values
```

- `fill()` dispatches events that React date/time inputs may not listen to
- Form appears filled visually but React state is empty
- Only affects date/time input types — text inputs work fine with `fill()`

**Correct:**

```javascript
// Good: Use keyboard.type() to simulate real user input
const dateInput = page.locator('#preferred-date');
await dateInput.scrollIntoViewIfNeeded();
await dateInput.click();
await page.keyboard.type('16042026'); // DDMMYYYY for DD/MM/YYYY locale

// Time inputs accept digits + AM/PM
const timeInput = page.locator('#preferred-time');
await timeInput.click();
await page.keyboard.type('1000AM'); // 10:00 AM

// Brief wait needed: keyboard.type() on date inputs triggers React state
// updates asynchronously — 200ms allows the controlled component to sync
await page.waitForTimeout(200);
```

```javascript
// Alternative: Use evaluate to set value + dispatch native events
await page.evaluate((val) => {
    const el = document.getElementById('preferred-date');
    const setter = Object.getOwnPropertyDescriptor(
        window.HTMLInputElement.prototype, 'value'
    ).set;
    setter.call(el, val);
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
}, '2026-04-16');
```

**When to use `keyboard.type()` vs `fill()`:**

- `fill()` — text, number, email, password, search inputs
- `keyboard.type()` — date, time, datetime-local inputs in React apps
- Both require `.click()` first to focus the input

---

## 6. Handle Custom Checkbox Components

**Impact: HIGH (prevents click-no-effect bugs on styled checkboxes)**

Custom checkbox components (like those using Tailwind's `sr-only` pattern) hide
the native `<input>` and render a styled `<div>`. Playwright's `.check()` may
not trigger React's `onChange` on hidden inputs. Multiple `<label htmlFor>`
elements pointing to the same input cause double-toggle (check then uncheck).

**Incorrect:**

```javascript
// Bad: .check() on sr-only input — may not trigger React onChange
await page.locator('#terms').check();

// Bad: .check({ force: true }) — bypasses visibility but still no React event
await page.locator('#terms').check({ force: true });

// Bad: clicking a label when there are TWO labels for the same input
// <Checkbox id="terms" />          ← has its own <label> wrapper
// <label htmlFor="terms">I agree</label>  ← second label
// Clicking either label toggles twice = no change
await page.locator('label[for="terms"]').click();
```

- `sr-only` inputs are invisible — `.check()` can't find them
- `force: true` clicks the element but React doesn't see the event
- Two `<label htmlFor>` elements cause double-toggle (browser behavior)

**Correct:**

```javascript
// Good: Click the component's own <label> wrapper (contains the visual checkbox)
await page.locator('label:has(#terms)').click();

// Good: Click the T&C text that toggles via onClick handler
await page.getByText('I agree to the terms').click();

// Good: For components with only one label, click the label directly
await page.locator('label[for="remember"]').click();

// Good: Verify the checkbox state with web-first assertion
await expect(page.locator('#terms')).toBeChecked();
```

**Fix the component if two labels exist (code bug):**

```jsx
// Bad: Two labels for same input — browser toggles twice
<Checkbox id="terms" />
<label htmlFor="terms">I agree</label>

// Good: Use <span> for the text, let Checkbox own the label
<Checkbox id="terms" />
<span onClick={() => setAgreed(v => !v)}>I agree</span>
```

---

## 7. Mirror Route Structure in Test Organization

**Impact: MEDIUM (scalable test organization as app grows)**

Organize E2E test files to mirror your application's route groups. This makes
tests discoverable and scalable as features are added.

**Incorrect:**

```
tests/e2e/specs/
  test1.spec.js          # What does this test?
  test2.spec.js          # No grouping
  all-tests.spec.js      # One giant file with 200 tests
  login-and-buy.spec.js  # Mixed concerns
```

- Can't find the test for a specific feature
- One giant file causes merge conflicts
- Mixed concerns make failures hard to diagnose

**Correct:**

```
tests/e2e/specs/
  auth/
    login.spec.js
    register.spec.js
  customer/                    # matches role:customer routes
    egold/
      buy.spec.js
      sell.spec.js
    gold-saving/
      new-agreement.spec.js
  admin/                       # matches role:admin routes
    customers/
      kyc-approve.spec.js
    egold/
      approve-reject.spec.js
  ui/                          # cross-cutting concerns
    dark-mode.spec.js
    responsive.spec.js
    navigation.spec.js
```

**Naming convention:**

- Folders match route prefixes (`/admin/*` → `admin/`)
- Files match the feature or page name
- `ui/` folder for cross-cutting concerns (theme, responsive, navigation)
- One `describe` block per file, focused on one page/feature

---

## 8. Never Use Arbitrary waitForTimeout

**Impact: MEDIUM (prevents slow and flaky tests)**

Playwright auto-waits for elements before interacting. Adding `waitForTimeout`
is almost always a sign of a missing assertion or incorrect locator strategy.

**Incorrect:**

```javascript
// Bad: Waiting for toast to appear
await page.click('#submit');
await page.waitForTimeout(3000);
await expect(page.getByText('Success')).toBeVisible();

// Bad: Waiting for React re-render
await page.fill('#amount', '100');
await page.waitForTimeout(1000);
const isEnabled = await page.locator('#submit').isEnabled();
```

- 3 second wait runs on every test even when page loads in 200ms
- On slow CI, 2 seconds may not be enough — still flaky
- Accumulates across test suite (30 tests x 3s = 90s wasted)

**Correct:**

```javascript
// Good: Wait for the element directly — auto-retries until visible
await page.click('#submit');
await expect(page.getByText('Success')).toBeVisible({ timeout: 8_000 });

// Good: Wait for URL change after navigation
await page.click('a[href="/dashboard"]');
await page.waitForURL('**/dashboard');
await expect(page.getByRole('heading')).toBeVisible();

// Good: Wait for button state to change
await page.fill('#amount', '100');
await expect(page.locator('#submit')).toBeEnabled({ timeout: 3_000 });

// Good: Wait for network request to complete
await Promise.all([
    page.waitForResponse('/api/data'),
    page.click('#load-data'),
]);
```

**Acceptable uses of waitForTimeout (rare):**

- After `keyboard.type()` on date inputs — React needs a tick to process (200ms max)
- After clipboard operations — OS-level delay
- Never more than 500ms, and always with a comment explaining why
