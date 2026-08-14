# Language Pattern Mapping

Same test patterns apply across languages. Generate tests that match the detected framework's
idioms — file layout, assertion style, fixtures, parametrization, async handling. Prefer **real
calls against real dependencies** (real database, real API, real filesystem) over mocks; mock only
a slow or third-party boundary you genuinely cannot stand up, and say why.

## Contents

- [Detection — what to scan for](#detection--what-to-scan-for)
- [Framework matrix](#framework-matrix)
- [Python — pytest](#python--pytest)
- [TS/JS — Vitest / Jest](#tsjs--vitest--jest)
- [Go — table-driven](#go--table-driven)
- [General Principles (Cross-Framework)](#general-principles-cross-framework)

## Detection — what to scan for

Detection priority: existing test files (naming conventions) → dependency manifests → test config files. If nothing found, ask which framework to use.

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

## Framework matrix

| Language | Test Framework | Runner | Assertion | Fixture/Param |
|----------|----------------|--------|-----------|---------------|
| Go | testing + testify | `go test` | `assert.Equal`, `require.NoError` | table-driven `tests := []struct` |
| Python | pytest | `pytest` | bare `assert`, `pytest.raises` | `@pytest.fixture`, `@pytest.mark.parametrize` |
| Java | JUnit 5 + AssertJ | mvn/gradle test | `assertThat().isEqualTo()` | `@ParameterizedTest`, `@BeforeEach` |
| Rust | test (built-in) | `cargo test` | `assert!`, `assert_eq!` | `#[test]`, helper fns, `rstest` crate |
| C# | xUnit + FluentAssertions | `dotnet test` | `result.Should().Be()` | `[Theory]`, `[InlineData]`, `IClassFixture` |
| TS/JS | Vitest / Jest | `vitest`/`jest` | `expect().toEqual()` | `describe/it`, `beforeEach`, `it.each` |
| Ruby | RSpec | `rspec` | `expect().to eq()` | `let`, `before`, shared contexts |
| PHP | PHPUnit | `phpunit` | `assertSame()` | `@dataProvider`, `setUp()` |

## Python — pytest

Real-data test against a test database; one assert per behavior; parametrize the boundaries.

```python
import pytest
from myapp.db import get_session
from myapp.models import User
from myapp.users import create_user

@pytest.fixture
def db():
    # Real test database, each test rolls back its own transaction — no mocks, no shared state
    session = get_session("postgresql://test:test@localhost/test_db")
    session.begin()
    yield session
    session.rollback()
    session.close()

@pytest.mark.parametrize("email, should_pass", [
    ("alice@example.com", True),
    ("not-an-email", False),
    ("", False),
    ("UPPER@EXAMPLE.COM", True),  # case normalization
])
def test_create_user_validation(db, email, should_pass):
    if should_pass:
        user = create_user(db, email=email)
        assert user.id is not None
        assert db.query(User).filter_by(email=email.lower()).one()
    else:
        with pytest.raises(ValueError):
            create_user(db, email=email)
```

- File naming: `test_<module>.py`, functions `test_<behavior>`.
- Use `@pytest.mark.parametrize` to cover boundaries; don't write 5 nearly identical tests.
- Assert exceptions with `pytest.raises(Error)`, not try/except + assert.
- For async, use `@pytest.mark.asyncio` + `await`.

## TS/JS — Vitest / Jest

```typescript
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { createServer } from "http";
import { apiClient } from "../src/client";

// Spin up a real local server instance, send real HTTP requests — don't mock fetch
describe("user API", () => {
  let server: ReturnType<typeof createServer>;
  let baseUrl: string;

  beforeEach(async () => {
    server = createServer({ port: 0, db: testDbUrl });  // random port, real server
    await new Promise<void>(r => server.listen(0, () => r()));
    baseUrl = `http://127.0.0.1:${(server.address() as any).port}`;
  });
  afterEach(() => new Promise<void>(r => server.close(() => r())));

  it.each([
    ["alice@example.com", 201],
    ["bad", 422],
  ])("POST /users with %s returns %i", async (email, status) => {
    const res = await apiClient(baseUrl).createUser({ email });
    expect(res.status).toBe(status);
  });
});
```

- `describe` groups, `it` individual cases — name them "subject + behavior".
- `it.each` for boundary parametrization.
- Avoid snapshot tests (`toMatchSnapshot`) for behavior assertions — they only lock strings, not correctness.

## Go — table-driven

```go
func TestCreateUser(t *testing.T) {
    db := testdb.Connect(t) // t.Cleanup auto-cleans, real DB
    tests := []struct {
        name      string
        email     string
        wantErr   bool
        wantEmail string // expected value after normalization
    }{
        {"valid", "alice@example.com", false, "alice@example.com"},
        {"empty", "", true, ""},
        {"invalid", "not-an-email", true, ""},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            user, err := CreateUser(db, tt.email)
            if tt.wantErr {
                require.Error(t, err)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.wantEmail, user.Email)
        })
    }
}
```

- Table-driven is the Go idiom: one `tests` slice + `t.Run` subtests.
- `testdb.Connect(t)` uses `t.Cleanup` to roll back, real connection.
- `require` stops on failure (preconditions), `assert` collects multiple failures.

## General Principles (Cross-Framework)

- **One test, one behavior** — when it fails, you see exactly what broke. Split multiple unrelated assertions into separate tests.
- **Test names are specs**: `test_create_user_rejects_invalid_email` is valuable; `test_user_1` is not.
- **Arrange-Act-Assert** in three sections separated by blank lines; the Act section is one line (the call under test).
- **Real data first**: use a real database/service when you can, isolated via transaction rollback or random ports. Mock only third-party boundaries you genuinely cannot stand up (payment gateway, SMS), and comment why.
- **Test behavior, not implementation**: don't assert private method call counts or internal ordering; tests shouldn't fail when the implementation is refactored.
- **Always test boundaries**: empty, null, zero, negative, max, concurrency, timeout, error paths — happy path alone is not enough.
