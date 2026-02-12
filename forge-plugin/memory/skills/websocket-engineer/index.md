# websocket-engineer Memory

Project-specific memory for WebSocket connection patterns, message schema decisions, and real-time scaling configurations.

## Purpose

This memory helps the `skill:websocket-engineer` remember:
- Which WebSocket libraries and frameworks each project uses
- Established message schemas, envelope formats, and serialization choices
- Room/channel topology and naming conventions
- Scaling architecture decisions (Redis pub/sub, NATS, sticky sessions)
- Authentication and authorization patterns for WebSocket connections
- Known issues, performance baselines, and technical debt

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Recommended Files

#### `connection_patterns.md`

**Purpose**: Track WebSocket connection configuration, lifecycle settings, and client management patterns for this project

**Should contain**:
- **Library/framework**: Which WebSocket library is used (Socket.IO, ws, gorilla/websocket, Django Channels, etc.)
- **Connection settings**: Ping interval, pong timeout, max payload size, connection limits
- **Authentication flow**: How clients authenticate during the upgrade handshake
- **Reconnection strategy**: Backoff parameters, max retries, state recovery on reconnect
- **Client types**: Browser, mobile, IoT, server-to-server — and any per-client configuration
- **Transport fallbacks**: Whether polling or SSE fallback is configured

**Example structure**:
```markdown
# Connection Patterns - MyProject

## WebSocket Library
- Server: Socket.IO 4.7 (Node.js)
- Client: socket.io-client 4.7
- Transport: WebSocket primary, long-polling fallback

## Connection Settings
- Ping interval: 25s
- Ping timeout: 20s
- Max payload: 1MB
- Max connections per server: 10,000

## Authentication
- Method: JWT in handshake auth object
- Validation: io.use() middleware verifies token on connect
- Token refresh: Client disconnects and reconnects with new token

## Reconnection
- Strategy: Exponential backoff (1s–30s) with jitter
- Max attempts: Infinite
- State recovery: Client re-subscribes to rooms on reconnect
```

**When to update**: After any WebSocket infrastructure change, library upgrade, or connection policy modification

---

#### `message_schemas.md`

**Purpose**: Document message envelope formats, event types, serialization choices, and protocol versioning

**Should contain**:
- **Envelope format**: Standard message structure (type, action, payload, correlationId)
- **Event inventory**: List of all defined message types and their payload schemas
- **Serialization**: Format used (JSON, Protocol Buffers, MessagePack) and rationale
- **Protocol versioning**: How schema changes are handled across client versions
- **Validation rules**: Payload size limits, required fields, type constraints

**Example structure**:
```markdown
# Message Schemas - MyProject

## Envelope Format
{
  "type": "<domain>",
  "action": "<verb>",
  "payload": { ... },
  "correlationId": "<uuid>",
  "version": 1
}

## Event Types (18 defined)
### Chat Domain (6 events)
- chat:message — Send/receive chat message
- chat:typing — Typing indicator start/stop
- chat:read — Read receipt acknowledgment
...

### Presence Domain (4 events)
- presence:join — User came online
- presence:leave — User went offline
- presence:list — Request current online users
- presence:update — Status change (away, busy, etc.)
...

## Serialization
- Format: JSON (browser clients)
- Max payload: 64KB per message
- Binary: Not currently used; planned for file transfer

## Versioning
- Current version: 1
- Strategy: Additive changes only; new fields are optional
- Breaking changes: New message type + deprecation period
```

**When to update**: When new event types are added, schemas change, or serialization format evolves

---

#### `scaling_config.md`

**Purpose**: Document horizontal scaling strategy, message broker setup, and infrastructure topology

**Should contain**:
- **Scaling approach**: Single server, Redis pub/sub, dedicated message broker, or managed service
- **Broker configuration**: Connection strings, topic patterns, retention settings
- **Load balancing**: Sticky session configuration, health check endpoints
- **Capacity planning**: Connections per instance, messages per second benchmarks
- **Monitoring**: WebSocket-specific metrics, alerting thresholds, dashboards

**Example structure**:
```markdown
# Scaling Configuration - MyProject

## Architecture
- Topology: 4 WebSocket server instances behind ALB
- Broker: Redis 7.2 pub/sub for cross-instance messaging
- Sticky sessions: ALB cookie-based (AWSALB, 1 hour TTL)

## Redis Pub/Sub
- Host: redis-ws.internal:6379
- Channel pattern: ws:{namespace}:{room}
- Adapter: @socket.io/redis-adapter 8.x

## Capacity
- Per instance: 5,000 connections, 1,000 msg/s
- Total cluster: 20,000 connections, 4,000 msg/s
- Autoscaling: Add instance at 3,500 connections

## Monitoring
- Metrics: connection_count, message_rate, latency_p99
- Alerts: connection_count > 4,000 (warning), > 4,500 (critical)
- Dashboard: Grafana "WebSocket Overview"
```

**When to update**: After scaling events, infrastructure changes, or capacity planning reviews

---

## Usage in skill:websocket-engineer

### Loading Memory

```markdown
# In skill workflow Step 3

project_name = detect_project_name()
memory = memoryStore.getSkillMemory("websocket-engineer", "{project-name}")

if memory exists:
    connection_patterns = read(memory, "connection_patterns.md")
    message_schemas = read(memory, "message_schemas.md")
    scaling_config = read(memory, "scaling_config.md")

    # Use for design decisions
    - Follow established library and framework choices
    - Reuse message envelope format and event naming conventions
    - Reference scaling architecture when adding new features
```

### Updating Memory

```markdown
# In skill workflow Step 5

After implementing WebSocket features:

1. Check if new decisions were made:
   - New library or connection configuration?
   - New message types or schema changes?
   - Scaling topology updates?

2. If yes, update relevant memory file:
   memoryStore.update(layer="skill-specific", skill="websocket-engineer",
                      project="{project-name}", ...)

3. If first time building WebSocket features for project:
   - Create directory and all memory files
   - Populate with observations from this implementation
```

---

## Memory Evolution Over Time

### After 1st WebSocket Task
```markdown
# connection_patterns.md

## WebSocket Library
- Server: ws 8.x (Node.js)
- Auth: JWT on upgrade

# message_schemas.md

## Envelope Format
- type + action + payload (JSON)
- 3 event types defined
```

### After 5 WebSocket Tasks
```markdown
# connection_patterns.md

## WebSocket Library
- Server: ws 8.16 (Node.js)
- Connection pool: 5,000 max per instance
- Reconnection: Exponential backoff 1s–30s with jitter
- Auth: JWT + per-channel ACL

# message_schemas.md

## Event Types (14 defined)
- Chat: 6 events
- Presence: 4 events
- Notifications: 4 events
- Serialization: JSON, considering MessagePack for binary data

# scaling_config.md

## Architecture
- 3 instances behind nginx (ip_hash)
- Redis pub/sub for cross-instance messaging
- Monitoring: connection_count, message_rate dashboards
```

### After 20 WebSocket Tasks
```markdown
# Comprehensive real-time system knowledge — full protocol documented,
# scaling patterns proven, message schemas versioned and stable.
# Memory now provides high-value project-specific WebSocket guidance.
```

---

## Related Documentation

- **Main Memory Index**: `../index.md` for memory system overview
- **Skill Documentation**: `../../skills/websocket-engineer/SKILL.md` for skill workflow
- **Context Files**: `../../context/` for general development knowledge
- **Memory Lifecycle**: `../lifecycle.md` for memory freshness and pruning
- **Memory Quality**: `../quality_guidance.md` for memory validation
