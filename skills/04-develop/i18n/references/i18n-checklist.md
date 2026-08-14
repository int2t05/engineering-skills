# i18n Checklist

Depth reference for the `i18n` skill. Locale-surface audit template, ICU syntax reference, RTL
conversion checklist, locale-detection patterns, and the test-locale matrix.

## Contents

- [1. Locale-surface audit template](#1-locale-surface-audit-template)
- [2. ICU MessageFormat syntax reference](#2-icu-messageformat-syntax-reference)
- [3. RTL conversion checklist](#3-rtl-conversion-checklist)
- [4. Locale-detection patterns](#4-locale-detection-patterns)
- [5. Test-locale matrix](#5-test-locale-matrix)

## 1. Locale-surface audit template

Before writing code, find every locale-sensitive surface. Run this audit:

### User-facing strings
- [ ] UI labels (buttons, headers, menu items, tooltips)
- [ ] Form labels and placeholder text
- [ ] Error messages (validation, server errors, empty states)
- [ ] Empty/loading states ("No results", "Loading...")
- [ ] Email / SMS / push notification templates
- [ ] Date/time display (absolute and relative: "2 hours ago")
- [ ] Number display (counts, percentages, measurements)
- [ ] Currency display
- [ ] Pluralized strings ("1 item" / "3 items")
- [ ] Gendered phrasing (if applicable to target locales)
- [ ] SEO strings (title, meta description, og: tags)

### Layout and formatting
- [ ] Date/time format (locale-specific ordering, calendar system)
- [ ] Number format (decimal separator, grouping, negative sign placement)
- [ ] Currency format (symbol position, symbol vs. code)
- [ ] First day of week (Sunday vs. Monday)
- [ ] Address format (order of fields varies by country)
- [ ] Phone number format
- [ ] Text direction (LTR / RTL)
- [ ] Text length expansion (translations are 30-50% longer than English)

### Code surfaces
- [ ] Hardcoded strings in components (grep for string literals in JSX/template)
- [ ] String concatenation to build sentences (`"Hello, " + name`)
- [ ] Plural logic (`if (count === 1)`)
- [ ] Date/number formatting via hand-built strings (not Intl)
- [ ] Fixed-width containers that can't flex with text length
- [ ] CSS directional properties (`margin-left` instead of `margin-inline-start`)
- [ ] Timezone handling (server assumes a timezone; stored without zone)

## 2. ICU MessageFormat syntax reference

ICU MessageFormat is the standard for grammar that varies across locales. Use it for anything
beyond simple interpolation.

### Simple interpolation
```
Hello, {name}.
```

### Pluralization (the 6 CLDR categories)
```
{count, plural,
  =0 {No items}
  one {# item}
  two {# items}
  few {# items}
  many {# items}
  other {# items}
}
```
English uses `one` and `other`. Arabic uses all six. Chinese uses only `other`. The `#` placeholder
renders the count with locale-appropriate digit formatting.

### Plural with offset (e.g. "you and N others")
```
{count, plural,
  =0 {No one liked this}
  =1 {You liked this}
  other {You and # others liked this}
}
```

### Select (gender / context-dependent)
```
{gender, select,
  male {He added a comment}
  female {She added a comment}
  other {They added a comment}
}
```

### Nested (plural inside select)
```
{hostGender, select,
  female {{guestCount, plural, =1 {She invited one guest} other {She invited # guests}}}
  male {{guestCount, plural, =1 {He invited one guest} other {He invited # guests}}}
  other {{guestCount, plural, =1 {They invited one guest} other {They invited # guests}}}
}
```

### Rich text (inline components)
Don't split a string around a link — translation breaks. Use rich-text placeholders:
```
Read our <link>privacy policy</link>.
```
The i18n library renders `<link>` as a component, keeping the sentence intact for translation.

## 3. RTL conversion checklist

When adding RTL support (Arabic, Hebrew, Persian, Urdu):

### HTML structure
- [ ] `<html dir="rtl" lang="ar">` set on the root (or per-route)
- [ ] `dir` attribute cascades to children; don't override unless a specific element must stay LTR
      (e.g. a code block, a phone number)

### CSS — use logical properties (not physical)
| Physical (LTR-only) | Logical (direction-aware) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `left: 0` (positioned) | `inset-inline-start: 0` |
| `border-left` | `border-inline-start` |

Logical properties automatically mirror in RTL. Physical properties don't — they break the layout.

### Directional assets
- [ ] Icons with direction (arrows, chevrons, "back" button) — mirror them, or use a library
      that auto-flips in RTL
- [ ] Progress bars / sliders — fill direction reverses
- [ ] Breadcrumbs — order reverses
- [ ] Avatar / content layout in lists (avatar on the start side)

### Layout that breaks in RTL
- [ ] Fixed-width containers with text (RTL text is often shorter; but truncation logic must use
      `inline-start` ellipsis, not `left`)
- [ ] Flexbox / grid order — `flex-direction: row` auto-mirrors in RTL with logical properties;
      explicit `order` values may need review
- [ ] Absolute positioning with physical values (`left: 20px`) — use `inset-inline-start`

### Testing RTL
- [ ] Run the app in an RTL locale (Arabic or Hebrew) — not by eyeballing in LTR
- [ ] Check: text alignment, icon direction, layout mirroring, no overflow
- [ ] Check: forms (label position, input direction for LTR data like email in an RTL page)
- [ ] Check: numbers and dates still render correctly (they stay LTR within RTL text)

## 4. Locale-detection patterns

The order in which locale is detected, and where it's persisted:

```
1. Explicit user preference (account setting) — highest priority, user chose it
2. URL path or query (/en/..., ?lang=fr) — shareable, SEO-friendly
3. Cookie (last chosen locale) — persists across visits for logged-out users
4. Accept-Language header — browser default, a hint not a command
5. Geo (with extreme caution) — geo ≠ language (a user in Japan may want English)
6. Default locale (fallback) — the source language or the primary market's language
```

### Routing strategies

| Strategy | Example | Best for |
|---|---|---|
| Path-prefixed | `/en/about`, `/ar/about` | Public content; SEO and shareability matter |
| Subdomain | `en.example.com`, `ar.example.com` | Large localized sites; separate caching per locale |
| Path-less (client detection) | `example.com/about` + cookie | App-only (not public content); simpler but not shareable |

### SSR / hydration

The server must render in the detected locale. If the server renders a default locale and the
client corrects on hydration, users see a flash of the wrong language (hydration mismatch):

- Detect locale on the server (from URL path, cookie, or Accept-Language)
- Render the correct locale server-side
- The client hydration must match — pass the detected locale to the client bundle
- For RSC / App Router message loading, per-locale bundle splitting, and the `setRequestLocale`
  pattern, see [server-i18n.md](server-i18n.md).

## 5. Test-locale matrix

Test in locales that surface different challenges:

| Locale | Script | Direction | Plural rules | What it tests |
|---|---|---|---|---|
| `en` (English) | Latin | LTR | one/other | Baseline; your source language |
| `de` (German) | Latin | LTR | one/other | Text expansion (30-50% longer than English) |
| `ar` (Arabic) | Arabic | RTL | all 6 categories | RTL layout, full plural set, right-to-left rendering |
| `zh` (Chinese) | Han | LTR | other only | No plural distinction; shorter text; CJK line-breaking |
| `ja` (Japanese) | Han/Kana | LTR | other only | CJK; locale-specific date/calendar (era-based) |
| `ru` (Russian) | Cyrillic | LTR | one/few/many/other | 4 plural categories; Cyrillic charset |

Minimum: test in `en` + one RTL (`ar`) + one with different plural rules (`ru`). This catches
the majority of i18n bugs.

### E2E parameterized by locale

Where feasible, run E2E tests parameterized by locale:

```
locales = ['en', 'ar', 'ru']
for locale in locales:
  test('checkout flow renders in ' + locale, () => {
    setLocale(locale)
    expect(checkoutButton).toHaveText(translatedString(locale, 'checkout'))
  })
```

This catches: missing translations (rendered as IDs or fallback), layout overflow in RTL, and
plural-form errors — automatically, across every locale.
