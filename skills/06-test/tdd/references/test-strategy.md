# Test Strategy

Load this reference when deciding what kind of test to write and where to put testing effort.

## The Test Pyramid

Invest testing effort according to the pyramid — most tests small and fast, progressively fewer
at higher levels:

- **Unit (~80%)** — pure logic, isolated, milliseconds each
- **Integration (~15%)** — component interactions, API boundaries
- **E2E (~5%)** — full user flows, real browser; limit to critical paths

### Test sizes (resource model)

| Size | Constraints | Speed | Example |
|------|------------|-------|---------|
| **Small** | Single process, no I/O, no network, no database | Milliseconds | Pure function tests, data transforms |
| **Medium** | Multi-process OK, localhost only, no external services | Seconds | API tests with test DB, component tests |
| **Large** | Multi-machine OK, external services allowed | Minutes | E2E tests, performance benchmarks, staging integration |

Small tests should make up the vast majority of your suite — they're fast, reliable, and easy to
debug when they fail.

### Decision guide

- Pure logic with no side effects → unit test (small)
- Crosses a boundary (API, database, file system) → integration test (medium)
- Critical user flow that must work end-to-end → E2E test (large), limited to critical paths

## Test-double preference hierarchy

Use the simplest test double that gets the job done. The more your tests use real code, the more
confidence they provide.

1. **Real implementation** — highest confidence, catches real bugs
2. **Fake** — in-memory version of a dependency (e.g., fake DB)
3. **Stub** — returns canned data, no behavior
4. **Mock (interaction)** — verifies method calls; use sparingly

Use mocks only when the real implementation is too slow, non-deterministic, or has side effects you
can't control (external APIs, email sending). Over-mocking creates tests that pass while production
breaks.

## DAMP over DRY in tests

In production code, DRY (Don't Repeat Yourself) is usually right. In tests, **DAMP (Descriptive And
Meaningful Phrases)** is better. A test should read like a specification — each test tells a complete
story without requiring the reader to trace through shared helpers. Duplication in tests is acceptable
when it makes each test independently understandable.
