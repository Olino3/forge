# Azure Auth - Memory System

This file documents the memory structure for the `azure-auth` skill. Memory is project-specific knowledge that accumulates over time through repeated authentication implementations.

---

## Purpose

The memory system enables the skill to:
- **Learn project patterns** — understand project-specific auth configurations
- **Avoid repeat work** — reuse established MSAL.js and jose configurations
- **Track decisions** — record why specific auth choices were made
- **Prevent errors** — remember project-specific redirect URIs, scopes, and tenant settings
- **Improve accuracy** — better recommendations based on project history

---

## Memory vs Context

**Memory** (this directory):
- Project-specific
- Dynamic (changes with each implementation)
- Per-project subdirectories
- Example: "This project uses tenant ID xyz and scope api://my-app/access_as_user"

**Context** (`../../context/security/`):
- Universal security and OAuth 2.0 knowledge
- Static (changes rarely)
- Shared across all projects
- Example: "Authorization Code Flow + PKCE best practices"

---

## Memory Structure

```
memory/skills/azure-auth/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # CRITICAL — Azure AD config, stack, tenant info
    └── common_patterns.md         # Project-specific auth patterns
```

---

## Per-Project Memory Files

### 1. project_overview.md (CRITICAL)

**Purpose**: High-level understanding of the project's authentication setup.

**Always Update On First Run**:
- Azure AD tenant ID and type (single-tenant, multi-tenant)
- Application (client) ID
- Redirect URIs (dev and production)
- API scopes and permissions
- Frontend framework and version (React, Vite, CRA)
- Backend platform (Cloudflare Workers, Pages Functions)
- MSAL.js version
- jose library version
- Token cache location (sessionStorage, localStorage)
- Authentication flow (Authorization Code + PKCE)

**Update Incrementally**:
- Add new redirect URIs for additional environments
- Record new API scopes as they are added
- Document auth-related configuration changes
- Note any workarounds for tenant-specific issues

**Example Structure**:
```markdown
# Project Overview: MyApp

## Azure AD Configuration
- **Tenant ID**: contoso.onmicrosoft.com
- **Tenant Type**: Single-tenant (organizational accounts only)
- **Client ID**: 12345678-abcd-efgh-ijkl-123456789abc
- **API Application ID URI**: api://my-app

## Redirect URIs
- **Dev**: http://localhost:5173
- **Staging**: https://staging.myapp.com
- **Production**: https://myapp.com

## API Scopes
- api://my-app/access_as_user
- api://my-app/reports.read

## Frontend Stack
- **Framework**: React 18.2 with Vite 5.x
- **MSAL.js**: @azure/msal-browser 3.x, @azure/msal-react 2.x
- **Token Cache**: sessionStorage

## Backend Stack
- **Platform**: Cloudflare Workers
- **JWT Library**: jose 5.x
- **Clock Tolerance**: 300 seconds

## Authentication Flow
- Authorization Code Flow + PKCE
- Silent token renewal with interactive fallback
- Token attached to API calls via fetch wrapper
```

### 2. common_patterns.md

**Purpose**: Document recurring auth patterns specific to this project.

**What to Document**:
- MSAL.js configuration patterns
- Token acquisition strategies
- API call authentication patterns
- Error handling approaches
- Redirect handling patterns
- Logout flow implementation
- Role-based access control patterns
- Multi-environment configuration

**Example**:
```markdown
# Common Patterns: MyApp

## Token Acquisition
All API calls use this pattern:
1. Attempt `acquireTokenSilent` with cached account
2. On `InteractionRequiredAuthError`, fallback to `acquireTokenRedirect`
3. Attach token to fetch via `apiClient` wrapper

## API Client Pattern
Centralized API client handles:
- Bearer token injection
- Token refresh before expiration
- 401 response → re-authenticate flow
- CORS headers for cross-origin requests

## Protected Routes
- `ProtectedRoute` component wraps authenticated pages
- `AuthenticatedTemplate` / `UnauthenticatedTemplate` for conditional rendering
- Role checks performed via token claims after validation

## JWT Validation
Cloudflare Worker middleware:
- JWKS fetched and cached from Azure AD endpoint
- Clock tolerance: 300 seconds
- Claims validated: aud, iss, exp, nbf
- User identity extracted from `preferred_username` and `oid` claims

## Environment Configuration
- Frontend env vars prefixed with VITE_
- Backend vars set in wrangler.toml [vars] section
- Secrets (if any) stored via `wrangler secret put`
```

---

## Workflow

### First Use on a Project

1. **Check for existing memory**: Does `{project-name}/` directory exist?
2. **If NO**: Create memory directory and both files
3. **If YES**: Load existing memory files

### Subsequent Uses

1. **Load all existing memory files** (Step 2 of skill workflow)
2. **Use memory to inform implementation** (understand existing auth setup)
3. **After implementation**: Update ALL memory files with new insights

---

## Memory Update Guidelines

### project_overview.md Updates
- **First run**: Create comprehensive overview of Azure AD configuration
- **Subsequent runs**: Add new environments, scopes, or configuration changes
- **Update when**: New redirect URIs added, scopes changed, libraries upgraded

### common_patterns.md Updates
- **Add patterns** observed or implemented in this session
- **Don't remove patterns** unless they are no longer applicable
- **Refine patterns** as the auth setup evolves
- **Document workarounds** for tenant-specific or environment-specific issues

---

## Benefits of Memory System

1. **Consistency**
   - Same auth patterns applied across the project
   - New team members follow established conventions

2. **Speed**
   - Subsequent auth changes are faster (context already loaded)
   - Known configuration values readily available

3. **Error Prevention**
   - Redirect URIs and scopes stored — prevents mismatch errors
   - Known workarounds documented — prevents repeating mistakes

4. **Traceability**
   - Auth decisions recorded with rationale
   - Configuration changes tracked over time

---

## Memory File Size

**Keep memory files concise**:
- project_overview.md: ~100-300 lines
- common_patterns.md: ~200-400 lines

**If memory grows too large**:
- Consolidate similar patterns
- Archive outdated environment configurations
- Summarize historical changes

---

## Related Documentation

- **Skill Workflow**: `../../skills/azure-auth/SKILL.md`
- **Context System**: `../../context/security/index.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
