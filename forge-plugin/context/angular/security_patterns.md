---
id: "angular/security_patterns"
domain: angular
title: "Angular Security Patterns"
type: pattern
estimatedTokens: 600
loadingStrategy: onDemand
version: "0.1.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "XSS Prevention"
    estimatedTokens: 59
    keywords: [xss, prevention, xss]
  - name: "Authentication"
    estimatedTokens: 69
    keywords: [authentication, authentication]
  - name: "HTTP Interceptors"
    estimatedTokens: 65
    keywords: [http, interceptors, interceptors]
  - name: "Authorization"
    estimatedTokens: 38
    keywords: [authorization, authorization]
  - name: "Input Validation"
    estimatedTokens: 51
    keywords: [input, validation, validation]
  - name: "Sensitive Data"
    estimatedTokens: 30
    keywords: [sensitive, data, sensitive-data]
tags: [angular, security, xss, authentication, csrf, jwt, guards, interceptors]
---

# Angular Security Patterns

Security best practices specific to Angular applications.

---

## XSS Prevention {#xss}

### Template Security (Default)

**Angular automatically sanitizes**:
```html
<!-- Safe - Angular escapes user input -->
<div>{{ userInput }}</div>
```

### Unsafe Operations

**innerHTML - Dangerous**:
```typescript
// Bad - XSS vulnerability
element.innerHTML = userInput;
```

**Good - Use DomSanitizer**:
```typescript
import { DomSanitizer } from '@angular/platform-browser';

constructor(private sanitizer: DomSanitizer) {}

getSafeHtml(html: string) {
  return this.sanitizer.sanitize(SecurityContext.HTML, html);
}
```

### bypass Security Trust (Use Sparingly)

```typescript
// Only if you ABSOLUTELY trust the source
trustedHtml = this.sanitizer.bypassSecurityTrustHtml(html);
```

---

## Authentication {#authentication}

### Route Guards

```typescript
@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    return this.authService.isAuthenticated$.pipe(
      map(isAuth => {
        if (!isAuth) {
          this.router.navigate(['/login'], {
            queryParams: { returnUrl: state.url }
          });
          return false;
        }
        return true;
      }),
      catchError(() => {
        this.router.navigate(['/login']);
        return of(false);
      })
    );
  }
}
```

### JWT Token Storage

**Avoid localStorage (XSS risk)**:
```typescript
// Bad
localStorage.setItem('token', token);
```

**Use httpOnly cookies (preferred)**:
```typescript
// Backend sets:
Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict
```

---

## HTTP Interceptors {#interceptors}

### Auth Token Injection

```typescript
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const token = this.authService.getToken();
    if (token) {
      const cloned = req.clone({
        setHeaders: { Authorization: `Bearer ${token}` }
      });
      return next.handle(cloned);
    }
    return next.handle(req);
  }
}
```

### CSRF Protection

```typescript
@Injectable()
export class CsrfInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    if (req.method !== 'GET') {
      const csrfToken = this.getCsrfToken();
      const cloned = req.clone({
        setHeaders: { 'X-CSRF-Token': csrfToken }
      });
      return next.handle(cloned);
    }
    return next.handle(req);
  }
}
```

---

## Authorization {#authorization}

### Role-Based Access Control

```typescript
@Injectable()
export class RoleGuard implements CanActivate {
  canActivate(route: ActivatedRouteSnapshot): boolean {
    const requiredRoles = route.data['roles'] as string[];
    const userRoles = this.authService.getUserRoles();

    return requiredRoles.some(role => userRoles.includes(role));
  }
}

// Route configuration
{
  path: 'admin',
  component: AdminComponent,
  canActivate: [AuthGuard, RoleGuard],
  data: { roles: ['admin'] }
}
```

---

## Input Validation {#validation}

### Form Validation

```typescript
form = this.fb.group({
  email: ['', [Validators.required, Validators.email]],
  password: ['', [
    Validators.required,
    Validators.minLength(8),
    this.strongPasswordValidator
  ]]
});

strongPasswordValidator(control: AbstractControl) {
  const value = control.value;
  if (!value) return null;

  const hasNumber = /[0-9]/.test(value);
  const hasUpper = /[A-Z]/.test(value);
  const hasLower = /[a-z]/.test(value);
  const hasSpecial = /[!@#$%^&*]/.test(value);

  const valid = hasNumber && hasUpper && hasLower && hasSpecial;
  return valid ? null : { weakPassword: true };
}
```

---

## Sensitive Data {#sensitive-data}

### Avoid Logging Sensitive Data

```typescript
// Bad
console.log('User:', user); // May log passwords, tokens

// Good
console.log('User ID:', user.id);
```

### Remove Debug Code

```typescript
// Remove before production
// console.log('API Token:', token);
// debugger;
```

---

**Version**: 0.1.0-alpha
