# Firebase Cloud Storage Skill Examples

This file demonstrates typical usage scenarios for the `firebase-storage` skill.

---

## Example 1: User Profile Image Upload with Automatic Thumbnail Generation

### Scenario

A social media application needs to let users upload profile avatars. Uploaded images must be automatically resized into three thumbnail sizes (64x64, 200x200, 600x600) for use across the app. Only authenticated users can upload to their own profile path, and images must be under 5 MB.

### User Request

"I need to implement profile image uploads for our social app. Users should be able to crop and upload an avatar, and we need automatic thumbnail generation in three sizes. We're using the Web v9 modular SDK with React."

### Skill Workflow

**Step 1: Initial Analysis**
- Application type: Web (React)
- SDK: Firebase Web v9 (modular)
- File types: Images only (JPEG, PNG, WebP)
- Max file size: 5 MB
- Processing needs: Resize to 64x64, 200x200, 600x600
- Access pattern: Public read for avatars, authenticated write to own path only

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("firebase-storage", "social-app")` → No existing memory (first-time setup)

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load file storage patterns
- Review image processing best practices

**Step 4: Storage Implementation**

**Bucket Structure:**
```
users/
└── {uid}/
    └── profile/
        ├── avatar.jpg              # Original upload
        └── thumbnails/
            ├── avatar_64x64.jpg    # Small (list views, comments)
            ├── avatar_200x200.jpg  # Medium (profile cards)
            └── avatar_600x600.jpg  # Large (profile page)
```

**Security Rules (storage.rules):**
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // User profile images
    match /users/{userId}/profile/{allPaths=**} {
      // Anyone can view profile images
      allow read: if true;

      // Only the authenticated owner can upload
      allow write: if request.auth != null
                   && request.auth.uid == userId
                   && request.resource.size < 5 * 1024 * 1024
                   && request.resource.contentType.matches('image/(jpeg|png|webp)');
    }
  }
}
```

**CORS Configuration (cors.json):**
```json
[
  {
    "origin": ["https://social-app.example.com"],
    "method": ["GET", "POST", "PUT", "DELETE"],
    "maxAgeSeconds": 3600,
    "responseHeader": ["Content-Type", "Authorization"]
  }
]
```

**Upload Implementation (React component):**
```typescript
import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';
import { storage } from '../firebase-config';

async function uploadAvatar(
  userId: string,
  file: File,
  onProgress: (percent: number) => void
): Promise<string> {
  // Client-side validation
  const MAX_SIZE = 5 * 1024 * 1024; // 5 MB
  const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

  if (!ALLOWED_TYPES.includes(file.type)) {
    throw new Error('Only JPEG, PNG, and WebP images are allowed');
  }
  if (file.size > MAX_SIZE) {
    throw new Error('Image must be under 5 MB');
  }

  const storageRef = ref(storage, `users/${userId}/profile/avatar.jpg`);
  const metadata = {
    contentType: file.type,
    cacheControl: 'public, max-age=86400', // 24-hour cache
    customMetadata: {
      uploadedBy: userId,
      originalName: file.name,
    },
  };

  const uploadTask = uploadBytesResumable(storageRef, file, metadata);

  return new Promise((resolve, reject) => {
    uploadTask.on(
      'state_changed',
      (snapshot) => {
        const percent = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        onProgress(percent);
      },
      (error) => {
        switch (error.code) {
          case 'storage/unauthorized':
            reject(new Error('You do not have permission to upload'));
            break;
          case 'storage/canceled':
            reject(new Error('Upload was cancelled'));
            break;
          case 'storage/retry-limit-exceeded':
            reject(new Error('Upload failed after retries. Check your connection.'));
            break;
          default:
            reject(error);
        }
      },
      async () => {
        const downloadURL = await getDownloadURL(uploadTask.snapshot.ref);
        resolve(downloadURL);
      }
    );
  });
}
```

**Thumbnail Cloud Function:**
```typescript
import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';
import * as sharp from 'sharp';
import * as path from 'path';

admin.initializeApp();

const THUMBNAIL_SIZES = [
  { width: 64, height: 64, suffix: '64x64' },
  { width: 200, height: 200, suffix: '200x200' },
  { width: 600, height: 600, suffix: '600x600' },
];

export const generateThumbnails = functions.storage
  .object()
  .onFinalize(async (object) => {
    const filePath = object.name;
    if (!filePath) return;

    // Only process avatar uploads, skip thumbnails
    if (!filePath.match(/^users\/[^/]+\/profile\/avatar\./)) return;
    if (filePath.includes('/thumbnails/')) return;

    const bucket = admin.storage().bucket(object.bucket);
    const file = bucket.file(filePath);
    const [buffer] = await file.download();

    const dir = path.dirname(filePath);
    const ext = path.extname(filePath);
    const baseName = path.basename(filePath, ext);

    const promises = THUMBNAIL_SIZES.map(async (size) => {
      const thumbBuffer = await sharp(buffer)
        .resize(size.width, size.height, { fit: 'cover' })
        .jpeg({ quality: 80 })
        .toBuffer();

      const thumbPath = `${dir}/thumbnails/${baseName}_${size.suffix}.jpg`;
      const thumbFile = bucket.file(thumbPath);

      await thumbFile.save(thumbBuffer, {
        metadata: {
          contentType: 'image/jpeg',
          cacheControl: 'public, max-age=86400',
        },
      });
    });

    await Promise.all(promises);
  });
```

**Step 5: Generate Output**
- `storage.rules` with path-based ownership and file validation
- `cors.json` for browser-based upload access
- Upload component with progress tracking and error handling
- Cloud Function for thumbnail generation
- Bucket structure documentation

**Step 6: Update Memory**
- Store bucket structure in `bucket_structure.md`
- Store security rules in `security_rules.md`
- Store upload patterns in `upload_patterns.md`

### Expected Output

A complete profile image upload system with:
- Client-side file validation (type, size)
- Resumable upload with progress bar
- Automatic thumbnail generation in 3 sizes via Cloud Functions
- Security rules enforcing ownership and file constraints
- CORS configuration for browser access
- 24-hour CDN caching for avatars

---

## Example 2: Document Management System with Access Control

### Scenario

A business application needs document storage with role-based access control. Users can upload PDF and Office documents to shared team folders. Documents have view/edit permissions per team, and signed URLs are used for time-limited sharing with external users.

### User Request

"We need a document management system where teams can upload and share documents. Each team has its own folder, users can only access their team's documents, and we need to generate shareable links that expire after 24 hours for external sharing. We're using the Admin SDK on our Node.js backend."

### Skill Workflow

**Step 1: Initial Analysis**
- Application type: Server-side (Node.js backend)
- SDK: Firebase Admin SDK
- File types: PDF, DOCX, XLSX, PPTX
- Max file size: 50 MB
- Access pattern: Team-based read/write, time-limited external sharing
- Processing needs: None (document storage only)

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("firebase-storage", "team-docs-app")` → No existing memory

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load access control patterns

**Step 4: Storage Implementation**

**Bucket Structure:**
```
teams/
└── {teamId}/
    └── documents/
        ├── contracts/
        │   ├── {docId}_contract_v1.pdf
        │   └── {docId}_contract_v2.pdf
        ├── reports/
        │   └── {docId}_quarterly_report.xlsx
        └── presentations/
            └── {docId}_pitch_deck.pptx
```

**Security Rules (storage.rules):**
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // Team documents: only authenticated team members
    match /teams/{teamId}/documents/{allPaths=**} {
      allow read: if request.auth != null
                  && request.auth.token.teamId == teamId;

      allow write: if request.auth != null
                   && request.auth.token.teamId == teamId
                   && request.auth.token.role in ['admin', 'editor']
                   && request.resource.size < 50 * 1024 * 1024
                   && request.resource.contentType.matches(
                        'application/(pdf|msword|vnd\\.openxmlformats.*|vnd\\.ms-excel.*|vnd\\.ms-powerpoint.*)'
                      );

      allow delete: if request.auth != null
                    && request.auth.token.teamId == teamId
                    && request.auth.token.role == 'admin';
    }
  }
}
```

**Server-Side Upload (Node.js Admin SDK):**
```typescript
import * as admin from 'firebase-admin';
import { v4 as uuidv4 } from 'uuid';
import * as path from 'path';

const bucket = admin.storage().bucket();

interface UploadOptions {
  teamId: string;
  category: string;
  originalName: string;
  filePath: string;
  uploadedBy: string;
}

async function uploadDocument(options: UploadOptions): Promise<{
  storagePath: string;
  downloadUrl: string;
}> {
  const { teamId, category, originalName, filePath, uploadedBy } = options;

  const ext = path.extname(originalName);
  const docId = uuidv4();
  const sanitizedName = originalName
    .replace(/[^a-zA-Z0-9._-]/g, '_')
    .toLowerCase();
  const storagePath = `teams/${teamId}/documents/${category}/${docId}_${sanitizedName}`;

  await bucket.upload(filePath, {
    destination: storagePath,
    metadata: {
      contentType: getMimeType(ext),
      metadata: {
        uploadedBy,
        teamId,
        category,
        originalName,
        uploadedAt: new Date().toISOString(),
      },
    },
  });

  // Generate download URL (long-lived)
  const file = bucket.file(storagePath);
  const [downloadUrl] = await file.getSignedUrl({
    action: 'read',
    expires: Date.now() + 365 * 24 * 60 * 60 * 1000, // 1 year for internal use
  });

  return { storagePath, downloadUrl };
}

function getMimeType(ext: string): string {
  const mimeTypes: Record<string, string> = {
    '.pdf': 'application/pdf',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  };
  return mimeTypes[ext.toLowerCase()] || 'application/octet-stream';
}
```

**External Sharing with Expiring URLs:**
```typescript
async function generateShareableLink(
  storagePath: string,
  expirationHours: number = 24
): Promise<string> {
  const file = bucket.file(storagePath);

  // Verify file exists
  const [exists] = await file.exists();
  if (!exists) {
    throw new Error('Document not found');
  }

  const [signedUrl] = await file.getSignedUrl({
    action: 'read',
    expires: Date.now() + expirationHours * 60 * 60 * 1000,
    responseDisposition: 'attachment', // Force download instead of inline
  });

  return signedUrl;
}

// Listing team documents
async function listTeamDocuments(
  teamId: string,
  category?: string
): Promise<Array<{ name: string; size: number; updated: string }>> {
  const prefix = category
    ? `teams/${teamId}/documents/${category}/`
    : `teams/${teamId}/documents/`;

  const [files] = await bucket.getFiles({ prefix });

  return files.map((file) => ({
    name: file.metadata.metadata?.originalName || file.name,
    size: parseInt(file.metadata.size as string, 10),
    updated: file.metadata.updated as string,
  }));
}
```

**Step 5: Generate Output**
- Security rules with team-based access control
- Admin SDK upload with metadata and signed URLs
- External sharing with configurable expiration
- Document listing and management functions

**Step 6: Update Memory**
- Store team folder structure in `bucket_structure.md`
- Store role-based security rules in `security_rules.md`
- Store signed URL patterns in `upload_patterns.md`

### Expected Output

A complete document management system with:
- Team-based folder isolation with role-based access (admin, editor)
- File type validation (PDF, Office documents only) and 50 MB size limit
- Server-side upload with UUID-based naming and metadata
- Signed URLs for internal use (1 year) and external sharing (24 hours)
- Document listing by team and category
- Forced download disposition for shared links

---

## Example 3: Storage Security Rules for a Media-Sharing Platform

### Scenario

A media-sharing platform (similar to Instagram) needs comprehensive storage security rules. Users upload photos and videos to their profiles, can share media to public or friends-only feeds, and admins can moderate content. The platform supports multiple file types with strict size limits.

### User Request

"We need production-ready storage security rules for our media-sharing platform. Users upload photos (max 10 MB) and videos (max 100 MB) to their profiles. They can set content as public or friends-only. Admins need to be able to delete any content for moderation. We also need a separate path for temporary upload processing."

### Skill Workflow

**Step 1: Initial Analysis**
- Application type: Web and Mobile (cross-platform)
- Key requirements: Multi-tier access control, content moderation, file type/size enforcement
- File types: Images (JPEG, PNG, WebP, GIF), Videos (MP4, MOV, WebM)
- Size limits: Images 10 MB, Videos 100 MB
- Access tiers: Public, Friends-only, Private, Admin

**Step 2: Load Memory**
- `memoryStore.getSkillMemory("firebase-storage", "media-platform")` → No existing memory

**Step 3: Load Context**
- `contextProvider.getDomainIndex("schema")` → Load security rule patterns

**Step 4: Storage Implementation**

**Bucket Structure:**
```
users/
└── {uid}/
    ├── media/
    │   ├── photos/
    │   │   └── {photoId}.jpg
    │   └── videos/
    │       └── {videoId}.mp4
    ├── thumbnails/
    │   └── {mediaId}_thumb.jpg
    └── profile/
        └── avatar.jpg

processing/
└── {uid}/
    └── {uploadId}/              # Temporary processing area
        └── raw_upload.*         # Cleaned up after processing

public-feed/
└── {uid}/
    └── {mediaId}.*             # Copies for public feed (CDN-optimized)
```

**Comprehensive Security Rules (storage.rules):**
```
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // ===== Helper Functions =====

    // Check if user is authenticated
    function isAuthenticated() {
      return request.auth != null;
    }

    // Check if user owns the resource
    function isOwner(userId) {
      return isAuthenticated() && request.auth.uid == userId;
    }

    // Check if user is admin
    function isAdmin() {
      return isAuthenticated() && request.auth.token.role == 'admin';
    }

    // Check if user is a friend (via custom claim containing friend list)
    function isFriend(userId) {
      return isAuthenticated()
        && request.auth.token.friends is list
        && userId in request.auth.token.friends;
    }

    // Validate image file
    function isValidImage() {
      return request.resource.contentType.matches('image/(jpeg|png|webp|gif)')
        && request.resource.size < 10 * 1024 * 1024; // 10 MB
    }

    // Validate video file
    function isValidVideo() {
      return request.resource.contentType.matches('video/(mp4|quicktime|webm)')
        && request.resource.size < 100 * 1024 * 1024; // 100 MB
    }

    // ===== User Media =====

    // User photos
    match /users/{userId}/media/photos/{photoId} {
      // Owner and admins can always read
      // Public photos are readable by anyone authenticated
      allow read: if isOwner(userId)
                  || isAdmin()
                  || (isAuthenticated() && resource.metadata.visibility == 'public')
                  || (isFriend(userId) && resource.metadata.visibility in ['public', 'friends']);

      // Only owner can upload, must be valid image
      allow create: if isOwner(userId) && isValidImage();

      // Owner can update metadata (e.g., change visibility)
      allow update: if isOwner(userId) && isValidImage();

      // Owner and admins can delete (moderation)
      allow delete: if isOwner(userId) || isAdmin();
    }

    // User videos
    match /users/{userId}/media/videos/{videoId} {
      allow read: if isOwner(userId)
                  || isAdmin()
                  || (isAuthenticated() && resource.metadata.visibility == 'public')
                  || (isFriend(userId) && resource.metadata.visibility in ['public', 'friends']);

      allow create: if isOwner(userId) && isValidVideo();
      allow update: if isOwner(userId) && isValidVideo();
      allow delete: if isOwner(userId) || isAdmin();
    }

    // User thumbnails (auto-generated, read-only for clients)
    match /users/{userId}/thumbnails/{thumbId} {
      allow read: if isAuthenticated();
      allow write: if false; // Only Cloud Functions can write
    }

    // User profile avatar
    match /users/{userId}/profile/{fileName} {
      allow read: if true; // Avatars are always public
      allow write: if isOwner(userId)
                   && isValidImage()
                   && request.resource.size < 5 * 1024 * 1024; // 5 MB for avatars
    }

    // ===== Processing Area =====

    // Temporary upload processing (auto-cleaned)
    match /processing/{userId}/{uploadId}/{fileName} {
      allow read: if isOwner(userId);
      allow create: if isOwner(userId)
                    && (isValidImage() || isValidVideo());
      allow delete: if isOwner(userId) || isAdmin();
      // No update — upload once, process, then delete
      allow update: if false;
    }

    // ===== Public Feed =====

    // CDN-optimized public content
    match /public-feed/{userId}/{mediaId} {
      allow read: if true; // Public feed is world-readable
      allow write: if false; // Only Cloud Functions populate this
    }

    // ===== Catch-all: Deny everything else =====
    match /{allPaths=**} {
      allow read, write: if false;
    }
  }
}
```

**CORS Configuration (cors.json):**
```json
[
  {
    "origin": [
      "https://media-platform.example.com",
      "https://admin.media-platform.example.com"
    ],
    "method": ["GET", "POST", "PUT", "DELETE", "HEAD"],
    "maxAgeSeconds": 3600,
    "responseHeader": [
      "Content-Type",
      "Authorization",
      "Content-Length",
      "X-Upload-Content-Type",
      "X-Upload-Content-Length"
    ]
  }
]
```

**Visibility-Aware Upload (Web SDK):**
```typescript
import { ref, uploadBytesResumable, getDownloadURL } from 'firebase/storage';
import { storage } from '../firebase-config';

type Visibility = 'public' | 'friends' | 'private';
type MediaType = 'photos' | 'videos';

interface MediaUploadOptions {
  userId: string;
  file: File;
  mediaType: MediaType;
  visibility: Visibility;
  onProgress?: (percent: number) => void;
}

async function uploadMedia(options: MediaUploadOptions): Promise<{
  downloadURL: string;
  storagePath: string;
}> {
  const { userId, file, mediaType, visibility, onProgress } = options;

  // Client-side validation
  const limits = {
    photos: { maxSize: 10 * 1024 * 1024, types: ['image/jpeg', 'image/png', 'image/webp', 'image/gif'] },
    videos: { maxSize: 100 * 1024 * 1024, types: ['video/mp4', 'video/quicktime', 'video/webm'] },
  };

  const config = limits[mediaType];
  if (!config.types.includes(file.type)) {
    throw new Error(`Invalid file type for ${mediaType}: ${file.type}`);
  }
  if (file.size > config.maxSize) {
    throw new Error(`File exceeds ${config.maxSize / (1024 * 1024)} MB limit`);
  }

  const mediaId = crypto.randomUUID();
  const ext = file.name.split('.').pop();
  const storagePath = `users/${userId}/media/${mediaType}/${mediaId}.${ext}`;
  const storageRef = ref(storage, storagePath);

  const metadata = {
    contentType: file.type,
    cacheControl: visibility === 'public'
      ? 'public, max-age=86400'
      : 'private, max-age=3600',
    customMetadata: {
      visibility,
      uploadedBy: userId,
      originalName: file.name,
      mediaId,
    },
  };

  const uploadTask = uploadBytesResumable(storageRef, file, metadata);

  return new Promise((resolve, reject) => {
    uploadTask.on(
      'state_changed',
      (snapshot) => {
        if (onProgress) {
          const percent = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
          onProgress(percent);
        }
      },
      (error) => reject(error),
      async () => {
        const downloadURL = await getDownloadURL(uploadTask.snapshot.ref);
        resolve({ downloadURL, storagePath });
      }
    );
  });
}
```

**Admin Moderation Function:**
```typescript
import * as admin from 'firebase-admin';

const bucket = admin.storage().bucket();

async function moderateContent(
  storagePath: string,
  action: 'delete' | 'flag',
  reason: string,
  moderatorId: string
): Promise<void> {
  const file = bucket.file(storagePath);
  const [exists] = await file.exists();

  if (!exists) {
    throw new Error('Content not found');
  }

  if (action === 'delete') {
    // Log moderation action before deletion
    const [metadata] = await file.getMetadata();
    console.log(`Moderation: ${moderatorId} deleted ${storagePath}. Reason: ${reason}`);
    console.log(`Original uploader: ${metadata.metadata?.uploadedBy}`);

    await file.delete();

    // Also delete associated thumbnails
    const mediaId = metadata.metadata?.mediaId;
    if (mediaId) {
      const userId = metadata.metadata?.uploadedBy;
      try {
        await bucket.file(`users/${userId}/thumbnails/${mediaId}_thumb.jpg`).delete();
      } catch {
        // Thumbnail may not exist
      }
    }
  } else if (action === 'flag') {
    // Update metadata to flag content
    await file.setMetadata({
      metadata: {
        flagged: 'true',
        flagReason: reason,
        flaggedBy: moderatorId,
        flaggedAt: new Date().toISOString(),
      },
    });
  }
}
```

**Step 5: Generate Output**
- Comprehensive security rules with helper functions
- Multi-tier visibility support (public, friends, private)
- CORS configuration for web and admin portals
- Upload implementation with client-side validation
- Admin moderation functions

**Step 6: Update Memory**
- Store media path hierarchy in `bucket_structure.md`
- Store multi-tier security rules in `security_rules.md`
- Store visibility-aware upload patterns in `upload_patterns.md`
- Store CDN cache strategies in `cdn_config.md`

### Expected Output

A complete media-sharing storage system with:
- Multi-tier security rules (public, friends-only, private, admin)
- Helper functions for DRY rule logic (isOwner, isAdmin, isFriend)
- Separate validation for images (10 MB) and videos (100 MB)
- Temporary processing area with write-once semantics
- Public feed path managed exclusively by Cloud Functions
- Catch-all deny rule preventing unauthorized access
- CORS configuration for web and admin interfaces
- Admin moderation with content flagging and deletion
- Visibility-aware cache control headers

---

## Common Patterns

### Pattern 1: Content-Hash File Naming
```typescript
async function hashFileName(file: File): Promise<string> {
  const buffer = await file.arrayBuffer();
  const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex.substring(0, 16);
}
```

### Pattern 2: Upload Retry with Exponential Backoff
```typescript
async function uploadWithRetry(
  storageRef: StorageReference,
  file: File,
  maxRetries: number = 3
): Promise<string> {
  let attempt = 0;
  while (attempt < maxRetries) {
    try {
      const snapshot = await uploadBytes(storageRef, file);
      return await getDownloadURL(snapshot.ref);
    } catch (error: any) {
      attempt++;
      if (attempt >= maxRetries) throw error;
      const delay = Math.pow(2, attempt) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error('Upload failed after retries');
}
```

### Pattern 3: File Cleanup on Document Deletion
```typescript
export const cleanupStorageOnDelete = functions.firestore
  .document('posts/{postId}')
  .onDelete(async (snapshot) => {
    const data = snapshot.data();
    if (!data?.storagePath) return;

    const bucket = admin.storage().bucket();
    try {
      await bucket.file(data.storagePath).delete();
    } catch (error: any) {
      if (error.code !== 404) throw error;
    }
  });
```

---

## Tips for Using Firebase Cloud Storage

1. **Validate on client AND server**: Client validation improves UX; security rules enforce compliance
2. **Always configure CORS first**: Deploy `cors.json` before any browser-based uploads
3. **Use resumable uploads for large files**: Anything over 5 MB should use resumable uploads
4. **Set meaningful metadata**: Include content type, cache control, and custom metadata on every upload
5. **Design paths for security**: Structure paths so security rules can use path segments for access control
6. **Clean up orphaned files**: Implement Cloud Functions to delete files when parent resources are removed
7. **Monitor storage usage**: Set up alerts for quota thresholds to avoid service disruptions
8. **Version your files**: Use content-hash or versioned naming to enable CDN cache busting
