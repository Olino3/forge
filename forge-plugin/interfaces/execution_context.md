# ExecutionContext Interface

**Version**: 1.0.0
**Status**: Phase 4 - Interface Definition

## Purpose

The ExecutionContext interface enables **command chaining with context passthrough** — allowing sequential command invocations (e.g., `/brainstorm` → `/implement` → `/test`) to share loaded context, discovered project information, and accumulated results without redundant reloading.

### What It Replaces

Commands currently operate in isolation. When a user runs `/brainstorm` followed by `/implement`, the second command:
- Reloads all context files from scratch
- Re-detects the project type
- Re-reads memory that was just written by the previous command
- Has no knowledge of what the previous command discovered or decided

The ExecutionContext provides a shared state container that persists across chained command invocations within a single session.

---

## Types

### ExecutionState

Captures the accumulated state of a command chain session.

```
ExecutionState {
  sessionId: string           // Unique identifier for this command chain
  startedAt: string           // ISO 8601 timestamp
  projectName: string         // Detected or user-specified project name
  projectType: string         // Detected project type (python, angular, dotnet, etc.)
  
  loadedContext: Map<string, string>   // domain:topic → content (already loaded)
  loadedMemory: Map<string, string>    // layer:key → content (already loaded)
  
  commandHistory: CommandExecution[]   // Ordered list of commands executed
  sharedData: Map<string, any>        // Arbitrary data passed between commands
}
```

### CommandExecution

Records the execution of a single command in a chain.

```
CommandExecution {
  command: string             // Command name (e.g., "brainstorm", "implement")
  startedAt: string           // ISO 8601 timestamp
  completedAt: string         // ISO 8601 timestamp
  status: "success" | "partial" | "failed"
  
  inputs: Map<string, any>    // Arguments/flags passed to the command
  outputs: Map<string, any>   // Key results produced by the command
  
  contextLoaded: string[]     // List of context files loaded (domain:topic keys)
  memoryUpdated: string[]     // List of memory files updated (layer:key keys)
  skillsInvoked: string[]     // List of skills invoked during execution
}
```

---

## Interface Methods

### `create(projectName, projectType) → ExecutionState`

Create a new execution context for a command chain session.

**When to use**: At the start of the first command in a chain, or when no existing context is available.

**Behavior**:
- Generates a unique `sessionId`
- Sets `startedAt` to current timestamp
- Initializes empty maps for context, memory, and shared data
- Returns the new `ExecutionState`

---

### `getOrCreate(projectName) → ExecutionState`

Retrieve an existing execution context for the current session, or create a new one.

**When to use**: At the start of any command — handles both first-in-chain and continuation scenarios.

**Behavior**:
- If an active session exists for the project, returns it
- If no session exists, creates a new one via `create()`
- Ensures commands don't need to know if they're first in a chain

---

### `recordContextLoad(state, domain, topic, content) → ExecutionState`

Record that a context file was loaded, caching it for subsequent commands.

**When to use**: After calling `contextProvider.getConditionalContext()`.

**Behavior**:
- Stores content in `loadedContext` under `domain:topic` key
- Adds key to current `CommandExecution.contextLoaded`
- Returns updated state

---

### `getCachedContext(state, domain, topic) → string | null`

Check if context was already loaded in a previous command in the chain.

**When to use**: Before calling `contextProvider.getConditionalContext()` — avoids redundant file reads.

**Behavior**:
- Returns cached content if `domain:topic` exists in `loadedContext`
- Returns `null` if not previously loaded
- Commands should fall through to `contextProvider` on cache miss

---

### `recordMemoryLoad(state, layer, key, content) → ExecutionState`

Record that memory was loaded, caching it for subsequent commands.

**When to use**: After calling `memoryStore.getCommandMemory()` or similar.

---

### `getCachedMemory(state, layer, key) → string | null`

Check if memory was already loaded in a previous command.

**When to use**: Before calling `memoryStore` methods — avoids re-reading memory that was just written.

---

### `setSharedData(state, key, value) → ExecutionState`

Store arbitrary data for use by subsequent commands in the chain.

**When to use**: When a command produces results that downstream commands need.

**Examples**:
- `/brainstorm` stores requirements as `sharedData["requirements"]`
- `/implement` reads `sharedData["requirements"]` to know what to build
- `/test` reads `sharedData["implementation_files"]` to know what to test

---

### `getSharedData(state, key) → any | null`

Retrieve data stored by a previous command in the chain.

**When to use**: At the start of a command to check if upstream commands provided relevant context.

---

### `startCommand(state, command, inputs) → ExecutionState`

Record the start of a new command execution in the chain.

**When to use**: At the beginning of every command's Step 1.

**Behavior**:
- Creates a new `CommandExecution` entry
- Sets `startedAt` to current timestamp
- Records command name and inputs

---

### `completeCommand(state, command, status, outputs) → ExecutionState`

Record the completion of a command execution.

**When to use**: At the end of every command's execution.

**Behavior**:
- Sets `completedAt` on the current `CommandExecution`
- Records status and outputs
- Updates `commandHistory`

---

### `getPreviousCommand(state, command?) → CommandExecution | null`

Get the execution record of a previous command in the chain.

**When to use**: When a command needs to check what a specific prior command did.

**Parameters**:
- `command` (optional): Specific command name to look up. If omitted, returns the most recent.

---

## Integration Pattern

### In COMMAND.md Files

Commands integrate ExecutionContext alongside ContextProvider and MemoryStore:

```markdown
### Step 1: Understand Request
1. Parse user input and flags
2. `executionContext.getOrCreate(projectName)` — get or start session
3. `executionContext.startCommand(state, "implement", inputs)`

### Step 2: Load Context & Memory (with caching)
1. Check cache first: `executionContext.getCachedContext(state, "commands", "implementation_patterns")`
2. On cache miss: `contextProvider.getConditionalContext("commands", "implementation_patterns")`
3. Record load: `executionContext.recordContextLoad(state, "commands", "implementation_patterns", content)`

### Step N: Check Upstream Data
1. Check if brainstorm provided requirements: `executionContext.getSharedData(state, "requirements")`
2. If available, skip requirements gathering step

### Final: Complete
1. `executionContext.setSharedData(state, "implementation_files", files)`
2. `executionContext.completeCommand(state, "implement", "success", outputs)`
```

### Common Command Chains

| Chain | Shared Data Flow |
|-------|-----------------|
| `/brainstorm` → `/implement` | Requirements, architecture decisions, tech choices |
| `/implement` → `/test` | Implementation files, function signatures, test targets |
| `/analyze` → `/improve` | Analysis findings, severity rankings, fix suggestions |
| `/brainstorm` → `/implement` → `/test` | Full chain: requirements → code → validation |
| `/azure-function` → `/azure-pipeline` | Function config, deployment targets, resource group |

---

## Interface References

- **ContextProvider**: [context_provider.md](context_provider.md) — used for loading context on cache miss
- **MemoryStore**: [memory_store.md](memory_store.md) — used for loading/storing memory on cache miss
- **SkillInvoker**: [skill_invoker.md](skill_invoker.md) — skills invoked are tracked in `CommandExecution`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-10 | Initial interface definition (Phase 4) |
