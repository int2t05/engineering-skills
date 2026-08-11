# Log Triage

Sub-guide for the `debugging` skill. Use when the goal is reading error output
or logs to understand what happened — before (or without) building a full
reproduction loop. Not every log needs reproduction; some just need reading.

## When to use this sub-guide

- "Read this error log and tell me what happened."
- "What does this error mean?"
- "The deploy failed — here's the output, what went wrong?"
- Triage of a stack trace, a CI failure log, or a container crash output.

## When NOT to use

- You already have a reproducing command → skip triage, go straight to the
  main `debugging` red-loop.
- The system is slow, not failing → `performance`.
- You need to add instrumentation to see what's happening → `observability`.

## Steps

1. **Read the full error, top to bottom, once.** Don't fixate on the first
   red line — the root cause is often a line above it or at the bottom of a
   stack trace. Note the timestamp, the failing component, and the exact
   error message verbatim.
2. **Identify the error class.** Common classes:
   - **Startup/config** — missing env var, bad port, unreadable file. Fixable
     in config, no code change.
   - **Dependency/version** — module not found, incompatible API. Points at
     `deprecation-migration` or a missing install.
   - **Logic/runtime** — null reference, type error, unhandled exception.
     Points at a code path needing the full debugging loop.
   - **Resource** — OOM, disk full, connection refused. Points at
     infrastructure, not code.
   - **Permission/auth** — 401/403, expired token. Points at auth config.
3. **Trace the stack to your code.** Framework internals are noise; the first
   frame inside your codebase is the entry point. Note its file:line.
4. **Form a one-sentence hypothesis.** "X failed because Y happened at Z."
   If you can't form one, you don't have enough — gather more log context
   before guessing.
5. **Decide: fix now, or escalate to the full loop.**
   - Startup/config/resource/permission errors → often fixable directly from
     the log. Fix, redeploy, verify the log is clean.
   - Logic/runtime errors → escalate to the main `debugging` skill: build a
     reproducing command, then red-green to root cause.

## Reading craft

- **Timestamps reveal causality.** If service A errors at 12:03:01 and
  service B's log shows a restart at 12:03:00, B caused A.
- **First occurrence vs recurring.** `grep` for the error string across the
  log history — a brand-new error correlates with a recent change; a
  long-standing one is environmental.
- **Surrounding context.** Read 20 lines before and after the error. The
  log entry that explains it is rarely the error line itself.
- **Multiple errors.** Usually one is the cause and the rest are cascading
  failures. Find the earliest one.

## When to escalate to the full debugging loop

- The log points at a logic/runtime bug you can't confirm from output alone.
- You need to reproduce to be sure of the fix.
- The error is intermittent and the log doesn't show the triggering input.

In those cases, hand off to the main `debugging` skill with the hypothesis
and the file:line you found — that's real progress, not a restart.

## Verify

- You can state the error class and a one-sentence hypothesis.
- The file:line in your codebase is identified (for logic errors).
- Either: the fix is applied and the log is clean on retry, OR: you've
  escalated to the full debugging loop with a concrete starting point.
