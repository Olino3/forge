---
id: "angular/service_patterns"
domain: angular
title: "Angular Service Patterns"
type: pattern
estimatedTokens: 600
loadingStrategy: onDemand
version: "0.3.0-alpha"
lastUpdated: "2026-02-10"
sections:
  - name: "Service Basics"
    estimatedTokens: 48
    keywords: [service, basics, basics]
  - name: "HTTP Service Patterns"
    estimatedTokens: 90
    keywords: [http, service, patterns, http]
  - name: "State Management Service"
    estimatedTokens: 57
    keywords: [state, management, service, state]
  - name: "Dependency Injection Patterns"
    estimatedTokens: 54
    keywords: [dependency, injection, patterns]
  - name: "HTTP Interceptors"
    estimatedTokens: 75
    keywords: [http, interceptors, interceptors]

tags: [angular, services, dependency-injection, http, state-management, interceptors]
---
# Angular Service Patterns

Best practices for Angular service design, dependency injection, and state management.

---

## Service Basics {#basics}

### Tree-Shakable Services (Recommended)

```typescript
@Injectable({
  providedIn: 'root' // Single instance, tree-shakable
})
export class UserService {
  constructor(private http: HttpClient) {}
}
```

**Benefits**:
- Single instance across app
- Automatically tree-shaken if unused
- No need to provide in module

### Module-Scoped Services

```typescript
@Injectable()
export class FeatureService {}

@NgModule({
  providers: [FeatureService] // New instance per module
})
export class FeatureModule {}
```

---

## HTTP Service Patterns {#http}

### Basic HTTP Service

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private apiUrl = '/api/users';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl).pipe(
      catchError(this.handleError)
    );
  }

  getUser(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`).pipe(
      catchError(this.handleError)
    );
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(this.apiUrl, user).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    console.error('API error:', error);
    return throwError(() => error);
  }
}
```

### Caching Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private cache$ = new BehaviorSubject<User[] | null>(null);

  getUsers(forceRefresh = false): Observable<User[]> {
    if (!forceRefresh && this.cache$.value) {
      return this.cache$.asObservable().pipe(
        filter(users => users !== null)
      );
    }

    return this.http.get<User[]>('/api/users').pipe(
      tap(users => this.cache$.next(users)),
      catchError(error => {
        console.error(error);
        return of([]);
      })
    );
  }

  clearCache() {
    this.cache$.next(null);
  }
}
```

---

## State Management Service {#state}

### BehaviorSubject Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class UserStateService {
  private usersSubject = new BehaviorSubject<User[]>([]);
  users$ = this.usersSubject.asObservable();

  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  private errorSubject = new BehaviorSubject<string | null>(null);
  error$ = this.errorSubject.asObservable();

  constructor(private userService: UserService) {}

  loadUsers() {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);

    this.userService.getUsers().subscribe({
      next: users => {
        this.usersSubject.next(users);
        this.loadingSubject.next(false);
      },
      error: error => {
        this.errorSubject.next(error.message);
        this.loadingSubject.next(false);
      }
    });
  }

  addUser(user: User) {
    const currentUsers = this.usersSubject.value;
    this.usersSubject.next([...currentUsers, user]);
  }
}
```

---

## Dependency Injection Patterns {#di}

### Constructor Injection (Standard)

```typescript
constructor(
  private http: HttpClient,
  private router: Router,
  private authService: AuthService
) {}
```

### Optional Dependencies

```typescript
constructor(
  @Optional() private configService: ConfigService
) {
  if (this.configService) {
    // Use config
  }
}
```

### Injection Tokens

```typescript
export const API_URL = new InjectionToken<string>('apiUrl');

@Injectable()
export class ApiService {
  constructor(@Inject(API_URL) private apiUrl: string) {}
}

// Provide
providers: [
  { provide: API_URL, useValue: 'https://api.example.com' }
]
```

---

## HTTP Interceptors {#interceptors}

### Auth Interceptor

```typescript
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();

    if (token) {
      const cloned = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${token}`)
      });
      return next.handle(cloned);
    }

    return next.handle(req);
  }
}
```

### Error Interceptor

```typescript
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          // Handle unauthorized
        } else if (error.status === 500) {
          // Handle server error
        }
        return throwError(() => error);
      })
    );
  }
}
```

---

**Version**: 0.3.0-alpha
