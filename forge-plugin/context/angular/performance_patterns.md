# Angular Performance Patterns

Optimization techniques for Angular applications.

---

## Change Detection Optimization {#change-detection}

### OnPush Strategy

```typescript
@Component({
  selector: 'app-user-list',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div *ngFor="let user of users; trackBy: trackById">
      {{ user.name }}
    </div>
  `
})
export class UserListComponent {
  @Input() users: User[] = [];

  trackById(index: number, user: User): number {
    return user.id;
  }
}
```

**Use OnPush When**:
- Component receives data via @Input()
- Component is presentational
- No internal state mutations

### Detach Change Detection

```typescript
constructor(private cdr: ChangeDetectorRef) {
  this.cdr.detach(); // Stop automatic CD
}

updateData() {
  this.data = newData;
  this.cdr.detectChanges(); // Manual CD
}
```

---

## TrackBy Functions {#trackby}

**Always use trackBy in *ngFor**:

```typescript
@Component({
  template: `
    <div *ngFor="let item of items; trackBy: trackById">
      {{ item.name }}
    </div>
  `
})
export class ListComponent {
  trackById(index: number, item: any): number {
    return item.id; // Use unique identifier
  }
}
```

---

## Lazy Loading {#lazy-loading}

### Route-Based Lazy Loading

```typescript
const routes: Routes = [
  {
    path: 'admin',
    loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule)
  }
];
```

### Component Lazy Loading (Angular 17+)

```typescript
import { Component } from '@angular/core';

@Component({
  template: `
    @defer (on viewport) {
      <heavy-component />
    } @placeholder {
      <div>Loading...</div>
    }
  `
})
```

---

## Virtual Scrolling {#virtual-scrolling}

```typescript
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  imports: [ScrollingModule],
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      <div *cdkVirtualFor="let item of items">{{ item }}</div>
    </cdk-virtual-scroll-viewport>
  `
})
```

---

## Bundle Size Optimization {#bundle}

### Tree Shaking

```typescript
// Good - imports only what's needed
import { map } from 'rxjs/operators';

// Bad - imports everything
import * as operators from 'rxjs/operators';
```

### Analyze Bundle

```bash
ng build --stats-json
npx webpack-bundle-analyzer dist/stats.json
```

---

## Memory Leak Prevention {#memory}

### Unsubscribe Patterns

```typescript
private destroy$ = new Subject<void>();

ngOnInit() {
  this.observable$
    .pipe(takeUntil(this.destroy$))
    .subscribe();
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
```

### Remove Event Listeners

```typescript
ngOnDestroy() {
  window.removeEventListener('resize', this.onResize);
  document.removeEventListener('click', this.onClick);
}
```

---

**Version**: 1.0.0
