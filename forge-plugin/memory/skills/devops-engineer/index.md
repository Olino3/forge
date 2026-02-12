# devops-engineer Memory

Project-specific memory for DevOps engineering, including CI/CD pipeline configurations, deployment strategies, automation patterns, and optimization learnings.

## Purpose

This memory helps the `skill:devops-engineer` remember:
- Pipeline configurations and patterns used
- Deployment strategies and their effectiveness
- Build and test optimization techniques
- Security integration patterns
- Infrastructure automation learnings
- Common issues and their resolutions

## Memory Files Per Project

Each project gets its own directory: `{project-name}/`

### Required Files

#### `project_overview.md` ⭐ CRITICAL

**Purpose**: High-level project understanding - ALWAYS CREATE THIS FIRST

**Must contain**:
- **Project name and purpose**: What does this application do?
- **Source control platform**: GitHub, GitLab, Azure DevOps, Bitbucket
- **CI/CD platform**: GitHub Actions, Azure Pipelines, GitLab CI, Jenkins
- **Language(s) and build tools**: Node/npm, .NET/MSBuild, Python/pip, etc.
- **Deployment targets**: AWS, Azure, GCP, on-premise, hybrid
- **Release frequency**: Continuous, daily, weekly, monthly
- **Team size**: Number of developers
- **Testing strategy**: Unit, integration, E2E, performance
- **Security requirements**: SAST, DAST, SCA, container scanning

#### `pipeline_patterns.md`

**Purpose**: Document reusable pipeline patterns and configurations

**Must contain**:
- **Pipeline stages**: Build, test, package, deploy stages
- **Trigger configuration**: Push, PR, schedule, manual triggers
- **Parallelization strategy**: Which jobs run in parallel
- **Caching strategy**: Dependency caching, Docker layer caching
- **Artifact management**: What artifacts are produced and where stored
- **Environment configuration**: dev, staging, production setups

#### `deployment_strategies.md`

**Purpose**: Track deployment approaches and results

**Must contain**:
- **Strategy type**: Blue/green, canary, rolling, recreate
- **Rollback procedures**: How to revert deployments
- **Deployment gates**: Manual approvals, automated quality gates
- **Health checks**: Post-deployment verification steps
- **Downtime windows**: Scheduled maintenance patterns
- **Incident history**: Failed deployments and lessons learned

### Optional Files

#### `optimization_notes.md`
- Build time optimizations and impact
- Test execution time improvements
- Dependency caching strategies
- Pipeline parallelization wins
- Resource utilization improvements

#### `security_integrations.md`
- Security scanning tools integrated (Snyk, SonarQube, etc.)
- Vulnerability management process
- Secret management patterns
- Compliance requirements and controls

#### `troubleshooting_guide.md`
- Common pipeline failures and fixes
- Flaky test mitigations
- Deployment rollback procedures
- Emergency procedures and contacts

## Cross-Skill Integration

The `devops-engineer` skill integrates with:
- **cloud-architect**: Infrastructure design and provisioning
- **kubernetes-specialist**: Container orchestration and deployment
- **sre-engineer**: Monitoring, alerting, and reliability
- **terraform-engineer**: Infrastructure as Code automation
- **testing**: Test automation and quality gates

Use `memoryStore.getByProject("{project-name}")` to discover insights from other skills.

## Memory Lifecycle

- **Fresh** (0-30 days): Active pipeline development, full detail
- **Active** (31-90 days): Stable pipeline, maintain key patterns
- **Stale** (91-180 days): Legacy pipeline, summarize optimizations
- **Archived** (181+ days): Deprecated pipeline, keep lessons learned only

## Example Memory Entry

### Example: `my-api/pipeline_patterns.md`

```markdown
# Pipeline Patterns - My API

**Last Updated**: 2026-02-10
**CI/CD Platform**: GitHub Actions
**Language**: Node.js 20.x
**Deployment**: AWS ECS Fargate

## Pipeline Architecture

### Stages
1. **Build & Test** (4 min)
   - Dependency installation with npm ci
   - TypeScript compilation
   - ESLint + Prettier
   - Jest unit tests (80% coverage required)
   
2. **Security Scan** (2 min, parallel with integration tests)
   - Snyk dependency scanning
   - CodeQL SAST analysis
   - Docker image scanning
   
3. **Integration Tests** (6 min, parallel with security scan)
   - PostgreSQL service container
   - API integration tests with Supertest
   - Test database seeding and cleanup
   
4. **Package** (3 min, main branch only)
   - Docker build with multi-stage Dockerfile
   - Push to AWS ECR
   - Tag with git SHA and 'latest'
   
5. **Deploy Staging** (2 min, main branch only)
   - Update ECS task definition
   - Deploy to staging cluster
   - Wait for service stability
   - Run smoke tests
   
6. **Deploy Production** (2 min, manual approval)
   - Blue/green deployment to ECS
   - Health check monitoring
   - Automated rollback on error rate spike

## Optimization History

### 2026-02-01: Parallelization Win
- **Change**: Run security scan and integration tests in parallel
- **Impact**: Reduced total pipeline time from 19 min → 13 min (32% improvement)
- **Trade-off**: Uses 2 concurrent runners instead of 1

### 2026-01-15: Dependency Caching
- **Change**: Enabled npm cache in GitHub Actions
- **Impact**: Reduced dependency install from 90s → 15s (83% improvement)
- **Configuration**: `actions/setup-node@v4` with `cache: 'npm'`

### 2025-12-10: Docker Layer Caching
- **Change**: Multi-stage Dockerfile with build cache
- **Impact**: Reduced Docker build from 5min → 2min (60% improvement)
- **Implementation**: Separated dependency install from source copy

## Deployment Strategy

### Blue/Green Deployment Pattern
- **Implementation**: AWS ECS with two target groups
- **Cutover**: ALB switches traffic via task definition update
- **Rollback**: Revert to previous task definition (< 1 minute)
- **Health Checks**: `/health` endpoint must return 200, 3 consecutive checks
- **Monitoring Window**: 5 minutes post-deployment
- **Rollback Trigger**: Error rate > 1% for 2 consecutive minutes

### Deployment Schedule
- **Staging**: Automatic on merge to main
- **Production**: Manual approval, typically 2-3x per week
- **Emergency Hotfix**: Skip staging with manager approval

## Common Issues & Resolutions

### Issue 1: Flaky Integration Tests
- **Symptom**: Random test failures in `order.test.ts`
- **Root Cause**: Race condition in database cleanup
- **Fix**: Added `beforeEach` hook with `TRUNCATE CASCADE`
- **Result**: 100% pass rate for 30 days

### Issue 2: Docker Build Timeouts
- **Symptom**: Docker build exceeds 10-minute timeout
- **Root Cause**: npm install fetching packages every time
- **Fix**: Multi-stage build with layer caching
- **Result**: Build time reduced to 2 minutes

### Issue 3: ECS Deployment Stuck
- **Symptom**: Deployment hangs at "waiting for service stability"
- **Root Cause**: New task failing health checks
- **Fix**: Increased health check grace period from 30s → 60s
- **Result**: Successful deployments, properly handles cold start
```

## Guidelines

1. **Always load memory first** before designing pipelines
2. **Document optimization impact** with before/after metrics
3. **Track deployment failures** and root causes
4. **Update patterns** when pipeline changes significantly
5. **Cross-reference related skills** for infrastructure context
6. **Measure everything** - build times, test duration, deployment frequency
7. **Keep troubleshooting current** - add new issues as they occur

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-12 | Initial memory structure for devops-engineer skill |
