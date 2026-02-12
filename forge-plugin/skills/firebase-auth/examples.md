# Firebase Auth - Usage Examples

This document provides practical examples of how to use the `firebase-auth` skill in various scenarios.

---

## Example 1: Setting Up Email/Password Authentication in a React Application

**Scenario**: A new React application needs Firebase Authentication with email/password sign-up, sign-in, email verification, and password reset functionality.

**Command**:
```
skill:firebase-auth

Set up Firebase email/password authentication in my React app. I need sign-up with email verification, sign-in, password reset, and a protected dashboard route.
```

**What Happens**:
1. Skill detects React from `package.json` and `src/App.tsx`
2. Loads memory — no existing memory found, creates new project directory
3. Loads security domain context for authentication and session management patterns
4. Installs `firebase` package and creates Firebase config:
   ```ts
   // src/lib/firebase.ts
   import { initializeApp } from 'firebase/app'
   import { getAuth } from 'firebase/auth'

   const firebaseConfig = {
     apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
     authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
     projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
     storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
     messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
     appId: import.meta.env.VITE_FIREBASE_APP_ID,
   }

   const app = initializeApp(firebaseConfig)
   export const auth = getAuth(app)
   ```
5. Creates AuthProvider context with `onAuthStateChanged`:
   ```tsx
   // src/contexts/AuthContext.tsx
   import { createContext, useContext, useEffect, useState } from 'react'
   import { User, onAuthStateChanged } from 'firebase/auth'
   import { auth } from '../lib/firebase'

   interface AuthContextType {
     user: User | null
     loading: boolean
   }

   const AuthContext = createContext<AuthContextType>({ user: null, loading: true })

   export function AuthProvider({ children }: { children: React.ReactNode }) {
     const [user, setUser] = useState<User | null>(null)
     const [loading, setLoading] = useState(true)

     useEffect(() => {
       const unsubscribe = onAuthStateChanged(auth, (user) => {
         setUser(user)
         setLoading(false)
       })
       return () => unsubscribe()
     }, [])

     return (
       <AuthContext.Provider value={{ user, loading }}>
         {children}
       </AuthContext.Provider>
     )
   }

   export const useAuth = () => useContext(AuthContext)
   ```
6. Creates sign-up with email verification:
   ```tsx
   // src/pages/SignUp.tsx
   import { createUserWithEmailAndPassword, sendEmailVerification } from 'firebase/auth'
   import { auth } from '../lib/firebase'

   async function handleSignUp(email: string, password: string) {
     try {
       const userCredential = await createUserWithEmailAndPassword(auth, email, password)
       await sendEmailVerification(userCredential.user)
       // Redirect to verification notice page
     } catch (error: any) {
       switch (error.code) {
         case 'auth/email-already-in-use':
           // Handle duplicate email
           break
         case 'auth/weak-password':
           // Handle weak password
           break
         default:
           // Handle other errors
       }
     }
   }
   ```
7. Creates protected route component:
   ```tsx
   // src/components/ProtectedRoute.tsx
   import { Navigate } from 'react-router-dom'
   import { useAuth } from '../contexts/AuthContext'

   export function ProtectedRoute({ children }: { children: React.ReactNode }) {
     const { user, loading } = useAuth()
     if (loading) return <div>Loading...</div>
     if (!user) return <Navigate to="/sign-in" />
     return <>{children}</>
   }
   ```
8. Saves output to `/claudedocs/firebase-auth_myapp_2026-02-12.md`
9. Creates memory with project overview and auth patterns

**Expected Output**:
```markdown
# Firebase Auth Implementation: MyApp
**Date**: 2026-02-12

## SDK Configuration
- Package: firebase v10.x (modular SDK)
- Framework: React with Vite
- Auth instance: getAuth(app) in src/lib/firebase.ts

## Authentication Methods
- Email/Password: sign-up with email verification, sign-in, password reset
- Persistence: browserLocalPersistence (default)

## Route Protection
- Public: /, /sign-in, /sign-up, /forgot-password
- Protected: /dashboard/* (via ProtectedRoute component)
- Auth state: AuthProvider context with useAuth hook

## Files Created
- src/lib/firebase.ts — Firebase initialization
- src/contexts/AuthContext.tsx — Auth state provider
- src/pages/SignUp.tsx — Sign-up with email verification
- src/pages/SignIn.tsx — Sign-in form
- src/pages/ForgotPassword.tsx — Password reset
- src/components/ProtectedRoute.tsx — Route guard
- .env.local — Firebase environment variables

## Environment Variables
- VITE_FIREBASE_API_KEY
- VITE_FIREBASE_AUTH_DOMAIN
- VITE_FIREBASE_PROJECT_ID
- VITE_FIREBASE_STORAGE_BUCKET
- VITE_FIREBASE_MESSAGING_SENDER_ID
- VITE_FIREBASE_APP_ID
```

---

## Example 2: Adding Google OAuth Sign-In with Firebase

**Scenario**: An existing React application with Firebase needs Google OAuth sign-in alongside the existing email/password authentication.

**Command**:
```
skill:firebase-auth

Add Google OAuth sign-in to my React app that already has Firebase email/password auth. I want both popup and redirect options, and I need to capture the user's Google profile photo and display name.
```

**What Happens**:
1. Skill detects React with existing Firebase setup from `src/lib/firebase.ts`
2. Loads memory — finds existing project with email/password auth configured
3. Loads security context for OAuth and social authentication patterns
4. Configures Google Auth Provider with profile scopes:
   ```ts
   // src/lib/auth.ts
   import {
     GoogleAuthProvider,
     signInWithPopup,
     signInWithRedirect,
     getRedirectResult,
   } from 'firebase/auth'
   import { auth } from './firebase'

   const googleProvider = new GoogleAuthProvider()
   googleProvider.addScope('profile')
   googleProvider.addScope('email')
   googleProvider.setCustomParameters({ prompt: 'select_account' })

   export async function signInWithGoogle(useRedirect = false) {
     try {
       if (useRedirect) {
         await signInWithRedirect(auth, googleProvider)
       } else {
         const result = await signInWithPopup(auth, googleProvider)
         const credential = GoogleAuthProvider.credentialFromResult(result)
         return {
           user: result.user,
           accessToken: credential?.accessToken,
         }
       }
     } catch (error: any) {
       if (error.code === 'auth/popup-closed-by-user') {
         // User closed the popup — not an error to display
         return null
       }
       if (error.code === 'auth/account-exists-with-different-credential') {
         // Handle account linking scenario
         throw new Error('An account already exists with this email. Sign in with your original method.')
       }
       throw error
     }
   }
   ```
5. Handles redirect result on app initialization:
   ```ts
   // src/lib/auth.ts (continued)
   export async function handleRedirectResult() {
     try {
       const result = await getRedirectResult(auth)
       if (result) {
         const credential = GoogleAuthProvider.credentialFromResult(result)
         return {
           user: result.user,
           accessToken: credential?.accessToken,
         }
       }
       return null
     } catch (error: any) {
       console.error('Redirect sign-in failed:', error)
       throw error
     }
   }
   ```
6. Creates Google sign-in button component:
   ```tsx
   // src/components/GoogleSignInButton.tsx
   import { signInWithGoogle } from '../lib/auth'

   export function GoogleSignInButton() {
     const handleClick = async () => {
       try {
         const result = await signInWithGoogle()
         if (result) {
           console.log('Signed in:', result.user.displayName)
           console.log('Photo URL:', result.user.photoURL)
         }
       } catch (error) {
         // Display error to user
       }
     }

     return (
       <button onClick={handleClick}>
         Sign in with Google
       </button>
     )
   }
   ```
7. Saves output and updates memory with OAuth patterns

**Expected Output**:
```markdown
# Firebase Auth - Google OAuth: MyApp
**Date**: 2026-02-12

## Google OAuth Configuration
- Provider: GoogleAuthProvider with profile + email scopes
- Sign-in method: Popup (default) with redirect fallback
- Custom parameters: prompt=select_account (forces account picker)

## User Profile Data
- displayName: Available from result.user.displayName
- photoURL: Available from result.user.photoURL
- email: Available from result.user.email

## Firebase Console Checklist
- [ ] Enable Google sign-in in Authentication → Sign-in method
- [ ] Add authorized domains for OAuth redirects
- [ ] Configure OAuth consent screen in Google Cloud Console

## Error Handling
| Error Code | Handling |
|------------|----------|
| auth/popup-closed-by-user | Silent — user cancelled |
| auth/account-exists-with-different-credential | Prompt to sign in with original method |
| auth/popup-blocked | Fall back to redirect flow |

## Files Created/Modified
- src/lib/auth.ts — Google OAuth sign-in functions
- src/components/GoogleSignInButton.tsx — Sign-in button component
```

---

## Example 3: Implementing Phone Authentication with reCAPTCHA Verification

**Scenario**: A Next.js application needs phone number authentication for users who prefer SMS-based sign-in. The implementation must include reCAPTCHA verification and handle the two-step verification flow.

**Command**:
```
skill:firebase-auth

Implement phone authentication with reCAPTCHA in my Next.js app. I need invisible reCAPTCHA, SMS code input, and proper error handling for invalid phone numbers and expired codes.
```

**What Happens**:
1. Skill detects Next.js App Router from `next.config.ts` and `app/` directory
2. Loads memory — finds existing project with Firebase configured
3. Loads security context for phone authentication and reCAPTCHA patterns
4. Creates phone auth utility with reCAPTCHA setup:
   ```ts
   // src/lib/phone-auth.ts
   import {
     RecaptchaVerifier,
     signInWithPhoneNumber,
     ConfirmationResult,
   } from 'firebase/auth'
   import { auth } from './firebase'

   let recaptchaVerifier: RecaptchaVerifier | null = null

   export function initRecaptcha(containerId: string) {
     if (recaptchaVerifier) {
       recaptchaVerifier.clear()
     }
     recaptchaVerifier = new RecaptchaVerifier(auth, containerId, {
       size: 'invisible',
       callback: () => {
         // reCAPTCHA solved — allow signInWithPhoneNumber
       },
       'expired-callback': () => {
         // reCAPTCHA expired — reset and prompt user to retry
         recaptchaVerifier?.clear()
         recaptchaVerifier = null
       },
     })
     return recaptchaVerifier
   }

   export async function sendVerificationCode(phoneNumber: string): Promise<ConfirmationResult> {
     if (!recaptchaVerifier) {
       throw new Error('reCAPTCHA not initialized. Call initRecaptcha() first.')
     }

     try {
       const confirmationResult = await signInWithPhoneNumber(auth, phoneNumber, recaptchaVerifier)
       return confirmationResult
     } catch (error: any) {
       recaptchaVerifier.clear()
       recaptchaVerifier = null

       switch (error.code) {
         case 'auth/invalid-phone-number':
           throw new Error('Invalid phone number format. Use E.164 format (e.g., +1234567890).')
         case 'auth/too-many-requests':
           throw new Error('Too many attempts. Please try again later.')
         case 'auth/captcha-check-failed':
           throw new Error('reCAPTCHA verification failed. Please refresh and try again.')
         default:
           throw error
       }
     }
   }

   export async function confirmVerificationCode(
     confirmationResult: ConfirmationResult,
     code: string
   ) {
     try {
       const userCredential = await confirmationResult.confirm(code)
       return userCredential.user
     } catch (error: any) {
       switch (error.code) {
         case 'auth/invalid-verification-code':
           throw new Error('Invalid verification code. Please check and try again.')
         case 'auth/code-expired':
           throw new Error('Verification code expired. Please request a new code.')
         default:
           throw error
       }
     }
   }

   export function cleanupRecaptcha() {
     if (recaptchaVerifier) {
       recaptchaVerifier.clear()
       recaptchaVerifier = null
     }
   }
   ```
5. Creates phone sign-in page component:
   ```tsx
   // app/phone-sign-in/page.tsx
   'use client'

   import { useEffect, useRef, useState } from 'react'
   import { ConfirmationResult } from 'firebase/auth'
   import {
     initRecaptcha,
     sendVerificationCode,
     confirmVerificationCode,
     cleanupRecaptcha,
   } from '@/lib/phone-auth'

   export default function PhoneSignIn() {
     const [phone, setPhone] = useState('')
     const [code, setCode] = useState('')
     const [step, setStep] = useState<'phone' | 'code'>('phone')
     const [error, setError] = useState<string | null>(null)
     const [loading, setLoading] = useState(false)
     const confirmationRef = useRef<ConfirmationResult | null>(null)

     useEffect(() => {
       initRecaptcha('recaptcha-container')
       return () => cleanupRecaptcha()
     }, [])

     async function handleSendCode() {
       setError(null)
       setLoading(true)
       try {
         confirmationRef.current = await sendVerificationCode(phone)
         setStep('code')
       } catch (err: any) {
         setError(err.message)
       } finally {
         setLoading(false)
       }
     }

     async function handleVerifyCode() {
       if (!confirmationRef.current) return
       setError(null)
       setLoading(true)
       try {
         await confirmVerificationCode(confirmationRef.current, code)
         // User is signed in — redirect to dashboard
       } catch (err: any) {
         setError(err.message)
       } finally {
         setLoading(false)
       }
     }

     return (
       <div>
         <h1>Phone Sign-In</h1>
         {error && <p style={{ color: 'red' }}>{error}</p>}

         {step === 'phone' ? (
           <div>
             <input
               type="tel"
               value={phone}
               onChange={(e) => setPhone(e.target.value)}
               placeholder="+1234567890"
             />
             <button onClick={handleSendCode} disabled={loading}>
               {loading ? 'Sending...' : 'Send Code'}
             </button>
           </div>
         ) : (
           <div>
             <input
               type="text"
               value={code}
               onChange={(e) => setCode(e.target.value)}
               placeholder="Enter 6-digit code"
               maxLength={6}
             />
             <button onClick={handleVerifyCode} disabled={loading}>
               {loading ? 'Verifying...' : 'Verify Code'}
             </button>
           </div>
         )}

         <div id="recaptcha-container" />
       </div>
     )
   }
   ```
6. Saves output with Firebase Console phone auth configuration checklist
7. Updates memory with phone auth patterns and reCAPTCHA setup

**Expected Output**:
```markdown
# Firebase Auth - Phone Authentication: MyApp
**Date**: 2026-02-12

## Phone Auth Configuration
- reCAPTCHA: Invisible mode
- Phone format: E.164 (e.g., +1234567890)
- Two-step flow: Send code → Verify code

## Firebase Console Checklist
- [ ] Enable Phone sign-in in Authentication → Sign-in method
- [ ] Add test phone numbers for development (Authentication → Phone → Test phone numbers)
- [ ] Configure reCAPTCHA settings (default is sufficient for most use cases)

## Error Handling
| Error Code | User Message |
|------------|-------------|
| auth/invalid-phone-number | Invalid phone number format |
| auth/too-many-requests | Rate limited — try again later |
| auth/captcha-check-failed | reCAPTCHA failed — refresh page |
| auth/invalid-verification-code | Invalid code — re-enter |
| auth/code-expired | Code expired — request new code |

## Files Created
- src/lib/phone-auth.ts — Phone auth utilities with reCAPTCHA
- app/phone-sign-in/page.tsx — Two-step phone sign-in page

## Security Notes
- Invisible reCAPTCHA prevents automated abuse
- reCAPTCHA verifier cleared on error and component unmount
- Phone numbers validated in E.164 format before sending
- Test phone numbers should only be used in development
```

---

## Common Usage Patterns

### Pattern 1: Basic Email/Password Setup
```
skill:firebase-auth
Set up Firebase email/password auth in my React app with sign-up, sign-in, and password reset
```
Use for new projects needing basic Firebase authentication.

### Pattern 2: Add OAuth Provider
```
skill:firebase-auth
Add Google and GitHub OAuth sign-in to my existing Firebase auth setup
```
Use when adding social login to a project with existing Firebase auth.

### Pattern 3: Phone Auth
```
skill:firebase-auth
Implement phone number authentication with reCAPTCHA in my Next.js app
```
Use for SMS-based authentication flows.

### Pattern 4: Custom Tokens for Server Auth
```
skill:firebase-auth
Set up Firebase custom token authentication for my API server that issues tokens from a Node.js backend
```
Use when server-side systems need to generate Firebase auth tokens.

### Pattern 5: Session Management
```
skill:firebase-auth
Configure Firebase auth session persistence and add protected route guards to my Vue app
```
Use when configuring auth state persistence and route protection.

---

## Tips for Effective Usage

1. **Have Firebase config ready** — obtain your Firebase project config from Firebase Console → Project Settings → General before running the skill
2. **Specify your framework** — mention React, Next.js, Angular, or Vue to get framework-specific implementations
3. **Use modular SDK imports** — Firebase v9+ modular imports enable tree-shaking and smaller bundle sizes
4. **Always unsubscribe auth listeners** — forgetting cleanup causes memory leaks and stale state
5. **Handle all error codes** — Firebase auth has specific error codes; generic error handling loses useful information
6. **Test with emulator** — use `connectAuthEmulator(auth, 'http://localhost:9099')` for local development

---

## When to Use This Skill

**Ideal Scenarios**:
- Projects using Firebase as the backend platform
- Applications needing multiple auth methods (email, OAuth, phone)
- Projects requiring auth state persistence and session management
- Applications with protected routes and role-based access
- Mobile-first applications using Firebase across platforms

**Not Ideal For**:
- Projects using Clerk for managed auth (use `clerk-auth` skill)
- Self-hosted authentication (use `better-auth` skill)
- Azure AD / Entra ID authentication (use `azure-auth` skill)
- Projects not using Firebase as a backend platform
