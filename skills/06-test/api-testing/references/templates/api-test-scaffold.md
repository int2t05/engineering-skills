# API Test Patterns and Scaffold

## Contents

- [REST API Test Structure (Jest/Supertest)](#rest-api-test-structure-jestsupertest)
- [Consumer-Driven Contracts](#consumer-driven-contracts)
- [REST CRUD lifecycle](#rest-crud-lifecycle)

## REST API Test Structure (Jest/Supertest)
```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('{{Resource}} API', () => {
  // Setup
  let authToken: string;

  beforeAll(async () => {
    authToken = await getTestToken();
  });

  describe('GET /api/{{resource}}', () => {
    it('returns paginated list with valid auth', async () => {
      const res = await request(app)
        .get('/api/{{resource}}')
        .set('Authorization', `Bearer ${authToken}`)
        .query({ page: 1, limit: 10 });

      expect(res.status).toBe(200);
      expect(res.body.data).toBeInstanceOf(Array);
      expect(res.body.pagination).toMatchObject({
        page: 1,
        limit: 10,
        total: expect.any(Number)
      });
    });

    it('returns 401 without auth', async () => {
      const res = await request(app).get('/api/{{resource}}');
      expect(res.status).toBe(401);
    });

    it('returns 400 for invalid query params', async () => {
      const res = await request(app)
        .get('/api/{{resource}}')
        .set('Authorization', `Bearer ${authToken}`)
        .query({ page: -1 });
      expect(res.status).toBe(400);
    });
  });

  describe('POST /api/{{resource}}', () => {
    it('creates resource with valid payload', async () => {
      const payload = { /* valid fields */ };
      const res = await request(app)
        .post('/api/{{resource}}')
        .set('Authorization', `Bearer ${authToken}`)
        .send(payload);

      expect(res.status).toBe(201);
      expect(res.body.id).toBeDefined();
    });

    it('returns 422 for invalid payload', async () => {
      const res = await request(app)
        .post('/api/{{resource}}')
        .set('Authorization', `Bearer ${authToken}`)
        .send({});
      expect(res.status).toBe(422);
      expect(res.body.errors).toBeDefined();
    });

    it('is idempotent with same idempotency key', async () => {
      const idempotencyKey = crypto.randomUUID();
      const payload = { /* valid fields */ };

      const res1 = await request(app)
        .post('/api/{{resource}}')
        .set('Authorization', `Bearer ${authToken}`)
        .set('Idempotency-Key', idempotencyKey)
        .send(payload);

      const res2 = await request(app)
        .post('/api/{{resource}}')
        .set('Authorization', `Bearer ${authToken}`)
        .set('Idempotency-Key', idempotencyKey)
        .send(payload);

      expect(res1.body.id).toBe(res2.body.id);
    });
  });
});
```

## Consumer-Driven Contracts

Test from the consumer perspective using schema validation, not exact values. Consumers
depend on the contract (status codes, response shape); they don't care about internal
structure. Use **Pact** or **Spring Cloud Contract** for consumer-driven contract testing
in microservice architectures.

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

## REST CRUD lifecycle

Test the full resource lifecycle — CREATE, READ, UPDATE, DELETE — as a sequence that
proves each operation and its side effects.

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
