---
name: firebase-storage
description: Build with Firebase Cloud Storage — file uploads, downloads, and secure access. Use when uploading images/files, generating download URLs, implementing file pickers, setting up storage security rules. Prevents 9 common Storage errors.
version: "1.0.0"
context:
  primary_domain: "schema"
  always_load_files: []
  detection_required: false
  file_budget: 4
memory:
  scopes:
    - type: "skill-specific"
      files: [bucket_structure.md, security_rules.md, upload_patterns.md, cdn_config.md, quota_management.md]
    - type: "shared-project"
      usage: "reference"
---

# Skill: firebase-storage

**Version**: 1.0.0
**Purpose**: Build with Firebase Cloud Storage — file uploads, downloads, and secure access
**Author**: The Forge
**Last Updated**: 2025-07-14

---

## Title

**Firebase Cloud Storage** - Implement file uploads, downloads, and secure storage with Firebase Cloud Storage including signed URLs, security rules, image processing, and CDN optimization

---

## File Structure

```
forge-plugin/skills/firebase-storage/
├── SKILL.md                  # This file - mandatory workflow
└── examples.md               # Usage scenarios and examples
```

---

## Required Reading

**Before executing this skill**, load context and memory via interfaces:

1. **Context**: Use `contextProvider.getDomainIndex("schema")` for relevant domain context. See [ContextProvider Interface](../../interfaces/context_provider.md).

2. **Skill memory**: Use `memoryStore.getSkillMemory("firebase-storage", "{project-name}")` for previous Storage configurations. See [MemoryStore Interface](../../interfaces/memory_store.md).

## Interface References

- **Context**: Loaded via [ContextProvider Interface](../../interfaces/context_provider.md)
- **Memory**: Accessed via [MemoryStore Interface](../../interfaces/memory_store.md)
- **Shared Patterns**: [Shared Loading Patterns](../../interfaces/shared_loading_patterns.md)
- **Schemas**: Validated against [context_metadata.schema.json](../../interfaces/schemas/context_metadata.schema.json) and [memory_entry.schema.json](../../interfaces/schemas/memory_entry.schema.json)

---

## Design Requirements

### Core Functionality

This skill must:
1. **Implement file uploads** (web, mobile, server — resumable, multipart, and simple)
2. **Generate download URLs** (signed URLs, public URLs, download tokens)
3. **Write storage security rules** (authentication, file type/size validation, path-based access)
4. **Manage file metadata** (content type, custom metadata, cache control headers)
5. **Configure resumable uploads** (progress tracking, pause/resume, retry on failure)
6. **Set up image resizing and thumbnails** (Firebase Extensions, Cloud Functions triggers)
7. **Optimize CDN caching** (cache control headers, CDN invalidation strategies)
8. **Configure CORS** (cross-origin access for browser-based uploads/downloads)
9. **Organize storage buckets** (path conventions, multi-bucket strategies, lifecycle rules)
10. **Monitor and manage quotas** (bandwidth limits, storage limits, rate limiting)

### Output Requirements

Generate **complete, production-ready Cloud Storage implementations** with:
- Upload implementations (Web, Admin, Mobile SDKs)
- Download URL generation with appropriate expiration
- Storage security rules (storage.rules)
- CORS configuration (cors.json)
- File metadata management code
- Image processing pipeline setup (resize, thumbnail, watermark)
- Bucket organization documentation
- Quota monitoring configuration

### Quality Requirements

Generated implementations must:
- **Follow Cloud Storage best practices** (file size limits, naming conventions, folder structure)
- **Include comprehensive security rules** (never deploy with open rules)
- **Handle edge cases** (upload cancellation, network failures, concurrent access, oversized files)
- **Be SDK-appropriate** (Web v9 modular, Admin SDK, Flutter, iOS, Android)
- **Include error handling** (quota exceeded, permission denied, file not found, network timeout)
- **Be well-documented** (bucket structure, upload flows, security rule logic)

---

## 9 Common Storage Errors Prevented

This skill actively prevents these frequently encountered Cloud Storage mistakes:

### 1. Missing CORS Configuration
**Error**: `No 'Access-Control-Allow-Origin' header is present on the requested resource`
**Prevention**: Always generate a `cors.json` configuration and deploy it with `gsutil cors set cors.json gs://bucket-name`. Include allowed origins, methods (GET, POST, PUT, DELETE), and headers (Content-Type, Authorization).

### 2. Oversized File Uploads Without Client Validation
**Error**: Wasted bandwidth and failed uploads from files exceeding limits
**Prevention**: Always validate file size on the client before uploading. Enforce size limits in security rules with `request.resource.size < maxSize`. Implement chunked/resumable uploads for large files (>5 MB).

### 3. Insecure Storage Security Rules
**Error**: Data breach from `allow read, write: if true;`
**Prevention**: Never generate open rules. Always require authentication, validate file types via content type checks, enforce path-based ownership (`request.auth.uid == userId`), and restrict file sizes.

### 4. Expired or Invalid Download URLs
**Error**: `403 Forbidden` or `401 Unauthorized` when accessing signed URLs after expiration
**Prevention**: Set appropriate expiration times for signed URLs (default 1 hour, max 7 days). Implement URL refresh logic before expiration. Use long-lived download tokens for persistent public access instead of signed URLs.

### 5. Missing Content-Type Metadata
**Error**: Files served with `application/octet-stream` instead of correct MIME type, breaking browser rendering
**Prevention**: Always set `contentType` metadata during upload. Detect MIME type from file extension or file header. Validate content type in security rules with `request.resource.contentType.matches('image/.*')`.

### 6. No Upload Progress or Resumable Handling
**Error**: Users see no feedback during uploads; large uploads fail without recovery
**Prevention**: Always implement upload progress callbacks with `uploadTask.on('state_changed')`. Use resumable uploads for files over 5 MB. Implement pause/resume/cancel controls. Handle `storage/retry-limit-exceeded` with user feedback.

### 7. Unorganized Bucket Structure
**Error**: Flat file dumping making files impossible to query, manage, or secure
**Prevention**: Design a hierarchical path structure (e.g., `users/{uid}/profile/avatar.jpg`). Use consistent naming conventions. Separate public and private content into distinct paths. Document the bucket organization.

### 8. Missing Cleanup for Deleted Resources
**Error**: Orphaned files consuming storage quota after parent resources are deleted
**Prevention**: Implement Cloud Functions triggers to delete associated files when parent documents are removed. Use lifecycle rules for temporary files. Track file references in Firestore for cleanup verification.

### 9. CDN Cache Serving Stale Content
**Error**: Updated files not visible to users due to aggressive cache headers
**Prevention**: Use versioned file paths or unique filenames (e.g., `avatar_v2.jpg` or content-hash naming). Set appropriate `Cache-Control` headers. Use `cacheControl: 'public, max-age=3600'` for static assets and `no-cache` for frequently updated files.

---

## Instructions

### MANDATORY STEPS (Must Execute in Order)

---

#### **Step 1: Initial Analysis**

**Purpose**: Understand the Cloud Storage implementation requirements

**Actions**:
1. Identify the application type (web, mobile, server-side)
2. Determine the SDK environment (Web v9 modular, Admin SDK, Flutter, iOS, Android)
3. Review existing Storage configuration if present (firebase.json, storage.rules, cors.json)
4. Understand the file types and sizes to be stored (images, documents, videos, user-generated content)
5. Identify access patterns (public vs private, shared access, temporary URLs)
6. Note any existing bucket structure or migration needs
7. Determine image processing requirements (thumbnails, resizing, format conversion)

**Output**: Clear understanding of Storage requirements and constraints

---

#### **Step 2: Load Memory**

**Purpose**: Retrieve previous Cloud Storage configurations for this project

> Follow [Standard Memory Loading](../../interfaces/shared_loading_patterns.md#pattern-1-standard-memory-loading) with `skill="firebase-storage"` and `domain="schema"`.

**Actions**:
1. Use `memoryStore.getSkillMemory("firebase-storage", "{project-name}")` to load project memory. See [MemoryStore Interface](../../interfaces/memory_store.md).
2. If memory exists, review:
   - `bucket_structure.md` - Existing bucket organization and path conventions
   - `security_rules.md` - Current security rules and access patterns
   - `upload_patterns.md` - Established upload flows and file handling
   - `cdn_config.md` - CDN caching and CORS configuration
   - `quota_management.md` - Storage limits and monitoring setup
3. If not exists, note this is first-time Storage setup

**Output**: Understanding of project Storage history or recognition of new project

---

#### **Step 3: Load Context**

**Purpose**: Load relevant storage and file management knowledge

> Follow [Standard Context Loading](../../interfaces/shared_loading_patterns.md#pattern-2-standard-context-loading) for the `schema` domain. Stay within the file budget declared in frontmatter.

**Actions**:
1. Use `contextProvider.getDomainIndex("schema")` for data storage context
2. Load relevant context files based on requirements:
   - File storage patterns and best practices
   - Security best practices
   - CDN and caching optimization guidelines
3. Note any best practices for Cloud Storage implementation

**Output**: Comprehensive understanding of Cloud Storage patterns and best practices

---

#### **Step 4: Storage Implementation**

**Purpose**: Design and implement the Cloud Storage solution

**Actions**:

**A. Bucket Organization and Path Design:**

1. **Design path hierarchy**:
   - Map file types to path segments (e.g., `users/{uid}/avatars/`, `posts/{postId}/media/`)
   - Separate public and private content paths
   - Define naming conventions (original filenames, UUIDs, content-hash)
   - Plan for multi-bucket strategies if needed (hot/cold storage)
   - Document path structure for team reference

2. **File metadata strategy**:
   - Define custom metadata fields per file type
   - Set content type detection and validation
   - Configure cache control headers per path
   - Plan content disposition for downloads vs inline viewing

**B. Security Rules:**

1. **Design storage security rules** (storage.rules):
   - Authentication requirements per path
   - File type validation (`request.resource.contentType`)
   - File size limits (`request.resource.size`)
   - Path-based ownership (`request.auth.uid == userId`)
   - Role-based access using custom claims
   - Rate limiting patterns

2. **Security rules testing**:
   - Provide test scenarios for rules
   - Cover allow and deny cases
   - Test edge cases (wrong file type, oversized files, unauthenticated access)

**C. Upload Implementation:**

1. **Simple uploads**: Small files (<5 MB) with `uploadBytes()`
2. **Resumable uploads**: Large files with `uploadBytesResumable()` and progress tracking
3. **Server-side uploads**: Admin SDK uploads with `bucket.upload()`
4. **Upload controls**: Pause, resume, cancel functionality
5. **Progress tracking**: Real-time upload percentage with `state_changed` observer
6. **Client validation**: File type, size, and dimension checks before upload

**D. Download URL Generation:**

1. **Signed URLs**: Time-limited access with configurable expiration
2. **Download tokens**: Long-lived public URLs via `getDownloadURL()`
3. **Public URLs**: CDN-served public content
4. **URL refresh**: Automatic re-generation before expiration
5. **Streaming downloads**: Large file downloads with progress

**E. Image Processing and Thumbnails:**

1. **Resize on upload**: Cloud Functions triggered by storage events
2. **Thumbnail generation**: Multiple sizes (small, medium, large)
3. **Format conversion**: WebP optimization for web delivery
4. **Watermarking**: Overlay watermarks on uploaded images
5. **Firebase Extensions**: Configure "Resize Images" extension

**F. CORS and CDN Configuration:**

1. **CORS configuration**: Generate and deploy `cors.json`
2. **Cache headers**: Set `Cache-Control` per file type
3. **CDN invalidation**: Strategies for updated content
4. **Custom domains**: Configure custom CDN domains if needed

**Output**: Complete Cloud Storage implementation

---

#### **Step 5: Generate Output**

**Purpose**: Produce deliverable artifacts

**Actions**:
1. Save output to `/claudedocs/firebase-storage_{project}_{YYYY-MM-DD}.md`
2. Follow naming conventions in `../OUTPUT_CONVENTIONS.md`
3. Generate deliverable files:
   - `storage.rules` - Security rules
   - `cors.json` - CORS configuration
   - Bucket organization documentation
   - Upload implementation code (appropriate SDK)
   - Download URL generation code
   - Image processing Cloud Functions (if applicable)
   - Quota monitoring setup
4. Include the 9-error prevention checklist in output

**Output**: Complete, production-ready Cloud Storage implementation artifacts

---

#### **Step 6: Update Memory**

**Purpose**: Store configuration for future reference

> Follow [Standard Memory Update](../../interfaces/shared_loading_patterns.md#pattern-3-standard-memory-update) for `skill="firebase-storage"`. Store any newly learned patterns, conventions, or project insights.

**Actions**:
1. Use `memoryStore.update(layer="skill-specific", skill="firebase-storage", project="{project-name}", ...)` to store:
2. **bucket_structure.md**:
   - Path hierarchy and naming conventions
   - File type to path mappings
   - Multi-bucket strategies
   - Public vs private path separation
3. **security_rules.md**:
   - Current storage security rules
   - File type and size validation logic
   - Access control patterns
   - Rule testing results
4. **upload_patterns.md**:
   - Upload implementation details (simple, resumable, server-side)
   - Client-side validation rules
   - Progress tracking configuration
   - File processing pipelines
5. **cdn_config.md**:
   - CORS configuration
   - Cache control headers per path
   - CDN invalidation strategies
   - Custom domain setup
6. **quota_management.md**:
   - Storage quota limits
   - Bandwidth monitoring
   - Cleanup automation rules
   - Cost optimization notes

**Output**: Memory stored for future skill invocations

---

## Best Practices

### Bucket Organization

1. **Use structured paths**: Design paths around ownership and access patterns (e.g., `users/{uid}/`)
2. **Separate public and private**: Keep publicly accessible files in a distinct path
3. **Avoid deep nesting**: Limit path depth to 3-4 levels for manageability
4. **Use consistent naming**: Choose UUID or content-hash naming to avoid collisions
5. **Document your structure**: Maintain a bucket map for the team

### Security Rules

1. **Never deploy open rules**: Always require authentication for writes
2. **Validate file types**: Check `request.resource.contentType` against allowed MIME types
3. **Enforce size limits**: Use `request.resource.size` to prevent oversized uploads
4. **Path-based ownership**: Ensure users can only write to their own paths
5. **Keep rules simple**: Complex rules are harder to audit and more error-prone

### Upload Optimization

1. **Validate before upload**: Check file type, size, and dimensions on the client
2. **Use resumable uploads**: For any file over 5 MB
3. **Show progress**: Always provide upload progress feedback to users
4. **Handle failures gracefully**: Implement retry logic with exponential backoff
5. **Compress before upload**: Resize images and compress files client-side when possible

### CDN and Caching

1. **Set cache headers**: Configure `Cache-Control` based on content update frequency
2. **Use versioned paths**: Append version or hash to filenames for cache busting
3. **Configure CORS early**: Set up CORS before any browser-based access
4. **Monitor bandwidth**: Track CDN usage to avoid unexpected costs
5. **Use appropriate formats**: Serve WebP for web, optimize image quality settings

---

## Error Handling

### Common Issues

1. **Permission denied**: Check security rules and user authentication state
2. **CORS errors**: Verify `cors.json` is deployed and includes the requesting origin
3. **File not found**: Handle gracefully with fallback UI or placeholder images
4. **Quota exceeded**: Implement storage monitoring and alert on thresholds
5. **Network errors**: Use resumable uploads, implement retry logic

### Debugging

1. **Use Firebase Emulator**: Test uploads and rules locally without affecting production
2. **Check rules in console**: Use the Storage Rules simulator for testing
3. **Monitor in Firebase Console**: Track storage usage, bandwidth, and operations
4. **Enable debug logging**: Check browser network tab for detailed error responses
5. **Review CORS config**: Use `gsutil cors get gs://bucket-name` to verify deployed configuration

---

## Compliance Checklist

Before completing, verify:

- [ ] All mandatory workflow steps executed in order
- [ ] Standard Memory Loading pattern followed (Step 2)
- [ ] Standard Context Loading pattern followed (Step 3)
- [ ] Output saved with standard naming convention
- [ ] Standard Memory Update pattern followed (Step 6)
- [ ] Security rules require authentication (no open rules)
- [ ] CORS configuration generated and documented
- [ ] File type and size validation implemented (client and rules)
- [ ] Upload progress tracking implemented for large files
- [ ] 9-error prevention checklist verified

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-07-14 | Initial release with interface-based patterns, 9-error prevention, comprehensive Cloud Storage workflow |

---

## Related Skills

- **firebase-firestore**: For managing Firestore documents that reference stored files
- **database-schema-analysis**: For analyzing data structures that include file references
- **generate-azure-functions**: For server-side file processing patterns

---

## References

- [Cloud Storage for Firebase](https://firebase.google.com/docs/storage)
- [Storage Security Rules](https://firebase.google.com/docs/storage/security)
- [Upload Files](https://firebase.google.com/docs/storage/web/upload-files)
- [Download Files](https://firebase.google.com/docs/storage/web/download-files)
- [Firebase Extensions - Resize Images](https://firebase.google.com/products/extensions/firebase-storage-resize-images)
- [Cloud Storage Pricing](https://firebase.google.com/pricing)
- [Firebase Emulator Suite](https://firebase.google.com/docs/emulator-suite)
