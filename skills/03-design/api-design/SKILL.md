---
name: api-design
description: Use when designing APIs or interfaces — REST/GraphQL contracts, request/response shapes, versioning, error models, and interface ergonomics. Triggers on "design API", "REST contract", "GraphQL schema", "接口设计", "API 契约", "API 设计".
---

# API and Interface Design

Design stable, well-documented interfaces that are hard to misuse. Good interfaces make the right
thing easy and the wrong thing hard. Applies to REST APIs, GraphQL schemas, module boundaries,
component props, and any surface where one piece of code talks to another.

## When to use

- Designing new REST or GraphQL endpoints
- Defining module boundaries or contracts between teams
- Creating component prop interfaces or type contracts
- Establishing database schema that informs API shape
- Changing existing public interfaces
- Triggers on "API design", "interface design", "REST", "GraphQL", "contract", "接口设计", "API 契约", "API 设计"

**Not for:** system-level architecture decisions (use `architecture`); deep-module or codebase
structure (use `codebase-design`).

## Steps

### 1. Define the contract first

The contract is the spec — implementation follows. Define typed input and output schemas before
writing handlers. The types ARE the documentation.

### 2. Apply core principles

**Hyrum's Law:** With enough users, all observable behaviors become de-facto contracts — including
undocumented quirks, error text, timing, and ordering. Be intentional about what you expose; don't
leak implementation details; plan for deprecation at design time.

**The One-Version Rule:** Avoid forcing consumers to choose between multiple versions. Design for a
world where only one version exists at a time — extend rather than fork. Multiple versions multiply
maintenance cost and create diamond dependency problems.

**Addition Over Modification:** Extend interfaces without breaking consumers — add optional fields,
never change existing field types or remove fields. Breaking changes without versioning break
consumers.

### 3. Pick one error strategy and use it everywhere

Every error response follows the same shape. Don't mix patterns — if some endpoints throw, others
return null, and others return `{ error }`, the consumer can't predict behavior.

```
interface APIError {
  error: {
    code: string;        // Machine-readable: "VALIDATION_ERROR"
    message: string;     // Human-readable: "Email is required"
    details?: unknown;   // Additional context when helpful
  };
}
```

Status code mapping: 400 invalid data, 401 not authenticated, 403 not authorized, 404 not found,
409 conflict (duplicate, version mismatch), 422 validation failed, 500 server error (never expose
internal details).

### 4. Validate at boundaries

Trust internal code. Validate at system edges where external input enters: API route handlers, form
submissions, external service response parsing (third-party data is **always untrusted**), and
environment variable loading. Do NOT validate between internal functions that share type contracts,
in utility functions called by already-validated code, or on data from your own database.

### 5. Follow predictable naming

| Pattern | Convention | Example |
|---------|-----------|---------|
| REST endpoints | Plural nouns, no verbs | `GET /api/tasks`, `POST /api/tasks` |
| Query params | camelCase | `?sortBy=createdAt&pageSize=20` |
| Response fields | camelCase | `{ createdAt, updatedAt, taskId }` |
| Boolean fields | is/has/can prefix | `isComplete`, `hasAttachments` |
| Enum values | UPPER_SNAKE | `"IN_PROGRESS"`, `"COMPLETED"` |

### 6. Apply REST resource patterns

```
GET    /api/tasks              → List tasks (with query params for filtering)
POST   /api/tasks              → Create a task
GET    /api/tasks/:id          → Get a single task
PATCH  /api/tasks/:id          → Update a task (partial)
DELETE /api/tasks/:id          → Delete a task (idempotent)
GET    /api/tasks/:id/comments → List comments for a task (sub-resource)
```

Paginate every list endpoint from the start — you will need it the moment someone has 100+ items.
Accept partial objects on PATCH (only update what's provided), not full objects on PUT.

### 7. Use discriminated unions for variants

```typescript
type TaskStatus =
  | { type: 'pending' }
  | { type: 'in_progress'; assignee: string; startedAt: Date }
  | { type: 'completed'; completedAt: Date; completedBy: string }
  | { type: 'cancelled'; reason: string; cancelledAt: Date };
```

Consumer gets type narrowing — each variant is explicit, no optional fields that don't apply.
Separate input types (what the caller provides) from output types (what the system returns,
including server-generated fields). Use branded types for IDs to prevent accidentally passing a
`UserId` where a `TaskId` is expected.

**Output:** `docs/API/*.md` — one file per endpoint group, with full request/response shapes, parameters, errors, and examples.

## Verify

- [ ] Every endpoint has typed input and output schemas
- [ ] Error responses follow a single consistent format across all endpoints
- [ ] Validation happens at system boundaries only, not scattered through internal code
- [ ] List endpoints support pagination
- [ ] New fields are additive and optional (backward compatible)
- [ ] Naming follows consistent conventions across all endpoints
- [ ] API documentation or types are committed alongside the implementation

**Red flags:** endpoints that return different shapes depending on conditions; inconsistent error
formats; validation scattered through internal code; breaking changes to existing fields; list
endpoints without pagination; verbs in REST URLs (`/api/createTask`); third-party API responses
used without validation.

**Common rationalizations:** "We'll document later" — the types ARE the documentation, define them
first. "We don't need pagination for now" — add it from the start. "PATCH is complicated, use PUT"
— PATCH is what clients actually want. "We'll version when we need to" — design for extension from
the start. "Nobody uses that undocumented behavior" — Hyrum's Law says someone does.

## References

- [${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md](${CLAUDE_PLUGIN_ROOT}/references/engineering-principles.md) — shared discipline (enforce simplicity, surgical scope, verify don't assume)
