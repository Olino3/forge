---
name: mcp-developer
## description: Guides the development and integration of Model Context Protocol (MCP) servers — from architecture design and tool registration to resource exposure, prompt templates, and client integration. Covers transport layer selection (stdio/SSE), JSON Schema-based input validation, security sandboxing, and testing with MCP Inspector. Like Hephaestus designing the divine automatons that served the gods, this skill ensures every MCP server is robust, well-structured, and seamlessly connects AI assistants to the tools and data they need.

# MCP Server Developer

## ⚠️ MANDATORY COMPLIANCE ⚠️

**CRITICAL**: The 5-step workflow outlined in this document MUST be followed in exact order for EVERY MCP server development task. Skipping steps or deviating from the procedure will result in incomplete or insecure server implementations. This is non-negotiable.

## File Structure

- **SKILL.md** (this file): Main instructions and MANDATORY workflow
- **examples.md**: Usage scenarios with different MCP server types and integration patterns
- **Memory**: Project-specific memory accessed via `memoryStore.getSkillMemory("mcp-developer", "{project-name}")`. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **ContextProvider**: `contextProvider.getIndex("mcp")` — Load MCP-related context. See [ContextProvider Interface](../../interfaces/context_provider.md).
- **MemoryStore**: `memoryStore.getSkillMemory("mcp-developer", "{project-name}")` — Read/write project-specific MCP memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
- **Schemas**: Validate configurations against `agent_config.schema.json` and `context_metadata.schema.json`. See [Schemas](../../interfaces/schemas/).

## Focus Areas

MCP server development evaluates 7 critical dimensions:

1. **MCP Server Architecture**: Design the server lifecycle including initialization, request handling, and graceful shutdown. Select the appropriate transport layer (stdio for local CLI tools, SSE for remote/web integrations). Implement robust session management for stateful interactions.
2. **Tool Registration**: Define tools with precise JSON Schema input specifications, implement thorough input validation, and provide structured error responses. Each tool must have a clear name, description, and well-documented parameter schema.
3. **Resource Exposure**: Expose application data as MCP resources with well-designed URI templates. Support appropriate content types (text, binary, JSON) and implement resource listing with pagination where needed.
4. **Prompt Templates**: Create reusable prompt templates with typed parameters that guide AI assistants toward effective use of the server's tools and resources. Templates should encode best practices and common workflows.
5. **Security & Sandboxing**: Implement input sanitization for all tool parameters, enforce permission boundaries to limit server capabilities, and apply rate limiting to prevent abuse. Never trust client input without validation.
6. **Testing & Debugging**: Use MCP Inspector for interactive testing, write integration tests with mock clients, and verify protocol compliance. Test edge cases including malformed requests, timeouts, and concurrent access.
7. **Client Integration**: Configure and connect the MCP server to Claude Desktop, VS Code, and other MCP-compatible clients. Handle transport negotiation, capability advertisement, and graceful degradation.

**Note**: The skill guides architecture, implementation, and testing of MCP servers. It does not deploy servers to production unless explicitly requested.

---

## Purpose

[TODO: Add purpose description]


## MANDATORY WORKFLOW (MUST FOLLOW EXACTLY)

### ⚠️ STEP 1: Analyze MCP Requirements (REQUIRED)

**YOU MUST:**
1. Determine which **tools** the server needs to expose (actions the AI can perform)
2. Determine which **resources** the server needs to expose (data the AI can read)
3. Determine which **prompt templates** would guide effective server usage
4. Identify the target AI clients (Claude Desktop, VS Code, custom integrations)
5. Assess data sensitivity and security requirements for exposed capabilities
6. Review any existing API or service that the MCP server will wrap

**DO NOT PROCEED WITHOUT UNDERSTANDING THE REQUIREMENTS**

### ⚠️ STEP 2: Design Server Architecture (REQUIRED)

**YOU MUST:**
1. **Choose transport layer**:
   - `stdio` — for local CLI tools, subprocess-based integrations, low latency
   - `SSE` (Server-Sent Events) — for remote/web integrations, multi-client support
2. **Define tool schemas**: For each tool, specify name, description, and JSON Schema for `inputSchema`
3. **Define resource URIs**: Design URI templates for each resource (e.g., `db://tables/{table_name}/schema`)
4. **Define prompt templates**: Design parameterized prompts for common workflows
5. **Plan security boundaries**: Determine what the server is allowed to access and what is off-limits
6. **Plan error handling strategy**: Define how validation errors, runtime errors, and permission errors are surfaced to clients

**DO NOT PROCEED WITHOUT A CLEAR ARCHITECTURE**

### ⚠️ STEP 3: Load Project Memory (REQUIRED)

**YOU MUST:**
1. Use `memoryStore.getSkillMemory("mcp-developer", "{project-name}")` to load project-specific MCP patterns. See [MemoryStore Interface](../../interfaces/memory_store.md).
2. Check for existing server architecture decisions and tool registries
3. Check for known integration patterns or client-specific workarounds
4. If no memory exists, proceed with defaults and create memory entries after implementation

**DO NOT PROCEED WITHOUT CHECKING PROJECT MEMORY**

### ⚠️ STEP 4: Implement MCP Server (REQUIRED)

**YOU MUST:**
1. **Server setup**: Initialize the MCP server with name, version, and capability declarations
2. **Tool implementation**: Register each tool with its handler, input validation, and error handling
3. **Resource implementation**: Register resource handlers with URI templates and content type negotiation
4. **Prompt implementation**: Register prompt templates with parameter definitions and template rendering
5. **Error handling**: Implement structured error responses following MCP error codes
6. **Testing**: Write integration tests using MCP Inspector or mock client, verify each tool/resource/prompt

**DO NOT PROCEED WITHOUT TESTING ALL ENDPOINTS**

### ⚠️ STEP 5: Review & Output (REQUIRED)

**YOU MUST validate the implementation against these criteria:**
1. **Protocol compliance**:
   - [ ] Server responds correctly to `initialize` handshake
   - [ ] All tools return valid `CallToolResult` responses
   - [ ] All resources return valid `ReadResourceResult` responses
   - [ ] Error responses use proper MCP error codes
2. **Security review**:
   - [ ] All tool inputs are validated against JSON Schema
   - [ ] No unsanitized user input reaches system commands or queries
   - [ ] Permission boundaries are enforced
3. **Documentation**:
   - [ ] Each tool has a clear description and input schema
   - [ ] Each resource has a documented URI template
   - [ ] Client configuration instructions are provided
4. **Output** the final implementation to `/claudedocs/` following `OUTPUT_CONVENTIONS.md`
5. **Update memory**: Use `memoryStore.update("mcp-developer", "{project-name}", ...)` to store architecture decisions, tool registries, and integration patterns. See [MemoryStore Interface](../../interfaces/memory_store.md).

**DO NOT SKIP VALIDATION**

---

### Step 6: Generate Output

Create deliverables and save to `/claudedocs/`:
- Follow OUTPUT_CONVENTIONS.md naming: `mcp-developer_{project}_{YYYY-MM-DD}.md`
- Include all required sections
- Provide clear, actionable recommendations

## Compliance Checklist

Before completing ANY MCP server development task, verify:
- [ ] Step 1: Requirements analyzed — tools, resources, prompts, security needs identified
- [ ] Step 2: Architecture designed — transport chosen, schemas defined, security planned
- [ ] Step 3: Project memory checked for existing patterns and decisions
- [ ] Step 4: Server implemented with tools, resources, prompts, error handling, and tests
- [ ] Step 5: Implementation validated, output generated, memory updated

**FAILURE TO COMPLETE ALL STEPS INVALIDATES THE IMPLEMENTATION**

---

## MCP Architecture Reference

### Server Types

| Type | Transport | Use Case |
|------|-----------|----------|
| Local tool server | stdio | CLI tools, file operations, local databases |
| Remote service server | SSE | Web APIs, cloud services, multi-client access |
| Hybrid server | stdio + SSE | Servers that support both local and remote clients |

### Transport Options

| Transport | Pros | Cons |
|-----------|------|------|
| stdio | Low latency, simple setup, no network | Single client, local only |
| SSE | Multi-client, remote access, web-friendly | Higher latency, requires HTTP server |

### Message Flow

```
Client                          Server
  │                               │
  │── initialize ────────────────►│
  │◄── initialize response ───────│
  │── initialized notification ──►│
  │                               │
  │── tools/list ────────────────►│
  │◄── tools list response ───────│
  │                               │
  │── tools/call ────────────────►│
  │◄── call result ───────────────│
  │                               │
  │── resources/list ────────────►│
  │◄── resources list response ───│
  │                               │
  │── resources/read ────────────►│
  │◄── read result ───────────────│
  │                               │
  │── shutdown ──────────────────►│
  │◄── shutdown response ─────────│
```

---

## Output File Naming Convention

**Format**: `mcp_server_{server_name}.md`

Where:
- `{server_name}` = the name of the MCP server being developed

**Examples**:
- `mcp_server_database_query.md`
- `mcp_server_file_manager.md`
- `mcp_server_github_integration.md`

---

## Further Reading

Refer to official documentation:
- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **MCP TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **MCP Inspector**: https://github.com/modelcontextprotocol/inspector
- **MCP Servers Repository**: https://github.com/modelcontextprotocol/servers

---

## Version History

- v1.0.0 (2026-02-12): Initial release
  - Mandatory 5-step workflow for MCP server development

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
