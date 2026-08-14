---
name: api-testing
description: Use when testing APIs or designing API test strategies — contract testing, REST/GraphQL testing, and integration testing. Triggers on "test API", "contract testing", "integration test", "API 测试", "接口测试", "契约测试".
---

# API Testing Patterns

API testing verifies contracts and behavior from the consumer perspective —
correct responses, proper error handling, acceptable performance. Focus on what
matters to consumers, not implementation details.

## When to use

- Testing REST or GraphQL APIs
- Validating microservice contracts
- Designing API test strategies
- Preventing breaking API changes
- Triggers on "test API", "contract testing", "integration test", "API 测试", "接口测试", "契约测试"

**Not for:** generating test scaffolds for non-API code (use `test-generation`); browser/E2E flows (use `e2e-testing`); the TDD loop itself (use `tdd`).

## Steps

### 1. Identify the testing level

| Level | Purpose | Dependencies | Speed |
|-------|---------|--------------|-------|
| Contract | Provider-consumer agreement | None | Fast |
| Component | API in isolation | Mocked external deps | Fast |
| Integration | Real dependencies | Database, services | Slower |

### 2. Test the contract, not implementation

Test from the consumer perspective using schema validation, not exact values.
Consumers depend on the contract (status codes, response shape); they don't
care about internal structure.

**Pattern — Consumer-Driven Contracts:**

```javascript
const contract = {
  request: { method: 'POST', path: '/orders', body: { productId: 'abc', quantity: 2 } },
  response: { status: 201, body: { orderId: 'string', total: 'number' } }
};

test('order API meets contract', async () => {
  const response = await api.post('/orders', { productId: 'abc', quantity: 2 });
  expect(response.status).toBe(201);
  expect(response.body).toMatchSchema({
    orderId: expect.any(String),
    total: expect.any(Number)
  });
});
```

Use **Pact** or **Spring Cloud Contract** for consumer-driven contract testing
in microservice architectures.

### 3. Cover critical scenarios

| Scenario | Must test | Example |
|----------|----------|---------|
| Auth | 401/403 handling | Expired token, wrong user, cross-user access |
| Input | 400 validation | Missing fields, wrong types, out-of-range values |
| Errors | 500 graceful handling | DB down, timeout, upstream failure |
| Idempotency | Duplicate prevention | Same idempotency key → same result |
| Concurrency | Race conditions | Parallel checkout on shared inventory |

**Idempotency:** send the same request twice with an `Idempotency-Key` header;
both responses must return the same `orderId` (no duplicate created).

### 4. REST CRUD pattern

Test the full resource lifecycle — CREATE, READ, UPDATE, DELETE — as a sequence
that proves each operation and its side effects.

```javascript
describe('Product CRUD', () => {
  let productId;

  it('CREATE', async () => {
    const r = await api.post('/products', { name: 'Widget', price: 10 });
    expect(r.status).toBe(201);
    productId = r.body.id;
  });

  it('READ', async () => {
    const r = await api.get(`/products/${productId}`);
    expect(r.body.name).toBe('Widget');
  });

  it('UPDATE', async () => {
    const r = await api.put(`/products/${productId}`, { price: 12 });
    expect(r.body.price).toBe(12);
  });

  it('DELETE', async () => {
    expect((await api.delete(`/products/${productId}`)).status).toBe(204);
    expect((await api.get(`/products/${productId}`)).status).toBe(404);
  });
});
```

### 5. GraphQL-specific checks

- Query validation: reject invalid queries, enforce typed schemas
- Complexity limits: prevent abusive nested queries (depth/complexity analysis)
- Introspection: test against staging schema (production may disable it)

### 6. Automate and monitor

Automate all API tests in CI/CD with schema validation. Version API tests
alongside the API to prevent breaking changes. Monitor production APIs for
contract drift between deployed behavior and the spec.

## Best practices

**Do:**

- Test from consumer perspective
- Use schema validation (not exact field values)
- Test error scenarios extensively — not just happy paths
- Version API tests with the API
- Mock external services to keep tests fast and deterministic

**Avoid:**

- Testing implementation, not contract
- Ignoring HTTP semantics (status codes)
- No negative testing
- Asserting on field order or extra fields
- Slow tests (mock external services)

## Gotchas

- Tests generated against the documented API must be validated against the
  running service first — docs and reality drift
- Auth tokens expire between runs — use fixtures with refresh logic
- Rate limiting in CI causes intermittent 429s — add retry with exponential
  backoff
- Idempotency tests need unique request IDs per run — hardcoded IDs cause false
  passes on retry
- GraphQL introspection may be disabled in production — test against staging

**Output:** API test files (contract + integration) under `test/` — code, not a report.

## Verify

- [ ] Contract tests cover every consumer expectation
- [ ] Auth: 401 without token, 403 for wrong user, expired token rejected
- [ ] Input validation: missing fields, wrong types, out-of-range values → 400
- [ ] Error states: 500 graceful, timeout handled
- [ ] Idempotency: duplicate request with same key → same result
- [ ] REST resources tested across full CRUD lifecycle
- [ ] Tests automated in CI with schema validation

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — discipline every skill shares
- [references/templates/api-test-scaffold.md](references/templates/api-test-scaffold.md) — REST API test scaffold template (Jest/Supertest)
