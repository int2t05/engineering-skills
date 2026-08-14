# Server-side i18n (RSC / App Router)

Depth reference for the `i18n` skill. How message loading, bundle splitting, and request-scoped
locale work in React Server Components and the Next.js App Router — and the principles that apply
to any RSC-style framework (Remix, TanStack Start, Astro).

The core shift from SPA i18n: messages are loaded on the server per request, not bundled once on
the client. This turns locale from a global singleton into a per-request value, and lets
server-only messages stay out of the client bundle entirely.

## Contents

- [1. Principles](#1-principles)
- [2. Per-locale bundle splitting](#2-per-locale-bundle-splitting)
- [3. Request-scoped locale](#3-request-scoped-locale)
- [4. Hydration alignment](#4-hydration-alignment)
- [5. Server-only messages stay out of the client bundle](#5-server-only-messages-stay-out-of-the-client-bundle)
- [6. Next.js App Router example](#6-nextjs-app-router-example)

## 1. Principles

Framework-agnostic rules that hold across any RSC framework:

- **Load only the request's locale.** Never ship every locale's messages to the client. A 10-locale
  app bundling all messages ships 10x the JSON it needs per request.
- **Locale is per-request, not global.** A server handling concurrent requests for different
  locales cannot store the active locale in a module-level variable — request A's locale would
  leak into request B. Use the framework's request-scoped context (AsyncLocalStorage, React
  `cache()`, or the i18n library's request-scoped API).
- **Server and client must render the same locale.** The locale the server renders in must be the
  locale the client hydrates with. Any divergence is a hydration mismatch.
- **Server-only messages never reach the client.** Messages used only in Server Components (admin
  labels, server-side email/SMS templates, server-generated error text) should not be in the
  client message bundle — the client never renders them.

## 2. Per-locale bundle splitting

Each locale's messages live in their own JSON file, loaded on demand:

```
messages/
  en.json
  ar.json
  de.json
  ...
```

Load the request's locale with a dynamic import so the bundler splits each locale into its own
chunk:

```js
// Server-side: load the single locale this request needs
async function loadMessages(locale) {
  const mod = await import(`./messages/${locale}.json`);
  return mod.default;
}
```

The bundler creates one chunk per locale. A request for `ar` loads only `ar.json`; `en.json` and
`de.json` never ship. Contrast with the SPA anti-pattern: `import messages from './messages'`
where an index file re-exports all locales, forcing every locale into the client bundle.

## 3. Request-scoped locale

The active locale is a property of the request, not the process. The pattern:

1. A request arrives for `/ar/about`
2. The server extracts `ar` from the route
3. The server sets `ar` as the request-scoped locale (via the framework's context primitive)
4. All Server Components in that request read the locale from context — never from a global

**Next.js App Router:** `next-intl` and `next-i18next` expose `setRequestLocale(locale)` (called in
the root layout or at the top of `layout.tsx`) which binds the locale to the current request via
React's `cache()` / AsyncLocalStorage. Server Components call `getTranslations()` with no argument
— the locale is implicit, read from request context.

**Anti-pattern:** storing the locale in a module-level variable (`let currentLocale = 'en'`).
Under concurrent requests this is a data race — request A sets `ar`, request B sets `en`, and
request A renders `en`. The symptom is intermittent wrong-locale renders under load, which won't
show in single-request local testing.

## 4. Hydration alignment

Hydration mismatch occurs when the server-rendered HTML and the client's first render differ. For
i18n this means: the server renders in locale X, the client hydrates expecting locale Y, and React
warns (or in stricter modes, throws).

Rules:

- **Pass the locale and its messages to the client.** The server detects the locale and must pass
  both the locale identifier and the messages it used to the client bundle (via props, a script
  tag, or the framework's hydration data). The client does not re-detect.
- **The client uses the server-provided messages for the initial render.** After hydration, the
  client may lazy-load additional locales for client-side navigation — but the initial render must
  match.
- **No client-side locale detection before first paint.** Reading `navigator.language` on the
  client and switching locales before hydration guarantees a mismatch. Detection happens on the
  server (from URL / cookie / Accept-Language) and is passed down.

## 5. Server-only messages stay out of the client bundle

A key RSC advantage: messages used only in Server Components do not need to be in the client
message bundle at all.

- Server Components read messages directly from the server-loaded JSON — no client involvement.
- Messages for server-only surfaces (admin panel labels rendered on the server, server-generated
  email/SMS templates, server-side error logging) stay server-side.
- The client bundle contains only the messages the client actually renders (interactive components,
  client-side error states, dynamic UI).

This is impossible in a pure SPA (everything is client). In RSC it is automatic when the message
provider is server-side: the server loads the full message set, renders Server Components with it,
and passes only the client-needed subset to the client provider.

## 6. Next.js App Router example

Next.js is the canonical RSC framework; the pattern below uses `next-intl` (the most widely adopted
App Router i18n library). The structure generalizes — Remix, TanStack Start, and Astro follow the
same request-scoped shape with their own primitives.

```
app/
  [locale]/
    layout.tsx     # setRequestLocale(locale); wrap children in NextIntlClientProvider
    page.tsx       # Server Component — useTranslations() reads from request context
  i18n/
    routing.ts     # locale routing config (pathnames, default locale)
    request.ts     # getRequestConfig() — loads the request's messages
```

**`app/[locale]/layout.tsx`** — bind the locale to the request, pass messages to the client:

```tsx
import { setRequestLocale, getMessages } from 'next-intl/server';
import { NextIntlClientProvider } from 'next-intl';

export default async function LocaleLayout({ children, params }) {
  const { locale } = await params;
  setRequestLocale(locale);                  // request-scoped, not global
  const messages = await getMessages();      // loads only messages/{locale}.json
  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
```

**`app/i18n/request.ts`** — load only the request's locale:

```ts
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`../../messages/${locale}.json`)).default
}));
```

The dynamic import is the bundle split: each locale is its own chunk. `getRequestConfig` runs
per-request; `setRequestLocale` makes the locale available to `getMessages()` /
`useTranslations()` in any Server Component in the same request without passing it as a prop.

**What stays out of the client bundle:** any message used only in a Server Component
(`app/[locale]/page.tsx` calling `useTranslations('admin.dashboard')` where the dashboard is
server-rendered) is resolved on the server and never serialized into the client provider. Only the
messages the client tree actually needs are passed via `NextIntlClientProvider`.
