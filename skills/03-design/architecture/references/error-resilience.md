# Error Handling & Resilience Strategy

Cross-cutting strategy for how a system handles failure. `api-design` defines the error response
envelope; `observability` defines how errors are logged; `debugging` diagnoses one bug. This
reference owns the architecture between them — how errors propagate across layers, when to retry,
how to fail gracefully, and how internal errors become user-facing messages.

## 1. Throw vs. return — pick a convention and hold it

The most common source of error-handling confusion is mixing two models. Choose one per layer and
enforce it:

- **Throw (exceptions):** for invariant violations and unexpected failures — "this should never
  happen, and the current operation cannot continue." Catch at boundaries, not at every call.
- **Return (result/error values):** for expected, recoverable failures — "this input was invalid,
  this resource was not found, this conflict happened." The caller decides what to do.

Rule of thumb: throw for bugs and infrastructure failures; return for business-rule failures the
caller must branch on. Never use exceptions for control flow that the caller expects to handle
routinely (a 404 is not an exception, it's a result).

## 2. Error propagation across layers

Errors must not leak raw across architectural boundaries. A DB error reaching the HTTP handler
untranslated becomes a 500 with a SQL fragment — an information leak and an unhelpful response.

- **Data layer:** throw on infrastructure failure (connection lost); return `not_found` / `conflict`
  as typed results for business states.
- **Business/service layer:** catch infrastructure exceptions, log with context, rethrow or wrap as
  a typed domain error. Translate data-layer results into domain-meaningful outcomes.
- **API/edge layer:** map domain errors to HTTP status + a stable error code. Never expose internal
  messages, stack traces, or SQL.

Every layer has a contract: what it throws, what it returns, what it wraps. Document it.

## 3. Internal error → user-facing message mapping

Maintain a single mapping from stable error codes to user-facing messages, at the edge:

- **Stable error codes** (not free-text): `PAYMENT_DECLINED`, `RATE_LIMITED`, `RESOURCE_NOT_FOUND`.
  The code is the contract across services; the message is localized/display text.
- **Never pass internal messages to the user.** "Foreign key constraint failed" is a bug report,
  not a user message. Map to "Could not complete this action" + a correlation ID for support.
- **Include a correlation ID** in every user-facing error so support can trace it to the log entry.
- **Actionable messages:** tell the user what to do, not just what broke ("Check your payment
  details and try again" beats "Error 4002").

## 4. Retry, backoff, and circuit breakers

For calls to external systems (APIs, databases, message queues), failure is transient some of the
time. A retry policy turns transient failures into successes — but uncontrolled retries turn a slow
downstream into a cascading failure.

- **Retry with exponential backoff + jitter:** base × 2^n, capped, with random jitter so retries
  don't synchronize and stampede. 3 attempts covers most transient blips.
- **Only retry idempotent operations** (GET, PUT, DELETE with stable IDs). Retrying a non-idempotent
  POST on an ambiguous response (timeout before confirmation) causes duplicate side effects — see
  §5.
- **Circuit breaker:** after N consecutive failures, stop trying for a cooldown period. Prevents
  the retry storm from making a struggling downstream worse. States: closed (normal) → open
  (failing fast) → half-open (probe one request to test recovery).
- **Timeout on every call.** A call without a timeout is a call that can hang forever and hold
  resources. Set the timeout shorter than the caller's patience.

## 5. Idempotency under retry

Retries and network ambiguity (did the request reach the server? did the response get lost on the
way back?) make duplicate requests inevitable. Design mutations so a duplicate is safe:

- **Idempotency key** on mutations: client generates a unique key (UUID); server deduplicates —
  same key returns the original result, doesn't re-execute the side effect. Stripe's idempotency-key
  pattern is the canonical example.
- **PUT /resource/{id}** is naturally idempotent (same state after repeated applies); exploit that
  for updates.
- **POST without an idempotency key** is dangerous under retry: a timeout-then-retry can double-charge,
  double-create, double-send. Make POSTs idempotent via a client-generated key or a deduplication
  check on a natural key.
- **Background jobs:** dedupe by a job ID before enqueuing; a retried enqueue should not create a
  second job.

## 6. Fallback UX and graceful degradation

When a dependency fails, the system should degrade gracefully, not fail completely. A missing
recommendation widget should not break the product page.

- **Fail isolated, not cascading:** a non-critical dependency failure (recommendations, search,
  analytics) is caught and replaced with a fallback (cached data, empty state, default) — the core
  page still renders.
- **Critical vs. non-critical path:** know which dependencies are on the critical path (payment,
  auth, core data) vs. off it (recommendations, social proof). Critical failures fail the request;
  non-critical failures degrade.
- **Cache as fallback:** a stale cache is better than a blank page for read-heavy, non-financial
  data — serve stale-while-revalidate and refresh in the background.
- **Feature-flag kill switch:** for integration failures that recur, a flag to disable the feature
  path instantly beats a multi-hour debug session under load.

## 7. Error boundaries and containment

In frontend applications, an uncaught render error crashes the whole tree. Error boundaries contain
the blast radius:

- Wrap route-level or feature-level subtrees in error boundaries so a failure in one section
  (comments, sidebar) doesn't blank the page.
- Each boundary renders a meaningful fallback ("This section failed to load — retry") + logs the
  error with a correlation ID.
- In backend services, the equivalent is request-scoped error handling: one request's failure
  never crashes the process or poisons the next request. Fail the request, log it, keep serving.

## Anti-patterns

- **Swallowed exceptions:** `catch (e) { }` — the error disappears, the bug persists invisibly. If
  you catch, you log or you rethrow.
- **Generic catches at the wrong layer:** a top-level catch-all that turns every error into a 500
  with no context. Catch where you can act.
- **Retrying non-idempotent operations:** double-charges, duplicate records.
- **No timeout on outbound calls:** hung connections holding resources.
- **Leaking internal messages to users:** SQL fragments, stack traces, internal hostnames.
- **Retry without backoff/jitter:** synchronized retry stampedes overload the recovering downstream.
- **Cascading failure from a non-critical dependency:** the whole page dies because the
  recommendation widget threw.
- **Error codes as free text:** "Something went wrong" with no code — untraceable, unlocalizable.
