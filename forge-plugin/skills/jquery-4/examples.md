# jQuery 4.0 Migration Examples

This file contains example migration scenarios demonstrating how the `skill:jquery-4` handles real-world jQuery 3.x → 4.0 upgrades.

---

## Example 1: Migrating a WordPress Theme from jQuery 3.6 to 4.0

### Scenario

A WordPress theme uses `$.trim`, `$.isFunction`, and relies on focus event ordering for a custom form validation system. The theme wraps all jQuery code in `jQuery(document).ready(function($) { ... })` per WordPress convention.

### User Prompt

> "Migrate my WordPress theme's JavaScript from jQuery 3.6 to jQuery 4.0. The theme has custom form validation that uses $.trim and $.isFunction, and the focus/blur behavior seems important for the validation UX."

### Skill Execution

**Step 1 — Initial Analysis**

Scan `wp-content/themes/my-theme/js/`:
- `theme.js` — main theme script (jQuery 3.6 via `wp_enqueue_script`)
- `form-validation.js` — custom validation using `$.trim`, `$.isFunction`
- `navigation.js` — mobile menu with focus/blur handlers

**Step 4 — Audit Breaking Changes**

```
AUDIT RESULTS
─────────────
File: js/form-validation.js

  Line 12:  $.trim(input.val())
            ⚠️ CRITICAL — $.trim removed in jQuery 4.0
            Replace with: input.val().trim()

  Line 28:  if ($.isFunction(callback)) {
            ⚠️ CRITICAL — $.isFunction removed in jQuery 4.0
            Replace with: if (typeof callback === "function") {

  Line 45:  $.isNumeric(ageField.val())
            ⚠️ CRITICAL — $.isNumeric removed in jQuery 4.0
            Replace with: !isNaN(parseFloat(ageField.val())) && isFinite(ageField.val())

File: js/navigation.js

  Line 8:   $menuItem.on('focus', function() { ... })
  Line 14:  $menuItem.on('focusin', function() { ... })
            ⚠️ HIGH — Focus event order changed in jQuery 4.0
            focus now fires BEFORE focusin (was after in 3.x)
            Review: Verify that handler at line 14 does not depend
            on state set by handler at line 8
```

**Step 5 — Generate Migration Plan**

```diff
--- a/js/form-validation.js
+++ b/js/form-validation.js
@@ -10,7 +10,7 @@
 jQuery(document).ready(function($) {
     function validateField(input, callback) {
-        var value = $.trim(input.val());
+        var value = input.val().trim();
         if (value.length === 0) {
             showError(input, 'This field is required');
             return false;
@@ -26,7 +26,7 @@
-        if ($.isFunction(callback)) {
+        if (typeof callback === "function") {
             callback(input, value);
         }

@@ -43,7 +43,7 @@
     function validateAge(ageField) {
-        if (!$.isNumeric(ageField.val())) {
+        if (isNaN(parseFloat(ageField.val())) || !isFinite(ageField.val())) {
             showError(ageField, 'Please enter a valid number');
         }
     }
```

**Step 7 — Validation Checklist**

- [ ] Form submission works with trimmed whitespace-only inputs
- [ ] Callback-based validators still fire correctly
- [ ] Age field rejects non-numeric input and accepts valid numbers
- [ ] Mobile menu keyboard navigation (Tab/Shift+Tab) works correctly with new focus order
- [ ] No JS console errors on any admin or front-end page

---

## Example 2: Upgrading a Legacy Admin Dashboard with Heavy Deferred/Promise Usage

### Scenario

A legacy admin dashboard built with jQuery 3.4 uses `$.Deferred()` extensively for chaining AJAX calls. The code relies on synchronous `.then()` resolution and uses `$.proxy` for context binding in callbacks.

### User Prompt

> "Our admin dashboard has dozens of Deferred chains for API calls. We need to upgrade to jQuery 4.0 but I'm worried about the Promise behavior changes breaking our data loading sequence."

### Skill Execution

**Step 1 — Initial Analysis**

Scan `src/js/admin/`:
- `api-client.js` — central AJAX wrapper using `$.Deferred()`
- `dashboard.js` — dashboard init with chained Deferreds
- `data-loader.js` — sequential data loading with `.then()` chains
- `utils.js` — utility functions using `$.proxy`, `$.type`, `$.parseJSON`

**Step 4 — Audit Breaking Changes**

```
AUDIT RESULTS
─────────────
File: src/js/admin/api-client.js

  Line 22:  var deferred = $.Deferred();
  Line 35:  deferred.then(function(data) {
            ⚠️ HIGH — Deferred.then() now follows native Promise semantics
            .then() callbacks are now asynchronous (microtask-scheduled)
            Code that depends on synchronous resolution WILL BREAK

  Line 48:  $.proxy(this.handleResponse, this)
            ⚠️ CRITICAL — $.proxy removed in jQuery 4.0
            Replace with: this.handleResponse.bind(this)

File: src/js/admin/data-loader.js

  Line 15:  loadUsers().then(loadPermissions).then(renderDashboard);
            ⚠️ HIGH — .then() chain may behave differently
            In jQuery 3.x, if loadPermissions threw, renderDashboard
            could still run. In 4.0, errors propagate like native Promises.

  Line 30:  $.type(response) === "array"
            ⚠️ CRITICAL — $.type removed in jQuery 4.0
            Replace with: Array.isArray(response)

File: src/js/admin/utils.js

  Line 5:   $.parseJSON(rawData)
            ⚠️ CRITICAL — $.parseJSON removed in jQuery 4.0
            Replace with: JSON.parse(rawData)

  Line 18:  $.proxy(handler, context)
            ⚠️ CRITICAL — $.proxy removed in jQuery 4.0
            Replace with: handler.bind(context)
```

**Step 5 — Generate Migration Plan**

Priority 1 — Deferred/Promise behavioral changes (highest risk):

```diff
--- a/src/js/admin/data-loader.js
+++ b/src/js/admin/data-loader.js
@@ -13,7 +13,11 @@
-    loadUsers().then(loadPermissions).then(renderDashboard);
+    loadUsers()
+        .then(loadPermissions)
+        .then(renderDashboard)
+        .catch(function(err) {
+            console.error('Dashboard load failed:', err);
+            showErrorState();
+        });
```

Priority 2 — Removed static methods:

```diff
--- a/src/js/admin/utils.js
+++ b/src/js/admin/utils.js
@@ -3,7 +3,7 @@
-    var data = $.parseJSON(rawData);
+    var data = JSON.parse(rawData);

@@ -16,7 +16,7 @@
-    return $.proxy(handler, context);
+    return handler.bind(context);
```

```diff
--- a/src/js/admin/api-client.js
+++ b/src/js/admin/api-client.js
@@ -46,7 +46,7 @@
-        success: $.proxy(this.handleResponse, this),
+        success: this.handleResponse.bind(this),
```

**Step 7 — Validation Checklist**

- [ ] Dashboard loads all data panels in correct order
- [ ] API errors display user-friendly error state (not silent failures)
- [ ] Network failure during chained loads does not leave dashboard in partial state
- [ ] All `$.proxy` replacements preserve correct `this` context
- [ ] JSON parsing still handles malformed input gracefully

---

## Example 3: Migrating a jQuery Plugin Using Removed Static Methods and Slim Build

### Scenario

A custom jQuery plugin (`jquery.datatable-enhanced.js`) uses multiple removed static methods and is loaded via the slim build (`jquery.slim.min.js`). The plugin also uses `:even`/`:odd` selectors for row striping and `jQuery.unique()` for deduplication.

### User Prompt

> "We have a custom datatable plugin that depends on jquery.slim.min.js. It uses $.isArray, $.isFunction, $.type, :even/:odd selectors, and jQuery.unique(). Migrate it to jQuery 4.0."

### Skill Execution

**Step 1 — Initial Analysis**

Scan plugin files:
- `jquery.datatable-enhanced.js` — main plugin (1,200 lines)
- `index.html` — demo page loading `jquery.slim.min.js` via CDN
- `package.json` — lists `jquery` as `^3.5.0`

Key findings:
- Plugin loaded via slim build — slim build no longer exists in jQuery 4.0
- Plugin uses AJAX internally — slim build excluded AJAX, but jQuery 4.0 full build includes it
- 14 occurrences of removed static methods across the plugin

**Step 4 — Audit Breaking Changes**

```
AUDIT RESULTS
─────────────
File: jquery.datatable-enhanced.js

  Line 45:   if ($.isArray(columns)) {
             ⚠️ CRITICAL — Replace with: if (Array.isArray(columns)) {

  Line 67:   if ($.isFunction(options.onSort)) {
             ⚠️ CRITICAL — Replace with: if (typeof options.onSort === "function") {

  Line 102:  var colType = $.type(value);
             ⚠️ CRITICAL — $.type removed; no single native equivalent
             Replace with custom helper or inline typeof checks

  Line 189:  $rows.filter(':even').addClass('row-even');
  Line 190:  $rows.filter(':odd').addClass('row-odd');
             ⚠️ MEDIUM — :even/:odd are now 0-based in jQuery 4.0
             :even now selects index 0, 2, 4 (1st, 3rd, 5th rows)
             This is actually the CORRECT visual behavior for row striping
             Verify: previous behavior may have been off-by-one

  Line 245:  var unique = jQuery.unique(nodeList);
             ⚠️ CRITICAL — jQuery.unique removed
             Replace with: var unique = jQuery.uniqueSort(nodeList);

File: index.html

  Line 8:    <script src="https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.slim.min.js">
             ⚠️ MEDIUM — Slim build removed in jQuery 4.0
             Replace with: https://cdn.jsdelivr.net/npm/jquery@4/dist/jquery.min.js
```

**Step 5 — Generate Migration Plan**

Priority 1 — Build change and removed APIs:

```diff
--- a/index.html
+++ b/index.html
@@ -6,7 +6,7 @@
-<script src="https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.slim.min.js"></script>
+<script src="https://cdn.jsdelivr.net/npm/jquery@4/dist/jquery.min.js"></script>
```

```diff
--- a/jquery.datatable-enhanced.js
+++ b/jquery.datatable-enhanced.js
@@ -43,7 +43,7 @@
-        if ($.isArray(columns)) {
+        if (Array.isArray(columns)) {

@@ -65,7 +65,7 @@
-        if ($.isFunction(options.onSort)) {
+        if (typeof options.onSort === "function") {

@@ -100,7 +100,12 @@
-        var colType = $.type(value);
+        // jQuery 4.0: $.type removed — use native type checking
+        var colType;
+        if (Array.isArray(value)) colType = "array";
+        else if (value === null) colType = "null";
+        else if (value instanceof Date) colType = "date";
+        else if (value instanceof RegExp) colType = "regexp";
+        else colType = typeof value;

@@ -243,7 +248,7 @@
-        var unique = jQuery.unique(nodeList);
+        var unique = jQuery.uniqueSort(nodeList);
```

Priority 2 — Selector behavior change (verify only):

```javascript
// :even/:odd are now 0-based — verify row striping still looks correct
// In jQuery 4.0: :even → index 0, 2, 4 (visually: rows 1, 3, 5)
// This matches the expected visual striping pattern
// If the old code relied on 1-based behavior, swap :even and :odd
```

Priority 3 — Update package.json:

```diff
--- a/package.json
+++ b/package.json
@@ -5,7 +5,7 @@
-    "jquery": "^3.5.0"
+    "jquery": "^4.0.0"
```

**Step 7 — Validation Checklist**

- [ ] Plugin initializes without errors on jQuery 4.0
- [ ] Column type detection works for strings, numbers, arrays, dates, null
- [ ] Sort callbacks fire correctly for all column types
- [ ] Row striping visually alternates correctly (1st row light, 2nd dark, etc.)
- [ ] `jQuery.uniqueSort` deduplicates DOM nodes identically to old `jQuery.unique`
- [ ] No slim build references remain in HTML, CDN links, or build configs
- [ ] Plugin works when AJAX features are present (no conflicts from full build)
