# OAuth Integrations - Memory System

This file documents the memory structure for the `oauth-integrations` skill. Memory is project-specific knowledge that accumulates over time through repeated OAuth 2.0 implementations across GitHub, Okta, Google, and Microsoft Entra providers.

---

## Purpose

The memory system enables the skill to:
- **Learn project patterns** — understand project-specific OAuth configurations, provider setups, and token management strategies
- **Avoid repeat work** — reuse established provider configurations, callback handlers, and scope settings
- **Track decisions** — record why specific OAuth flows, providers, or token storage strategies were chosen
- **Prevent errors** — remember project-specific redirect URIs, tenant IDs, and scope requirements
- **Improve accuracy** — better recommendations based on project history

---

## Memory vs Context

**Memory** (this directory):
- Project-specific
- Dynamic (changes with each implementation)
- Per-project subdirectories
- Example: "This project uses GitHub OAuth App with read:user scope and server-side session storage"

**Context** (`../../context/security/`):
- Universal security and authentication knowledge
- Static (changes rarely)
- Shared across all projects
- Example: "OAuth 2.0 Authorization Code Flow best practices and PKCE implementation"

---

## Memory Structure

```
memory/skills/oauth-integrations/
├── index.md (this file)
└── {project-name}/
    ├── project_overview.md        # CRITICAL — OAuth providers, flows, redirect URIs
    └── common_patterns.md         # Project-specific OAuth patterns and conventions
```

---

## Per-Project Memory Files

### 1. project_overview.md (CRITICAL)

**Purpose**: High-level understanding of the project's OAuth 2.0 setup.

**Always Update On First Run**:
- Configured OAuth providers (GitHub, Okta, Google, Microsoft Entra)
- OAuth flow type per provider (Authorization Code, PKCE, Device Flow)
- Framework (Express, Next.js, FastAPI, Spring Boot) and version
- Token storage strategy (server-side session, encrypted cookies, database)
- Registered redirect URIs per provider
- Scope configuration per provider
- Environment variables configured
- Multi-provider account linking strategy (if applicable)

**Update Incrementally**:
- Add new OAuth providers as they are integrated
- Record new or changed redirect URIs
- Document scope changes and incremental authorization
- Note token refresh and rotation configurations
- Track provider-specific customizations

**Example Structure**:
```markdown
# Project Overview: MySaaSApp

## Architecture
- **Pattern**: Backend-for-Frontend (BFF)
- **Backend**: Express 4.x with TypeScript
- **Frontend**: React 18.x with Vite
- **Token Storage**: Server-side sessions (express-session + Redis)

## OAuth Providers
### GitHub
- **Type**: OAuth App
- **Flow**: Authorization Code Flow
- **Scopes**: read:user, user:email
- **Redirect URI**: https://app.example.com/api/auth/github/callback
- **Environment**: GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET

### Google
- **Flow**: Authorization Code Flow + PKCE
- **Scopes**: openid, profile, email
- **Redirect URI**: https://app.example.com/api/auth/google/callback
- **Consent Screen**: External, verified
- **Offline Access**: Enabled (refresh tokens)
- **Environment**: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

## Security
- State parameter: 32-byte random hex, stored in session
- PKCE: S256 for Google (public client flow)
- Tokens never sent to browser (BFF pattern)

## Account Linking
- Users can link multiple providers to one account
- Linked via email address matching
- Primary provider determined by first sign-in
```

### 2. common_patterns.md

**Purpose**: Document recurring OAuth patterns specific to this project.

**What to Document**:
- OAuth flow implementation patterns (authorization, callback, token exchange)
- Provider configuration patterns and initialization
- Token management patterns (storage, refresh, rotation, revocation)
- PKCE implementation details
- State parameter generation and validation
- Error handling approaches for OAuth operations
- Multi-provider routing and account linking patterns
- Middleware patterns for auth guards and token refresh

**Example**:
```markdown
# Common Patterns: MySaaSApp

## Authorization Flow
All providers follow the same pattern:
1. Generate state + PKCE verifier (store in session)
2. Redirect to provider authorization endpoint
3. Provider redirects to callback with code + state
4. Validate state, exchange code for tokens
5. Fetch user profile, create/update session
6. Redirect to frontend

## Token Refresh
- Check token expiration before API calls
- Use refresh_token grant type for new access tokens
- Google: refresh tokens only on first auth (prompt=consent)
- Entra: refresh token rotation enabled

## Error Handling
All OAuth callbacks use try/catch with provider-specific handling:
- Invalid state → 403 redirect to /auth-error
- Token exchange failure → Log error, redirect to /auth-error
- User profile fetch failure → Retry once, then redirect to /auth-error
- Rate limiting (GitHub) → Exponential backoff

## Account Linking
When user signs in with new provider:
1. Check if email matches existing account
2. If match: link provider to existing account
3. If no match: create new account
4. Store provider-specific user ID in database
```

---

## Workflow

### First Use on a Project

1. **Check for existing memory**: Does `{project-name}/` directory exist?
2. **If NO**: Create memory directory and both files
3. **If YES**: Load existing memory files

### Subsequent Uses

1. **Load all existing memory files** (Step 2 of skill workflow)
2. **Use memory to inform implementation** (understand existing OAuth setup)
3. **After implementation**: Update ALL memory files with new insights

---

## Memory Update Guidelines

### project_overview.md Updates
- **First run**: Create comprehensive overview of OAuth configuration
- **Subsequent runs**: Add new providers, update scopes, record redirect URI changes
- **Update when**: New OAuth provider added, flow type changed, token storage strategy updated, scopes modified

### common_patterns.md Updates
- **Add patterns** observed or implemented in this session
- **Don't remove patterns** unless they are no longer applicable
- **Refine patterns** as the OAuth setup evolves
- **Document workarounds** for provider-specific quirks and version issues

---

## Benefits of Memory System

1. **Consistency**
   - Same OAuth patterns applied across the project
   - Provider configurations follow established conventions

2. **Speed**
   - Subsequent provider additions are faster (architecture already known)
   - Known token management patterns readily available

3. **Error Prevention**
   - Redirect URIs documented — prevents OAuth callback mismatches
   - Scope configurations tracked — prevents authorization failures
   - Provider quirks recorded — prevents known pitfalls

4. **Traceability**
   - OAuth provider decisions recorded with rationale
   - Token management strategy changes tracked over time

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

- **Skill Workflow**: `../../skills/oauth-integrations/SKILL.md`
- **Context System**: `../../context/security/index.md`
- **Main Memory Index**: `../index.md`

---

**Version**: 1.0.0
**Last Updated**: 2026-02-12
