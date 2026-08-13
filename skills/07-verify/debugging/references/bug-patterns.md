# Bug Pattern Catalog

Reference for the `debugging` skill. A catalog of recurring bug shapes and the signals that point
to each — so a symptom routes to a hypothesis faster. Pair with the red-loop workflow in SKILL.md:
this narrows *what to suspect*, not *how to confirm* (confirm by reproducing).

## Concurrency / race conditions

**Signals:** intermittent, "works on retry", fails under load but not in single-user tests,
heisenbug (disappears under a debugger or extra logging), time- or order-dependent.

- **Check-now-use-later (TOCTOU):** code checks a condition, then acts on it; state changes between.
  - `if (user exists) { create }` → two requests race, both pass the check, duplicate created.
- **Shared mutable without a lock:** counter/accumulator updated from multiple goroutines/threads.
- **Lazy init not synchronized:** singleton initialized on first use; two threads both init.
- **Awaiting in a loop that assumes ordering:** `Promise.all` results land in input order, not finish order.

Confirm by: stress-test the exact path (N concurrent requests), add a deliberate delay between
check and use, log thread/coroutine id with each step.

## Null / None / undefined

**Signals:** `NullPointerException`, `AttributeError: 'NoneType'`, `TypeError: Cannot read
properties of undefined`, "works for some records, crashes for others".

- **Missing row / empty query result** used without a null check.
- **Optional field** the schema allows null but code assumes present.
- **Chain traversal** `a.b.c.d` where any link can be null.
- **Function returns null on edge case** caller didn't read the contract for.

Confirm by: log the value and type right before the crash, check the DB row that produced it.

## Off-by-one / boundary

**Signals:** correct for most inputs, wrong at 0, 1, max, or "first/last element"; pagination
off by one row; loop runs one too few/many times.

- `<` vs `<=` in loop bound or range end.
- Zero-indexed vs one-indexed confusion (page 1 → offset 0).
- Slice end exclusive: `arr[0:n]` has n elements, `arr[0:n-1]` has n-1.
- `size()` vs last-index (`arr[size()]` is out of bounds).

Confirm by: test exactly the boundary value (0, 1, n-1, n), print indices alongside values.

## State / staleness

**Signals:** "it worked before, now doesn't", "works after restart", depends on action order,
"works in fresh session, breaks in existing one".

- **Cached value not invalidated** when source changes.
- **Session/cart holds stale data** after the underlying record changed.
- **Migration ran in one env but not another** — schema drift.
- **Environment variable** set in dev, missing/defaulting in prod.

Confirm by: clear the cache / restart / fresh session and retry; diff env configs.

## Type / encoding

**Signals:** works locally (UTF-8), breaks in prod; mojibake; "comparison says equal but
they're not"; number formatted wrong by locale.

- **String encoding mismatch** (UTF-8 vs Latin-1 vs BOM).
- **Timezone-naive datetime** compared across zones — `2026-01-01 00:00` is different instants in UTC vs Asia.
- **Float equality** — `0.1 + 0.2 !== 0.3`; compare with epsilon, not `===`.
- **Locale formatting** — `1,234` is 1234 (en) or 1.234 (de).

Confirm by: log raw bytes / epoch millis / typeof, not the formatted display value.

## Error handling / control flow

**Signals:** exception swallowed, "no error but wrong result", silent failure.

- **Empty catch** — `catch (e) {}` hides the real cause.
- **Caught too broadly** — `except Exception` swallows the specific error you needed.
- **Error returned but caller didn't check** (Go `err` ignored, Result unused).
- **Fallback value masks failure** — `return default` on error looks like success.

Confirm by: re-throw or log every caught exception; remove the fallback temporarily.

## Resource / leak

**Signals:** "slows down over time", OOM after hours, "works N times then fails",
too many open files.

- **Connection not returned to pool** — missing close in error path.
- **File handle leak** — opened, exception before close.
- **Unbounded growth** — cache/map that never evicts, listener never removed.
- **Goroutine/thread leak** — spawned, never terminates.

Confirm by: monitor the resource (conn count, fd count, heap, goroutine count) over repeated runs.

## Log analysis checklist

When the entry point is a log line, not a repro:

1. **Read the full stack trace, bottom-up.** The bottom frame is where it died; the frames above
   are the call path. The error message names the immediate failure; the stack names the code path.
2. **Note the timestamp + request id.** Correlate lines that share an id — they're one request's
   lifecycle. A line at 14:03:01 and one at 14:03:15 with the same id show a 14-second gap (a stall).
3. **Find the first error, not the last.** Cascading failures bury the cause: the 50th error is a
   symptom of the 1st. Scroll to the earliest ERROR/WARN for that request id.
4. **Separate signal from noise.** Health-check failures, retry logs, and dependency timeouts often
   *follow* the real fault. Ask: "which line is the first to deviate from normal?"
5. **Match the error class to the catalog above.** A `Connection refused` after a deploy → state/
   staleness (service not up). A `null` on one record of thousands → null/None pattern. Intermittent
   under load → concurrency.
6. **Form one hypothesis, then reproduce.** The log tells you *what* and *where*; reproduce to prove
   *why*. Don't "fix" from the log alone — a log-derived patch is a guess with extra steps.
7. **If logs are insufficient, add instrumentation** — don't stare at partial logs. Log the values of
   the variables in the suspect path, redeploy/reproduce, read the new output.

## Anti-patterns

- **Shotgun debugging** — changing things at random until it "works". Every change must be a
  hypothesis test, not a lottery ticket.
- **Fixing the symptom** — catching the NPE instead of fixing why the value is null. The bug moves,
  it doesn't die.
- **"It works on my machine"** as a closing statement — that's the start of the investigation, not
  the end. What differs between the environments?
- **Debugging by addition** — adding try/catch, retries, `?.` chains to make the error go away.
  Each addition is a new place for bugs to hide. Remove them once the root cause is fixed.
