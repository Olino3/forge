# WebSocket Engineer Examples

This file contains example scenarios demonstrating how to use the websocket-engineer skill to design and implement real-time communication systems.

---

## Example 1: Real-Time Chat Application with Socket.IO

### Scenario
Build a real-time chat application using Node.js and Socket.IO with support for multiple rooms, user presence tracking, and message history.

### User Prompt
```
I need a real-time chat system for our SaaS platform. Users should be able to join rooms, see who's online, and get instant messages. We expect around 5,000 concurrent users.
```

### Skill Execution

**Step 1 — Analyze Real-Time Requirements**:
- **Use case**: Multi-room chat with presence for a SaaS platform
- **Message patterns**: Bidirectional — clients send messages, server broadcasts to room members
- **Scale**: ~5,000 concurrent connections, ~200 messages/second across all rooms
- **Latency**: Sub-200ms delivery expected for chat messages
- **Clients**: Web browsers (React frontend)
- **Durability**: Messages must persist for history; delivery during brief disconnects is desired

**Step 2 — Design WebSocket Architecture**:
- **Protocol**: Socket.IO (automatic reconnection, room abstraction, fallback to polling)
- **Message schema**:
  ```json
  {
    "type": "chat",
    "action": "message",
    "room": "project-alpha",
    "payload": {
      "text": "Hello team!",
      "author": "user_123",
      "timestamp": "2026-02-12T10:30:00Z"
    },
    "correlationId": "msg_abc123"
  }
  ```
- **Room topology**: One Socket.IO room per chat channel, namespaced by team
- **Scaling**: Single server initially, Redis adapter ready for horizontal scaling
- **Auth**: JWT validated on Socket.IO handshake via `io.use()` middleware
- **Error handling**: Socket.IO built-in reconnection with exponential backoff (1s–30s)

**Step 3 — Load Project Memory**:
```
memoryStore.getSkillMemory("websocket-engineer", "saas-platform")
→ No existing memory found. Greenfield WebSocket implementation.
```

**Step 4 — Implement WebSocket System**:

Server setup (Node.js + Socket.IO):
```javascript
const { Server } = require("socket.io");
const { createAdapter } = require("@socket.io/redis-adapter");
const { createClient } = require("redis");

const io = new Server(server, {
  cors: { origin: process.env.ALLOWED_ORIGINS?.split(",") },
  pingInterval: 25000,
  pingTimeout: 20000,
  maxHttpBufferSize: 1e6,
});

// Authentication middleware
io.use(async (socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const user = await verifyJWT(token);
    socket.data.user = user;
    next();
  } catch (err) {
    next(new Error("Authentication failed"));
  }
});

// Redis adapter for horizontal scaling
const pubClient = createClient({ url: process.env.REDIS_URL });
const subClient = pubClient.duplicate();
Promise.all([pubClient.connect(), subClient.connect()]).then(() => {
  io.adapter(createAdapter(pubClient, subClient));
});

// Connection handler
io.on("connection", (socket) => {
  console.log(`User connected: ${socket.data.user.id}`);

  // Join room
  socket.on("room:join", async (roomId) => {
    if (!await canAccessRoom(socket.data.user, roomId)) {
      socket.emit("error", { message: "Unauthorized" });
      return;
    }
    socket.join(roomId);
    socket.to(roomId).emit("presence:join", {
      userId: socket.data.user.id,
      username: socket.data.user.name,
    });
  });

  // Send message
  socket.on("chat:message", async (data) => {
    const message = {
      id: generateId(),
      text: data.text,
      author: socket.data.user.id,
      room: data.room,
      timestamp: new Date().toISOString(),
    };
    await saveMessage(message);
    io.to(data.room).emit("chat:message", message);
  });

  // Handle disconnect
  socket.on("disconnecting", () => {
    for (const room of socket.rooms) {
      if (room !== socket.id) {
        socket.to(room).emit("presence:leave", {
          userId: socket.data.user.id,
        });
      }
    }
  });
});
```

Client setup (React):
```javascript
import { io } from "socket.io-client";

const socket = io(WS_URL, {
  auth: { token: getAuthToken() },
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 30000,
  reconnectionAttempts: Infinity,
});

socket.on("connect", () => {
  socket.emit("room:join", currentRoomId);
});

socket.on("chat:message", (message) => {
  addMessageToUI(message);
});

socket.on("presence:join", (data) => {
  updateOnlineUsers(data.userId, true);
});
```

**Step 5 — Review & Output**:
- ✅ **Connection resilience**: Socket.IO handles reconnection with backoff automatically
- ✅ **Message integrity**: Messages persisted to DB before broadcast; correlation IDs for deduplication
- ✅ **Security**: JWT validated on handshake, room access checked before join
- ✅ **Scale readiness**: Redis adapter configured for multi-instance deployment
- 📄 Output: `websocket_server_saas_chat.md` generated to `/claudedocs/`
- 💾 Memory updated with connection patterns, message schema, and Socket.IO configuration

---

## Example 2: Live Dashboard with Server Push

### Scenario
Build a live market data dashboard using Go and gorilla/websocket that pushes real-time price updates to connected browser clients.

### User Prompt
```
We need a live dashboard that streams market data updates to browser clients. Data comes from an upstream feed at ~500 updates/second. We'll have around 2,000 concurrent viewers. Use Go for the backend.
```

### Skill Execution

**Step 1 — Analyze Real-Time Requirements**:
- **Use case**: Server-push live dashboard for market data
- **Message patterns**: Unidirectional — server pushes updates to clients, clients subscribe to symbols
- **Scale**: ~2,000 concurrent viewers, ~500 upstream updates/second, fan-out to subscribers
- **Latency**: Sub-50ms from upstream feed to client display is critical for market data
- **Clients**: Web browsers with JavaScript
- **Durability**: Ephemeral — clients only need the latest values, not historical replay

**Step 2 — Design WebSocket Architecture**:
- **Protocol**: Raw WebSocket via gorilla/websocket (minimal overhead for high-frequency push)
- **Message schema**:
  ```json
  {
    "type": "market_data",
    "action": "price_update",
    "payload": {
      "symbol": "AAPL",
      "price": 182.45,
      "change": 1.23,
      "volume": 45892100,
      "timestamp": 1707735000000
    }
  }
  ```
- **Channel topology**: Topic per symbol — clients subscribe to specific symbols
- **Scaling**: Single Go server (goroutine-per-connection handles 2K connections easily)
- **Auth**: API key validated during HTTP upgrade via query parameter
- **Backpressure**: Per-client write buffer with drop-oldest policy for slow consumers

**Step 3 — Load Project Memory**:
```
memoryStore.getSkillMemory("websocket-engineer", "trading-platform")
→ Found existing memory: upstream feed uses NATS, internal services use protobuf
→ Applying: subscribe to NATS for upstream data, use JSON for browser clients
```

**Step 4 — Implement WebSocket System**:

Server (Go + gorilla/websocket):
```go
package main

import (
    "log"
    "net/http"
    "sync"
    "time"

    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
        origin := r.Header.Get("Origin")
        return isAllowedOrigin(origin)
    },
}

type Client struct {
    conn        *websocket.Conn
    send        chan []byte
    symbols     map[string]bool
    mu          sync.RWMutex
}

type Hub struct {
    clients    map[*Client]bool
    topics     map[string]map[*Client]bool
    register   chan *Client
    unregister chan *Client
    mu         sync.RWMutex
}

func (h *Hub) Run() {
    for {
        select {
        case client := <-h.register:
            h.mu.Lock()
            h.clients[client] = true
            h.mu.Unlock()
        case client := <-h.unregister:
            h.mu.Lock()
            if _, ok := h.clients[client]; ok {
                delete(h.clients, client)
                close(client.send)
                // Remove from all topic subscriptions
                for symbol := range client.symbols {
                    delete(h.topics[symbol], client)
                }
            }
            h.mu.Unlock()
        }
    }
}

func (h *Hub) Broadcast(symbol string, data []byte) {
    h.mu.RLock()
    defer h.mu.RUnlock()
    subscribers := h.topics[symbol]
    for client := range subscribers {
        select {
        case client.send <- data:
        default:
            // Drop message for slow consumer (backpressure)
            log.Printf("dropping message for slow client")
        }
    }
}

func serveWs(hub *Hub, w http.ResponseWriter, r *http.Request) {
    apiKey := r.URL.Query().Get("api_key")
    if !validateAPIKey(apiKey) {
        http.Error(w, "Unauthorized", http.StatusUnauthorized)
        return
    }

    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Printf("upgrade error: %v", err)
        return
    }

    conn.SetPingHandler(func(appData string) error {
        return conn.WriteControl(
            websocket.PongMessage, []byte(appData),
            time.Now().Add(10*time.Second),
        )
    })

    client := &Client{
        conn:    conn,
        send:    make(chan []byte, 256),
        symbols: make(map[string]bool),
    }
    hub.register <- client

    go client.writePump()
    go client.readPump(hub)
}
```

Client (JavaScript):
```javascript
class MarketDataClient {
  constructor(url, apiKey) {
    this.url = `${url}?api_key=${apiKey}`;
    this.reconnectDelay = 1000;
    this.maxReconnectDelay = 30000;
    this.handlers = new Map();
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      this.reconnectDelay = 1000;
      this.subscriptions.forEach((sym) => this.subscribe(sym));
    };

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "market_data") {
        const handler = this.handlers.get(msg.payload.symbol);
        if (handler) handler(msg.payload);
      }
    };

    this.ws.onclose = () => {
      setTimeout(() => this.connect(), this.reconnectDelay);
      this.reconnectDelay = Math.min(
        this.reconnectDelay * 2,
        this.maxReconnectDelay
      );
    };
  }

  subscribe(symbol) {
    this.ws.send(JSON.stringify({
      type: "subscribe", payload: { symbol }
    }));
  }
}
```

**Step 5 — Review & Output**:
- ✅ **Connection resilience**: Client reconnects with exponential backoff; server detects stale connections via ping/pong
- ✅ **Message integrity**: Backpressure via buffered channel with drop-oldest protects server from slow consumers
- ✅ **Security**: API key validated on upgrade, origin checking enabled
- ✅ **Scale readiness**: Go goroutine-per-connection model handles thousands of connections; NATS integration for upstream feed
- 📄 Output: `websocket_server_market_dashboard.md` generated to `/claudedocs/`
- 💾 Memory updated with Go WebSocket patterns and market data schema

---

## Example 3: Collaborative Editing System

### Scenario
Build a collaborative document editor using Python, Django Channels, and operational transforms so multiple users can edit the same document simultaneously.

### User Prompt
```
We're building a collaborative document editor like Google Docs. Multiple users editing the same document at the same time. We need to handle concurrent edits gracefully. Use Python and Django.
```

### Skill Execution

**Step 1 — Analyze Real-Time Requirements**:
- **Use case**: Collaborative real-time document editing with conflict resolution
- **Message patterns**: Bidirectional — clients send edit operations, server transforms and broadcasts
- **Scale**: ~50 concurrent editors per document, ~100 documents active simultaneously
- **Latency**: Sub-100ms for local echo, eventual consistency within 500ms across all clients
- **Clients**: Web browsers (React-based editor)
- **Durability**: Critical — every operation must be persisted for document reconstruction and undo history

**Step 2 — Design WebSocket Architecture**:
- **Protocol**: Django Channels with WebSocket consumers and channel layers
- **Message schema**:
  ```json
  {
    "type": "operation",
    "action": "transform",
    "payload": {
      "docId": "doc_789",
      "revision": 42,
      "ops": [
        { "retain": 10 },
        { "insert": "Hello " },
        { "retain": 85 }
      ],
      "clientId": "client_abc"
    },
    "correlationId": "op_xyz789"
  }
  ```
- **Channel topology**: One channel group per document (`document_{docId}`)
- **Scaling**: Redis channel layer for multi-worker deployment
- **Auth**: Django session auth validated in WebSocket consumer's `connect()` method
- **Conflict resolution**: Operational Transform (OT) — server maintains authoritative revision history

**Step 3 — Load Project Memory**:
```
memoryStore.getSkillMemory("websocket-engineer", "collab-editor")
→ No existing memory found. Greenfield collaborative editing implementation.
→ Noting: Django 5.x project, PostgreSQL database, Redis already in stack
```

**Step 4 — Implement WebSocket System**:

Django Channels consumer (Python):
```python
import json
from channels.generic.websocket import AsyncWebSocketConsumer
from channels.db import database_sync_to_async
from .ot_engine import OperationalTransform
from .models import Document, Operation


class DocumentConsumer(AsyncWebSocketConsumer):
    async def connect(self):
        self.doc_id = self.scope["url_route"]["kwargs"]["doc_id"]
        self.group_name = f"document_{self.doc_id}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close(code=4001)
            return

        if not await self.has_document_access(self.user, self.doc_id):
            await self.close(code=4003)
            return

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )
        await self.accept()

        # Send current document state and revision
        doc = await self.get_document(self.doc_id)
        await self.send(text_data=json.dumps({
            "type": "document",
            "action": "init",
            "payload": {
                "content": doc.content,
                "revision": doc.revision,
            },
        }))

        # Broadcast presence
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence.join",
                "userId": str(self.user.id),
                "username": self.user.username,
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "presence.leave",
                "userId": str(self.user.id),
            },
        )
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "operation" and data["action"] == "transform":
            await self.handle_operation(data["payload"])
        elif data["type"] == "cursor":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "cursor.update",
                    "userId": str(self.user.id),
                    "position": data["payload"]["position"],
                },
            )

    async def handle_operation(self, payload):
        client_revision = payload["revision"]
        client_ops = payload["ops"]
        client_id = payload["clientId"]

        # Transform against concurrent operations
        transformed_ops, new_revision = await self.apply_ot(
            self.doc_id, client_revision, client_ops
        )

        # Acknowledge to sender
        await self.send(text_data=json.dumps({
            "type": "operation",
            "action": "ack",
            "payload": {"revision": new_revision},
        }))

        # Broadcast transformed operation to other editors
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "operation.broadcast",
                "ops": transformed_ops,
                "revision": new_revision,
                "clientId": client_id,
                "sender_channel": self.channel_name,
            },
        )

    async def operation_broadcast(self, event):
        # Don't send back to the originating client
        if self.channel_name == event["sender_channel"]:
            return
        await self.send(text_data=json.dumps({
            "type": "operation",
            "action": "remote",
            "payload": {
                "ops": event["ops"],
                "revision": event["revision"],
                "clientId": event["clientId"],
            },
        }))

    async def presence_join(self, event):
        await self.send(text_data=json.dumps({
            "type": "presence",
            "action": "join",
            "payload": {
                "userId": event["userId"],
                "username": event["username"],
            },
        }))

    async def presence_leave(self, event):
        await self.send(text_data=json.dumps({
            "type": "presence",
            "action": "leave",
            "payload": {"userId": event["userId"]},
        }))

    async def cursor_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "cursor",
            "action": "move",
            "payload": {
                "userId": event["userId"],
                "position": event["position"],
            },
        }))

    @database_sync_to_async
    def apply_ot(self, doc_id, client_revision, client_ops):
        ot = OperationalTransform()
        doc = Document.objects.select_for_update().get(id=doc_id)
        server_ops = Operation.objects.filter(
            document=doc, revision__gt=client_revision
        ).order_by("revision")

        transformed = client_ops
        for server_op in server_ops:
            transformed, _ = ot.transform(transformed, server_op.ops)

        doc.content = ot.apply(doc.content, transformed)
        doc.revision += 1
        doc.save()

        Operation.objects.create(
            document=doc,
            revision=doc.revision,
            ops=transformed,
        )
        return transformed, doc.revision

    @database_sync_to_async
    def get_document(self, doc_id):
        return Document.objects.get(id=doc_id)

    @database_sync_to_async
    def has_document_access(self, user, doc_id):
        return Document.objects.filter(
            id=doc_id, collaborators=user
        ).exists()
```

Routing configuration:
```python
# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/document/(?P<doc_id>\w+)/$",
        consumers.DocumentConsumer.as_asgi(),
    ),
]
```

Channel layer configuration:
```python
# settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
            "capacity": 1500,
            "expiry": 10,
        },
    },
}
```

**Step 5 — Review & Output**:
- ✅ **Connection resilience**: Django Channels handles reconnection; client re-syncs document state on reconnect
- ✅ **Message integrity**: Operational Transform guarantees eventual consistency; all operations persisted with revision numbers
- ✅ **Security**: Django session auth on connect, per-document access control, close codes for auth failures
- ✅ **Scale readiness**: Redis channel layer for multi-worker; `select_for_update` prevents race conditions on OT
- 📄 Output: `websocket_collab_editor.md` generated to `/claudedocs/`
- 💾 Memory updated with Django Channels patterns, OT message schema, and channel layer configuration

---

## Summary of Patterns

1. **Chat (Socket.IO)** — Bidirectional messaging with rooms, presence, and JWT auth
2. **Live Dashboard (gorilla/websocket)** — Server push with topic subscriptions and backpressure
3. **Collaborative Editing (Django Channels)** — Bidirectional OT with conflict resolution and persistence

## Best Practices

- Always authenticate during the WebSocket upgrade, not after connection
- Implement exponential backoff with jitter for client reconnection
- Use buffered channels or queues to handle backpressure from slow consumers
- Design message schemas with a type/action envelope for extensibility
- Track message correlation IDs for debugging and deduplication
- Plan for horizontal scaling from day one — use Redis pub/sub or a message broker
- Test with realistic concurrent connection counts and message rates
- Monitor WebSocket-specific metrics: connection count, message rate, latency, error rate
