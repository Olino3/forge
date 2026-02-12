# Firebase Auth - Memory System

This file documents the memory structure for the `firebase-auth` skill. Memory is project-specific knowledge that accumulates over time through repeated Firebase Authentication implementations.

---

## Purpose

The memory system enables the skill to:
- **Learn project patterns** — understand project-specific Firebase configurations, auth providers, and route guards
- **Avoid repeat work** — reuse established auth provider setups and protected route patterns
- **Track decisions** — record why specific providers, persistence modes, or guard implementations were chosen
- **Prevent errors** — remember project-specific authorized domains, reCAPTCHA settings, and custom token configurations
- **Improve accuracy** — better recommendations based on project history

---

## Memory vs Context

**Memory** (this directory):
- Project-specific
- Dynamic (changes with each implementation)
- Per-project subdirectories
- Example: "This project uses Google and GitHub OAuth with popup sign-in and browserSessionPersistence"

**Context** (`../../context/security/`):
- Universal security and authentication knowledge
- Static (changes rarely)
- Shared across all projects
- Example: "OAuth 2.0 best practices and session management patterns"

---

## Memory Structure

```
memory/skills/firebase-auth/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # CRITICAL — Firebase config, SDK version, auth providers
    └── common_patterns.md         # Project-specific auth patterns and conventions
```

---

## Per-Project Memory Files

### 1. project_overview.md (CRITICAL)

**Purpose**: High-level understanding of the project's Firebase Authentication setup.

**Always Update On First Run**:
- Firebase SDK version (v9 modular or v8 compat)
- Framework (React, Next.js, Angular, Vue) and version
- Enabled auth providers (email/password, Google, Facebook, GitHub, Apple, phone, anonymous, custom tokens)
- Auth persistence mode (`browserLocalPersistence`, `browserSessionPersistence`, `inMemoryPersistence`)
- Protected routes and public routes
- Auth state management approach (Context API, NgRx, Pinia, etc.)
- Environment variables configured
- Firebase project ID and auth domain

**Update Incrementally**:
- Add new auth providers as they are enabled
- Record new protected or public routes
- Document persistence mode changes
- Note custom token configurations
- Track environment-specific configuration (dev, staging, production)

**Example Structure**:
```markdown
# Project Overview: MySaaSApp

## Firebase Configuration
- **SDK**: firebase v10.x (modular)
- **Project ID**: my-saas-app-12345
- **Auth Domain**: my-saas-app-12345.firebaseapp.com

## Framework
- **Framework**: React 18.x with Vite
- **Auth State**: AuthProvider context with useAuth hook

## Auth Providers
- **Email/Password**: Enabled with email verification
- **Google OAuth**: Popup sign-in with profile + email scopes
- **GitHub OAuth**: Popup sign-in
- **Phone**: Invisible reCAPTCHA

## Route Protection
- **Public**: /, /sign-in, /sign-up, /forgot-password
- **Protected**: /dashboard/*, /settings/*, /profile
- **Guard**: ProtectedRoute component with useAuth hook

## Persistence
- **Mode**: browserLocalPersistence (default)
- **Session**: onAuthStateChanged observer in AuthProvider

## Environment Variables
- VITE_FIREBASE_API_KEY
- VITE_FIREBASE_AUTH_DOMAIN
- VITE_FIREBASE_PROJECT_ID
- VITE_FIREBASE_STORAGE_BUCKET
- VITE_FIREBASE_MESSAGING_SENDER_ID
- VITE_FIREBASE_APP_ID
```

### 2. common_patterns.md

**Purpose**: Document recurring Firebase auth patterns specific to this project.

**What to Document**:
- Auth provider configuration patterns
- Sign-in/sign-up flow implementations
- Auth state observer patterns (`onAuthStateChanged`, `onIdTokenChanged`)
- Protected route guard implementations
- Error handling approaches for auth operations
- Custom token generation and verification patterns
- reCAPTCHA integration patterns
- Client-side component integration patterns

**Example**:
```markdown
# Common Patterns: MySaaSApp

## Auth Initialization
Firebase initialized in src/lib/firebase.ts:
1. Config from environment variables
2. initializeApp(firebaseConfig)
3. Export auth = getAuth(app)

## Auth State Management
AuthProvider context wraps the app:
1. onAuthStateChanged sets user state
2. Unsubscribe in useEffect cleanup
3. Loading state during auth initialization
4. useAuth hook for consuming components

## Sign-In Patterns
- Email/Password: signInWithEmailAndPassword with error code handling
- Google OAuth: signInWithPopup with fallback to signInWithRedirect
- Phone: Two-step flow with invisible reCAPTCHA

## Error Handling
All auth operations use try/catch with switch on error.code:
- auth/email-already-in-use → "Account exists" message
- auth/wrong-password → "Invalid credentials" message
- auth/user-not-found → "No account found" message
- auth/too-many-requests → "Rate limited" message

## Route Protection
ProtectedRoute component pattern:
1. Check useAuth() for user and loading state
2. Show loading spinner during initialization
3. Redirect to /sign-in if no user
4. Render children if authenticated
```

---

## Workflow

### First Use on a Project

1. **Check for existing memory**: Does `{project-name}/` directory exist?
2. **If NO**: Create memory directory and both files
3. **If YES**: Load existing memory files

### Subsequent Uses

1. **Load all existing memory files** (Step 2 of skill workflow)
2. **Use memory to inform implementation** (understand existing Firebase setup)
3. **After implementation**: Update ALL memory files with new insights

---

## Memory Update Guidelines

### project_overview.md Updates
- **First run**: Create comprehensive overview of Firebase configuration
- **Subsequent runs**: Add new providers, routes, or configuration changes
- **Update when**: New auth providers enabled, route guards added, persistence mode changed, custom tokens configured

### common_patterns.md Updates
- **Add patterns** observed or implemented in this session
- **Don't remove patterns** unless they are no longer applicable
- **Refine patterns** as the Firebase auth setup evolves
- **Document workarounds** for version-specific or framework-specific issues

---

## Benefits of Memory System

1. **Consistency**
   - Same auth patterns applied across the project
   - Provider configurations follow established conventions

2. **Speed**
   - Subsequent auth changes are faster (context already loaded)
   - Known providers and route guards readily available

3. **Error Prevention**
   - Authorized domains documented — prevents OAuth redirect failures
   - Auth listener cleanup tracked — prevents memory leaks
   - Persistence mode recorded — prevents unexpected session behavior

4. **Traceability**
   - Auth provider decisions recorded with rationale
   - Route protection changes tracked over time

---

## Memory File Size

**Keep memory files concise**:
- project_overview.md: ~100-300 lines
- common_patterns.md: ~200-400 lines

**If memory grows too large**:
- Consolidate similar patterns
- Archive outdated provider configurations
- Summarize historical changes

---

## Related Documentation

- **Skill Workflow**: `../../skills/firebase-auth/SKILL.md`
- **Context System**: `../../context/security/index.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
