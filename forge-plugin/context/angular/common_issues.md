# Angular Common Issues

This file catalogs the most frequently encountered issues in Angular applications. These are universal problems that occur across projects regardless of architecture or tech stack.

**Load this file**: ALWAYS (for every Angular code review)

---

## Table of Contents

1. [Memory Leaks](#memory-leaks)
2. [Change Detection Errors](#change-detection-errors)
3. [Lifecycle Hook Misuse](#lifecycle-hook-misuse)
4. [Observable Subscription Problems](#observable-subscription-problems)
5. [Template Syntax Mistakes](#template-syntax-mistakes)
6. [Zone.js Issues](#zonejs-issues)
7. [Dependency Injection Problems](#dependency-injection-problems)
8. [Router Navigation Issues](#router-navigation-issues)

---

## Memory Leaks {#memory-leaks}

### 1. Unmanaged Observable Subscriptions

**Problem**: Most common Angular memory leak - subscriptions not cleaned up.

**Bad**:
```typescript
ngOnInit() {
  this.userService.getUsers().subscribe(users => {
    this.users = users;
  });
  // Subscription never cleaned up!
}
```

**Good - Option 1 (takeUntil pattern)**:
```typescript
private destroy$ = new Subject<void>();

ngOnInit() {
  this.userService.getUsers()
    .pipe(takeUntil(this.destroy$))
    .subscribe(users => this.users = users);
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
```

**Good - Option 2 (async pipe - preferred)**:
```typescript
// Component
users$ = this.userService.getUsers();

// Template
<div *ngFor="let user of users$ | async">
  {{ user.name }}
</div>
```

**Detection**: Look for `.subscribe()` calls without corresponding cleanup.

### 2. Event Listener Leaks

**Bad**:
```typescript
ngOnInit() {
  window.addEventListener('resize', this.onResize);
}
// Listener never removed!
```

**Good**:
```typescript
ngOnInit() {
  window.addEventListener('resize', this.onResize);
}

ngOnDestroy() {
  window.removeEventListener('resize', this.onResize);
}
```

### 3. Interval/Timeout Leaks

**Bad**:
```typescript
ngOnInit() {
  setInterval(() => {
    this.updateData();
  }, 5000);
  // Interval continues after component destroyed!
}
```

**Good**:
```typescript
private intervalId: any;

ngOnInit() {
  this.intervalId = setInterval(() => {
    this.updateData();
  }, 5000);
}

ngOnDestroy() {
  if (this.intervalId) {
    clearInterval(this.intervalId);
  }
}
```

---

## Change Detection Errors {#change-detection-errors}

### 1. ExpressionChangedAfterItHasBeenCheckedError

**Problem**: Most confusing Angular error - expression changes during change detection.

**Common Cause - Modifying State in Lifecycle Hooks**:
```typescript
// Bad
ngAfterViewInit() {
  this.isLoading = false; // Changes state after view checked
}
```

**Fix - Use setTimeout or ChangeDetectorRef**:
```typescript
// Option 1: setTimeout (pushes to next event loop)
ngAfterViewInit() {
  setTimeout(() => {
    this.isLoading = false;
  });
}

// Option 2: Manual change detection
constructor(private cdr: ChangeDetectorRef) {}

ngAfterViewInit() {
  this.isLoading = false;
  this.cdr.detectChanges();
}
```

**Common Cause - Child Component Modifying Parent State**:
```typescript
// Bad - Child modifying parent in ngOnInit
@Output() loaded = new EventEmitter();

ngOnInit() {
  this.loaded.emit(true); // Parent state changes during CD
}
```

**Fix - Emit in next cycle**:
```typescript
ngOnInit() {
  setTimeout(() => {
    this.loaded.emit(true);
  });
}
```

### 2. OnPush Not Triggering

**Problem**: OnPush components don't update when expected.

**Cause - Mutating Objects**:
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyComponent {
  @Input() data: any[];

  // Bad - parent does: this.data.push(item)
  // OnPush won't detect because reference didn't change
}
```

**Fix - Immutable Updates**:
```typescript
// Parent should do:
this.data = [...this.data, newItem];
```

---

## Lifecycle Hook Misuse {#lifecycle-hook-misuse}

### 1. Using ngAfterViewInit for Data Loading

**Bad**:
```typescript
ngAfterViewInit() {
  this.loadData(); // Too late - causes flickering
}
```

**Good**:
```typescript
ngOnInit() {
  this.loadData(); // Correct - before view renders
}
```

### 2. Not Implementing ngOnDestroy

**Problem**: Missing cleanup logic.

**Always Implement When**:
- Manual subscriptions exist
- Event listeners registered
- Intervals/timeouts created
- Third-party library instances created

```typescript
ngOnDestroy() {
  // Clean up ALL resources
  this.destroy$.next();
  this.destroy$.complete();
  this.removeEventListeners();
  this.clearIntervals();
}
```

### 3. Using Constructor for Initialization

**Bad**:
```typescript
constructor(private userService: UserService) {
  // Bad - component not fully initialized
  this.loadUsers();
}
```

**Good**:
```typescript
constructor(private userService: UserService) {
  // Constructor only for DI
}

ngOnInit() {
  // Good - component fully initialized
  this.loadUsers();
}
```

---

## Observable Subscription Problems {#observable-subscription-problems}

### 1. Nested Subscriptions (Callback Hell)

**Bad**:
```typescript
this.userService.getUser(id).subscribe(user => {
  this.postService.getPosts(user.id).subscribe(posts => {
    this.commentService.getComments(posts[0].id).subscribe(comments => {
      this.comments = comments; // Callback hell!
    });
  });
});
```

**Good - Use RxJS Operators**:
```typescript
this.userService.getUser(id).pipe(
  switchMap(user => this.postService.getPosts(user.id)),
  switchMap(posts => this.commentService.getComments(posts[0].id))
).subscribe(comments => {
  this.comments = comments;
});
```

### 2. No Error Handling

**Bad**:
```typescript
this.http.get('/api/users').subscribe(users => {
  this.users = users;
  // If API fails, no error handling!
});
```

**Good**:
```typescript
this.http.get('/api/users').pipe(
  catchError(error => {
    console.error('Failed to load users:', error);
    this.errorMessage = 'Failed to load users';
    return of([]); // Return empty array
  })
).subscribe(users => {
  this.users = users;
});
```

### 3. Manual Subscription Instead of Async Pipe

**Bad**:
```typescript
ngOnInit() {
  this.userService.getUsers().subscribe(users => {
    this.users = users;
  });
}
```

**Good**:
```typescript
// Component
users$ = this.userService.getUsers();

// Template
<div *ngFor="let user of users$ | async">{{ user.name }}</div>
```

**Benefits of async pipe**:
- Automatic subscription management
- Automatic change detection
- No memory leaks

---

## Template Syntax Mistakes {#template-syntax-mistakes}

### 1. Missing trackBy in *ngFor

**Bad**:
```html
<div *ngFor="let item of items">
  {{ item.name }}
</div>
```

**Good**:
```html
<div *ngFor="let item of items; trackBy: trackById">
  {{ item.name }}
</div>
```

```typescript
trackById(index: number, item: any): number {
  return item.id;
}
```

### 2. Using Function Calls in Templates

**Bad**:
```html
<!-- Function called on every change detection! -->
<div>{{ getFormattedDate(user.createdAt) }}</div>
```

**Good - Use Pipe**:
```html
<div>{{ user.createdAt | date:'short' }}</div>
```

**Good - Use Property**:
```typescript
get formattedDate(): string {
  return this.formatDate(this.user.createdAt);
}
```

```html
<div>{{ formattedDate }}</div>
```

### 3. Unsafe Property Access

**Bad**:
```html
<!-- Will error if user is null/undefined -->
<div>{{ user.profile.name }}</div>
```

**Good - Use Optional Chaining**:
```html
<div>{{ user?.profile?.name }}</div>
```

**Good - Use *ngIf**:
```html
<div *ngIf="user && user.profile">
  {{ user.profile.name }}
</div>
```

---

## Zone.js Issues {#zonejs-issues}

### 1. Running Outside Angular Zone

**Problem**: Updates don't trigger change detection.

**Symptom**: View doesn't update even though data changes.

**Cause - Third-Party Libraries**:
```typescript
// Third-party library callback runs outside Zone
thirdPartyLib.on('data', (data) => {
  this.data = data; // View won't update!
});
```

**Fix - Run Inside Zone**:
```typescript
constructor(private zone: NgZone) {}

thirdPartyLib.on('data', (data) => {
  this.zone.run(() => {
    this.data = data; // Now triggers change detection
  });
});
```

### 2. Performance Issues from Too Much Change Detection

**Problem**: Running expensive operations inside Zone.

**Fix - Run Outside Zone for Performance**:
```typescript
ngOnInit() {
  this.zone.runOutsideAngular(() => {
    // Expensive operation that doesn't need CD
    setInterval(() => {
      this.updateChartData(); // Doesn't trigger CD
    }, 100);
  });
}
```

---

## Dependency Injection Problems {#dependency-injection-problems}

### 1. Multiple Service Instances

**Problem**: Service not singleton when expected.

**Bad - Service Not Root**:
```typescript
@Injectable() // No providedIn!
export class DataService {}

// Each module creates new instance
```

**Good - Tree-Shakable Provider**:
```typescript
@Injectable({
  providedIn: 'root' // Single instance app-wide
})
export class DataService {}
```

### 2. Circular Dependencies

**Problem**: Services depend on each other.

**Bad**:
```typescript
// user.service.ts
constructor(private authService: AuthService) {}

// auth.service.ts
constructor(private userService: UserService) {}
// Circular dependency!
```

**Fix - Use Forwarder Ref or Restructure**:
```typescript
// Better - create shared service or use events
```

---

## Router Navigation Issues {#router-navigation-issues}

### 1. Programmatic Navigation Without Error Handling

**Bad**:
```typescript
this.router.navigate(['/users', userId]);
// No error handling if navigation fails
```

**Good**:
```typescript
this.router.navigate(['/users', userId]).then(
  success => console.log('Navigation success'),
  error => console.error('Navigation failed:', error)
);
```

### 2. Route Guards Not Handling Errors

**Bad**:
```typescript
canActivate(): Observable<boolean> {
  return this.authService.isAuthenticated$;
  // If auth check fails, no fallback
}
```

**Good**:
```typescript
canActivate(): Observable<boolean> {
  return this.authService.isAuthenticated$.pipe(
    catchError(() => {
      this.router.navigate(['/login']);
      return of(false);
    })
  );
}
```

---

## Quick Checklist

When reviewing Angular code, always check for:

- [ ] All subscriptions cleaned up in ngOnDestroy
- [ ] Event listeners removed in ngOnDestroy
- [ ] Intervals/timeouts cleared in ngOnDestroy
- [ ] trackBy functions used in *ngFor
- [ ] No function calls in templates
- [ ] Error handling in HTTP requests
- [ ] Proper lifecycle hook usage
- [ ] Optional chaining for nullable properties
- [ ] Immutable updates with OnPush
- [ ] Avoid nested subscriptions (use operators)
- [ ] No ExpressionChangedAfterItHasBeenCheckedError
- [ ] Services using providedIn: 'root'

---

## Related Context

- `rxjs_patterns.md` - Detailed RxJS patterns
- `component_patterns.md` - Component best practices
- `service_patterns.md` - Service design patterns
- `performance_patterns.md` - Performance optimization

---

**Version**: 1.0.0
**Last Updated**: 2025-01-14
