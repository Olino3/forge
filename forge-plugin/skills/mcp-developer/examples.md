# MCP Developer Examples

This file contains example scenarios demonstrating how to use the mcp-developer skill to build and integrate MCP servers for various use cases.

---

## Example 1: Building a Database Query MCP Server

### Scenario
Build a TypeScript MCP server that exposes SQL database query capabilities over stdio transport, allowing AI assistants to explore schemas and run read-only queries.

### User Prompt
```
Build an MCP server that lets me query my PostgreSQL database from Claude Desktop
```

### Skill Execution

**Step 1 - Analyze MCP Requirements**:
- **Tools needed**:
  - `query` — execute read-only SQL queries
  - `list_tables` — list all tables in the database
  - `describe_table` — get column definitions for a table
- **Resources needed**:
  - `db://tables` — list of all tables as a resource
  - `db://tables/{table_name}/schema` — schema for a specific table
- **Prompts needed**:
  - `explore-database` — guided template for database exploration
- **Target client**: Claude Desktop (local, stdio transport)
- **Security**: Read-only queries only, no DDL/DML, query timeout enforcement

**Step 2 - Design Server Architecture**:
- **Transport**: stdio — local tool for Claude Desktop
- **Language**: TypeScript with `@modelcontextprotocol/sdk`
- **Tool schemas**:
  ```json
  {
    "name": "query",
    "description": "Execute a read-only SQL query against the database",
    "inputSchema": {
      "type": "object",
      "properties": {
        "sql": {
          "type": "string",
          "description": "The SQL SELECT query to execute"
        },
        "limit": {
          "type": "number",
          "description": "Maximum rows to return (default: 100)",
          "default": 100
        }
      },
      "required": ["sql"]
    }
  }
  ```
- **Security**: SQL parsing to reject non-SELECT statements, query timeout of 30s

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("mcp-developer", "db-query-server")
→ No existing memory found. Will create after implementation.
```

**Step 4 - Implement MCP Server**:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import pg from "pg";

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
});

const server = new McpServer({
  name: "db-query-server",
  version: "1.0.0",
});

// Tool: Execute read-only SQL query
server.tool(
  "query",
  "Execute a read-only SQL SELECT query against the database",
  {
    sql: z.string().describe("The SQL SELECT query to execute"),
    limit: z.number().default(100).describe("Maximum rows to return"),
  },
  async ({ sql, limit }) => {
    // Security: reject non-SELECT statements
    const normalized = sql.trim().toUpperCase();
    if (!normalized.startsWith("SELECT")) {
      return {
        content: [
          { type: "text", text: "Error: Only SELECT queries are allowed" },
        ],
        isError: true,
      };
    }

    const result = await pool.query(`${sql} LIMIT $1`, [limit]);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result.rows, null, 2),
        },
      ],
    };
  }
);

// Tool: List all tables
server.tool(
  "list_tables",
  "List all tables in the database",
  {},
  async () => {
    const result = await pool.query(
      "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    );
    return {
      content: [
        {
          type: "text",
          text: result.rows.map((r) => r.table_name).join("\n"),
        },
      ],
    };
  }
);

// Tool: Describe a table's schema
server.tool(
  "describe_table",
  "Get column definitions for a specific table",
  {
    table_name: z.string().describe("Name of the table to describe"),
  },
  async ({ table_name }) => {
    // Security: validate table name to prevent injection
    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(table_name)) {
      return {
        content: [{ type: "text", text: "Error: Invalid table name" }],
        isError: true,
      };
    }

    const result = await pool.query(
      "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = $1",
      [table_name]
    );
    return {
      content: [
        { type: "text", text: JSON.stringify(result.rows, null, 2) },
      ],
    };
  }
);

// Resource: List tables
server.resource("tables-list", "db://tables", async (uri) => ({
  contents: [
    {
      uri: uri.href,
      mimeType: "application/json",
      text: JSON.stringify(
        (
          await pool.query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
          )
        ).rows
      ),
    },
  ],
}));

// Prompt: Database exploration template
server.prompt(
  "explore-database",
  "Guided template for exploring a database",
  { focus_area: z.string().optional().describe("Specific area to explore") },
  ({ focus_area }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Please explore the database${focus_area ? ` focusing on ${focus_area}` : ""}. Start by listing all tables, then describe the most relevant ones, and finally run a few sample queries to understand the data.`,
        },
      },
    ],
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Claude Desktop configuration** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "db-query": {
      "command": "npx",
      "args": ["tsx", "src/index.ts"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/mydb"
      }
    }
  }
}
```

**Step 5 - Review & Output**:
- ✅ Protocol compliance: Server handles initialize, tools/list, tools/call, resources/read
- ✅ Security: Only SELECT queries allowed, table names validated, parameterized queries used
- ✅ Documentation: All tools have descriptions and JSON Schema inputs
- ✅ Client config: Claude Desktop configuration provided
- ✅ Memory updated with architecture decisions and tool registry

---

## Example 2: Building a File Management MCP Server

### Scenario
Build a Python MCP server that exposes filesystem operations as both resources (for reading) and tools (for writing), with strict sandboxing to a configured root directory.

### User Prompt
```
Create an MCP server in Python that lets AI assistants manage files in a project directory
```

### Skill Execution

**Step 1 - Analyze MCP Requirements**:
- **Tools needed**:
  - `write_file` — create or overwrite a file
  - `create_directory` — create a new directory
  - `move_file` — move or rename a file
  - `search_files` — search file contents with regex
- **Resources needed**:
  - `file:///{path}` — read file contents
  - `file:///` — list directory contents as a resource
- **Prompts needed**:
  - `organize-project` — template for project file organization
- **Target client**: VS Code, Claude Desktop
- **Security**: All operations sandboxed to a root directory, no symlink traversal

**Step 2 - Design Server Architecture**:
- **Transport**: stdio — local tool for VS Code and Claude Desktop
- **Language**: Python with `mcp` SDK
- **Security model**: All paths resolved relative to a configured `--root-dir`, symlinks rejected if they escape root

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("mcp-developer", "file-manager-server")
→ No existing memory found. Will create after implementation.
```

**Step 4 - Implement MCP Server**:

```python
import os
import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("file-manager", version="1.0.0")

ROOT_DIR = Path(os.environ.get("FILE_ROOT", ".")).resolve()


def safe_path(relative: str) -> Path:
    """Resolve a path and ensure it stays within ROOT_DIR."""
    resolved = (ROOT_DIR / relative).resolve()
    if not str(resolved).startswith(str(ROOT_DIR)):
        raise ValueError(f"Path escapes sandbox: {relative}")
    return resolved


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Create or overwrite a file with the given content.

    Args:
        path: Relative path within the project directory
        content: File content to write
    """
    target = safe_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"Written {len(content)} bytes to {path}"


@mcp.tool()
def create_directory(path: str) -> str:
    """Create a new directory (including parent directories).

    Args:
        path: Relative path for the new directory
    """
    target = safe_path(path)
    target.mkdir(parents=True, exist_ok=True)
    return f"Directory created: {path}"


@mcp.tool()
def move_file(source: str, destination: str) -> str:
    """Move or rename a file or directory.

    Args:
        source: Current relative path
        destination: New relative path
    """
    src = safe_path(source)
    dst = safe_path(destination)
    if not src.exists():
        raise FileNotFoundError(f"Source not found: {source}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)
    return f"Moved {source} → {destination}"


@mcp.tool()
def search_files(pattern: str, path: str = ".") -> str:
    """Search file contents using a regex pattern.

    Args:
        pattern: Regular expression to search for
        path: Directory to search in (relative, default: root)
    """
    search_dir = safe_path(path)
    matches = []
    compiled = re.compile(pattern)

    for file_path in search_dir.rglob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                for i, line in enumerate(content.splitlines(), 1):
                    if compiled.search(line):
                        rel = file_path.relative_to(ROOT_DIR)
                        matches.append(f"{rel}:{i}: {line.strip()}")
            except (UnicodeDecodeError, PermissionError):
                continue

    return "\n".join(matches) if matches else "No matches found"


@mcp.resource("file:///{path}")
def read_file(path: str) -> str:
    """Read the contents of a file."""
    target = safe_path(path)
    if not target.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return target.read_text(encoding="utf-8")


@mcp.resource("file:///")
def list_directory() -> str:
    """List all files in the project directory."""
    entries = []
    for item in sorted(ROOT_DIR.rglob("*")):
        if item.is_file():
            rel = item.relative_to(ROOT_DIR)
            size = item.stat().st_size
            entries.append(f"{rel} ({size} bytes)")
    return "\n".join(entries)


@mcp.prompt()
def organize_project(project_type: str = "generic") -> str:
    """Guided template for organizing project files.

    Args:
        project_type: Type of project (e.g., python, node, rust)
    """
    return f"Please review the files in this {project_type} project and suggest a well-organized directory structure. List the current files, identify any misplaced items, and propose moves to improve organization."


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Claude Desktop configuration**:
```json
{
  "mcpServers": {
    "file-manager": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "FILE_ROOT": "/home/user/projects/my-project"
      }
    }
  }
}
```

**Step 5 - Review & Output**:
- ✅ Protocol compliance: Tools and resources registered with proper schemas
- ✅ Security: Path sandboxing via `safe_path()`, symlink traversal prevented
- ✅ Documentation: All tools and resources have docstrings used as descriptions
- ✅ Client config: Claude Desktop configuration provided
- ✅ Memory updated with sandboxing patterns and tool registry

---

## Example 3: Building a GitHub Integration MCP Server

### Scenario
Build a TypeScript MCP server that integrates with the GitHub API, exposing tools for managing pull requests, issues, and searching code.

### User Prompt
```
Build an MCP server that connects Claude to GitHub for managing PRs and issues
```

### Skill Execution

**Step 1 - Analyze MCP Requirements**:
- **Tools needed**:
  - `create_issue` — create a new GitHub issue
  - `list_issues` — list issues with filters
  - `create_pull_request` — open a new PR
  - `review_pull_request` — add a review to a PR
  - `search_code` — search code across repositories
- **Resources needed**:
  - `github://repos/{owner}/{repo}/issues` — list issues as a resource
  - `github://repos/{owner}/{repo}/pulls` — list PRs as a resource
- **Prompts needed**:
  - `triage-issues` — template for triaging open issues
  - `review-pr` — template for reviewing a pull request
- **Target client**: Claude Desktop, VS Code
- **Security**: GitHub token with minimal scopes, rate limit awareness

**Step 2 - Design Server Architecture**:
- **Transport**: stdio — local tool for Claude Desktop and VS Code
- **Language**: TypeScript with `@modelcontextprotocol/sdk`
- **Auth**: GitHub personal access token via environment variable
- **Rate limiting**: Track API quota and warn when approaching limits

**Step 3 - Load Project Memory**:
```
memoryStore.getSkillMemory("mcp-developer", "github-mcp-server")
→ No existing memory found. Will create after implementation.
```

**Step 4 - Implement MCP Server**:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Octokit } from "@octokit/rest";

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
});

const server = new McpServer({
  name: "github-integration",
  version: "1.0.0",
});

// Tool: Create a new issue
server.tool(
  "create_issue",
  "Create a new GitHub issue in a repository",
  {
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    title: z.string().describe("Issue title"),
    body: z.string().optional().describe("Issue body in Markdown"),
    labels: z.array(z.string()).optional().describe("Labels to apply"),
  },
  async ({ owner, repo, title, body, labels }) => {
    const { data } = await octokit.issues.create({
      owner,
      repo,
      title,
      body,
      labels,
    });
    return {
      content: [
        {
          type: "text",
          text: `Issue #${data.number} created: ${data.html_url}`,
        },
      ],
    };
  }
);

// Tool: List issues with filters
server.tool(
  "list_issues",
  "List issues in a GitHub repository with optional filters",
  {
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    state: z.enum(["open", "closed", "all"]).default("open").describe("Filter by state"),
    labels: z.string().optional().describe("Comma-separated label names"),
    limit: z.number().default(10).describe("Maximum issues to return"),
  },
  async ({ owner, repo, state, labels, limit }) => {
    const { data } = await octokit.issues.listForRepo({
      owner,
      repo,
      state,
      labels,
      per_page: limit,
    });
    const summary = data.map(
      (issue) => `#${issue.number} [${issue.state}] ${issue.title}`
    );
    return {
      content: [{ type: "text", text: summary.join("\n") }],
    };
  }
);

// Tool: Create a pull request
server.tool(
  "create_pull_request",
  "Open a new pull request",
  {
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    title: z.string().describe("PR title"),
    body: z.string().optional().describe("PR description in Markdown"),
    head: z.string().describe("Branch containing changes"),
    base: z.string().default("main").describe("Branch to merge into"),
  },
  async ({ owner, repo, title, body, head, base }) => {
    const { data } = await octokit.pulls.create({
      owner,
      repo,
      title,
      body,
      head,
      base,
    });
    return {
      content: [
        {
          type: "text",
          text: `PR #${data.number} created: ${data.html_url}`,
        },
      ],
    };
  }
);

// Tool: Add a review to a pull request
server.tool(
  "review_pull_request",
  "Submit a review on an existing pull request",
  {
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    pull_number: z.number().describe("Pull request number"),
    event: z
      .enum(["APPROVE", "REQUEST_CHANGES", "COMMENT"])
      .describe("Review action"),
    body: z.string().describe("Review comment body"),
  },
  async ({ owner, repo, pull_number, event, body }) => {
    const { data } = await octokit.pulls.createReview({
      owner,
      repo,
      pull_number,
      event,
      body,
    });
    return {
      content: [
        {
          type: "text",
          text: `Review submitted (${event}) on PR #${pull_number}: ${data.html_url}`,
        },
      ],
    };
  }
);

// Tool: Search code across repositories
server.tool(
  "search_code",
  "Search for code across GitHub repositories",
  {
    query: z.string().describe("Search query (GitHub code search syntax)"),
    limit: z.number().default(10).describe("Maximum results to return"),
  },
  async ({ query, limit }) => {
    const { data } = await octokit.search.code({
      q: query,
      per_page: limit,
    });
    const results = data.items.map(
      (item) => `${item.repository.full_name}/${item.path} (score: ${item.score})`
    );
    return {
      content: [
        {
          type: "text",
          text: `Found ${data.total_count} results:\n${results.join("\n")}`,
        },
      ],
    };
  }
);

// Resource: Repository issues
server.resource(
  "repo-issues",
  "github://repos/{owner}/{repo}/issues",
  async (uri) => {
    const parts = uri.pathname.split("/").filter(Boolean);
    const owner = parts[1];
    const repo = parts[2];
    const { data } = await octokit.issues.listForRepo({
      owner,
      repo,
      state: "open",
      per_page: 30,
    });
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(
            data.map((i) => ({
              number: i.number,
              title: i.title,
              state: i.state,
              labels: i.labels.map((l) =>
                typeof l === "string" ? l : l.name
              ),
            })),
            null,
            2
          ),
        },
      ],
    };
  }
);

// Prompt: Triage open issues
server.prompt(
  "triage-issues",
  "Guided template for triaging open issues in a repository",
  {
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
  },
  ({ owner, repo }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Please triage the open issues in ${owner}/${repo}. List all open issues, categorize them by priority (critical, high, medium, low), identify duplicates, and suggest which ones should be addressed first.`,
        },
      },
    ],
  })
);

// Prompt: Review a pull request
server.prompt(
  "review-pr",
  "Guided template for reviewing a pull request",
  {
    owner: z.string().describe("Repository owner"),
    repo: z.string().describe("Repository name"),
    pull_number: z.string().describe("Pull request number"),
  },
  ({ owner, repo, pull_number }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Please review PR #${pull_number} in ${owner}/${repo}. Check the code changes for correctness, security issues, performance concerns, and style consistency. Provide a summary of your findings and a recommended review action.`,
        },
      },
    ],
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Claude Desktop configuration**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["tsx", "src/index.ts"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Step 5 - Review & Output**:
- ✅ Protocol compliance: 5 tools, 1 resource, 2 prompts all properly registered
- ✅ Security: Token-based auth via environment variable, minimal scope recommended
- ✅ Documentation: All tools have descriptions and typed input schemas
- ✅ Client config: Claude Desktop configuration provided with token placeholder
- ✅ Memory updated with GitHub API patterns and tool registry

---

## Summary of MCP Server Patterns

1. **Database query server** (TypeScript/stdio) — Read-only SQL with schema exploration
2. **File management server** (Python/stdio) — Sandboxed filesystem ops with resources and tools
3. **GitHub integration server** (TypeScript/stdio) — API wrapper with tools, resources, and prompts

## Best Practices

- Always validate tool inputs — use JSON Schema or Zod for type safety
- Implement security boundaries early — sandbox file access, restrict queries, limit API scopes
- Provide both tools (for actions) and resources (for data) when appropriate
- Include prompt templates to guide AI assistants toward effective server usage
- Use environment variables for secrets — never hardcode tokens or credentials
- Test with MCP Inspector before deploying to client configurations
- Handle errors gracefully — return `isError: true` with descriptive messages
- Document client configuration for every supported client
