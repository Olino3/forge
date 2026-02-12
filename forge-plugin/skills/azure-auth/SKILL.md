---
name: azure-auth
description: "Microsoft Entra ID (Azure AD) authentication for React SPAs with MSAL.js and Cloudflare Workers JWT validation using jose library. Full-stack pattern with Authorization Code Flow + PKCE. Prevents 8 errors."
version: "1.0.0"
context:
  primary_domain: "security"
  always_load_files: []
  detection_required: true
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [project_overview.md, common_patterns.md]
    - type: "shared-project"
      usage: "reference"
---

# skill:azure-auth - Microsoft Entra ID Authentication

## Version: 1.0.0

## Purpose

Implements Microsoft Entra ID (Azure AD) authentication for full-stack applications using React SPAs with MSAL.js on the frontend and Cloudflare Workers JWT validation with the jose library on the backend. This skill sets up Authorization Code Flow with PKCE — the recommended OAuth 2.0 flow for public clients (SPAs).

**Use this skill when**:
- Building a React SPA that requires Azure AD / Entra ID sign-in
- Protecting Cloudflare Workers API routes with JWT validation
- Setting up Authorization Code Flow + PKCE for browser-based apps
- Configuring MSAL.js `PublicClientApplication` with proper redirect URIs
- Validating access tokens issued by Entra ID in edge workers

**What it produces**:
- MSAL.js configuration and authentication wrapper for React
- Cloudflare Workers middleware for JWT validation using jose
- Token acquisition, caching, and silent renewal setup
- Protected API route patterns
- Azure AD app registration guidance

**Errors it prevents**:
1. **Token expiration** — silent token renewal not configured
2. **CORS issues** — mismatched origins between SPA and API
3. **Redirect URI mismatch** — app registration doesn't match deployed URI
4. **Silent token acquisition failures** — missing fallback to interactive auth
5. **PKCE verifier issues** — code verifier not persisted across redirects
6. **Audience validation** — API not validating the `aud` claim correctly
7. **Issuer validation** — wrong tenant or issuer URL in token validation
8. **Clock skew** — token validation fails due to server time differences

## File Structure

```
skills/azure-auth/
├── SKILL.md (this file)
└── examples.md
```

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

## Mandatory Workflow

> **IMPORTANT**: Execute ALL steps in order. Do not skip any step.

### Step 1: Initial Analysis

- Gather inputs: Azure AD tenant ID, client ID, redirect URIs, API scopes
- Detect project type: confirm React SPA frontend + Cloudflare Workers backend
- Determine project name for memory lookup
- Identify existing auth setup (if any) to avoid conflicts
- Check for existing MSAL.js or jose dependencies in `package.json`

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="azure-auth"` and `domain="security"`.

- Load `project_overview.md` — understand project's auth history and stack
- Load `common_patterns.md` — reuse previously established auth patterns
- If first run: create memory directory for the project

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `security` domain. Stay within the file budget declared in frontmatter.

- Load security domain context relevant to OAuth 2.0, JWT validation, and PKCE
- Cross-reference with any framework-specific context (React patterns)
- Respect the file budget of 4 context files maximum

### Step 4: Implement Authentication

This is the core action. Implement the full-stack authentication pattern:

#### 4a: MSAL.js Configuration for React SPA

- Configure `PublicClientApplication` with:
  - `auth.clientId` — Application (client) ID from Azure AD app registration
  - `auth.authority` — `https://login.microsoftonline.com/{tenantId}`
  - `auth.redirectUri` — must match app registration exactly
  - `auth.postLogoutRedirectUri` — for clean sign-out flow
- Set up `cache` configuration:
  - `cacheLocation: "sessionStorage"` (safer than localStorage for SPAs)
  - `storeAuthStateInCookie: false` (set `true` for IE11 support)

#### 4b: Authorization Code Flow + PKCE Setup

- Configure login request with appropriate scopes
- Implement `loginRedirect` / `loginPopup` with PKCE (automatic in MSAL.js v2+)
- Handle redirect promise on app initialization via `handleRedirectPromise()`
- Set up `AuthenticatedTemplate` and `UnauthenticatedTemplate` components

#### 4c: Token Acquisition and Caching

- Implement `acquireTokenSilent` with fallback to `acquireTokenRedirect`
- Configure token cache with appropriate expiration handling
- Set up automatic token renewal before expiration
- Handle `InteractionRequiredAuthError` for consent/MFA scenarios

#### 4d: Cloudflare Workers JWT Validation with jose

- Import `jwtVerify` and `createRemoteJWKSet` from jose
- Configure JWKS endpoint: `https://login.microsoftonline.com/{tenantId}/discovery/v2.0/keys`
- Validate required claims:
  - `aud` — must match the API's Application ID URI or client ID
  - `iss` — must match `https://login.microsoftonline.com/{tenantId}/v2.0`
  - `exp` — token must not be expired
  - `nbf` — token must be valid (not before)
- Apply clock tolerance (recommended: 300 seconds) to handle clock skew
- Extract user identity from validated token claims

#### 4e: Protected API Routes

- Create authentication middleware for Cloudflare Workers
- Extract Bearer token from `Authorization` header
- Return 401 for missing/invalid tokens with appropriate error messages
- Return 403 for valid tokens with insufficient scopes
- Pass validated user claims to downstream route handlers

### Step 5: Generate Output

- Save output to `/claudedocs/azure-auth_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Azure AD app registration checklist
  - MSAL.js configuration code
  - Cloudflare Workers JWT validation middleware code
  - Environment variable list (tenant ID, client ID, scopes)
  - Testing instructions for the auth flow
  - Troubleshooting guide for the 8 common errors

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="azure-auth"`. Store any newly learned patterns, conventions, or project insights.

- Update `project_overview.md` with Azure AD configuration details
- Update `common_patterns.md` with token handling patterns used
- Record any project-specific auth customizations

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] MSAL.js configured with PKCE (not implicit flow)
- [ ] JWT validation uses jose library (not manual decoding)
- [ ] All 8 common errors addressed in implementation
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — MSAL.js + Cloudflare Workers + jose |
