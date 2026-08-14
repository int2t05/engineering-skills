# Retry Patterns

Implementation reference for the `error-handling` skill — the math and code for
retry, backoff, circuit breakers, and idempotency. For the system-level strategy
(when to retry vs fail fast, error propagation across layers), see
`architecture/references/error-resilience.md`.

## Contents

- [1. Exponential backoff](#1-exponential-backoff)
- [2. Jitter strategies](#2-jitter-strategies)
- [3. Retry budget](#3-retry-budget)
- [4. Circuit breaker state machine](#4-circuit-breaker-state-machine)
- [5. Idempotency-key patterns](#5-idempotency-key-patterns)
- [6. Pseudocode: retry with backoff + jitter + circuit breaker](#6-pseudocode-retry-with-backoff--jitter--circuit-breaker)

## 1. Exponential backoff

Base delay doubles each attempt, capped at a maximum:

```
delay(n) = min(base * 2^n, cap)
```

- `base`: initial delay (e.g., 100ms)
- `cap`: maximum delay (e.g., 5000ms) — prevents absurd waits
- `n`: attempt number (0-indexed)

Example (base=100ms, cap=5s): 100ms, 200ms, 400ms, 800ms, 1600ms, 3200ms, 5000ms, 5000ms...

Without jitter, retries from multiple clients synchronize (thundering herd) — always add jitter (§2).

## 2. Jitter strategies

Jitter spreads retry attempts across time so clients don't stampede a recovering downstream. Three strategies, ranked by safety:

### Full jitter (default — safest)

Random delay uniformly distributed between 0 and the capped exponential value:

```
delay(n) = random(0, min(base * 2^n, cap))
```

Maximum spread; retries can't cluster. Use this unless you have a reason not to.

### Equal jitter

Half the delay is fixed, half is random — prevents very short retries while keeping spread:

```
temp = min(base * 2^n, cap)
delay(n) = temp/2 + random(0, temp/2)
```

### Decorrelated jitter

Next delay is a function of the previous delay, not the attempt count:

```
delay = random(base, prev_delay * 3)
```

Less synchronization across retry cycles; harder to reason about.

## 3. Retry budget

A retry budget caps total retry attempts across time, preventing retry storms from
amplifying a downstream outage. Two common implementations:

### Token bucket

- Bucket starts with N tokens (e.g., 10% of request rate).
- Each retry consumes a token; tokens refill at rate R.
- When the bucket is empty, fail fast instead of retrying.
- Effect: retries can never exceed N/R of total traffic — protects the downstream.

### Time window

- Track retry attempts in a rolling window (e.g., 60s).
- If retries exceed a threshold (e.g., 30% of requests), stop retrying for the window.
- Simpler to implement; less precise than token bucket.

A retry budget is the complement to the circuit breaker: the circuit breaker protects
during sustained outages; the budget protects during partial degradation.

## 4. Circuit breaker state machine

Three states with defined transitions:

```
                  failures >= threshold
    CLOSED  ──────────────────────────►  OPEN
      ▲                                    │
      │  probe success                      │ cooldown elapsed
      │                                    ▼
      └────────────────────────────  HALF_OPEN
                                    │  │
                    probe failure   │  │ probe success
                      ▼             │  │
                    OPEN ◄──────────┘  │
                                      │
                                      │ (close circuit)
```

- **Closed:** requests flow normally. Count failures in a rolling window.
- **Open:** requests fail fast immediately — no call to the downstream. Cooldown period (fixed or exponential) must elapse before transitioning to half-open.
- **Half-open:** allow one (or a small number of) probe request(s) through. Success → close the circuit (reset failure count). Failure → re-open the circuit (reset cooldown).

Parameters to set:

- **Failure threshold:** consecutive failures (e.g., 5) or failure rate over a window (e.g., 50% over 30s). Rate-based is more robust to traffic bursts.
- **Cooldown:** fixed (e.g., 30s) or exponential (doubles each re-open). Exponential backs off a persistently failing downstream.
- **Half-open probes:** 1 is the safe default. More probes recover faster but risk re-opening under partial recovery.

## 5. Idempotency-key patterns

Retries and network ambiguity (did the request reach the server? did the response get lost?) make duplicate requests inevitable. Idempotency ensures a duplicate is safe.

### Client-generated key

- Client generates a unique key (UUID) per logical operation, sends it in a header (`Idempotency-Key: <uuid>`).
- Server stores the key + response for a TTL (e.g., 24h).
- On duplicate key: server returns the stored response, does not re-execute the side effect.

### Natural-key deduplication

- For operations with a natural unique identifier (e.g., order ID), use it as the dedup key.
- Server checks existence before creating: `SELECT ... WHERE order_id = ?` → if exists, return existing.

### PUT is naturally idempotent

- `PUT /resource/{id}` with the same body produces the same state after repeated applies — no dedup needed.
- Exploit PUT for updates; avoid POST for idempotent operations when possible.

### Background jobs

- Dedupe by job ID before enqueuing: `if not exists(job_id): enqueue(job)`.
- A retried enqueue should not create a second job.

## 6. Pseudocode: retry with backoff + jitter + circuit breaker

```python
def call_with_resilience(operation, circuit_breaker, max_attempts=3, base_delay=0.1, cap_delay=5.0):
    if circuit_breaker.is_open():
        raise CircuitOpenError("circuit breaker is open")

    last_error = None
    for attempt in range(max_attempts):
        try:
            result = operation()
            circuit_breaker.record_success()
            return result
        except TransientError as e:
            last_error = e
            circuit_breaker.record_failure()
            if circuit_breaker.is_open():
                raise CircuitOpenError("circuit opened during retry") from e
            if attempt < max_attempts - 1:
                delay = full_jitter(base_delay, cap_delay, attempt)
                sleep(delay)
        except PermanentError as e:
            raise  # permanent errors are not retried

    raise last_error  # exhausted retries


def full_jitter(base, cap, attempt):
    capped = min(base * (2 ** attempt), cap)
    return random.uniform(0, capped)
```

Key points:

- Transient errors trigger retry; permanent errors fail immediately.
- Circuit breaker is checked before the call and updated after — an open circuit short-circuits retries.
- Last error is raised after exhausting attempts, preserving the original cause.
