# Language Pattern Mapping

Same test patterns apply across all languages. Key differences per language:

| Language | Test Framework | Test Runner | Assertion Style | Mock Library |
|----------|----------------|-------------|-----------------|--------------|
| Go | testing + testify | `go test` | `assert.Equal`, `require.NoError` | `gomock`, manual |
| Python | pytest | `pytest` | bare `assert`, `pytest.raises` | `unittest.mock`, fakeredis |
| Java | JUnit 5 + AssertJ | mvn/gradle test | `assertThat().isEqualTo()` | Mockito |
| Rust | test (built-in) | `cargo test` | `assert!`, `assert_eq!` | `mockall` |
| C# | xUnit + FluentAssertions | `dotnet test` | `result.Should().Be()` | Moq, NSubstitute |
| TS/JS | Vitest / Jest | `vitest`/`jest` | `expect().toEqual()` | vi.mock, jest.mock |
| Ruby | RSpec | `rspec` | `expect().to eq()` | rspec-mocks |
| PHP | PHPUnit | `phpunit` | `assertSame()`, `assertEquals()` | PHPUnit mocks |
| C/C++ | GoogleTest | `ctest` | `EXPECT_EQ`, `ASSERT_TRUE` | GMock |
| Swift | XCTest | `xcodebuild test` | `XCTAssertEqual` | Cuckoo |

Adapt generated test code to match the detected language's idioms from this table.
