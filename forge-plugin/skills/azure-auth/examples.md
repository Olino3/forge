# Azure Auth - Usage Examples

This document provides practical examples of how to use the `azure-auth` skill in various scenarios.

---

## Example 1: Setting Up MSAL.js in a React SPA with Authorization Code Flow + PKCE

**Scenario**: A new React SPA needs Azure AD sign-in with Authorization Code Flow + PKCE. The app has an Azure AD app registration but no authentication code yet.

**Command**:
```
skill:azure-auth

Set up MSAL.js authentication in my React SPA. My Azure AD tenant ID is "contoso.onmicrosoft.com", client ID is "12345678-abcd-efgh-ijkl-123456789abc", and the app runs at http://localhost:3000 in dev.
```

**What Happens**:
1. Skill detects a React SPA project from `package.json` (react, react-dom dependencies)
2. Loads memory — no existing memory found, creates new project directory
3. Loads security domain context for OAuth 2.0 and PKCE patterns
4. Generates `PublicClientApplication` configuration:
   - Sets `auth.clientId` and `auth.authority` from provided values
   - Configures `auth.redirectUri` to `http://localhost:3000`
   - Sets `cache.cacheLocation` to `sessionStorage`
5. Creates authentication wrapper components:
   - `AuthProvider` wrapping `MsalProvider` at app root
   - `useAuth` custom hook for login/logout/token acquisition
   - `ProtectedRoute` component using `AuthenticatedTemplate`
6. Implements `handleRedirectPromise()` on app initialization
7. Configures `acquireTokenSilent` with fallback to `acquireTokenRedirect`
8. Saves output to `/claudedocs/azure-auth_myapp_2026-02-12.md`
9. Creates memory with project overview and auth patterns

**Expected Output**:
```markdown
# Azure Auth Implementation: MyApp
**Date**: 2026-02-12

## Azure AD App Registration Checklist
- [x] Client ID configured
- [x] Redirect URI: http://localhost:3000
- [ ] Add production redirect URI when deploying

## MSAL.js Configuration
- PublicClientApplication with Auth Code + PKCE
- Session storage caching
- Silent token renewal with interactive fallback

## Files Created/Modified
- src/auth/msalConfig.ts — MSAL configuration
- src/auth/AuthProvider.tsx — React context provider
- src/auth/useAuth.ts — Custom authentication hook
- src/auth/ProtectedRoute.tsx — Route guard component

## Environment Variables
- REACT_APP_AZURE_CLIENT_ID
- REACT_APP_AZURE_TENANT_ID
- REACT_APP_AZURE_REDIRECT_URI
```

---

## Example 2: Configuring Cloudflare Workers JWT Validation with jose

**Scenario**: An existing Cloudflare Workers API needs to validate Azure AD access tokens. The React SPA is already sending Bearer tokens in the Authorization header.

**Command**:
```
skill:azure-auth

Add JWT validation to my Cloudflare Workers API. It needs to validate tokens issued by Azure AD tenant "contoso.onmicrosoft.com". The API's Application ID URI is "api://my-backend-api".
```

**What Happens**:
1. Skill detects Cloudflare Workers project from `wrangler.toml`
2. Loads memory — finds existing project with MSAL.js frontend already configured
3. Loads security context for JWT validation and token verification patterns
4. Generates JWT validation middleware using jose:
   - Imports `jwtVerify` and `createRemoteJWKSet` from jose
   - Configures JWKS URI for the Azure AD tenant
   - Validates `aud`, `iss`, `exp`, and `nbf` claims
   - Applies 300-second clock tolerance for clock skew
5. Creates authentication middleware:
   - Extracts Bearer token from `Authorization` header
   - Returns 401 with `WWW-Authenticate` header for missing/invalid tokens
   - Returns 403 for insufficient scopes
   - Passes validated claims to route handlers
6. Adds error handling for common JWT validation failures
7. Saves output to `/claudedocs/azure-auth_myapi_2026-02-12.md`
8. Updates memory with API-side auth patterns

**Expected Output**:
```markdown
# Azure Auth - API JWT Validation: MyAPI
**Date**: 2026-02-12

## JWT Validation Middleware
- jose library for token verification
- Azure AD JWKS endpoint for key rotation
- Claim validation: aud, iss, exp, nbf
- Clock tolerance: 300 seconds

## Files Created/Modified
- src/middleware/auth.ts — JWT validation middleware
- src/middleware/types.ts — AuthenticatedRequest type
- wrangler.toml — Added AZURE_TENANT_ID and AZURE_AUDIENCE vars

## Protected Routes
- All /api/* routes require valid Bearer token
- User claims available via request context

## Error Responses
- 401 Unauthorized — missing or invalid token
- 403 Forbidden — valid token, insufficient scopes
```

---

## Example 3: Full-Stack Authentication Flow (React SPA + Cloudflare Workers API)

**Scenario**: Building a new full-stack application from scratch. Both the React SPA and Cloudflare Workers API need Azure AD authentication configured end-to-end.

**Command**:
```
skill:azure-auth

Set up full-stack Azure AD authentication for my project. Frontend is React (Vite), backend is Cloudflare Workers. Tenant: "contoso.onmicrosoft.com", Client ID: "aaaabbbb-cccc-dddd-eeee-ffffgggghhhh", API scope: "api://my-app/access_as_user".
```

**What Happens**:
1. Skill detects both React SPA (`packages/frontend`) and Cloudflare Workers (`packages/api`) in monorepo
2. Loads memory — first run, creates new memory directory
3. Loads security context: OAuth 2.0 flows, JWT validation, CORS patterns
4. **Frontend implementation**:
   - Configures `PublicClientApplication` with tenant and client ID
   - Sets up Authorization Code Flow + PKCE (default in MSAL.js v2+)
   - Creates `AuthProvider`, `useAuth` hook, and `ProtectedRoute`
   - Configures `acquireTokenSilent` to request `api://my-app/access_as_user` scope
   - Adds automatic token attachment to API calls via fetch wrapper
5. **Backend implementation**:
   - Creates JWT validation middleware with jose
   - Configures JWKS endpoint for the tenant
   - Validates audience matches `api://my-app`
   - Validates issuer matches tenant's v2.0 endpoint
   - Applies clock tolerance for edge deployment clock skew
6. **Integration**:
   - Configures CORS headers for SPA origin
   - Sets up proper `Authorization: Bearer {token}` header injection
   - Handles token refresh before API calls
   - Implements error handling for expired/invalid tokens
7. **Error prevention** — addresses all 8 common errors:
   - Token expiration: silent renewal configured
   - CORS: origins matched between SPA and API
   - Redirect URI: matches app registration
   - Silent acquisition: fallback to interactive
   - PKCE verifier: handled by MSAL.js automatically
   - Audience validation: API validates `aud` claim
   - Issuer validation: tenant-specific issuer URL
   - Clock skew: 300-second tolerance
8. Saves output to `/claudedocs/azure-auth_myproject_2026-02-12.md`
9. Creates comprehensive memory entries for both frontend and backend patterns

**Expected Output**:
```markdown
# Azure Auth - Full Stack Implementation: MyProject
**Date**: 2026-02-12

## Architecture
- Frontend: React (Vite) with MSAL.js v2
- Backend: Cloudflare Workers with jose
- Flow: Authorization Code + PKCE

## Frontend Files
- packages/frontend/src/auth/msalConfig.ts
- packages/frontend/src/auth/AuthProvider.tsx
- packages/frontend/src/auth/useAuth.ts
- packages/frontend/src/auth/ProtectedRoute.tsx
- packages/frontend/src/utils/apiClient.ts

## Backend Files
- packages/api/src/middleware/auth.ts
- packages/api/src/middleware/types.ts
- packages/api/wrangler.toml (updated)

## Azure AD App Registration
- [x] SPA redirect URI: http://localhost:5173
- [x] API scope: api://my-app/access_as_user
- [ ] Add production redirect URIs
- [ ] Configure token version: v2.0

## Error Prevention Summary
✅ Token expiration — silent renewal configured
✅ CORS — origins matched
✅ Redirect URI — matches registration
✅ Silent acquisition — interactive fallback
✅ PKCE verifier — MSAL.js handles automatically
✅ Audience validation — aud claim checked
✅ Issuer validation — tenant-specific issuer
✅ Clock skew — 300s tolerance applied

## Environment Variables
### Frontend
- VITE_AZURE_CLIENT_ID
- VITE_AZURE_TENANT_ID
- VITE_AZURE_REDIRECT_URI
- VITE_API_SCOPE

### Backend
- AZURE_TENANT_ID
- AZURE_AUDIENCE
```

---

## Common Usage Patterns

### Pattern 1: SPA-Only Authentication
```
skill:azure-auth
Add Azure AD sign-in to my React app (no backend API)
```
Use when you only need user sign-in without API protection.

### Pattern 2: API-Only Token Validation
```
skill:azure-auth
Add JWT validation to my Cloudflare Worker for Azure AD tokens
```
Use when the SPA is already configured and you only need API-side validation.

### Pattern 3: Multi-Tenant Authentication
```
skill:azure-auth
Set up multi-tenant Azure AD auth — any organization should be able to sign in
```
Use `authority: "https://login.microsoftonline.com/common"` for multi-tenant apps.

### Pattern 4: Adding API Scopes
```
skill:azure-auth
Add a new API scope "api://my-app/reports.read" to my existing auth setup
```
Use when extending an existing auth setup with additional permissions.

---

## Tips for Effective Usage

1. **Have app registration ready** — create the Azure AD app registration before running the skill
2. **Know your scopes** — identify what API permissions the SPA needs upfront
3. **Specify the environment** — mention dev vs production redirect URIs
4. **Mention existing auth** — if replacing or upgrading an auth system, say so
5. **Monorepo structure** — specify where frontend and backend code live
6. **First run takes longer** — the skill creates memory on the first invocation

---

## When to Use This Skill

**Ideal Scenarios**:
- Greenfield React SPA needing Azure AD sign-in
- Adding token validation to Cloudflare Workers APIs
- Full-stack auth setup for React + Cloudflare Workers
- Migrating from implicit flow to Authorization Code + PKCE
- Troubleshooting Azure AD authentication issues

**Not Ideal For**:
- Non-React frontends (Angular, Vue — use framework-specific skills)
- Non-Cloudflare backends (use platform-specific skills)
- B2C / Azure AD B2C scenarios (different configuration)
- Service-to-service auth (use client credentials flow instead)
