# Language Pattern Mapping

Same test patterns apply across languages. Generate tests that match the detected framework's
idioms — file layout, assertion style, fixtures, parametrization, async handling. Prefer **real
calls against real dependencies** (real database, real API, real filesystem) over mocks; mock only
a slow or third-party boundary you genuinely cannot stand up, and say why.

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
    # 真实测试数据库，每个测试独立事务回滚——不 mock，不共享状态
    session = get_session("postgresql://test:test@localhost/test_db")
    session.begin()
    yield session
    session.rollback()
    session.close()

@pytest.mark.parametrize("email, should_pass", [
    ("alice@example.com", True),
    ("not-an-email", False),
    ("", False),
    ("UPPER@EXAMPLE.COM", True),  # 规范化大小写
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

- 文件名 `test_<module>.py`，函数 `test_<behavior>`。
- 用 `@pytest.mark.parametrize` 覆盖边界，不要写 5 个近乎相同的测试。
- 异常用 `pytest.raises(Error)` 断言，不要 try/except + assert。
- 异步用 `@pytest.mark.asyncio` + `await`。

## TS/JS — Vitest / Jest

```typescript
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { createServer } from "http";
import { apiClient } from "../src/client";

// 真实起一个本地服务实例，发真实 HTTP 请求——不 mock fetch
describe("user API", () => {
  let server: ReturnType<typeof createServer>;
  let baseUrl: string;

  beforeEach(async () => {
    server = createServer({ port: 0, db: testDbUrl });  // 随机端口，真实服务
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

- `describe` 分组、`it` 单例，命名"主语 + 行为"。
- `it.each` 参数化边界。
- 避免快照测试（`toMatchSnapshot`）做行为断言——它只锁字符串，不验证正确性。

## Go — table-driven

```go
func TestCreateUser(t *testing.T) {
    db := testdb.Connect(t) // t.Cleanup 自动清理，真实 DB
    tests := []struct {
        name      string
        email     string
        wantErr   bool
        wantEmail string // 规范化后期望值
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

- 表驱动是 Go 惯例：一个 `tests` slice + `t.Run` 子测试。
- `testdb.Connect(t)` 用 `t.Cleanup` 回滚，真实连接。
- `require` 失败即停（前置条件），`assert` 收集多个失败。

## 通用原则（跨框架）

- **一个测试断言一个行为**——失败时一眼看出哪里错。多个无关断言拆成多个测试。
- **测试名即规格**：`test_create_user_rejects_invalid_email` 比 `test_user_1` 有价值。
- **Arrange-Act-Assert** 三段式，段间空行分隔；Act 段只有一行（被测调用）。
- **真实数据优先**：能用真实数据库/服务就用，事务回滚或随机端口隔离。mock 仅用于你无法启动的第三方边界（支付网关、SMS），且注释说明为何 mock。
- **测行为不测实现**：不 assert 私有方法调用次数、不依赖内部顺序；重构实现后测试不应失败。
- **边界必测**：空、null、零、负、最大、并发、超时、错误路径——happy path 不够。
