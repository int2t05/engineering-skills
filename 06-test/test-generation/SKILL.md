---
name: test-generation
description: Use when asked to generate or write tests for a feature or bugfix. Language-agnostic, works with any test framework. Triggers on "generate tests", "create tests", "write tests for", "生成测试".
---

# Test Generation (Language-Agnostic)

Generate anti-pattern-free test code from PRD acceptance criteria and source
code. Read inputs, produce test files. No execution, no reports, no source
modifications.

**Input:** PRD acceptance criteria + architecture docs + source code
**Output:** Complete test files (unit + integration)

## When to use

- Generating tests for a feature or bugfix
- Creating tests from a PRD, API contract, or existing source
- Triggers on "generate tests", "create tests", "write tests for", "生成测试"

## Steps

### 1. Detect language & framework

Scan the project before generating. Detection priority: existing test files
(naming conventions) → dependency manifests → test config files. If nothing
found, ask which framework to use.

| Language | Check For | Common Frameworks |
|----------|-----------|-------------------|
| Go | `go.mod`, `*_test.go` | testing (stdlib), testify, ginkgo |
| Python | `pyproject.toml`, `pytest.ini`, `conftest.py` | pytest, unittest |
| Java/Kotlin | `pom.xml`, `build.gradle`, `*Test.java` | JUnit 5, TestNG, AssertJ, Mockito |
| Rust | `Cargo.toml` ([dev-dependencies]), `tests/` | test (built-in), rstest |
| C#/.NET | `*.csproj`, `*Tests.cs` | xUnit, NUnit, FluentAssertions |
| TS/JS | `package.json`, `jest.config.*`, `vitest.config.*` | Vitest, Jest |
| Ruby | `Gemfile`, `*_spec.rb`, `spec/` | RSpec, Minitest |
| PHP | `composer.json`, `phpunit.xml` | PHPUnit, Pest |
| C/C++ | `CMakeLists.txt`, `*_test.cpp` | GoogleTest, Catch2 |
| Swift | `Package.swift`, `*Tests.swift` | XCTest, Quick/Nimble |

### 2. Read inputs

Ask for or discover: PRD path (default `tasks/prd-*.md`), architecture docs
(default `docs/architecture/`), source code to test (default `src/`), and the
auto-detected language/framework. Ask only critical questions before proceeding.

### 3. Extract testable conditions

- Per acceptance criterion → one or more test cases
- Per API endpoint / function signature → contract tests
- Per defined error state → error path test
- Per security-sensitive input → injection test (SQL, command, path traversal, XSS)

```
PRD: "US-001: User login"
AC: "Valid credentials return an authenticated session"
AC: "Invalid credentials return an error"
AC: "Empty fields show validation errors"

→ Test cases:
  1. valid credentials → success + session established
  2. wrong password → error response + message present
  3. empty email → validation error for email field
  4. empty password → validation error for password field
```

### 4. Generate test files

Write anti-pattern-free test code to the correct test directories. Every file
starts with a comment linking to requirements:

```
// Generated from: tasks/prd-auth.md, US-001: User login
// Acceptance criteria: valid login, invalid credentials, empty fields
```

Adapt the comment syntax to the language (`#`, `//`, `/* */`, `--`).

## Coverage rules

Every generated test file covers these dimensions:

| Category | What to test | Anti-pattern to avoid |
|----------|-------------|----------------------|
| **Happy path** | Expected input → expected output | Don't mock the function under test |
| **Validation** | Invalid/missing fields → proper errors | Assert real error, not mock call |
| **Edge cases** | Boundary values, empty, null, very large | Don't mock out validation logic |
| **Error states** | Timeout, unavailable, 5xx | Mock at network/IO level, not error handler |
| **Security** | Injection patterns, auth bypass | Test real sanitization, not mock sanitizer |

### Mocking rules

**Mock only at external boundaries:** network, filesystem, clock, third-party
APIs. **Never mock:**

- The function/class under test itself
- Internal helpers that are fast and side-effect-free
- When mock setup would exceed 50% of the test body (use an integration test)
- When unsure of the dependency chain (run with real implementation first)

**Completeness rule:** when mocking an API response or data structure, include
ALL fields the real implementation returns — not just the fields the immediate
test touches. Partial mocks hide structural assumptions and fail silently.

## Integration tests are not optional

Always generate integration tests alongside unit tests for features that span
multiple components. Integration tests:

- Use fewer (or zero) mocks — wire real components together
- Verify the system behaves correctly end-to-end
- Use language-idiomatic file naming

```
Source: src/auth/login.go
  → Unit: src/auth/login_test.go
  → Integration: tests/integration/auth_login_test.go
```

## Generator decision matrix

| Input has | Generate |
|-----------|----------|
| User story + AC | Unit tests per AC + integration test for the story |
| API contract + schema | Contract / integration tests per endpoint |
| Source code without AC | Unit tests for public API surface |
| Error states in contract | Error path tests covering every defined error |
| Security-sensitive inputs | Injection tests (SQL, command, path traversal, XSS) |
| Database operations | Transaction/rollback tests |
| Auth-protected endpoints | Unauthenticated + forbidden tests |

## Verify

- [ ] Language and framework auto-detected (not defaulted blindly)
- [ ] Every acceptance criterion has a matching test case
- [ ] Happy path, validation, edge cases, and error states covered per feature
- [ ] Both unit AND integration tests generated for multi-component features
- [ ] Mocks mirror the complete real data structure — no partial mocks
- [ ] Every test file has a source comment linking to requirements
- [ ] No test-only methods added to production classes
- [ ] No assertions solely on mock behavior or call counts

## References

- [../../references/engineering-principles.md](../../references/engineering-principles.md) — discipline every skill shares
- [../../references/clean-code.md](../../references/clean-code.md) — clean code principles for test quality
