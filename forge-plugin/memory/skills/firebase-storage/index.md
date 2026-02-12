# Firebase Cloud Storage - Project Memory System

## Purpose

This directory stores project-specific knowledge learned during Firebase Cloud Storage implementation sessions. Each project gets its own subdirectory containing bucket structures, security rules, upload patterns, and configuration discovered during implementation.

## Directory Structure

```
memory/skills/firebase-storage/
├── index.md (this file)
└── {project-name}/
    ├── bucket_structure.md
    ├── security_rules.md
    ├── upload_patterns.md
    ├── cdn_config.md
    └── quota_management.md
```

## Project Memory Contents

### bucket_structure.md
- Storage bucket name and region
- Path hierarchy and naming conventions
- File type to path mappings
- Public vs private path separation
- Multi-bucket strategies (if applicable)
- Lifecycle rules for temporary files

### security_rules.md
- Current storage security rules (storage.rules)
- Authentication requirements per path
- File type and size validation logic
- Role-based access control patterns
- Helper functions used in rules
- Rule testing results and edge cases

### upload_patterns.md
- Upload implementation details (simple, resumable, server-side)
- Client-side validation rules (file type, size, dimensions)
- Progress tracking configuration
- Pause/resume/cancel implementation
- Image processing pipelines (resize, thumbnail, watermark)
- File naming strategies (UUID, content-hash, original)

### cdn_config.md
- CORS configuration (cors.json contents and deployed origins)
- Cache-Control headers per path/file type
- CDN invalidation strategies
- Custom domain configuration
- Content-Disposition settings (inline vs attachment)

### quota_management.md
- Storage quota limits and current usage
- Bandwidth monitoring setup
- Cleanup automation rules and schedules
- Orphaned file detection patterns
- Cost optimization notes and projections
- Alert thresholds configured

## Memory Lifecycle

### Creation
Memory is created the FIRST time a project's Cloud Storage is implemented. The project name is either:
1. Extracted from the Firebase project name
2. Specified by the user
3. Derived from the repository name

### Updates
Memory is UPDATED every time the skill implements Storage changes:
- Bucket structure changes are tracked
- New security rules are recorded
- Upload patterns updated
- CDN configuration refined
- Quota thresholds adjusted

### Usage
Memory is READ at the START of every implementation:
- Provides historical context on bucket organization
- Shows evolution of security rules over time
- Guides upload pattern consistency
- Informs CDN configuration decisions
- Ensures quota management continuity

## Best Practices

### DO:
- ✅ Update memory after every implementation
- ✅ Track security rule evolution over time
- ✅ Document path conventions for team consistency
- ✅ Record CORS and CDN configuration changes
- ✅ Note quota thresholds and cleanup schedules

### DON'T:
- ❌ Store actual file contents or user data
- ❌ Include service account keys or credentials
- ❌ Store signed URLs (they expire)
- ❌ Copy entire storage.rules files (summarize patterns instead)
- ❌ Include environment-specific bucket names in rules

## Memory vs Context

### Context (`../../context/schema/`)
- **Universal knowledge**: Applies to ALL Cloud Storage implementations
- **Platform-specific patterns**: Firebase, GCS, S3 comparisons
- **Best practices**: Industry standards, security guidelines
- **Static**: Updated by Forge maintainers

### Memory (this directory)
- **Project-specific**: Only for ONE project's storage setup
- **Learned patterns**: Discovered during implementation
- **Historical tracking**: Changes over time
- **Dynamic**: Updated by the skill automatically

## Example Memory Structure

```
media-platform/
├── bucket_structure.md
│   - Bucket: media-platform-prod.appspot.com (us-central1)
│   - Paths:
│     users/{uid}/media/photos/ — user photo uploads
│     users/{uid}/media/videos/ — user video uploads
│     users/{uid}/thumbnails/ — auto-generated thumbnails
│     users/{uid}/profile/ — profile avatars
│     processing/{uid}/ — temporary processing area
│     public-feed/{uid}/ — CDN-optimized public content
│   - Naming: UUID-based with original extension
│   - Last updated: 2025-07-14
│
├── security_rules.md
│   - Auth required for all writes
│   - Owner-only write to users/{uid}/ paths
│   - Public read for profile/ and public-feed/
│   - Friends-only read via custom claims
│   - Admin override for moderation (delete any)
│   - Image: max 10 MB, JPEG/PNG/WebP/GIF
│   - Video: max 100 MB, MP4/MOV/WebM
│   - Catch-all deny rule at bottom
│
├── upload_patterns.md
│   - Web: resumable upload with progress tracking
│   - Server: Admin SDK for processing pipeline
│   - Client validation: type + size before upload
│   - Thumbnails: Cloud Function on finalize (64, 200, 600)
│   - Naming: crypto.randomUUID() + original extension
│
├── cdn_config.md
│   - CORS: media-platform.example.com, admin portal
│   - Public content: Cache-Control: public, max-age=86400
│   - Private content: Cache-Control: private, max-age=3600
│   - Avatars: 24-hour cache with versioned filenames
│   - Videos: no-cache (streaming)
│
└── quota_management.md
    - Storage limit alert: 80% of plan quota
    - Processing cleanup: delete after 1 hour
    - Orphan detection: Cloud Function daily scan
    - Monthly bandwidth review scheduled
    - Estimated cost: ~$45/month at current growth
```

## Security Considerations

### DO Store:
- Bucket structure and path patterns
- Security rule patterns (anonymized)
- Upload flow configurations
- CDN and caching strategies
- Quota thresholds and cleanup rules

### DON'T Store:
- Service account keys or credentials
- Actual file contents or URLs
- PII or user-uploaded data
- Signed URLs or download tokens
- Production bucket names in sensitive contexts

## Integration with Tools

Memory can inform:
- **Security audits**: Historical context for rule evolution
- **Cost monitoring**: Expected storage and bandwidth baselines
- **Migration tools**: Bucket structure for data migration planning
- **CI/CD pipelines**: Security rule deployment validation
- **Documentation generators**: Project-specific storage patterns

---

**Memory System Version**: 1.0.0
**Last Updated**: 2025-07-14
**Maintained by**: firebase-storage skill
