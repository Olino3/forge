# /azure-pipeline Examples

## Example 1: Basic CI Pipeline

```
/azure-pipeline --type ci
```

**What happens**:
1. Detects Node.js project from `package.json`
2. Delegates to `skill:generate-azure-pipelines`
3. Generates `azure-pipelines.yml` with:
   - Build stage: `npm ci && npm run build`
   - Test stage: `npm test` with coverage
   - Lint stage: `npm run lint`
4. Configures triggers for main branch and PRs
5. Saves setup guide to `/claudedocs/azure-pipeline_ci_20260210.md`

## Example 2: Full CI/CD for Azure Functions

```
/azure-pipeline --type ci-cd --target function
```

**What happens**:
1. Detects Python Azure Functions project
2. Generates multi-stage pipeline:
   - **Build**: Install dependencies, run tests
   - **Deploy Dev**: Auto-deploy to dev function app
   - **Deploy Prod**: Deploy to prod with manual approval
3. Delegates to `skill:generate-azure-bicep` for infrastructure
4. Creates Bicep templates for Function App, Storage, App Insights
5. Provides service principal setup instructions

## Example 3: Container Pipeline to AKS

```
/azure-pipeline my-api --type ci-cd --target aks
```

**What happens**:
1. Detects Dockerfile in project
2. Generates pipeline with:
   - **Build**: Docker image build
   - **Push**: Push to Azure Container Registry (ACR)
   - **Deploy**: Deploy to AKS cluster with Helm
3. Creates Helm charts if not present
4. Configures image scanning for vulnerabilities
5. Sets up blue-green deployment strategy
6. Provides kubectl and Helm setup instructions

## Example 4: Web App with Database Migrations

```
/azure-pipeline web-app --type ci-cd --target webapp
```

**What happens**:
1. Detects .NET web application with Entity Framework
2. Asks: "Database migrations needed?"
   - User: "Yes, using EF Core migrations"
3. Generates pipeline with:
   - **Build**: dotnet build, dotnet publish
   - **Test**: Unit and integration tests
   - **Deploy**: App Service deployment
   - **Migrate**: EF migrations before deployment
4. Adds database connection string to variable groups
5. Configures slot swapping for zero-downtime

## Example 5: Multi-Environment Pipeline

```
/azure-pipeline --stages build,test,deploy --type ci-cd
```

**What happens**:
1. Creates pipeline with explicit stages
2. Configures three deployment environments:
   - **Dev**: Auto-deploy on commit to develop
   - **Staging**: Auto-deploy on commit to main, runs smoke tests
   - **Production**: Manual approval required, blue-green deployment
3. Sets up environment-specific variable groups
4. Configures approval gates:
   - Staging: Optional QA approval
   - Production: Required approval from 2 approvers

## Example 6: Microservices Pipeline

```
/azure-pipeline microservices --type ci-cd --target aks
```

**What happens**:
1. Detects multiple services in monorepo
2. Generates pipeline with:
   - Path-based triggers (only build changed services)
   - Parallel build jobs for each service
   - Separate Docker images per service
   - Coordinated deployment to AKS
3. Creates Kubernetes manifests for each service
4. Configures service mesh (Istio/Linkerd) if needed
5. Sets up distributed tracing integration

## Example 7: Infrastructure-First Pipeline

```
/azure-pipeline infra --type cd --target webapp
```

**What happens**:
1. Focuses on infrastructure deployment
2. Delegates to `skill:generate-azure-bicep`
3. Generates Bicep templates for:
   - App Service Plan
   - App Service (Web App)
   - Application Insights
   - Key Vault for secrets
4. Creates deployment pipeline:
   - Validate Bicep (dry-run)
   - Deploy infrastructure to dev
   - Deploy infrastructure to prod (with approval)
5. Outputs ARM deployment commands

## Example 8: Security-Focused Pipeline

```
/azure-pipeline secure-app --type ci-cd
```

**What happens**:
1. Adds comprehensive security stages:
   - **SAST**: Static code analysis (SonarQube)
   - **Dependency Check**: Vulnerable dependencies scan
   - **Container Scan**: Image vulnerability scanning (Trivy)
   - **Secrets Detection**: Check for committed secrets (GitLeaks)
2. Configures security gates (fail on high/critical issues)
3. Generates security report artifacts
4. Sets up compliance checks (OWASP Top 10)
5. Adds security notifications for failures
