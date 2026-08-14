---
name: i18n
description: Use when internationalizing an application — message extraction, ICU/MessageFormat, locale routing, RTL layout, pluralization/gender, and locale-aware formatting. Triggers on "i18n", "localization", "l10n", "RTL", "国际化", "本地化", "多语言".
---

# Internationalization (i18n)

Internationalization is not translation — it is the engineering discipline of making an application
locale-aware so translation is a content change, not a code change. Hardcoded strings, locale-blind
formatting, and LTR-only layouts all become bugs the moment a second locale is needed. Build the
scaffolding before the second locale arrives, not after.

## When to use

- Preparing an application for multiple locales (message extraction, locale routing, formatting)
- Adding RTL support or locale-specific pluralization/gender rules
- Auditing an existing app for hardcoded strings or locale-blind formatting
- Triggers on "i18n", "localization", "l10n", "RTL", "国际化", "本地化", "多语言"

**Not for:** frontend visual design (use `frontend-design`); API contract design (use `api-design`).
i18n is a cross-cutting implementation discipline touching frontend, backend, and build tooling.

## Steps

### 1. Audit the locale surface

Before writing code, find every locale-sensitive surface in the application:

- Hardcoded user-facing strings (UI labels, error messages, email templates, push notifications)
- Formatted values: dates, times, numbers, currencies, percentages, units
- Pluralization and gender-dependent phrasing
- Layout assumptions: LTR-only CSS, fixed-width containers, text concatenation
- Locale-affecting config: timezone handling, first-day-of-week, calendar system

_Verify: the audit produces a list of locale-sensitive surfaces grouped by type, not a vague "needs
translation."_

### 2. Extract messages

Replace every hardcoded string with a message ID resolved through an i18n library. Messages live
in locale files keyed by ID, not inline:

- Use the framework's i18n library (react-intl, i18next, FormatJS, vue-i18n, or equivalent)
- Message IDs are descriptive (`user.profile.edit_button`), not positional (`btn_3`)
- Leave source-locale strings as the fallback; never leave a missing-key hole in production
- Extract programmatically (CLI extractors) where the framework supports it — manual extraction
  drifts

_Verify: grep for user-facing literals in components returns only IDs; no hardcoded strings reach
the user._

### 3. Choose message format and handle pluralization

Use ICU MessageFormat — it is the standard for handling the grammar that varies across locales
(plurals, gender, select). Avoid string concatenation and naive plural rules (`if count === 1`);
they fail across locales:

- **Pluralization:** ICU plural syntax handles the 6 CLDR plural categories (zero, one, two, few,
  many, other) — English needs two, Arabic needs all six
- **Gender / select:** ICU select syntax for gendered or context-dependent phrasing
- **Interpolation:** named placeholders, never positional — translators reorder sentences
- **Rich text:** embed component placeholders (links, bold) via ICU rich-text or the library's
  component-interpolation, not by splitting strings around tags (splitting breaks translation)

_Verify: every message with a count uses ICU plural syntax; no `count + " items"` concatenation._

### 4. Set up locale routing and detection

Decide how a user's locale is determined and how it maps to routes:

- **Detection order:** explicit user preference (account setting) → URL path/query →
  Accept-Language header → geo (with caution — geo ≠ language) → default
- **Persistence:** store the choice (cookie / account) so it survives navigation
- **Routing:** locale-prefixed routes (`/en/...`, `/ar/...`) for SEO and shareability; or
  path-less with client detection for app-only surfaces — choose deliberately
- **SSR / hydration:** the server must render in the detected locale, not render a default then
  flash-correct on the client (hydration mismatch = broken UX)
- **Server-side message loading (RSC):** in App Router / RSC frameworks, load only the request's
  locale messages on the server (per-locale bundle split, not an all-locales bundle); bind locale
  per-request (`setRequestLocale`-style, never a module global); keep server-only messages out of
  the client bundle. See [references/server-i18n.md](references/server-i18n.md) for the full pattern.

_Verify: locale detection follows the documented order; the initial server render matches the
client locale (no flash)._

### 5. Handle formatting and layout

Locale-aware formatting for every user-facing value:

- **Dates/times:** format via Intl.DateTimeFormat or the i18n library; honor timezone, calendar,
  and locale-specific ordering. Never hand-build date strings.
- **Numbers/currencies:** Intl.NumberFormat; currencies need the locale (symbol placement) AND the
  currency code (¥ in Japan vs. ¥ in China).
- **RTL:** CSS logical properties (`margin-inline-start`, not `margin-left`); `dir` attribute on
  the root; mirror icons and directional layouts. Test in an RTL locale, not by eyeballing.
- **Text length:** translated text is 30–50% longer than English (German) or shorter (Chinese);
  layouts must flex, not truncate. No fixed-width buttons.

_Verify: dates/numbers render correctly in at least LTR + RTL locales; logical properties used;
layout survives 140% text expansion._

### 6. Test across locales

Run the app in a non-source locale — preferably an RTL one (Arabic, Hebrew) — to surface the bugs
that source-locale testing hides:

- Missing translations render as IDs or fallback (never blank)
- Pluralization correct for the locale's plural rules
- RTL layout mirrors correctly; no overflow or overlap
- Formatting (date, number, currency) matches the locale
- E2E tests parameterized by locale where feasible

## Verify

- [ ] No hardcoded user-facing strings in components (grep confirms)
- [ ] All messages extracted to locale files with descriptive IDs
- [ ] Pluralization uses ICU MessageFormat; no concatenation
- [ ] Locale detection documented; SSR matches client locale (no flash)
- [ ] Only the request's locale messages ship to the client (no all-locales bundle); locale is
      request-scoped, not a module global
- [ ] Dates/numbers/currencies via Intl APIs; correct in LTR + RTL
- [ ] CSS uses logical properties; layout survives 140% text expansion
- [ ] App tested in at least one RTL locale; no overflow, overlap, or missing translations

**Red flags:** `if (count === 1) "item" else "items"`; string concatenation to build sentences;
hand-built date formatting (`day + "/" + month`); `margin-left` in a layout that needs RTL;
fixed-width containers with text; positional placeholders; splitting a string around an inline link;
assuming `Accept-Language` is the right detection (users override); rendering a default locale
server-side then correcting on the client; a module-level `currentLocale` variable under concurrent
requests; `import messages from './messages'` where the index re-exports every locale (ships all
locales to every client).

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (surface assumptions, surgical scope, verify don't assume)
- [references/i18n-checklist.md](references/i18n-checklist.md) — locale-surface audit template, ICU syntax reference, RTL conversion checklist, locale-detection patterns, test-locale matrix
- [references/server-i18n.md](references/server-i18n.md) — RSC / App Router message loading, per-locale bundle splitting, request-scoped locale, hydration alignment
