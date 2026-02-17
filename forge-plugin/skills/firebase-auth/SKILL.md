---
name: firebase-auth
description: "Build with Firebase Authentication — email/password, OAuth providers, phone auth, and custom tokens. Use when: setting up auth flows, implementing sign-in/sign-up, managing user sessions, protecting routes. Prevents 12 errors."
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

# skill:firebase-auth - Firebase Authentication

## Version: 1.0.0

## Purpose

Implements Firebase Authentication for web and mobile applications. This skill covers the full Firebase auth lifecycle: email/password authentication, OAuth providers (Google, Facebook, GitHub, Apple), phone auth with reCAPTCHA verification, anonymous auth, custom token generation, session management, auth state persistence, and protected route guards.

**Use this skill when**:
- Setting up auth flows with Firebase Authentication
- Implementing sign-in/sign-up with email/password or OAuth providers
- Managing user sessions and auth state persistence
- Protecting routes based on authentication status
- Configuring phone authentication with reCAPTCHA verification
- Generating and verifying custom tokens for server-side auth
- Setting up anonymous authentication for guest users

**What it produces**:
- Firebase project initialization and SDK configuration
- Auth provider setup (email/password, Google, Facebook, GitHub, Apple)
- Phone auth with reCAPTCHA verifier integration
- Custom token generation and verification
- Session management and auth state persistence configuration
- Protected route guards for React/Next.js/Angular/Vue
- Auth state observer setup with `onAuthStateChanged`
- Environment variable configuration for Firebase config

**Triggers**: `firebase auth`, `firebase authentication`, `firebase sign-in`, `firebase login`

### 12 Common Errors Prevented

| # | Error | Prevention |
|---|-------|------------|
| 1 | Firebase config exposure | Store Firebase config in environment variables; never commit API keys to source control |
| 2 | Auth state race conditions | Use `onAuthStateChanged` observer; avoid checking `currentUser` before auth initialization completes |
| 3 | Unsubscribed auth listeners | Always unsubscribe from `onAuthStateChanged` in component cleanup (useEffect return / ngOnDestroy) |
| 4 | Incorrect persistence mode | Set `browserLocalPersistence`, `browserSessionPersistence`, or `inMemoryPersistence` explicitly based on use case |
| 5 | Missing error handling for auth operations | Wrap all auth calls in try/catch; handle specific error codes (`auth/email-already-in-use`, `auth/wrong-password`, etc.) |
| 6 | OAuth redirect domain mismatch | Add all deployment domains to Firebase Console → Authentication → Authorized domains |
| 7 | Phone auth reCAPTCHA issues | Initialize `RecaptchaVerifier` before calling `signInWithPhoneNumber`; use invisible reCAPTCHA for better UX |
| 8 | Custom token expiration | Custom tokens expire after 1 hour; implement token refresh logic on the client |
| 9 | Session cookie misconfiguration | Set correct `maxAge`, `httpOnly`, `secure`, and `sameSite` attributes; verify with `verifySessionCookie()` on server |
| 10 | CORS issues with auth endpoints | Configure Firebase Hosting rewrites or Cloud Functions CORS headers for custom auth endpoints |
| 11 | Insecure password reset flows | Use `sendPasswordResetEmail` with action code settings; validate action codes server-side before applying |
| 12 | Missing email verification | Enforce email verification with `sendEmailVerification` after sign-up; check `emailVerified` before granting access |

## File Structure

```
skills/firebase-auth/
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

- Gather inputs: auth requirements, provider needs, route protection scope
- Detect **framework** (React, Next.js, Angular, Vue) — determines route guard implementation and component patterns
- Detect **Firebase SDK version** (v9 modular vs v8 compat) — determines import style and API shape
- Check for existing Firebase setup (`firebase.json`, `firebaseConfig`, `@angular/fire`)
- Check `package.json` for `firebase`, `@angular/fire`, `react-firebase-hooks`, and related dependencies
- Determine project name for memory lookup

### Step 2: Load Memory

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="firebase-auth"` and `domain="security"`.

- Load `project_overview.md` — understand project's Firebase auth history and config
- Load `common_patterns.md` — reuse previously established auth patterns and provider configurations
- If first run: create memory directory for the project

### Step 3: Load Context

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `security` domain. Stay within the file budget declared in frontmatter.

- Load security domain context relevant to authentication, OAuth, and session management
- Cross-reference with any framework-specific context (React hooks, Angular guards, Vue router)
- Respect the file budget of 4 context files maximum

### Step 4: Implement Authentication

This is the core action. Set up Firebase Authentication for the detected framework:

#### 4a: Firebase Project Initialization

- Install `firebase` package (or `@angular/fire` for Angular projects)
- Create Firebase config file with environment variables:
  - `NEXT_PUBLIC_FIREBASE_API_KEY` / `REACT_APP_FIREBASE_API_KEY` / `VITE_FIREBASE_API_KEY`
  - `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` / equivalent per framework
  - `NEXT_PUBLIC_FIREBASE_PROJECT_ID` / equivalent per framework
- Initialize Firebase app with `initializeApp(firebaseConfig)`
- Export `auth` instance via `getAuth(app)`

#### 4b: Auth Provider Setup

- Configure email/password authentication:
  - Enable in Firebase Console → Authentication → Sign-in method
  - Implement `createUserWithEmailAndPassword` for sign-up
  - Implement `signInWithEmailAndPassword` for sign-in
  - Add `sendEmailVerification` after sign-up
  - Implement `sendPasswordResetEmail` for password recovery
- Configure OAuth providers (Google, Facebook, GitHub, Apple):
  - Create provider instances (`GoogleAuthProvider`, `FacebookAuthProvider`, etc.)
  - Configure scopes and custom parameters per provider
  - Implement `signInWithPopup` or `signInWithRedirect` based on UX requirements
  - Handle `getRedirectResult` for redirect-based flows

#### 4c: Phone Authentication with reCAPTCHA

- Initialize `RecaptchaVerifier` with container element or invisible mode
- Implement `signInWithPhoneNumber` with the reCAPTCHA verifier
- Handle SMS verification code confirmation with `confirmationResult.confirm(code)`
- Configure reCAPTCHA for test phone numbers in development

#### 4d: Custom Token Generation

- Set up Firebase Admin SDK on the server (`firebase-admin`)
- Generate custom tokens with `admin.auth().createCustomToken(uid, claims)`
- Implement client-side `signInWithCustomToken` for custom token authentication
- Handle token expiration (1-hour TTL) with refresh logic

#### 4e: Session Management and Auth State Persistence

- Configure auth persistence mode:
  - `browserLocalPersistence` — persists across browser sessions (default)
  - `browserSessionPersistence` — cleared when tab closes
  - `inMemoryPersistence` — cleared on page refresh
- Set up `onAuthStateChanged` observer for reactive auth state
- Implement sign-out with `signOut(auth)`
- Handle ID token refresh with `onIdTokenChanged`

#### 4f: Protected Route Guards

- **React/Next.js**: Create `AuthProvider` context with `useAuth` hook; wrap protected routes with auth check components
- **Angular**: Implement `AuthGuard` using `canActivate` with `@angular/fire/auth-guard`
- **Vue**: Create Vue Router navigation guards with `beforeEach` hook checking auth state
- Redirect unauthenticated users to sign-in page
- Handle loading states during auth initialization

### Step 5: Generate Output

- Save output to `/claudedocs/firebase-auth_{project}_{YYYY-MM-DD}.md`
- Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
- Include:
  - Firebase SDK setup and configuration code
  - Auth provider implementations (email/password, OAuth, phone)
  - Auth state management and persistence configuration
  - Protected route guard implementation
  - Environment variable list (API key, auth domain, project ID)
  - Error handling patterns for auth operations
  - Testing instructions for auth flows

### Step 6: Update Memory

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="firebase-auth"`. Store any newly learned patterns, conventions, or project insights.

- Update `project_overview.md` with Firebase configuration details
- Update `common_patterns.md` with auth patterns, provider configurations, and route guard implementations
- Record any project-specific auth customizations or workarounds

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Firebase config uses environment variables (not hardcoded keys)
- [ ] `onAuthStateChanged` listener properly unsubscribed in cleanup
- [ ] Auth persistence mode explicitly set based on requirements
- [ ] All auth operations wrapped in try/catch with specific error code handling
- [ ] OAuth redirect domains configured in Firebase Console
- [ ] Email verification enforced after sign-up
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial release — Firebase Authentication with email/password, OAuth providers, phone auth, custom tokens, session management, auth state persistence, protected route guards |
