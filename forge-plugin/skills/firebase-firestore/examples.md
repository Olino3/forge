# Firebase Firestore Skill Examples

This file demonstrates typical usage scenarios for the `firebase-firestore` skill.

---

## Example 1: E-Commerce Product Catalog with Real-Time Inventory

### Scenario

An e-commerce application needs a Firestore-backed product catalog with real-time inventory tracking. Products are organized by categories, and inventory must update in real-time across all connected clients.

### User Request

"I need to design a Firestore database for our e-commerce app. We have products organized by categories, and we need real-time inventory updates so customers see accurate stock levels. We're using the Web v9 modular SDK."

### Skill Workflow

**Step 1: Initial Analysis**
- Application type: Web (React)
- SDK: Firebase Web v9 (modular)
- Key requirements: Product catalog, categories, real-time inventory, search by category
- Real-time needs: Inventory counts, product availability

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("firebase-firestore", "ecommerce-app")` → No existing memory (first-time setup)

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load NoSQL data modeling patterns
- Review denormalization strategies for read-heavy workloads

**Step 4: Firestore Implementation**

**Collection Structure:**
```
products/
├── {productId}/
│   ├── name: string
│   ├── description: string
│   ├── price: number
│   ├── categoryId: string
│   ├── categoryName: string          # Denormalized for query display
│   ├── images: string[]
│   ├── tags: string[]
│   ├── inventory: number
│   ├── isAvailable: boolean
│   ├── rating: number
│   ├── reviewCount: number
│   ├── createdAt: timestamp
│   └── updatedAt: timestamp
│
categories/
├── {categoryId}/
│   ├── name: string
│   ├── slug: string
│   ├── productCount: number          # Aggregation field
│   ├── parentCategoryId: string|null
│   └── sortOrder: number
│
orders/
├── {orderId}/
│   ├── userId: string
│   ├── status: string
│   ├── total: number
│   ├── createdAt: timestamp
│   └── items/ (subcollection)
│       └── {itemId}/
│           ├── productId: string
│           ├── productName: string   # Denormalized snapshot
│           ├── price: number         # Price at time of order
│           ├── quantity: number
│           └── subtotal: number
```

**Security Rules:**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Products: anyone can read, only admins can write
    match /products/{productId} {
      allow read: if true;
      allow create, update: if isAdmin();
      allow delete: if isAdmin();

      function isValidProduct() {
        let data = request.resource.data;
        return data.name is string
            && data.name.size() > 0
            && data.name.size() <= 200
            && data.price is number
            && data.price > 0
            && data.inventory is int
            && data.inventory >= 0
            && data.categoryId is string;
      }
    }

    // Categories: anyone can read, only admins can write
    match /categories/{categoryId} {
      allow read: if true;
      allow write: if isAdmin();
    }

    // Orders: users can read/create their own, admins can read all
    match /orders/{orderId} {
      allow read: if isOwner(resource.data.userId) || isAdmin();
      allow create: if isAuthenticated()
                    && request.resource.data.userId == request.auth.uid;
      allow update: if isAdmin();

      match /items/{itemId} {
        allow read: if isOwner(get(/databases/$(database)/documents/orders/$(orderId)).data.userId)
                    || isAdmin();
        allow write: if isAuthenticated()
                     && get(/databases/$(database)/documents/orders/$(orderId)).data.userId == request.auth.uid;
      }
    }

    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }

    function isAdmin() {
      return isAuthenticated()
          && request.auth.token.role == 'admin';
    }

    function isOwner(userId) {
      return isAuthenticated()
          && request.auth.uid == userId;
    }
  }
}
```

**Query Implementation (Web v9 Modular SDK):**
```javascript
import {
  collection, query, where, orderBy, limit,
  startAfter, getDocs, onSnapshot, doc, runTransaction,
  writeBatch, serverTimestamp, increment
} from 'firebase/firestore';

// --- Product Queries ---

// Get products by category with pagination
async function getProductsByCategory(db, categoryId, pageSize = 20, lastDoc = null) {
  let q = query(
    collection(db, 'products'),
    where('categoryId', '==', categoryId),
    where('isAvailable', '==', true),
    orderBy('rating', 'desc'),
    limit(pageSize)
  );

  if (lastDoc) {
    q = query(q, startAfter(lastDoc));
  }

  const snapshot = await getDocs(q);
  return {
    products: snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })),
    lastDoc: snapshot.docs[snapshot.docs.length - 1] || null,
    hasMore: snapshot.docs.length === pageSize
  };
}

// Real-time inventory listener
function subscribeToProductInventory(db, productId, callback) {
  const productRef = doc(db, 'products', productId);

  return onSnapshot(productRef,
    (snapshot) => {
      if (snapshot.exists()) {
        const data = snapshot.data();
        callback({
          inventory: data.inventory,
          isAvailable: data.isAvailable,
          fromCache: snapshot.metadata.fromCache,
          hasPendingWrites: snapshot.metadata.hasPendingWrites
        });
      }
    },
    (error) => {
      console.error('Inventory listener error:', error);
      callback({ error: error.code });
    }
  );
}

// Atomic inventory decrement on purchase (transaction)
async function purchaseProduct(db, productId, quantity) {
  return runTransaction(db, async (transaction) => {
    const productRef = doc(db, 'products', productId);
    const productSnap = await transaction.get(productRef);

    if (!productSnap.exists()) {
      throw new Error('Product not found');
    }

    const currentInventory = productSnap.data().inventory;
    if (currentInventory < quantity) {
      throw new Error('Insufficient inventory');
    }

    const newInventory = currentInventory - quantity;
    transaction.update(productRef, {
      inventory: newInventory,
      isAvailable: newInventory > 0,
      updatedAt: serverTimestamp()
    });

    return { newInventory };
  });
}
```

**Composite Indexes (firestore.indexes.json):**
```json
{
  "indexes": [
    {
      "collectionGroup": "products",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "categoryId", "order": "ASCENDING" },
        { "fieldPath": "isAvailable", "order": "ASCENDING" },
        { "fieldPath": "rating", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "products",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "isAvailable", "order": "ASCENDING" },
        { "fieldPath": "price", "order": "ASCENDING" }
      ]
    },
    {
      "collectionGroup": "orders",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "userId", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

**Step 5: Generate Output**
- Saved to `/claudedocs/firebase-firestore_ecommerce-app_2025-07-14.md`
- Deliverables: Collection schemas, `firestore.rules`, `firestore.indexes.json`, query implementation code

**Step 6: Update Memory**
- Created `collection_structure.md` with product/category/order hierarchy
- Created `security_rules.md` with RBAC pattern (admin + owner)
- Created `query_patterns.md` with pagination and real-time inventory patterns
- Created `data_model.md` with denormalization decisions (categoryName in products)
- Created `performance_config.md` with composite index definitions

---

## Example 2: Chat Application with Real-Time Messaging

### Scenario

A chat application requires real-time messaging with support for direct messages and group chats. Messages must sync instantly across devices and work offline.

### User Request

"I'm building a chat app with Flutter. I need real-time messaging for both 1-on-1 and group chats. Messages should work offline and sync when back online. Users need to see typing indicators and read receipts."

### Skill Workflow

**Step 1: Initial Analysis**
- Application type: Mobile (Flutter)
- SDK: FlutterFire (cloud_firestore package)
- Key requirements: Real-time messaging, group chats, offline support, presence
- Real-time needs: Messages, typing indicators, read receipts, online status

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("firebase-firestore", "chat-app")` → No existing memory

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load real-time data modeling patterns

**Step 4: Firestore Implementation**

**Collection Structure:**
```
users/
├── {userId}/
│   ├── displayName: string
│   ├── avatarUrl: string
│   ├── status: 'online' | 'offline' | 'away'
│   ├── lastSeen: timestamp
│   └── fcmToken: string

chats/
├── {chatId}/
│   ├── type: 'direct' | 'group'
│   ├── name: string|null              # null for direct messages
│   ├── participants: string[]          # Array of user IDs (max ~100)
│   ├── participantDetails: map        # Denormalized { [userId]: { name, avatar } }
│   ├── lastMessage: map               # Denormalized { text, senderId, senderName, timestamp }
│   ├── createdAt: timestamp
│   ├── updatedAt: timestamp
│   │
│   ├── messages/ (subcollection)
│   │   └── {messageId}/
│   │       ├── text: string
│   │       ├── senderId: string
│   │       ├── senderName: string     # Denormalized for display
│   │       ├── type: 'text' | 'image' | 'file' | 'system'
│   │       ├── mediaUrl: string|null
│   │       ├── readBy: map            # { [userId]: timestamp }
│   │       ├── createdAt: timestamp
│   │       └── editedAt: timestamp|null
│   │
│   └── typing/ (subcollection)
│       └── {userId}/
│           ├── isTyping: boolean
│           └── updatedAt: timestamp
```

**Security Rules:**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    match /users/{userId} {
      allow read: if isAuthenticated();
      allow write: if isOwner(userId);
    }

    match /chats/{chatId} {
      allow read: if isParticipant(chatId);
      allow create: if isAuthenticated()
                    && request.resource.data.participants.hasAny([request.auth.uid]);
      allow update: if isParticipant(chatId)
                    && onlyUpdatingAllowedFields(['lastMessage', 'updatedAt', 'name']);

      match /messages/{messageId} {
        allow read: if isParticipant(chatId);
        allow create: if isParticipant(chatId)
                      && request.resource.data.senderId == request.auth.uid
                      && request.resource.data.text is string
                      && request.resource.data.text.size() > 0
                      && request.resource.data.text.size() <= 5000;
        allow update: if isParticipant(chatId)
                      && (request.resource.data.senderId == request.auth.uid
                          || onlyUpdatingAllowedFields(['readBy']));
      }

      match /typing/{userId} {
        allow read: if isParticipant(chatId);
        allow write: if isOwner(userId) && isParticipant(chatId);
      }
    }

    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return request.auth.uid == userId;
    }

    function isParticipant(chatId) {
      return isAuthenticated()
          && request.auth.uid in get(/databases/$(database)/documents/chats/$(chatId)).data.participants;
    }

    function onlyUpdatingAllowedFields(allowedFields) {
      return request.resource.data.diff(resource.data).affectedKeys().hasOnly(allowedFields);
    }
  }
}
```

**Query Implementation (Flutter/Dart):**
```dart
import 'package:cloud_firestore/cloud_firestore.dart';

class ChatService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  // Get user's chats ordered by most recent message
  Stream<List<Chat>> getUserChats(String userId) {
    return _db
        .collection('chats')
        .where('participants', arrayContains: userId)
        .orderBy('updatedAt', descending: true)
        .limit(50)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => Chat.fromFirestore(doc))
            .toList());
  }

  // Real-time message listener with pagination
  Stream<List<Message>> getChatMessages(String chatId, {int pageSize = 30}) {
    return _db
        .collection('chats')
        .doc(chatId)
        .collection('messages')
        .orderBy('createdAt', descending: true)
        .limit(pageSize)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => Message.fromFirestore(doc))
            .toList()
            .reversed
            .toList());
  }

  // Send message with denormalized last message update (batch write)
  Future<void> sendMessage(String chatId, String userId, String text) async {
    final batch = _db.batch();

    // Add message to subcollection
    final messageRef = _db
        .collection('chats')
        .doc(chatId)
        .collection('messages')
        .doc();

    batch.set(messageRef, {
      'text': text,
      'senderId': userId,
      'senderName': await _getUserName(userId),
      'type': 'text',
      'readBy': {userId: FieldValue.serverTimestamp()},
      'createdAt': FieldValue.serverTimestamp(),
    });

    // Update chat's lastMessage (denormalized)
    final chatRef = _db.collection('chats').doc(chatId);
    batch.update(chatRef, {
      'lastMessage': {
        'text': text.length > 100 ? '${text.substring(0, 100)}...' : text,
        'senderId': userId,
        'timestamp': FieldValue.serverTimestamp(),
      },
      'updatedAt': FieldValue.serverTimestamp(),
    });

    // Clear typing indicator
    final typingRef = _db
        .collection('chats')
        .doc(chatId)
        .collection('typing')
        .doc(userId);
    batch.set(typingRef, {'isTyping': false, 'updatedAt': FieldValue.serverTimestamp()});

    await batch.commit();
  }

  // Typing indicator
  Future<void> setTypingStatus(String chatId, String userId, bool isTyping) {
    return _db
        .collection('chats')
        .doc(chatId)
        .collection('typing')
        .doc(userId)
        .set({
          'isTyping': isTyping,
          'updatedAt': FieldValue.serverTimestamp(),
        });
  }

  // Mark messages as read
  Future<void> markAsRead(String chatId, String userId, List<String> messageIds) async {
    final batch = _db.batch();
    for (final messageId in messageIds) {
      final ref = _db
          .collection('chats')
          .doc(chatId)
          .collection('messages')
          .doc(messageId);
      batch.update(ref, {'readBy.$userId': FieldValue.serverTimestamp()});
    }
    await batch.commit();
  }

  // Configure offline persistence (call once at app startup)
  static void configureOfflinePersistence() {
    FirebaseFirestore.instance.settings = const Settings(
      persistenceEnabled: true,
      cacheSizeBytes: Settings.CACHE_SIZE_UNLIMITED,
    );
  }

  Future<String> _getUserName(String userId) async {
    final doc = await _db.collection('users').doc(userId).get();
    return doc.data()?['displayName'] ?? 'Unknown';
  }
}
```

**Composite Indexes:**
```json
{
  "indexes": [
    {
      "collectionGroup": "chats",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "participants", "arrayConfig": "CONTAINS" },
        { "fieldPath": "updatedAt", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "messages",
      "queryScope": "COLLECTION_GROUP",
      "fields": [
        { "fieldPath": "senderId", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

**Step 5: Generate Output**
- Saved to `/claudedocs/firebase-firestore_chat-app_2025-07-14.md`
- Deliverables: Collection schemas, security rules, Flutter service class, indexes

**Step 6: Update Memory**
- Created `collection_structure.md` with chat/message/typing hierarchy
- Created `security_rules.md` with participant-based access control
- Created `query_patterns.md` with real-time listeners and pagination
- Created `data_model.md` with denormalized lastMessage pattern
- Created `performance_config.md` with offline persistence settings

---

## Example 3: Security Rules Design for Multi-Tenant SaaS

### Scenario

A multi-tenant SaaS application needs strict data isolation between tenants with role-based access control within each tenant. The system supports organizations with members, projects, and tasks.

### User Request

"We're building a multi-tenant project management SaaS. Each organization has members with different roles (owner, admin, member, viewer). We need security rules that enforce complete data isolation between organizations and role-based access within each org. Using the Web v9 SDK with Admin SDK on the backend."

### Skill Workflow

**Step 1: Initial Analysis**
- Application type: Web (React) + Server (Node.js with Admin SDK)
- SDKs: Web v9 modular (client), Firebase Admin SDK (server)
- Key requirements: Multi-tenancy, data isolation, RBAC, audit trail
- Security requirements: Organization-level isolation, role hierarchy

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("firebase-firestore", "saas-platform")` → No existing memory

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load security and multi-tenant patterns

**Step 4: Firestore Implementation**

**Collection Structure:**
```
organizations/
├── {orgId}/
│   ├── name: string
│   ├── plan: 'free' | 'pro' | 'enterprise'
│   ├── ownerId: string
│   ├── createdAt: timestamp
│   ├── settings: map
│   │
│   ├── members/ (subcollection)
│   │   └── {userId}/
│   │       ├── role: 'owner' | 'admin' | 'member' | 'viewer'
│   │       ├── email: string
│   │       ├── displayName: string
│   │       ├── joinedAt: timestamp
│   │       └── invitedBy: string
│   │
│   ├── projects/ (subcollection)
│   │   └── {projectId}/
│   │       ├── name: string
│   │       ├── description: string
│   │       ├── status: 'active' | 'archived'
│   │       ├── createdBy: string
│   │       ├── createdAt: timestamp
│   │       ├── taskCount: number          # Distributed counter
│   │       ├── completedTaskCount: number
│   │       │
│   │       └── tasks/ (subcollection)
│   │           └── {taskId}/
│   │               ├── title: string
│   │               ├── description: string
│   │               ├── status: 'todo' | 'in_progress' | 'review' | 'done'
│   │               ├── priority: 'low' | 'medium' | 'high' | 'urgent'
│   │               ├── assigneeId: string|null
│   │               ├── assigneeName: string|null
│   │               ├── createdBy: string
│   │               ├── dueDate: timestamp|null
│   │               ├── tags: string[]
│   │               ├── createdAt: timestamp
│   │               └── updatedAt: timestamp
│   │
│   └── auditLog/ (subcollection)
│       └── {logId}/
│           ├── action: string
│           ├── userId: string
│           ├── userName: string
│           ├── resource: string
│           ├── resourceId: string
│           ├── details: map
│           └── createdAt: timestamp

userProfiles/
├── {userId}/
│   ├── email: string
│   ├── displayName: string
│   ├── organizations: string[]           # List of org IDs for quick lookup
│   └── lastActiveOrg: string
```

**Security Rules:**
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // ============================================================
    // USER PROFILES
    // ============================================================
    match /userProfiles/{userId} {
      allow read: if isAuthenticated();
      allow write: if isOwner(userId);
    }

    // ============================================================
    // ORGANIZATIONS (Multi-Tenant Root)
    // ============================================================
    match /organizations/{orgId} {

      // Only members can read org details
      allow read: if isMember(orgId);

      // Only authenticated users can create orgs (they become owner)
      allow create: if isAuthenticated()
                    && request.resource.data.ownerId == request.auth.uid;

      // Only owners can update org settings
      allow update: if hasRole(orgId, ['owner']);

      // Only owners can delete (with caution)
      allow delete: if hasRole(orgId, ['owner']);

      // ----------------------------------------------------------
      // MEMBERS subcollection
      // ----------------------------------------------------------
      match /members/{memberId} {
        // All members can read the member list
        allow read: if isMember(orgId);

        // Admins+ can add members
        allow create: if hasRole(orgId, ['owner', 'admin']);

        // Admins+ can update roles (but not promote above own level)
        allow update: if hasRole(orgId, ['owner', 'admin'])
                      && !isEscalatingRole();

        // Owners can remove anyone; admins can remove members/viewers
        allow delete: if hasRole(orgId, ['owner'])
                      || (hasRole(orgId, ['admin'])
                          && resource.data.role in ['member', 'viewer']);
      }

      // ----------------------------------------------------------
      // PROJECTS subcollection
      // ----------------------------------------------------------
      match /projects/{projectId} {
        // All members can read projects
        allow read: if isMember(orgId);

        // Members+ can create projects
        allow create: if hasRole(orgId, ['owner', 'admin', 'member'])
                      && isValidProject();

        // Members+ can update projects
        allow update: if hasRole(orgId, ['owner', 'admin', 'member']);

        // Admins+ can delete/archive projects
        allow delete: if hasRole(orgId, ['owner', 'admin']);

        // --------------------------------------------------------
        // TASKS subcollection
        // --------------------------------------------------------
        match /tasks/{taskId} {
          // All members can read tasks
          allow read: if isMember(orgId);

          // Members+ can create tasks
          allow create: if hasRole(orgId, ['owner', 'admin', 'member'])
                        && isValidTask();

          // Members+ can update tasks (assignee, status, etc.)
          allow update: if hasRole(orgId, ['owner', 'admin', 'member']);

          // Admins+ can delete tasks
          allow delete: if hasRole(orgId, ['owner', 'admin']);
        }
      }

      // ----------------------------------------------------------
      // AUDIT LOG subcollection (append-only)
      // ----------------------------------------------------------
      match /auditLog/{logId} {
        // Admins+ can read audit logs
        allow read: if hasRole(orgId, ['owner', 'admin']);

        // System writes only (via Admin SDK); no client writes
        allow write: if false;
      }
    }

    // ============================================================
    // HELPER FUNCTIONS
    // ============================================================

    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return request.auth.uid == userId;
    }

    function isMember(orgId) {
      return isAuthenticated()
          && exists(/databases/$(database)/documents/organizations/$(orgId)/members/$(request.auth.uid));
    }

    function getMemberRole(orgId) {
      return get(/databases/$(database)/documents/organizations/$(orgId)/members/$(request.auth.uid)).data.role;
    }

    function hasRole(orgId, allowedRoles) {
      return isMember(orgId)
          && getMemberRole(orgId) in allowedRoles;
    }

    function isEscalatingRole() {
      // Prevent admin from setting role to 'owner'
      return request.resource.data.role == 'owner'
          && getMemberRole(resource.data.__name__.split('/')[3]) != 'owner';
    }

    function isValidProject() {
      let data = request.resource.data;
      return data.name is string
          && data.name.size() > 0
          && data.name.size() <= 100
          && data.createdBy == request.auth.uid;
    }

    function isValidTask() {
      let data = request.resource.data;
      return data.title is string
          && data.title.size() > 0
          && data.title.size() <= 200
          && data.status in ['todo', 'in_progress', 'review', 'done']
          && data.priority in ['low', 'medium', 'high', 'urgent']
          && data.createdBy == request.auth.uid;
    }
  }
}
```

**Query Implementation (Web v9 + Admin SDK):**
```javascript
// === CLIENT-SIDE (Web v9 Modular) ===
import {
  collection, query, where, orderBy, limit,
  startAfter, getDocs, onSnapshot, collectionGroup
} from 'firebase/firestore';

// Get all tasks assigned to current user across all projects in an org
async function getMyTasks(db, orgId, userId, status = null) {
  const tasksRef = collectionGroup(db, 'tasks');
  const constraints = [
    where('assigneeId', '==', userId),
    orderBy('dueDate', 'asc'),
    limit(50)
  ];

  if (status) {
    constraints.splice(1, 0, where('status', '==', status));
  }

  const q = query(tasksRef, ...constraints);
  const snapshot = await getDocs(q);

  return snapshot.docs.map(doc => ({
    id: doc.id,
    projectId: doc.ref.parent.parent.id,
    ...doc.data()
  }));
}

// Real-time project tasks listener
function subscribeToProjectTasks(db, orgId, projectId, callback) {
  const q = query(
    collection(db, `organizations/${orgId}/projects/${projectId}/tasks`),
    orderBy('updatedAt', 'desc'),
    limit(100)
  );

  return onSnapshot(q,
    (snapshot) => {
      const changes = snapshot.docChanges().map(change => ({
        type: change.type,   // 'added' | 'modified' | 'removed'
        task: { id: change.doc.id, ...change.doc.data() }
      }));
      callback({
        tasks: snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })),
        changes,
        fromCache: snapshot.metadata.fromCache
      });
    },
    (error) => {
      console.error('Tasks listener error:', error);
      callback({ error: error.code });
    }
  );
}

// === SERVER-SIDE (Admin SDK for Audit Logging) ===
const admin = require('firebase-admin');

async function writeAuditLog(orgId, action, userId, userName, resource, resourceId, details) {
  const db = admin.firestore();
  await db
    .collection('organizations')
    .doc(orgId)
    .collection('auditLog')
    .add({
      action,
      userId,
      userName,
      resource,
      resourceId,
      details,
      createdAt: admin.firestore.FieldValue.serverTimestamp()
    });
}

// Admin SDK: Set custom claims for role-based access
async function setUserOrgRole(userId, orgId, role) {
  const db = admin.firestore();

  // Update Firestore member document
  await db
    .collection('organizations')
    .doc(orgId)
    .collection('members')
    .doc(userId)
    .set({ role, updatedAt: admin.firestore.FieldValue.serverTimestamp() }, { merge: true });

  // Write audit log
  await writeAuditLog(orgId, 'ROLE_CHANGE', userId, '', 'member', userId, { newRole: role });
}
```

**Composite Indexes:**
```json
{
  "indexes": [
    {
      "collectionGroup": "tasks",
      "queryScope": "COLLECTION_GROUP",
      "fields": [
        { "fieldPath": "assigneeId", "order": "ASCENDING" },
        { "fieldPath": "dueDate", "order": "ASCENDING" }
      ]
    },
    {
      "collectionGroup": "tasks",
      "queryScope": "COLLECTION_GROUP",
      "fields": [
        { "fieldPath": "assigneeId", "order": "ASCENDING" },
        { "fieldPath": "status", "order": "ASCENDING" },
        { "fieldPath": "dueDate", "order": "ASCENDING" }
      ]
    },
    {
      "collectionGroup": "tasks",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "status", "order": "ASCENDING" },
        { "fieldPath": "priority", "order": "DESCENDING" },
        { "fieldPath": "updatedAt", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "auditLog",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "userId", "order": "ASCENDING" },
        { "fieldPath": "createdAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

**Step 5: Generate Output**
- Saved to `/claudedocs/firebase-firestore_saas-platform_2025-07-14.md`
- Deliverables: Multi-tenant collection schemas, comprehensive security rules, client + server query implementations, composite indexes, audit logging

**Step 6: Update Memory**
- Created `collection_structure.md` with org → members/projects/tasks hierarchy
- Created `security_rules.md` with multi-tenant RBAC pattern, helper functions, role escalation prevention
- Created `query_patterns.md` with collection group queries, real-time task listeners
- Created `data_model.md` with multi-tenant isolation via subcollections, denormalized assignee names
- Created `performance_config.md` with collection group index strategy, audit log write patterns

---

## Common Patterns

### Pattern 1: Distributed Counter
```javascript
// For high-write counters (e.g., page views, likes)
import { doc, runTransaction, increment } from 'firebase/firestore';

async function incrementCounter(db, counterRef, numShards = 10) {
  const shardId = Math.floor(Math.random() * numShards);
  const shardRef = doc(counterRef, 'shards', `${shardId}`);
  await runTransaction(db, async (transaction) => {
    transaction.set(shardRef, { count: increment(1) }, { merge: true });
  });
}
```

### Pattern 2: Pagination with Cursors
```javascript
import { query, collection, orderBy, limit, startAfter, getDocs } from 'firebase/firestore';

async function paginateCollection(db, path, field, pageSize, lastDoc) {
  let q = query(collection(db, path), orderBy(field), limit(pageSize));
  if (lastDoc) {
    q = query(q, startAfter(lastDoc));
  }
  const snapshot = await getDocs(q);
  return {
    docs: snapshot.docs,
    hasMore: snapshot.docs.length === pageSize
  };
}
```

### Pattern 3: Listener Lifecycle (React)
```javascript
import { useEffect, useState } from 'react';
import { onSnapshot, query, collection, where } from 'firebase/firestore';

function useFirestoreQuery(db, path, constraints) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const q = query(collection(db, path), ...constraints);
    const unsubscribe = onSnapshot(q,
      (snapshot) => {
        setData(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })));
        setLoading(false);
      },
      (err) => {
        setError(err);
        setLoading(false);
      }
    );
    // Always clean up listener
    return () => unsubscribe();
  }, [db, path, JSON.stringify(constraints)]);

  return { data, loading, error };
}
```

---

## Tips for Using Firebase Firestore Skill

1. **Start with queries**: Design your data model around the queries you need, not entities
2. **Denormalize deliberately**: Accept write complexity to simplify reads
3. **Test security rules first**: Use the Firebase Emulator before deploying
4. **Monitor costs**: Track document reads/writes in the Firebase Console
5. **Use batch writes**: Group related writes for atomicity (max 500 operations)
6. **Paginate everything**: Never fetch an entire collection
7. **Scope listeners tightly**: Only listen to data the user currently sees
8. **Handle offline gracefully**: Design UI to indicate cached vs fresh data
