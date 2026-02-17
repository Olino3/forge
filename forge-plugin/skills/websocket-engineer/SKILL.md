---
name: websocket-engineer
## description: Architects real-time communication systems using the WebSocket protocol. Handles connection lifecycle management including handshake negotiation, heartbeat monitoring, and graceful disconnection. Designs efficient message routing with structured framing and serialization. Implements scalable pub/sub architectures with room management, presence tracking, and channel authorization. Like Hermes carrying messages between the gods with unerring speed, this skill ensures every real-time system delivers messages reliably, securely, and at scale.

# WebSocket Engineer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY WebSocket system design or implementation task. Skipping steps or deviating from the procedure will result in fragile, insecure, or unscalable real-time systems. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different WebSocket patterns and implementations
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("websocket-engineer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: Load domain context via `contextProvider.getIndex("{domain}")`. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: Read/write project memory via `memoryStore.getSkillMemory(...)`. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate configurations against `agent_config.schema.json`, `context_metadata.schema.json`, `memory_entry.schema.json`. See [schemas/](../../interfaces/schemas/).

## Focus Areas

WebSocket system design evaluates 7 critical dimensions:

1. **Connection Lifecycle**: Manage the full lifecycle — HTTP upgrade handshake, WebSocket connection establishment, heartbeat/ping-pong frames for keepalive, graceful close with status codes, and automatic reconnection with exponential backoff
2. **Message Protocol Design**: Define structured message framing with type/action envelopes, choose appropriate serialization formats (JSON, Protocol Buffers, MessagePack), implement protocol versioning for backward-compatible evolution
3. **Room & Channel Management**: Implement pub/sub patterns with named rooms and channels, enforce channel-level authorization policies, track user presence with join/leave events and online status broadcasting
4. **Scalability Patterns**: Design for horizontal scaling using Redis pub/sub or equivalent message brokers for cross-instance communication, configure sticky sessions for load-balanced deployments, integrate with message queues for durable delivery
5. **Error Handling & Resilience**: Handle connection drops and network interruptions gracefully, implement backpressure mechanisms to protect servers from slow consumers, apply circuit breakers around downstream dependencies, define retry strategies with jitter for reconnection storms
6. **Security**: Authenticate during the HTTP upgrade request using tokens or cookies, enforce per-message authorization for sensitive channels, apply rate limiting on message frequency and payload size, validate `Origin` headers to prevent cross-site WebSocket hijacking
7. **Testing & Debugging**: Build WebSocket test clients for integration testing, perform load testing with concurrent connection simulation, inspect message flows with protocol-aware tooling, implement message replay for debugging production issues

**Note**: The skill covers both server-side and client-side WebSocket implementation. It does not manage infrastructure provisioning unless explicitly requested.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze Real-Time Requirements (REQUIRED)

**YOU MUST:**
1. Identify specific real-time use cases (chat, live feeds, notifications, collaboration, gaming, etc.)
2. Determine message patterns — unidirectional server push, bidirectional communication, or request-response over WebSocket
3. Estimate scale requirements: concurrent connections, messages per second, average payload size
4. Assess latency sensitivity: is sub-100ms delivery critical, or is near-real-time (1-2s) acceptable?
5. Identify client environments: browsers, mobile apps, IoT devices, server-to-server
6. Determine durability needs: must messages survive server restarts or are they ephemeral?

**DO NOT PROCEED WITHOUT UNDERSTANDING THE REAL-TIME REQUIREMENTS**

### ⚠️ STEP 2: Design WebSocket Architecture (REQUIRED)

**YOU MUST:**
1. **Select the protocol layer**: Raw WebSocket, Socket.IO, or a higher-level abstraction
2. **Define the message schema**: Design the envelope format with fields for type, action, payload, and correlation ID
3. **Plan the room/channel topology**: Map use cases to rooms, channels, or topics
4. **Choose the scaling strategy**: Single-server, Redis pub/sub, or dedicated message broker (NATS, RabbitMQ)
5. **Design the authentication flow**: Token validation on upgrade, session binding, and per-channel authorization
6. **Specify error handling**: Define reconnection policy, backpressure strategy, and circuit breaker thresholds

**DO NOT PROCEED WITHOUT A CLEAR ARCHITECTURAL DESIGN**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Load existing project memory: `memoryStore.getSkillMemory("websocket-engineer", "{project-name}")`
2. Review previous connection patterns, message schemas, and scaling configurations
3. Identify established conventions: naming, serialization format, room hierarchy
4. Check for known issues or technical debt from prior implementations
5. If no memory exists, note this is a greenfield WebSocket implementation

See [MemoryStore Interface](../../interfaces/memory_store.md) for method details.

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 4: Implement WebSocket System (REQUIRED)

**YOU MUST:**
1. **Server setup**: Initialize the WebSocket server with appropriate configuration (max payload, ping interval, connection limits)
2. **Client implementation**: Build the client with connection management, automatic reconnection, and message queuing during disconnection
3. **Room/channel logic**: Implement join, leave, broadcast, and presence tracking
4. **Authentication & authorization**: Validate credentials on upgrade, enforce per-message permissions
5. **Error handling**: Add connection drop detection, backpressure handling, and structured error responses
6. **Message routing**: Implement the message dispatch pipeline — parse, validate, authorize, route, and acknowledge

**DO NOT DELIVER AN INCOMPLETE IMPLEMENTATION**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST validate the implementation against these criteria:**
1. **Connection resilience**: Verify reconnection logic with exponential backoff works correctly
2. **Message integrity**: Confirm messages are delivered in order and no silent drops occur
3. **Security review**: Ensure authentication on upgrade, origin validation, and rate limiting are in place
4. **Scale readiness**: Validate horizontal scaling path (Redis pub/sub or broker integration)
5. **Output files**: Generate deliverables to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`
6. **Update memory**: Use `memoryStore.update("websocket-engineer", "{project-name}", ...)` to persist:
   - Connection patterns and configuration decisions
   - Message schema definitions and versioning strategy
   - Scaling architecture and infrastructure choices

See [MemoryStore Interface](../../interfaces/memory_store.md) for `update()` and `append()` method details.

**DO NOT SKIP VALIDATION OR MEMORY UPDATE**

---

## Compliance Checklist

Before completing ANY WebSocket engineering task, verify:
- [ ] Step 1: Real-time requirements analyzed — use cases, scale, latency, durability
- [ ] Step 2: Architecture designed — protocol, message schema, scaling, auth, error handling
- [ ] Step 3: Project memory loaded and prior decisions reviewed
- [ ] Step 4: Implementation complete — server, client, rooms, auth, error handling, routing
- [ ] Step 5: Validated, output generated, and project memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE IMPLEMENTATION**

---

## Output File Naming Convention

**Format**: `websocket_{component}_{project}.md`

Where:
- `{component}` = The system component (e.g., `server`, `client`, `protocol`, `architecture`)
- `{project}` = The project or service name

**Examples**:
- `websocket_architecture_trading_platform.md`
- `websocket_server_chat_service.md`
- `websocket_protocol_collab_editor.md`

---

## WebSocket Technology Reference

| Technology | Language | Use Case |
|------------|----------|----------|
| **Socket.IO** | Node.js / Python / Java | Full-featured real-time framework with rooms, namespaces, fallback transports |
| **ws** | Node.js | Lightweight, high-performance raw WebSocket library |
| **gorilla/websocket** | Go | Production-grade WebSocket library for Go with connection management |
| **Django Channels** | Python | WebSocket support for Django with channel layers and consumer patterns |
| **FastAPI WebSockets** | Python | Async WebSocket support integrated with FastAPI's ASGI stack |
| **Spring WebSocket** | Java | Enterprise WebSocket support with STOMP sub-protocol and SockJS fallback |
| **ActionCable** | Ruby | Rails-integrated WebSocket framework with channels and subscriptions |
| **Phoenix Channels** | Elixir | High-concurrency real-time communication built on OTP and BEAM VM |
| **SignalR** | .NET | Microsoft's real-time framework with automatic transport negotiation |

---

## Further Reading

Refer to official documentation:
- **Protocol Specification**:
  - RFC 6455 — The WebSocket Protocol: https://datatracker.ietf.org/doc/html/rfc6455
  - RFC 7692 — Compression Extensions for WebSocket: https://datatracker.ietf.org/doc/html/rfc7692
- **Libraries & Frameworks**:
  - Socket.IO Documentation: https://socket.io/docs/v4/
  - ws (Node.js): https://github.com/websockets/ws
  - gorilla/websocket (Go): https://pkg.go.dev/github.com/gorilla/websocket
  - Django Channels: https://channels.readthedocs.io/
- **Best Practices**:
  - WebSocket Security: https://owasp.org/www-project-web-security-testing-guide/
  - Scaling WebSockets: https://ably.com/topic/scaling-websockets

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for WebSocket system design and implementation

### Step 1: Initial Analysis

Gather inputs and determine scope and requirements.

### Step 2: Load Memory

Load project-specific memory via MemoryStore interface.

### Step 3: Load Context

Load relevant context files via ContextProvider interface.

### Step 4: Core Implementation

Execute the skill-specific core action.

### Step 5: Generate Output

Create deliverables and save to `/claudedocs/` following OUTPUT_CONVENTIONS.md.

### Step 6: Update Memory

Update project memory with new patterns and decisions.
