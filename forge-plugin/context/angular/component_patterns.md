# Angular Component Patterns

Best practices for Angular component design, architecture, and implementation.

---

## Smart vs Presentational Components {#smart-vs-presentational}

### Presentational (Dumb) Components

**Purpose**: Display data, emit events, no business logic.

**Characteristics**:
- Receive data via `@Input()`
- Emit events via `@Output()`
- No service injection (except utility services)
- Stateless or minimal internal state
- Highly reusable
- OnPush change detection

**Example**:
```typescript
@Component({
  selector: 'app-user-card',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="user-card">
      <h3>{{ user.name }}</h3>
      <p>{{ user.email }}</p>
      <button (click)="onEdit()">Edit</button>
    </div>
  `
})
export class UserCardComponent {
  @Input() user!: User;
  @Output() edit = new EventEmitter<User>();

  onEdit() {
    this.edit.emit(this.user);
  }
}
```

### Smart (Container) Components

**Purpose**: Manage state, orchestrate data flow, contain business logic.

**Characteristics**:
- Inject services
- Manage component state
- Coordinate child components
- Handle routing
- API calls
- Default change detection (or OnPush with manual triggers)

**Example**:
```typescript
@Component({
  selector: 'app-user-list',
  template: `
    <app-user-card
      *ngFor="let user of users$ | async"
      [user]="user"
      (edit)="editUser($event)"
    ></app-user-card>
  `
})
export class UserListComponent {
  users$ = this.userService.getUsers();

  constructor(
    private userService: UserService,
    private router: Router
  ) {}

  editUser(user: User) {
    this.router.navigate(['/users', user.id, 'edit']);
  }
}
```

---

## Input/Output Best Practices {#input-output}

### @Input() Patterns

**Required Inputs**:
```typescript
@Input() user!: User; // ! = required (TypeScript strict mode)

// Or with validation
@Input() set user(value: User) {
  if (!value) {
    throw new Error('User is required');
  }
  this._user = value;
}
private _user!: User;
get user(): User {
  return this._user;
}
```

**Default Values**:
```typescript
@Input() maxItems = 10; // Default value
```

**Input Transformation**:
```typescript
@Input()
set items(value: any[]) {
  this._items = value || [];
}
get items(): any[] {
  return this._items;
}
private _items: any[] = [];
```

### @Output() Patterns

**Event Naming**:
```typescript
// Use present tense for actions
@Output() edit = new EventEmitter<User>();
@Output() delete = new EventEmitter<number>();
@Output() save = new EventEmitter<User>();

// Not past tense: edited, deleted, saved
```

**Type-Safe Events**:
```typescript
@Output() userSelected = new EventEmitter<User>();
// Not: @Output() userSelected = new EventEmitter<any>();
```

---

## Lifecycle Hooks {#lifecycle-hooks}

### Hook Usage Guide

| Hook | Use For | Don't Use For |
|------|---------|---------------|
| `ngOnChanges` | React to input changes | Initial data load |
| `ngOnInit` | Initialize component, load data | DOM manipulation |
| `ngDoCheck` | Custom change detection | Regular logic (performance issue) |
| `ngAfterContentInit` | Access content children | Modify state (CD error) |
| `ngAfterContentChecked` | After content CD | Modify state (CD error) |
| `ngAfterViewInit` | Access view children, DOM | Modify state (CD error) |
| `ngAfterViewChecked` | After view CD | Modify state (CD error) |
| `ngOnDestroy` | Cleanup (CRITICAL) | Skip this hook |

**ngOnDestroy Example**:
```typescript
private destroy$ = new Subject<void>();

ngOnInit() {
  this.dataService.getData()
    .pipe(takeUntil(this.destroy$))
    .subscribe(data => this.data = data);
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
```

---

## ViewChild & ContentChild {#viewchild}

**ViewChild** - Access child components/elements in template:
```typescript
@ViewChild('fileInput') fileInput!: ElementRef;
@ViewChild(ChildComponent) child!: ChildComponent;

ngAfterViewInit() {
  // Safe to access ViewChild here
  this.fileInput.nativeElement.focus();
}
```

**ContentChild** - Access projected content:
```typescript
@ContentChild(CardHeader) header!: CardHeader;

ngAfterContentInit() {
  // Safe to access ContentChild here
  if (this.header) {
    this.header.highlight();
  }
}
```

---

## Change Detection Strategies {#change-detection}

### Default Strategy

**When to Use**: Components with complex state mutations.

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.Default
})
```

### OnPush Strategy (Recommended)

**When to Use**: Performance-critical components, presentational components.

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  @Input() user!: User;
}
```

**Triggers OnPush CD**:
1. Input reference changes
2. Event in component or children
3. Async pipe emits
4. Manual: `cdr.markForCheck()` or `cdr.detectChanges()`

**Important**: With OnPush, use immutable updates:
```typescript
// Bad
this.users.push(newUser);

// Good
this.users = [...this.users, newUser];
```

---

## Component Communication {#communication}

### Parent → Child: @Input()
```typescript
// Parent
<app-child [data]="parentData"></app-child>

// Child
@Input() data!: any;
```

### Child → Parent: @Output()
```typescript
// Child
@Output() dataChange = new EventEmitter<any>();
this.dataChange.emit(newData);

// Parent
<app-child (dataChange)="handleDataChange($event)"></app-child>
```

### Sibling Communication: Service
```typescript
@Injectable({ providedIn: 'root' })
export class DataService {
  private dataSubject = new BehaviorSubject<any>(null);
  data$ = this.dataSubject.asObservable();

  updateData(data: any) {
    this.dataSubject.next(data);
  }
}

// Component A
this.dataService.updateData(newData);

// Component B
this.dataService.data$.subscribe(data => this.data = data);
```

---

## Template Best Practices {#templates}

### Avoid Function Calls
**Bad**:
```html
<div>{{ formatDate(user.createdAt) }}</div>
```

**Good**:
```html
<div>{{ user.createdAt | date }}</div>
```

### Use TrackBy
**Bad**:
```html
<div *ngFor="let item of items">{{ item.name }}</div>
```

**Good**:
```html
<div *ngFor="let item of items; trackBy: trackById">{{ item.name }}</div>
```

```typescript
trackById(index: number, item: any): number {
  return item.id;
}
```

### Safe Navigation
```html
<div>{{ user?.profile?.address?.city }}</div>
```

### Structural Directive Syntax (Angular 17+)
```html
@if (condition) {
  <div>Content</div>
} @else {
  <div>Alternative</div>
}

@for (item of items; track item.id) {
  <div>{{ item.name }}</div>
}
```

---

## Standalone Components (Angular 14+) {#standalone}

```typescript
@Component({
  standalone: true,
  imports: [CommonModule, FormsModule, UserCardComponent],
  selector: 'app-user-list',
  templateUrl: './user-list.component.html'
})
export class UserListComponent {}
```

**Benefits**:
- No NgModule needed
- Simpler dependency management
- Better tree shaking
- Easier testing

---

**Version**: 1.0.0
