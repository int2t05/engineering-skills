---
name: error-handling
description: Use when designing error-handling strategy for a feature — error classification, throw-vs-return conventions, retry/circuit-breaker/fallback decisions, and error-to-user-message mapping. Triggers on "error handling", "retry strategy", "circuit breaker", "error propagation", "错误处理", "重试策略", "熔断", "降级" — also when user says "这个错误该怎么处理" / "要不要重试". Not for diagnosing a specific bug (use debugging); system-level resilience architecture (use architecture).
---

## When to use

- Designing how errors propagate across layers for a new feature or service boundary
- Choosing retry, circuit-breaker, or fallback strategy for calls to external systems
- Establishing throw-vs-return conventions for a module or codebase
- Mapping internal errors to user-facing messages at an edge boundary

**Not for:** diagnosing a specific bug or test failure (use `debugging`); system-level resilience architecture — cross-service error strategy, overall failure posture (use `architecture`, specifically `architecture/references/error-resilience.md`); API error response envelope shape (use `api-design`); production logging/metrics instrumentation (use `observability`).

## Steps

For system-level resilience architecture (cross-service error propagation, failure posture design), read [architecture's error-resilience reference](${CLAUDE_PLUGIN_ROOT}/skills/03-design/architecture/references/error-resilience.md) first. This skill is the implementation-level companion — the decisions you make at the keyboard when writing the error-handling code.

### 1. Classify errors

Every error falls into one of four categories, and the category drives the strategy:

| Category | Examples | Strategy |
|---|---|---|
| **Transient** | network timeout, 503, connection reset | retry with backoff (step 3) |
| **Permanent** | 404, 400, logic failure | fail fast, no retry |
| **Validation** | bad input, schema mismatch | return 422-style result to caller |
| **Auth** | expired token, insufficient scope | return 401/403, prompt re-auth |

If you can't classify an error, default to permanent — retrying an unclassified error masks real bugs.

### 2. Choose throw-vs-return convention

Pick one convention per layer and enforce it (architecture ref §1 has the full rationale):

- **Throw (exceptions)** for invariant violations and infrastructure failures — "this should never happen, the operation cannot continue." Catch at boundaries, not at every call.
- **Return (Result/error values)** for expected, recoverable failures the caller must branch on — not-found, conflict, validation. A 404 is a result, not an exception.

Follow the language ecosystem's dominant convention: Rust/Go return error values; Python/Java/JS throw. Fighting the ecosystem creates inconsistent code.

### 3. Design retry strategy (transient errors only)

Retry only transient errors. Retrying permanent errors wastes resources and can amplify failures. See [references/retry-patterns.md](references/retry-patterns.md) for formulas and code.

- **Exponential backoff + jitter:** base × 2^n, capped, with jitter to prevent retry stampedes. Full jitter (random between 0 and the capped value) is the safe default.
- **Max attempts:** 3 covers most transient blips. More than 5 rarely helps and delays failure.
- **Idempotency:** retry only idempotent operations (GET, PUT, DELETE with stable IDs). For POST, require an idempotency key so a retry after an ambiguous timeout doesn't double-charge or double-create.
- **Timeout on every call.** A call without a timeout can hang forever and hold resources.

### 4. Add circuit breaker when retry is not enough

Retry handles isolated transient failures. A circuit breaker protects a struggling downstream from retry storms during a sustained outage.

- **States:** closed (normal) → open (fail fast, no calls) → half-open (probe one request to test recovery).
- **Open threshold:** N consecutive failures or a failure-rate threshold (e.g., 50% over a rolling window).
- **Cooldown:** fixed time or exponential reset. Half-open probes one request; success closes, failure re-opens.
- **Use when:** a downstream dependency has repeated sustained outages and retries would make things worse. Don't add a circuit breaker for a call that rarely fails.

### 5. Plan graceful degradation

When a dependency fails, decide what the user gets instead:

- **Critical path** (payment, auth, core data): fail the request — no degradation.
- **Non-critical path** (recommendations, search, analytics): catch the failure, serve a fallback (cached data, empty state, default) — the core page still renders.
- **Feature-flag kill switch:** for integration failures that recur, a flag to disable the feature path instantly beats debugging under load.

### 6. Map errors to user-facing messages (at the edge)

Maintain a single mapping from stable error codes to user-facing messages, at the edge boundary (architecture ref §3):

- **Stable error codes** (`PAYMENT_DECLINED`, `RATE_LIMITED`), not free text. The code is the cross-service contract.
- **Generic external, specific internal:** never expose SQL fragments, stack traces, or internal hostnames to users. Map to "Could not complete this action" + a correlation ID for support.
- **Actionable:** tell the user what to do ("Check your payment details and try again").

### 7. Log with structured context

Log every error with enough context to reproduce the diagnosis without re-running:

- Structured fields: error code, operation, correlation ID, request context.
- No secrets: redact tokens, passwords, PII before logging (see `debugging` skill's redaction discipline).
- Log at the boundary where the error is handled, not at every catch site — duplicated logs obscure the real failure path.

## Verify

- [ ] Every error in the new code is classified (transient / permanent / validation / auth) — strategy follows classification
- [ ] Throw-vs-return convention is consistent within each layer; no exceptions used for expected control flow
- [ ] Retry only fires on transient, idempotent operations; max attempts and backoff are set
- [ ] Circuit breaker (if used) has defined thresholds, cooldown, and half-open probe logic
- [ ] Non-critical dependency failures degrade gracefully (fallback/empty state), not cascade to a full page failure
- [ ] User-facing errors use stable codes + generic messages; no internal details leak
- [ ] Errors are logged with structured context and a correlation ID; no secrets in log output
- [ ] Tests cover: retry on transient, no-retry on permanent, circuit-breaker open/half-open/closed transitions, fallback path

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline shared by every skill
- [${CLAUDE_PLUGIN_ROOT}/skills/03-design/architecture/references/error-resilience.md](${CLAUDE_PLUGIN_ROOT}/skills/03-design/architecture/references/error-resilience.md) — system-level resilience architecture (cross-layer error propagation, failure posture); this skill is its implementation-level companion
- [references/retry-patterns.md](references/retry-patterns.md) — backoff/jitter formulas, circuit breaker state machine, idempotency-key patterns, retry budgets (with code)
