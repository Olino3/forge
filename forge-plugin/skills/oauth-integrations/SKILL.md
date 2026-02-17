---
name: oauth-integrations
description: "Implement OAuth 2.0 authentication with GitHub, Okta, Google, and Microsoft Entra (Azure AD)."
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
##       usage: "reference"

# skill:oauth-integrations - OAuth 2.0 Provider Integrations

## Version: 1.0.0

## Purpose

Implements OAuth 2.0 authentication with multiple providers: GitHub, Okta, Google, and Microsoft Entra (Azure AD). This skill covers the full OAuth 2.0 lifecycle: Authorization Code Flow, PKCE (Proof Key for Code Exchange), token exchange, refresh tokens, scope management, and provider-specific quirks.

**Use this skill when**:
- Implementing OAuth 2.0 authentication with GitHub, Okta, Google, or Microsoft Entra
- Setting up Authorization Code Flow with or without PKCE
- Configuring callback handling and token exchange
- Managing token storage, refresh, and revocation
- Handling provider-specific scope configuration and consent flows
- Implementing multi-provider authentication in a single application
- Setting up OIDC (OpenID Connect) for identity verification

**What it produces**:
- OAuth 2.0 provider configuration and client registration guidance
- Authorization Code Flow implementation with PKCE support
- Callback route handlers for token exchange
- Token storage and refresh logic (access tokens, refresh tokens, ID tokens)
- Scope configuration per provider
- State parameter CSRF protection
- Error handling for OAuth failure scenarios
- Multi-provider authentication architecture

**Triggers**: `oauth`, `oauth2`, `oauth integration`, `github oauth`, `okta auth`, `google oauth`, `microsoft entra`, `azure ad oauth`

### Provider-Specific Details

#### GitHub
- **OAuth App vs GitHub App**: OAuth Apps for user-level access; GitHub Apps for org/repo-level with fine-grained permissions
- **User and org scopes**: `user`, `repo`, `read:org`, `admin:org`, `gist`, `notifications`
- **Device flow**: For CLI tools and devices without browsers (`urn:ietf:params:oauth:grant-type:device_code`)
- **Quirks**: Access tokens don't expire by default (OAuth Apps); GitHub Apps use installation tokens with 1-hour TTL

#### Okta
- **Authorization Server configuration**: Default (`/oauth2/default`) vs custom authorization servers
- **Custom scopes**: Define and manage custom scopes in Okta Admin Console
- **OIDC**: Full OpenID Connect support with ID tokens, UserInfo endpoint, and claims mapping
- **Quirks**: Requires explicit authorization server ID in URLs; supports both Okta-hosted and custom login pages

#### Google
- **OAuth 2.0 for Web**: Google Identity Services (GIS) library for sign-in button and one-tap
- **Consent screen**: Configure in Google Cloud Console; unverified apps limited to 100 users
- **Offline access**: Use `access_type=offline` to receive refresh tokens; `prompt=consent` forces re-consent
- **Quirks**: Refresh tokens only returned on first authorization unless `prompt=consent` is set; Google uses `id_token` for identity via OIDC

#### Microsoft Entra (Azure AD)
- **Tenant types**: Single-tenant, multi-tenant, personal accounts, or B2C
- **App registration**: Register in Azure Portal → App registrations; configure redirect URIs per platform
- **Graph API scopes**: `User.Read`, `Mail.Read`, `Calendars.Read`, `Files.Read` — use `/.default` for application permissions
- **Quirks**: Uses MSAL.js library; v2.0 endpoint supports both work/school and personal accounts; token cache management via `msal-node` or `msal-browser`

## File Structure

```
skills/oauth-integrations/
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

- Gather inputs: required OAuth providers, application type, redirect URI requirements
- Detect **framework** (Express, Next.js, FastAPI, Spring Boot, ASP.NET) — determines callback handling and middleware patterns
- Detect **language** (TypeScript, JavaScript, Python, Java, C#) — determines SDK and library choices
- Identify **required OAuth providers** (GitHub, Okta, Google, Microsoft Entra) from user request
- Detect **existing auth setup** — check for existing OAuth configurations, Passport.js strategies, MSAL instances, or Okta SDKs
- Check for existing dependencies: `passport`, `@okta/okta-auth-js`, `@azure/msal-node`, `googleapis`, `octokit`
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="oauth-integrations"` and `domain="security"`.

- Load `project_overview.md` — understand project's OAuth history and configured providers
- Load `common_patterns.md` — reuse previously established OAuth patterns and token management strategies
- If first run: create memory directory for the project

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `security` domain. Stay within the file budget declared in frontmatter.

- Load security domain context relevant to OAuth 2.0, token management, and session security
- Cross-reference with any framework-specific context (Express middleware, Next.js API routes, etc.)
- Respect the file budget of 4 context files maximum

### Step 4: Implement OAuth Integration

This is the core action. Set up OAuth 2.0 authentication for the requested providers:

#### 4a: OAuth 2.0 Flow Setup

- Determine flow type:
  - **Authorization Code Flow** — standard server-side applications
  - **Authorization Code Flow + PKCE** — SPAs, mobile apps, and public clients
  - **Device Authorization Flow** — CLI tools and devices without browsers (GitHub)
- Generate cryptographically secure `state` parameter for CSRF protection
- Generate PKCE `code_verifier` (43-128 character random string) and `code_challenge` (SHA-256 hash, base64url-encoded)
- Construct authorization URL with required parameters (`client_id`, `redirect_uri`, `scope`, `state`, `code_challenge`, `code_challenge_method`)

#### 4b: Provider Configuration

- **GitHub**:
  - Register OAuth App or GitHub App in GitHub Developer Settings
  - Configure callback URL (e.g., `http://localhost:3000/auth/github/callback`)
  - Store `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in environment variables
  - Authorization endpoint: `https://github.com/login/oauth/authorize`
  - Token endpoint: `https://github.com/login/oauth/access_token`
  - User endpoint: `https://api.github.com/user`

- **Okta**:
  - Create application in Okta Admin Console (Web Application type for Auth Code flow)
  - Configure authorization server (default or custom)
  - Store `OKTA_DOMAIN`, `OKTA_CLIENT_ID`, `OKTA_CLIENT_SECRET` in environment variables
  - Authorization endpoint: `https://{okta-domain}/oauth2/{server-id}/v1/authorize`
  - Token endpoint: `https://{okta-domain}/oauth2/{server-id}/v1/token`
  - UserInfo endpoint: `https://{okta-domain}/oauth2/{server-id}/v1/userinfo`

- **Google**:
  - Create OAuth 2.0 credentials in Google Cloud Console → APIs & Services → Credentials
  - Configure OAuth consent screen (External or Internal)
  - Store `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in environment variables
  - Authorization endpoint: `https://accounts.google.com/o/oauth2/v2/auth`
  - Token endpoint: `https://oauth2.googleapis.com/token`
  - UserInfo endpoint: `https://www.googleapis.com/oauth2/v3/userinfo`

- **Microsoft Entra**:
  - Register application in Azure Portal → App registrations
  - Configure redirect URIs and supported account types (single-tenant, multi-tenant)
  - Store `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID` in environment variables
  - Authorization endpoint: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize`
  - Token endpoint: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token`
  - Use MSAL.js for client-side or `@azure/msal-node` for server-side

#### 4c: Callback Handling and Token Exchange

- Implement callback route to receive authorization code
- Validate `state` parameter matches the stored value (CSRF protection)
- Exchange authorization code for tokens via POST to token endpoint
- Parse token response: `access_token`, `refresh_token`, `id_token` (OIDC), `expires_in`, `token_type`
- Validate ID token signature and claims (for OIDC providers: Okta, Google, Microsoft Entra)

#### 4d: Token Storage and Refresh

- **Server-side**: Store tokens in encrypted server-side sessions or database; never expose to client
- **Client-side (SPA)**: Store in memory only; use backend-for-frontend (BFF) pattern for token management
- Implement token refresh logic:
  - Check `expires_in` before API calls
  - Use `refresh_token` grant type to obtain new access tokens
  - Handle refresh token rotation (Okta, Microsoft Entra)
  - Handle refresh token revocation on sign-out
- Token revocation: Call provider's revocation endpoint on sign-out

#### 4e: Scope Configuration

- Configure minimum required scopes per provider:
  - GitHub: `read:user`, `user:email` (minimum for authentication)
  - Okta: `openid`, `profile`, `email` (OIDC standard scopes)
  - Google: `openid`, `profile`, `email` (OIDC standard scopes)
  - Microsoft Entra: `openid`, `profile`, `email`, `User.Read` (Graph API access)
- Request additional scopes incrementally (progressive authorization)
- Handle scope changes and re-authorization flows

#### 4f: Error Handling

- Handle OAuth error responses: `access_denied`, `invalid_grant`, `invalid_scope`, `server_error`
- Handle token expiration and refresh failures
- Handle provider-specific errors:
  - GitHub: rate limiting (403), bad verification code
  - Okta: invalid authorization server, expired sessions
  - Google: consent required, unverified app restrictions
  - Microsoft Entra: admin consent required, tenant restrictions
- Implement user-facing error messages with appropriate detail level

#### 4g: State Parameter CSRF Protection

- Generate cryptographically random `state` value (minimum 32 bytes, base64url-encoded)
- Store `state` in server-side session or secure HTTP-only cookie before redirect
- Validate returned `state` matches stored value in callback handler
- Reject requests with missing or mismatched `state` values
- Clear stored `state` after validation (one-time use)

### Step 5: Generate Output

- Save output to `/claudedocs/oauth-integrations_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - OAuth provider configuration and registration instructions
  - Authorization flow implementation code
  - Callback handler implementation
  - Token management (storage, refresh, revocation)
  - Scope configuration per provider
  - Environment variable list
  - Error handling patterns
  - Security considerations and best practices
  - Provider console setup checklists

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="oauth-integrations"`. Store any newly learned patterns, conventions, or project insights.

- Update `project_overview.md` with configured OAuth providers and flow details
- Update `common_patterns.md` with OAuth patterns, token management strategies, and provider-specific quirks
- Record any project-specific customizations or workarounds

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Client secrets stored in environment variables (never hardcoded)
- [ ] State parameter CSRF protection implemented
- [ ] PKCE used for public clients (SPAs, mobile apps)
- [ ] Tokens stored securely (server-side session or encrypted storage)
- [ ] Token refresh logic implemented with expiration checks
- [ ] ID tokens validated (signature and claims) for OIDC providers
- [ ] OAuth error responses handled with user-facing messages
- [ ] Redirect URIs match registered values in provider consoles
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — OAuth 2.0 integrations with GitHub, Okta, Google, Microsoft Entra (Azure AD); Authorization Code Flow, PKCE, token management, scope configuration, CSRF protection |
