# OAuth Integrations - Usage Examples

This document provides practical examples of how to use the `oauth-integrations` skill in various scenarios.

---

## Example 1: Implementing GitHub OAuth in a Node.js/Express Application

**Scenario**: A Node.js/Express API needs GitHub OAuth to authenticate users and access their GitHub profile and repositories. The implementation uses Authorization Code Flow with server-side token exchange.

**Command**:
```
skill:oauth-integrations

Add GitHub OAuth sign-in to my Express API. I need to authenticate users with GitHub and access their profile info and public repos. Use Authorization Code Flow with session-based token storage.
```

**What Happens**:
1. Skill detects Express from `package.json` and `app.ts` / `server.ts`
2. Loads memory — no existing memory found, creates new project directory
3. Loads security domain context for OAuth 2.0 and session management patterns
4. Installs required dependencies:
   ```bash
   npm install express-session crypto
   ```
5. Creates GitHub OAuth configuration:
   ```ts
   // src/config/oauth.ts
   export const githubOAuth = {
     clientId: process.env.GITHUB_CLIENT_ID!,
     clientSecret: process.env.GITHUB_CLIENT_SECRET!,
     redirectUri: process.env.GITHUB_REDIRECT_URI || 'http://localhost:3000/auth/github/callback',
     authorizationEndpoint: 'https://github.com/login/oauth/authorize',
     tokenEndpoint: 'https://github.com/login/oauth/access_token',
     userEndpoint: 'https://api.github.com/user',
     scopes: ['read:user', 'user:email'],
   }
   ```
6. Creates authorization route with state parameter CSRF protection:
   ```ts
   // src/routes/auth.ts
   import { Router, Request, Response } from 'express'
   import crypto from 'crypto'
   import { githubOAuth } from '../config/oauth'

   const router = Router()

   router.get('/auth/github', (req: Request, res: Response) => {
     const state = crypto.randomBytes(32).toString('hex')
     req.session.oauthState = state

     const params = new URLSearchParams({
       client_id: githubOAuth.clientId,
       redirect_uri: githubOAuth.redirectUri,
       scope: githubOAuth.scopes.join(' '),
       state,
     })

     res.redirect(`${githubOAuth.authorizationEndpoint}?${params}`)
   })
   ```
7. Creates callback handler with token exchange:
   ```ts
   // src/routes/auth.ts (continued)
   router.get('/auth/github/callback', async (req: Request, res: Response) => {
     const { code, state } = req.query

     // Validate state parameter (CSRF protection)
     if (!state || state !== req.session.oauthState) {
       return res.status(403).json({ error: 'Invalid state parameter' })
     }
     delete req.session.oauthState

     try {
       // Exchange code for access token
       const tokenResponse = await fetch(githubOAuth.tokenEndpoint, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
           Accept: 'application/json',
         },
         body: JSON.stringify({
           client_id: githubOAuth.clientId,
           client_secret: githubOAuth.clientSecret,
           code,
           redirect_uri: githubOAuth.redirectUri,
         }),
       })

       const { access_token } = await tokenResponse.json()

       // Fetch user profile
       const userResponse = await fetch(githubOAuth.userEndpoint, {
         headers: { Authorization: `Bearer ${access_token}` },
       })
       const user = await userResponse.json()

       // Store token in session (server-side only)
       req.session.accessToken = access_token
       req.session.user = {
         id: user.id,
         login: user.login,
         name: user.name,
         avatarUrl: user.avatar_url,
         email: user.email,
       }

       res.redirect('/dashboard')
     } catch (error) {
       console.error('GitHub OAuth error:', error)
       res.redirect('/auth/error?reason=token_exchange_failed')
     }
   })

   export default router
   ```
8. Saves output to `/claudedocs/oauth-integrations_myapp_2026-02-12.md`
9. Creates memory with project overview and OAuth patterns

**Expected Output**:
```markdown
# OAuth Integration: MyExpressApp — GitHub
**Date**: 2026-02-12

## Provider Configuration
- **Provider**: GitHub (OAuth App)
- **Flow**: Authorization Code Flow (server-side)
- **Scopes**: read:user, user:email

## Environment Variables
- GITHUB_CLIENT_ID
- GITHUB_CLIENT_SECRET
- GITHUB_REDIRECT_URI
- SESSION_SECRET

## Routes
- GET /auth/github — Initiates OAuth flow with state parameter
- GET /auth/github/callback — Handles callback, exchanges code for token
- GET /auth/logout — Destroys session and revokes token

## Security
- State parameter: 32-byte random hex for CSRF protection
- Token storage: Server-side session (express-session)
- Secrets: Environment variables only

## Files Created
- src/config/oauth.ts — GitHub OAuth configuration
- src/routes/auth.ts — Authorization and callback routes
- src/middleware/requireAuth.ts — Auth guard middleware
- .env.example — Environment variable template
```

---

## Example 2: Setting Up Okta OIDC Authentication with Custom Scopes

**Scenario**: An enterprise Node.js application needs Okta OIDC authentication with custom scopes for role-based access control. The implementation uses Authorization Code Flow with PKCE and a custom authorization server.

**Command**:
```
skill:oauth-integrations

Set up Okta OIDC authentication in my Express app. I need Authorization Code Flow with PKCE, custom scopes for admin and editor roles, and ID token validation. We're using a custom Okta authorization server.
```

**What Happens**:
1. Skill detects Express with TypeScript from `tsconfig.json` and `package.json`
2. Loads memory — no existing Okta configuration found
3. Loads security domain context for OIDC, PKCE, and token validation patterns
4. Installs required dependencies:
   ```bash
   npm install @okta/jwt-verifier jose
   ```
5. Creates Okta OAuth configuration with custom authorization server:
   ```ts
   // src/config/okta.ts
   export const oktaConfig = {
     domain: process.env.OKTA_DOMAIN!,          // e.g., dev-123456.okta.com
     clientId: process.env.OKTA_CLIENT_ID!,
     clientSecret: process.env.OKTA_CLIENT_SECRET!,
     authServerId: process.env.OKTA_AUTH_SERVER_ID || 'default',
     redirectUri: process.env.OKTA_REDIRECT_URI || 'http://localhost:3000/auth/okta/callback',
     scopes: ['openid', 'profile', 'email', 'custom:admin', 'custom:editor'],
     get authorizationEndpoint() {
       return `https://${this.domain}/oauth2/${this.authServerId}/v1/authorize`
     },
     get tokenEndpoint() {
       return `https://${this.domain}/oauth2/${this.authServerId}/v1/token`
     },
     get userinfoEndpoint() {
       return `https://${this.domain}/oauth2/${this.authServerId}/v1/userinfo`
     },
     get jwksUri() {
       return `https://${this.domain}/oauth2/${this.authServerId}/v1/keys`
     },
   }
   ```
6. Creates PKCE utilities for code verifier and challenge generation:
   ```ts
   // src/utils/pkce.ts
   import crypto from 'crypto'

   export function generateCodeVerifier(): string {
     return crypto.randomBytes(32).toString('base64url')
   }

   export function generateCodeChallenge(verifier: string): string {
     return crypto.createHash('sha256').update(verifier).digest('base64url')
   }
   ```
7. Creates authorization route with PKCE and state:
   ```ts
   // src/routes/okta-auth.ts
   import { Router, Request, Response } from 'express'
   import crypto from 'crypto'
   import { oktaConfig } from '../config/okta'
   import { generateCodeVerifier, generateCodeChallenge } from '../utils/pkce'

   const router = Router()

   router.get('/auth/okta', (req: Request, res: Response) => {
     const state = crypto.randomBytes(32).toString('hex')
     const codeVerifier = generateCodeVerifier()
     const codeChallenge = generateCodeChallenge(codeVerifier)

     // Store PKCE verifier and state in session
     req.session.oauthState = state
     req.session.codeVerifier = codeVerifier

     const params = new URLSearchParams({
       client_id: oktaConfig.clientId,
       redirect_uri: oktaConfig.redirectUri,
       response_type: 'code',
       scope: oktaConfig.scopes.join(' '),
       state,
       code_challenge: codeChallenge,
       code_challenge_method: 'S256',
     })

     res.redirect(`${oktaConfig.authorizationEndpoint}?${params}`)
   })
   ```
8. Creates callback handler with PKCE token exchange and ID token validation:
   ```ts
   // src/routes/okta-auth.ts (continued)
   import { createRemoteJWKSet, jwtVerify } from 'jose'

   const JWKS = createRemoteJWKSet(new URL(oktaConfig.jwksUri))

   router.get('/auth/okta/callback', async (req: Request, res: Response) => {
     const { code, state } = req.query

     if (!state || state !== req.session.oauthState) {
       return res.status(403).json({ error: 'Invalid state parameter' })
     }

     const codeVerifier = req.session.codeVerifier
     delete req.session.oauthState
     delete req.session.codeVerifier

     try {
       // Exchange code for tokens with PKCE verifier
       const tokenResponse = await fetch(oktaConfig.tokenEndpoint, {
         method: 'POST',
         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
         body: new URLSearchParams({
           grant_type: 'authorization_code',
           client_id: oktaConfig.clientId,
           client_secret: oktaConfig.clientSecret,
           code: code as string,
           redirect_uri: oktaConfig.redirectUri,
           code_verifier: codeVerifier,
         }),
       })

       const tokens = await tokenResponse.json()

       // Validate ID token
       const { payload } = await jwtVerify(tokens.id_token, JWKS, {
         issuer: `https://${oktaConfig.domain}/oauth2/${oktaConfig.authServerId}`,
         audience: oktaConfig.clientId,
       })

       // Extract custom scopes/claims for RBAC
       req.session.user = {
         sub: payload.sub,
         name: payload.name as string,
         email: payload.email as string,
         roles: payload.roles as string[] || [],
       }
       req.session.accessToken = tokens.access_token
       req.session.refreshToken = tokens.refresh_token

       res.redirect('/dashboard')
     } catch (error) {
       console.error('Okta OIDC error:', error)
       res.redirect('/auth/error?reason=token_validation_failed')
     }
   })

   export default router
   ```
9. Creates token refresh middleware:
   ```ts
   // src/middleware/tokenRefresh.ts
   import { oktaConfig } from '../config/okta'

   export async function refreshAccessToken(refreshToken: string) {
     const response = await fetch(oktaConfig.tokenEndpoint, {
       method: 'POST',
       headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
       body: new URLSearchParams({
         grant_type: 'refresh_token',
         client_id: oktaConfig.clientId,
         client_secret: oktaConfig.clientSecret,
         refresh_token: refreshToken,
       }),
     })

     if (!response.ok) {
       throw new Error('Token refresh failed')
     }

     return response.json()
   }
   ```
10. Saves output and creates memory with Okta OIDC patterns

**Expected Output**:
```markdown
# OAuth Integration: MyEnterpriseApp — Okta OIDC
**Date**: 2026-02-12

## Provider Configuration
- **Provider**: Okta (Custom Authorization Server)
- **Flow**: Authorization Code Flow + PKCE
- **Scopes**: openid, profile, email, custom:admin, custom:editor

## OIDC Details
- ID token validated via JWKS endpoint
- Custom claims mapped: roles, permissions
- Token refresh with rotation enabled

## Environment Variables
- OKTA_DOMAIN
- OKTA_CLIENT_ID
- OKTA_CLIENT_SECRET
- OKTA_AUTH_SERVER_ID
- OKTA_REDIRECT_URI

## Custom Scopes (Okta Admin Console)
1. custom:admin — Full administrative access
2. custom:editor — Content editing permissions

## Files Created
- src/config/okta.ts — Okta OAuth/OIDC configuration
- src/utils/pkce.ts — PKCE code verifier/challenge utilities
- src/routes/okta-auth.ts — Authorization, callback, and logout routes
- src/middleware/tokenRefresh.ts — Token refresh logic
- src/middleware/requireRole.ts — Role-based access middleware
```

---

## Example 3: Multi-Provider OAuth Setup (Google + Microsoft Entra) in a React App

**Scenario**: A React SPA needs both Google and Microsoft Entra (Azure AD) sign-in with a backend-for-frontend (BFF) pattern. Users should be able to sign in with either provider and link accounts. The app uses Authorization Code Flow with PKCE routed through a BFF proxy.

**Command**:
```
skill:oauth-integrations

Set up Google and Microsoft Entra OAuth in my React app. I need both providers with a BFF pattern for token management, account linking, and PKCE. The backend is Express and the frontend is React with Vite.
```

**What Happens**:
1. Skill detects React (Vite) frontend from `vite.config.ts` and Express backend from `server/` directory
2. Loads memory — no existing OAuth configuration found
3. Loads security domain context for multi-provider OAuth, BFF pattern, and PKCE
4. Creates shared OAuth utilities:
   ```ts
   // server/src/utils/oauth.ts
   import crypto from 'crypto'

   export function generateState(): string {
     return crypto.randomBytes(32).toString('hex')
   }

   export function generateCodeVerifier(): string {
     return crypto.randomBytes(32).toString('base64url')
   }

   export function generateCodeChallenge(verifier: string): string {
     return crypto.createHash('sha256').update(verifier).digest('base64url')
   }
   ```
5. Creates Google OAuth configuration:
   ```ts
   // server/src/config/google.ts
   export const googleOAuth = {
     clientId: process.env.GOOGLE_CLIENT_ID!,
     clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
     redirectUri: process.env.GOOGLE_REDIRECT_URI || 'http://localhost:3000/api/auth/google/callback',
     authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
     tokenEndpoint: 'https://oauth2.googleapis.com/token',
     userinfoEndpoint: 'https://www.googleapis.com/oauth2/v3/userinfo',
     scopes: ['openid', 'profile', 'email'],
   }
   ```
6. Creates Microsoft Entra configuration:
   ```ts
   // server/src/config/entra.ts
   export const entraOAuth = {
     clientId: process.env.AZURE_CLIENT_ID!,
     clientSecret: process.env.AZURE_CLIENT_SECRET!,
     tenantId: process.env.AZURE_TENANT_ID || 'common',
     redirectUri: process.env.AZURE_REDIRECT_URI || 'http://localhost:3000/api/auth/entra/callback',
     scopes: ['openid', 'profile', 'email', 'User.Read'],
     get authorizationEndpoint() {
       return `https://login.microsoftonline.com/${this.tenantId}/oauth2/v2.0/authorize`
     },
     get tokenEndpoint() {
       return `https://login.microsoftonline.com/${this.tenantId}/oauth2/v2.0/token`
     },
   }
   ```
7. Creates BFF auth routes for both providers:
   ```ts
   // server/src/routes/multi-auth.ts
   import { Router, Request, Response } from 'express'
   import { googleOAuth } from '../config/google'
   import { entraOAuth } from '../config/entra'
   import { generateState, generateCodeVerifier, generateCodeChallenge } from '../utils/oauth'

   const router = Router()

   // --- Google OAuth ---
   router.get('/api/auth/google', (req: Request, res: Response) => {
     const state = generateState()
     const codeVerifier = generateCodeVerifier()

     req.session.oauthState = state
     req.session.codeVerifier = codeVerifier
     req.session.provider = 'google'

     const params = new URLSearchParams({
       client_id: googleOAuth.clientId,
       redirect_uri: googleOAuth.redirectUri,
       response_type: 'code',
       scope: googleOAuth.scopes.join(' '),
       state,
       code_challenge: generateCodeChallenge(codeVerifier),
       code_challenge_method: 'S256',
       access_type: 'offline',
       prompt: 'consent',
     })

     res.redirect(`${googleOAuth.authorizationEndpoint}?${params}`)
   })

   router.get('/api/auth/google/callback', async (req: Request, res: Response) => {
     const { code, state } = req.query

     if (!state || state !== req.session.oauthState) {
       return res.status(403).json({ error: 'Invalid state parameter' })
     }

     try {
       const tokenResponse = await fetch(googleOAuth.tokenEndpoint, {
         method: 'POST',
         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
         body: new URLSearchParams({
           grant_type: 'authorization_code',
           client_id: googleOAuth.clientId,
           client_secret: googleOAuth.clientSecret,
           code: code as string,
           redirect_uri: googleOAuth.redirectUri,
           code_verifier: req.session.codeVerifier,
         }),
       })

       const tokens = await tokenResponse.json()

       // Fetch user profile
       const userResponse = await fetch(googleOAuth.userinfoEndpoint, {
         headers: { Authorization: `Bearer ${tokens.access_token}` },
       })
       const profile = await userResponse.json()

       req.session.user = {
         provider: 'google',
         id: profile.sub,
         email: profile.email,
         name: profile.name,
         picture: profile.picture,
       }
       req.session.accessToken = tokens.access_token
       req.session.refreshToken = tokens.refresh_token

       delete req.session.oauthState
       delete req.session.codeVerifier

       res.redirect('/')
     } catch (error) {
       console.error('Google OAuth error:', error)
       res.redirect('/auth-error?reason=google_token_exchange_failed')
     }
   })

   // --- Microsoft Entra OAuth ---
   router.get('/api/auth/entra', (req: Request, res: Response) => {
     const state = generateState()
     const codeVerifier = generateCodeVerifier()

     req.session.oauthState = state
     req.session.codeVerifier = codeVerifier
     req.session.provider = 'entra'

     const params = new URLSearchParams({
       client_id: entraOAuth.clientId,
       redirect_uri: entraOAuth.redirectUri,
       response_type: 'code',
       scope: entraOAuth.scopes.join(' '),
       state,
       code_challenge: generateCodeChallenge(codeVerifier),
       code_challenge_method: 'S256',
     })

     res.redirect(`${entraOAuth.authorizationEndpoint}?${params}`)
   })

   router.get('/api/auth/entra/callback', async (req: Request, res: Response) => {
     const { code, state } = req.query

     if (!state || state !== req.session.oauthState) {
       return res.status(403).json({ error: 'Invalid state parameter' })
     }

     try {
       const tokenResponse = await fetch(entraOAuth.tokenEndpoint, {
         method: 'POST',
         headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
         body: new URLSearchParams({
           grant_type: 'authorization_code',
           client_id: entraOAuth.clientId,
           client_secret: entraOAuth.clientSecret,
           code: code as string,
           redirect_uri: entraOAuth.redirectUri,
           code_verifier: req.session.codeVerifier,
         }),
       })

       const tokens = await tokenResponse.json()

       // Fetch user profile from Microsoft Graph
       const userResponse = await fetch('https://graph.microsoft.com/v1.0/me', {
         headers: { Authorization: `Bearer ${tokens.access_token}` },
       })
       const profile = await userResponse.json()

       req.session.user = {
         provider: 'entra',
         id: profile.id,
         email: profile.mail || profile.userPrincipalName,
         name: profile.displayName,
       }
       req.session.accessToken = tokens.access_token
       req.session.refreshToken = tokens.refresh_token

       delete req.session.oauthState
       delete req.session.codeVerifier

       res.redirect('/')
     } catch (error) {
       console.error('Microsoft Entra OAuth error:', error)
       res.redirect('/auth-error?reason=entra_token_exchange_failed')
     }
   })

   // --- Auth Status (BFF endpoint for React frontend) ---
   router.get('/api/auth/me', (req: Request, res: Response) => {
     if (req.session.user) {
       res.json({ authenticated: true, user: req.session.user })
     } else {
       res.json({ authenticated: false })
     }
   })

   router.post('/api/auth/logout', (req: Request, res: Response) => {
     req.session.destroy((err) => {
       if (err) {
         return res.status(500).json({ error: 'Logout failed' })
       }
       res.json({ success: true })
     })
   })

   export default router
   ```
8. Creates React auth hook for frontend:
   ```tsx
   // src/hooks/useAuth.ts
   import { useState, useEffect, useCallback } from 'react'

   interface User {
     provider: 'google' | 'entra'
     id: string
     email: string
     name: string
     picture?: string
   }

   export function useAuth() {
     const [user, setUser] = useState<User | null>(null)
     const [loading, setLoading] = useState(true)

     useEffect(() => {
       fetch('/api/auth/me')
         .then((res) => res.json())
         .then((data) => {
           setUser(data.authenticated ? data.user : null)
           setLoading(false)
         })
         .catch(() => setLoading(false))
     }, [])

     const signInWithGoogle = useCallback(() => {
       window.location.href = '/api/auth/google'
     }, [])

     const signInWithEntra = useCallback(() => {
       window.location.href = '/api/auth/entra'
     }, [])

     const signOut = useCallback(async () => {
       await fetch('/api/auth/logout', { method: 'POST' })
       setUser(null)
     }, [])

     return { user, loading, signInWithGoogle, signInWithEntra, signOut }
   }
   ```
9. Creates sign-in page component:
   ```tsx
   // src/pages/SignIn.tsx
   import { useAuth } from '../hooks/useAuth'

   export function SignIn() {
     const { signInWithGoogle, signInWithEntra } = useAuth()

     return (
       <div>
         <h1>Sign In</h1>
         <button onClick={signInWithGoogle}>
           Sign in with Google
         </button>
         <button onClick={signInWithEntra}>
           Sign in with Microsoft
         </button>
       </div>
     )
   }
   ```
10. Saves output and updates memory with multi-provider OAuth patterns

**Expected Output**:
```markdown
# OAuth Integration: MyReactApp — Google + Microsoft Entra
**Date**: 2026-02-12

## Architecture
- **Pattern**: Backend-for-Frontend (BFF)
- **Frontend**: React (Vite) — no token handling
- **Backend**: Express — manages all OAuth flows and tokens

## Providers
| Provider | Flow | Scopes |
|----------|------|--------|
| Google | Auth Code + PKCE | openid, profile, email |
| Microsoft Entra | Auth Code + PKCE | openid, profile, email, User.Read |

## Environment Variables
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET
- GOOGLE_REDIRECT_URI
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
- AZURE_REDIRECT_URI
- SESSION_SECRET

## API Routes (BFF)
- GET /api/auth/google — Initiates Google OAuth
- GET /api/auth/google/callback — Google callback handler
- GET /api/auth/entra — Initiates Microsoft Entra OAuth
- GET /api/auth/entra/callback — Entra callback handler
- GET /api/auth/me — Returns current user (for React frontend)
- POST /api/auth/logout — Destroys session

## Security
- PKCE: S256 code challenge for both providers
- State parameter: 32-byte random hex for CSRF protection
- Tokens: Stored server-side only (never sent to browser)
- BFF pattern: React frontend has no direct access to tokens

## Files Created
- server/src/config/google.ts — Google OAuth config
- server/src/config/entra.ts — Microsoft Entra config
- server/src/utils/oauth.ts — Shared PKCE and state utilities
- server/src/routes/multi-auth.ts — BFF auth routes
- src/hooks/useAuth.ts — React auth hook
- src/pages/SignIn.tsx — Multi-provider sign-in page
```

---

## Common Usage Patterns

### Pattern 1: Single Provider (GitHub)
```
skill:oauth-integrations
Add GitHub OAuth to my Express API for user authentication
```
Use for simple GitHub-only authentication.

### Pattern 2: Enterprise OIDC (Okta)
```
skill:oauth-integrations
Set up Okta OIDC with PKCE and custom scopes for role-based access
```
Use for enterprise applications with Okta identity management.

### Pattern 3: Multi-Provider with BFF
```
skill:oauth-integrations
Add Google and Microsoft Entra OAuth to my React + Express app using the BFF pattern
```
Use for SPAs needing multiple providers with secure server-side token management.

### Pattern 4: SPA with PKCE
```
skill:oauth-integrations
Implement Google OAuth with PKCE in my React SPA (no backend)
```
Use when a backend is not available; PKCE protects the public client.

### Pattern 5: Device Flow (GitHub CLI)
```
skill:oauth-integrations
Set up GitHub Device Authorization Flow for my CLI tool
```
Use for CLI tools and devices that cannot open a browser for redirect-based flows.

---

## Tips for Effective Usage

1. **Always use PKCE for public clients** — SPAs and mobile apps must use PKCE since they cannot securely store client secrets
2. **Prefer the BFF pattern for SPAs** — route token exchange through a backend to keep tokens out of the browser
3. **Use `state` on every authorization request** — never skip CSRF protection, even in development
4. **Request minimal scopes** — start with `openid profile email` and add more incrementally as needed
5. **Store refresh tokens securely** — never in localStorage; use server-side sessions or encrypted HTTP-only cookies
6. **Handle provider-specific quirks** — Google requires `prompt=consent` for refresh tokens; GitHub tokens don't expire by default; Okta needs the authorization server ID in URLs

---

## When to Use This Skill

**Ideal Scenarios**:
- Applications needing OAuth 2.0 with GitHub, Okta, Google, or Microsoft Entra
- Multi-provider authentication architectures
- Enterprise SSO integration with OIDC
- SPAs needing secure token management via BFF pattern
- CLI tools needing GitHub Device Flow authentication

**Not Ideal For**:
- Firebase-based authentication (use `firebase-auth` skill)
- Clerk managed authentication (use `clerk-auth` skill)
- Self-hosted authentication with better-auth (use `better-auth` skill)
- Azure AD with MSAL.js only (use `azure-auth` skill for MSAL-specific patterns)
