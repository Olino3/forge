# RxJS Patterns for Angular

Comprehensive guide to RxJS patterns, operators, and best practices in Angular applications.

---

## Subscription Management {#subscription-management}

### takeUntil Pattern (Recommended)

```typescript
export class MyComponent implements OnDestroy {
  private destroy$ = new Subject<void>();

  ngOnInit() {
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => this.data = data);

    this.userService.getUser()
      .pipe(takeUntil(this.destroy$))
      .subscribe(user => this.user = user);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### Async Pipe (Best for Templates)

```typescript
// Component
users$ = this.userService.getUsers();

// Template
<div *ngFor="let user of users$ | async">{{ user.name }}</div>
```

**Benefits**:
- Automatic subscription/unsubscription
- No manual cleanup needed
- Triggers change detection

---

## Operator Selection {#operators}

### Flattening Operators

**switchMap** - Cancel previous, use latest:
```typescript
// Search: cancel old search when new one starts
this.searchQuery$.pipe(
  switchMap(query => this.searchService.search(query))
).subscribe(results => this.results = results);
```

**mergeMap** - Run concurrently:
```typescript
// Process items in parallel
this.items$.pipe(
  mergeMap(item => this.processItem(item))
).subscribe(result => this.results.push(result));
```

**concatMap** - Sequential, queued:
```typescript
// Process in order
this.requests$.pipe(
  concatMap(req => this.http.post('/api', req))
).subscribe();
```

**exhaustMap** - Ignore new while processing:
```typescript
// Button clicks: ignore clicks while processing
this.saveClick$.pipe(
  exhaustMap(() => this.saveData())
).subscribe();
```

---

## Error Handling {#error-handling}

### catchError

```typescript
this.http.get('/api/data').pipe(
  catchError(error => {
    console.error(error);
    return of([]); // Return default value
  })
).subscribe(data => this.data = data);
```

### retry

```typescript
this.http.get('/api/data').pipe(
  retry(3), // Retry 3 times
  catchError(error => {
    console.error('Failed after 3 retries');
    return of([]);
  })
).subscribe();
```

---

## Subject Types {#subjects}

**Subject** - No initial value, multicast:
```typescript
private clickSubject = new Subject<void>();
click$ = this.clickSubject.asObservable();
```

**BehaviorSubject** - Has initial value, replays latest:
```typescript
private dataSubject = new BehaviorSubject<any[]>([]);
data$ = this.dataSubject.asObservable();
```

**ReplaySubject** - Replays N values:
```typescript
private eventsSubject = new ReplaySubject<Event>(5);
events$ = this.eventsSubject.asObservable();
```

---

## Common Patterns {#patterns}

### Debounce Search

```typescript
this.searchControl.valueChanges.pipe(
  debounceTime(300),
  distinctUntilChanged(),
  switchMap(query => this.search(query))
).subscribe(results => this.results = results);
```

### Combine Multiple Streams

```typescript
combineLatest([
  this.userService.getUser(),
  this.settingsService.getSettings()
]).pipe(
  map(([user, settings]) => ({ user, settings }))
).subscribe(data => this.data = data);
```

---

**Version**: 1.0.0
