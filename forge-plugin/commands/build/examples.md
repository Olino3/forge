# /build Examples

## Example 1: Standard Project Build

```
/build
```

**What happens**:
1. Detects build system (e.g., `package.json` → npm)
2. Runs `npm run build`
3. Reports success/failure with timing
4. Lists generated artifacts
5. Saves build report to `/claudedocs/build_report_20260209.md`

## Example 2: Production Build with Clean

```
/build --type prod --clean
```

**What happens**:
1. Removes existing build artifacts (`dist/`, `build/`, `__pycache__/`)
2. Runs production build with optimizations:
   - npm: `npm run build:prod` (minification, tree-shaking)
   - dotnet: `dotnet publish -c Release`
   - Poetry: `poetry build`
3. Reports artifact sizes and optimization metrics
4. Generates deployment-ready artifacts

## Example 3: Docker Build

```
/build --type prod --verbose
```

**What happens** (Docker project):
1. Detects Dockerfile and docker-compose.yml
2. Loads Docker build patterns from context
3. Runs `docker compose build` with build args for production
4. Shows detailed build output (--verbose)
5. Reports image sizes and layer information

## Example 4: Targeted Service Build

```
/build frontend --verbose
```

**What happens**:
1. Identifies `frontend` as a specific build target
2. Runs build for just the frontend service
3. Shows detailed output for debugging
4. Reports frontend-specific artifacts

## Example 5: Build Error Debugging

```
/build
```

**What happens** (with build failure):
1. Runs build command, captures failure
2. Parses error: "Module 'auth' has no attribute 'verify_token'"
3. Analyzes: Import error in `src/api/middleware.py:15`
4. Checks memory for known build issues
5. Suggests fix: "Function was renamed to `validate_token` in recent commit"
6. Reports error with resolution guidance

## Example 6: Local Development Build (Tilt)

```
/build --type dev
```

**What happens** (Tilt project):
1. Detects Tiltfile
2. Loads Tilt context from `../../context/azure/tiltfile_reference.md`
3. Runs `tilt up --stream`
4. Monitors service startup
5. Reports which services are running and their ports
6. Saves development environment status to report
