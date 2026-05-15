---
description: >
name: api-design
version: 1.0.0
tags:
  - api
  - rest
  - graphql
  - design
  - contract
metadata:
  skill-author: 'Marie-Lynne Block'
---

## What this skill does

Applies REST and GraphQL design principles to produce or review an API contract. It covers resource modelling, URL conventions, HTTP semantics, request/response schemas, error formats, versioning strategy, and authentication patterns — producing OpenAPI-compatible snippets or GraphQL schema fragments.

## When to use it

- User asks to "design an API", "review this API", or "define the endpoints for X".
- User wants to model resources and operations before writing implementation code.
- User needs an OpenAPI snippet or GraphQL schema fragment.
- User is establishing API conventions for a team or project.

## Key concepts

### REST principles

| Principle | Guidance |
| --- | --- |
| **Resource naming** | Nouns, plural, lowercase, hyphenated: `/orders`, `/line-items`. Never verbs in URLs. |
| **HTTP methods** | `GET` read, `POST` create, `PUT` full replace, `PATCH` partial update, `DELETE` remove |
| **Idempotency** | `GET`, `PUT`, `DELETE` must be idempotent. `POST` is not. `PATCH` should be designed to be. |
| **Status codes** | 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorised, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 500 Internal Server Error |
| **Filtering/sorting** | Query parameters: `?status=active&sort=created_at&order=desc&page=2&per_page=25` |
| **Versioning** | URI prefix (`/v1/`) for breaking changes; header versioning (`Accept: application/vnd.api+json;version=2`) for content negotiation |

### Error response format

Consistent error bodies across all endpoints:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      { "field": "email", "issue": "must be a valid email address" }
    ]
  }
}
```

### GraphQL conventions

- Operations: `query` for reads, `mutation` for writes, `subscription` for real-time.
- Type names: PascalCase (`OrderLine`). Field names: camelCase (`lineItems`).
- Always paginate list fields using Relay-style connections (`edges`, `node`, `pageInfo`).
- Use input types for mutation arguments: `input CreateOrderInput { ... }`.
- Return a result union for mutations: `type CreateOrderResult = Order | ValidationError`.

### Security checklist

- [ ] Authentication required on all non-public endpoints (JWT, OAuth2, API key).
- [ ] Authorisation checked at the resource level, not just the route.
- [ ] Input validated and sanitised before processing.
- [ ] Rate limiting applied.
- [ ] Sensitive data (PII, tokens) not returned in error messages or logs.
- [ ] HTTPS enforced; HTTP redirects to HTTPS or is rejected.

## Instructions

1. **Identify the API type.** REST or GraphQL? If not stated, recommend based on use case (REST for CRUD-heavy APIs, GraphQL for flexible querying across related data).

2. **Model the resources or types.** Identify the entities involved and their relationships. Name them clearly.

3. **Define the operations.** For REST: map resources to endpoints and HTTP methods. For GraphQL: define queries, mutations, and types.

4. **Design request/response schemas.** Specify field names, types, and validation rules. Call out optional vs. required fields.

5. **Define the error contract.** Consistent error format across all operations.

6. **Address versioning and authentication.** State the versioning strategy and authentication mechanism.

7. **Flag design concerns.** Identify any REST anti-patterns, N+1 risks (GraphQL), or security gaps.

8. **Produce the output** using the format below.

## Output format

### REST — OpenAPI snippet

```yaml
openapi: 3.1.0
info:
  title: [API name]
  version: 1.0.0

paths:
  /[resource]:
    get:
      summary: List [resources]
      parameters:
        - name: status
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/[Resource]'
        '401':
          $ref: '#/components/responses/Unauthorised'

  /[resource]/{id}:
    get:
      summary: Get [resource] by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Success
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    [Resource]:
      type: object
      required: [id, created_at]
      properties:
        id:
          type: string
          format: uuid
        created_at:
          type: string
          format: date-time

  responses:
    Unauthorised:
      description: Missing or invalid credentials
    NotFound:
      description: Resource not found
```

### GraphQL — Schema fragment

```graphql
type Query {
  [resource](id: ID!): [Resource]
  [resources](filter: [Resource]FilterInput, first: Int, after: String): [Resource]Connection!
}

type Mutation {
  create[Resource](input: Create[Resource]Input!): Create[Resource]Result!
}

type [Resource] {
  id: ID!
  # fields
  createdAt: DateTime!
}

input Create[Resource]Input {
  # fields
}

union Create[Resource]Result = [Resource] | ValidationError

type ValidationError {
  message: String!
  fields: [FieldError!]!
}
```

### Design notes

```markdown
### Design decisions

- [Decision and rationale]

### Concerns / open questions

- [Anti-pattern, risk, or unresolved design question]
```

## Examples

### Example 1 — Order management REST API

**Input:** "Design a REST API for creating and managing orders. An order has line items, a customer, and a status."

**Expected output:** OpenAPI snippet with `/orders` (GET, POST) and `/orders/{id}` (GET, PATCH, DELETE) and `/orders/{id}/line-items` (GET, POST). Order schema with status enum. Error contract. Design note on whether to embed line items in the order response or use a separate endpoint.

### Example 2 — GraphQL API review

**Input:** User shares a GraphQL schema where a `User` type has a `posts` field returning a plain list with no pagination.

**Expected output:** Concern flagged for missing pagination (N+1 and performance risk at scale). Suggested fix using Relay connection pattern. Note on missing input types for mutations.

## Notes

- REST URLs identify resources, not actions. If a URL contains a verb (`/createOrder`, `/getUser`), it is an anti-pattern — model it as a resource operation instead.
- GraphQL is not a replacement for REST in all cases: file uploads, caching, and simple CRUD are often better served by REST.
- OpenAPI snippets in this skill are illustrative, not exhaustive. A full spec requires `info`, `servers`, and `security` sections.
- Do not design authentication schemes that store credentials in URLs (`?api_key=...`) — they appear in server logs and browser history.
