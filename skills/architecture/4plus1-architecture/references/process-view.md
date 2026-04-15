# Process View Reference

## Purpose

The process view describes **how the system behaves at runtime** — its dynamic aspects, concurrency model, and inter-process communication. It is the bridge between the static structure of the logical view and the deployed topology of the physical view.

**Target audience:** System integrators, performance engineers, reliability engineers, senior developers  
**Central question:** *How do the system's processes communicate, synchronise, and handle concurrency, failure, and scale?*

---

## Core Concepts

### Process
An independently schedulable unit of execution. May be an OS process, a JVM thread pool, a container, or an async event loop — the granularity depends on the system.

### Task / Thread
A unit of concurrency within a process.

### Message / Event
The mechanism of communication between processes. Characterise each:
- **Synchronous** (caller blocks waiting for response) — RPC, HTTP request/response
- **Asynchronous** (caller does not block) — message queue, event bus, webhook
- **One-way / fire-and-forget**
- **Request/reply**

### Concurrency Patterns
Document which patterns the system uses:
- Active object (object with its own thread of control)
- Half-sync / half-async
- Reactor (event loop)
- Thread-per-request vs. thread pool
- Actor model

---

## Document Structure

### 1. Audience Statement
Who reads this and what operational concern it addresses.

### 2. Process Inventory

List every major process/service, its role, and its concurrency model:

| Process | Role | Concurrency Model | Startup |
|---------|------|-------------------|---------|
| `api-gateway` | Ingress routing | Async event loop (Node.js) | Always-on |
| `order-processor` | Order state machine | Thread pool (16 workers) | On-demand |
| `notification-worker` | Email/SMS dispatch | Single-threaded queue consumer | Always-on |

### 3. Process Communication Map

Describe the communication topology as a graph. For each communication channel:
- Source process
- Destination process
- Protocol / transport
- Direction (sync / async)
- Failure semantics (what happens when the destination is unavailable)

```
[api-gateway] ──HTTP/sync──> [order-service]
[order-service] ──Kafka/async──> [notification-worker]
[order-service] ──HTTP/sync──> [payment-service]
[payment-service] ──Kafka/async──> [audit-logger]
```

### 4. Sequence Diagrams (key scenarios)

Select 3–5 critical runtime flows. For each, produce a sequence diagram covering:
- Initiating actor or event
- All participating processes
- All messages with labels
- Async responses and callbacks
- Error / timeout paths

Format:
```
Actor          api-gateway     order-service    payment-service   notification-worker
  |                |                |                  |                  |
  |──POST /orders──>|               |                  |                  |
  |                |──createOrder()─>|                 |                  |
  |                |                |──chargeCard()───>|                  |
  |                |                |<──{success}──────|                  |
  |                |                |──[publish OrderPlaced]──────────────>|
  |                |<──{orderId}────|                  |                  |
  |<──201 Created──|               |                  |                  |
```

### 5. Activity Diagrams (for complex flows with branching)

Use for workflows with significant branching, parallel execution, or join points.

Format:
```
[Start]
   │
   ▼
[Validate Request]
   │
   ├──[invalid]──> [Return 400]
   │
   ├──[valid]──> [Check Stock] ──────────┐
   │                                      │ (parallel)
   │                                 [Reserve Payment]
   │                                      │
   └──────────────── [Join] ─────────────┘
                        │
                        ▼
                   [Create Order]
```

### 6. Concurrency and Synchronisation

For each shared resource or critical section, document:
- What is shared
- Which processes access it
- Synchronisation mechanism (mutex, semaphore, optimistic lock, CRDT, etc.)
- Risk of deadlock or starvation and how it is mitigated

### 7. Failure and Resilience Patterns

| Failure Scenario | Detection | Response | Recovery |
|-----------------|-----------|----------|----------|
| `payment-service` timeout | Circuit breaker (3s) | Return 503 to client | Retry with exponential backoff |
| Kafka consumer lag spike | Prometheus alert | Scale consumer group | Auto-scaling policy |
| Database connection pool exhausted | Connection timeout | Queue requests (bounded) | Alert + drain |

### 8. Performance Characteristics

Document expected throughput and latency targets per critical path:

| Flow | Target Latency (p95) | Target Throughput |
|------|---------------------|-------------------|
| Place order (full path) | < 800ms | 500 rps |
| Payment callback processing | < 200ms | 100 rps |

---

## Common Mistakes to Avoid

- **Conflating process and class.** A `OrderService` class is not a process. A `order-service` container is.
- **Happy path only.** The process view must document failure paths — they are the reason this view exists for reliability engineers.
- **Missing async semantics.** If a message is async, document what happens to the caller while it waits (or doesn't).
- **Ignoring backpressure.** Any async channel needs a documented overflow strategy.

---

## Miro Prompt Pointer

When generating a Miro prompt for this view, read `examples/miro-process-view-prompt.md`. The swimlane layout is critical — each process gets its own lane. Async messages must be visually distinct from sync calls.
