---
name: tdd
description: Use when implementing any feature or bugfix, before writing implementation code. Red-green-refactor loop, one vertical slice at a time. Triggers on "tdd", "test-driven", "red green refactor".
---

# Test-Driven Development

Write the failing test first. Watch it fail. Write minimal code to pass. Refactor.
A test that passes immediately proves nothing — you never saw it catch a bug.

**Iron law:** No production code without a failing test first. If you wrote code
before the test, delete it and start over. "Keep as reference" is testing-after
in disguise — delete means delete.

## When to use

- Implementing any new feature or behavior
- Fixing a bug (reproduce it with a test first — the Prove-It Pattern)
- Refactoring or changing existing behavior
- Triggers on "tdd", "测试驱动开发", "red green refactor", "红绿重构"

**Exceptions (confirm with the user):** throwaway prototypes, generated code,
pure configuration changes with no behavioral impact.

## Steps

### 0. Discover the stack first

The cycle is universal; the commands are not. Before the first test, find how
*this* repo tests: read `package.json` / `pyproject.toml` / `Cargo.toml` /
`pom.xml` / `go.mod`, check for `./gradlew`, `Makefile`, CI workflows, and
existing test-file naming. Never assume `npm test` — use the repo's own command
for every RED, GREEN, and final verification.

### 1. RED — write one failing test

One behavior, one test, one **vertical slice** (tracer bullet that responds to
what the last cycle taught you). Write the test you wish existed — it describes
the desired API, not the implementation. Name it as a specification
("rejects empty email", not "test1").

Agree the **seam** (public interface under test) before writing. No test at an
unconfirmed seam. Use real code over mocks unless the dependency is a slow
external boundary; mocks are a means to isolate, not the thing being tested.

### 2. Verify RED — watch it fail

Run the focused test command. Confirm:

- It **fails** (not errors — errors mean fix the setup and re-run)
- It fails for the **right reason** (feature missing, not a typo)
- A test that passes immediately means you're testing existing behavior — fix
  the test

### 3. GREEN — write minimal code

The simplest code that passes the test. No speculative features, no
"flexibility", no refactoring adjacent code. YAGNI. Don't add test-only methods
(`destroy()`, `reset()`) to production classes — put cleanup in test utilities.

### 4. Verify GREEN — watch it pass

Run the focused test command, then the full suite. Confirm:

- The new test passes
- No other tests broke (if they did, fix now — don't skip)
- Output is pristine (no warnings, no skipped tests)

### 5. REFACTOR — clean up

Only while green: extract helpers, improve names, remove duplication. Run
tests after every refactor step. Don't add behavior. Refactoring belongs to the
review stage, not the red → green implementation cycle.

### 6. Commit

Commit the test and implementation together as one vertical slice. Then start
the next failing test.

### Bug fixes — the Prove-It Pattern

Don't start by fixing. Write a test that reproduces the bug (RED confirms it
exists), then fix (GREEN proves the fix works). The test stays as a regression
guard. Never fix a bug without a reproduction test.

## Verify

- [ ] Every new behavior has a test that failed first
- [ ] Full suite passes with the repo's own test command
- [ ] Bug fixes include a reproduction test that failed before the fix
- [ ] Test names describe behavior, not implementation
- [ ] No tests skipped or disabled; no test-only methods in production code

## References

- [../../references/engineering-principles.md](../../references/engineering-principles.md) — discipline every skill shares
- [references/testing-anti-patterns.md](references/testing-anti-patterns.md) — mock misuse, test-only methods, partial mocks, gate functions
- [references/mocking.md](references/mocking.md) — when to mock, designing for mockability
- [references/good-tests.md](references/good-tests.md) — good vs bad test examples, tautological tests
