# DevOps Engineer Examples

This file contains example scenarios demonstrating how the **devops-engineer** skill designs CI/CD pipelines and implements DevOps practices.

## Example 1: GitHub Actions Pipeline for Node.js Microservice

### Scenario

A team is building a Node.js microservice deployed to AWS ECS. They need a complete CI/CD pipeline with automated testing, security scanning, and blue/green deployment.

### Requirements
- **Build**: Install dependencies, run TypeScript compilation
- **Test**: Unit tests (Jest), integration tests, E2E tests (Playwright)
- **Security**: Dependency scanning, SAST, container scanning
- **Quality Gates**: 80% code coverage, no critical vulnerabilities
- **Deploy**: Blue/green deployment to ECS with automated rollback
- **Notifications**: Slack alerts for failures

### Pipeline Configuration (`.github/workflows/ci-cd.yml`)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20.x'
  AWS_REGION: us-east-1
  ECR_REPOSITORY: my-microservice
  ECS_CLUSTER: production-cluster
  ECS_SERVICE: my-microservice

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Build
        run: npm run build

      - name: Unit Tests
        run: npm run test:unit -- --coverage

      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json

      - name: Check Coverage Threshold
        run: |
          COVERAGE=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk Security Scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: SAST with CodeQL
        uses: github/codeql-action/analyze@v2

  integration-tests:
    runs-on: ubuntu-latest
    needs: [build-and-test]
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npm ci
      - run: npm run test:integration

  build-and-push-image:
    runs-on: ubuntu-latest
    needs: [build-and-test, security-scan, integration-tests]
    if: github.ref == 'refs/heads/main'
    outputs:
      image: ${{ steps.build-image.outputs.image }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push image
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Scan Container Image
        run: |
          docker scan ${{ steps.build-image.outputs.image }}

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [build-and-push-image]
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Deploy to ECS Staging
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: task-def-staging.json
          service: ${{ env.ECS_SERVICE }}-staging
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

      - name: Run Smoke Tests
        run: |
          curl -f https://staging.example.com/health || exit 1

  deploy-production:
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Blue/Green Deploy to ECS
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: task-def-prod.json
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

      - name: Monitor Error Rate
        run: |
          # Check CloudWatch metrics for error rate spike
          aws cloudwatch get-metric-statistics \
            --namespace AWS/ApplicationELB \
            --metric-name HTTPCode_Target_5XX_Count \
            --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%S) \
            --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
            --period 300 \
            --statistics Sum

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Key Features
- ✅ **Parallel Testing**: Build, security, and integration tests run in parallel
- ✅ **Quality Gates**: 80% coverage threshold enforced
- ✅ **Security**: Snyk, CodeQL, container scanning
- ✅ **Blue/Green**: ECS deployment with rollback capability
- ✅ **Environment Protection**: Manual approval for production
- ✅ **Monitoring**: Post-deployment health checks

---

## Example 2: Azure Pipelines for .NET Monorepo

### Scenario

Enterprise .NET solution with 10 microservices in a monorepo. Need intelligent CI that only builds/tests changed services, with automated release to Azure Kubernetes Service (AKS).

### Requirements
- **Monorepo**: Only build changed services
- **Multi-Stage**: Build → Test → Package → Deploy
- **Artifacts**: Helm charts and container images
- **Approvals**: Manager approval for production
- **Rollback**: Automated rollback on deployment failure

### Pipeline Configuration (`azure-pipelines.yml`)

```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - services/*
      - shared/*

pr:
  branches:
    include:
      - main
  paths:
    include:
      - services/*

variables:
  - group: production-secrets
  - name: buildConfiguration
    value: 'Release'
  - name: aksNamespace
    value: 'production'

stages:
  - stage: DetectChanges
    displayName: 'Detect Changed Services'
    jobs:
      - job: DetectChanges
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - bash: |
              # Detect which services changed
              git diff --name-only HEAD~1 HEAD > changed_files.txt
              cat changed_files.txt | grep "^services/" | cut -d'/' -f2 | sort -u > changed_services.txt
              echo "Changed services:"
              cat changed_services.txt
            displayName: 'Detect Changed Services'

          - publish: changed_services.txt
            artifact: ChangedServices

  - stage: Build
    displayName: 'Build Changed Services'
    dependsOn: DetectChanges
    jobs:
      - job: BuildServices
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          matrix:
            ${{ each service in ['user-service', 'order-service', 'payment-service'] }}:
              ${{ service }}:
                serviceName: ${{ service }}
        steps:
          - download: current
            artifact: ChangedServices

          - bash: |
              if grep -q "^$(serviceName)$" $(Pipeline.Workspace)/ChangedServices/changed_services.txt; then
                echo "##vso[task.setvariable variable=shouldBuild]true"
              else
                echo "##vso[task.setvariable variable=shouldBuild]false"
              fi
            displayName: 'Check if service changed'

          - task: DotNetCoreCLI@2
            condition: eq(variables['shouldBuild'], 'true')
            inputs:
              command: 'restore'
              projects: 'services/$(serviceName)/*.csproj'

          - task: DotNetCoreCLI@2
            condition: eq(variables['shouldBuild'], 'true')
            inputs:
              command: 'build'
              projects: 'services/$(serviceName)/*.csproj'
              arguments: '--configuration $(buildConfiguration) --no-restore'

          - task: DotNetCoreCLI@2
            condition: eq(variables['shouldBuild'], 'true')
            displayName: 'Run Unit Tests'
            inputs:
              command: 'test'
              projects: 'services/$(serviceName).Tests/*.csproj'
              arguments: '--configuration $(buildConfiguration) --collect:"XPlat Code Coverage"'

          - task: PublishCodeCoverageResults@1
            condition: eq(variables['shouldBuild'], 'true')
            inputs:
              codeCoverageTool: 'Cobertura'
              summaryFileLocation: '$(Agent.TempDirectory)/**/*coverage.cobertura.xml'

  - stage: Package
    displayName: 'Package and Push Images'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - job: PackageServices
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: Docker@2
            inputs:
              containerRegistry: 'ACR Connection'
              repository: '$(serviceName)'
              command: 'buildAndPush'
              Dockerfile: 'services/$(serviceName)/Dockerfile'
              tags: |
                $(Build.BuildId)
                latest

  - stage: DeployStaging
    displayName: 'Deploy to Staging'
    dependsOn: Package
    jobs:
      - deployment: DeployStaging
        environment: 'staging'
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: KubernetesManifest@0
                  inputs:
                    action: 'deploy'
                    kubernetesServiceConnection: 'AKS-Staging'
                    namespace: 'staging'
                    manifests: |
                      k8s/deployment.yml
                      k8s/service.yml
                    containers: 'myacr.azurecr.io/$(serviceName):$(Build.BuildId)'

                - bash: |
                    kubectl rollout status deployment/$(serviceName) -n staging --timeout=300s
                  displayName: 'Wait for Rollout'

  - stage: DeployProduction
    displayName: 'Deploy to Production'
    dependsOn: DeployStaging
    condition: succeeded()
    jobs:
      - deployment: DeployProduction
        environment: 'production'
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          canary:
            increments: [10, 25, 50, 100]
            preDeploy:
              steps:
                - bash: echo "Starting canary deployment"
            deploy:
              steps:
                - task: KubernetesManifest@0
                  inputs:
                    action: 'deploy'
                    kubernetesServiceConnection: 'AKS-Production'
                    namespace: '$(aksNamespace)'
                    manifests: 'k8s/deployment.yml'
                    containers: 'myacr.azurecr.io/$(serviceName):$(Build.BuildId)'
                    trafficSplitMethod: 'smi'
                    percentage: $(strategy.increment)

            routeTraffic:
              steps:
                - bash: |
                    # Monitor error rate during canary
                    ERROR_RATE=$(az monitor metrics list \
                      --resource /subscriptions/.../loadBalancer \
                      --metric "FailedRequests" \
                      --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%S) \
                      --interval PT1M \
                      --query "value[0].timeseries[0].data[-1].total")
                    
                    if (( $(echo "$ERROR_RATE > 1" | bc -l) )); then
                      echo "Error rate too high: $ERROR_RATE"
                      exit 1
                    fi
                  displayName: 'Check Canary Health'

            postRouteTraffic:
              steps:
                - bash: echo "Canary $(strategy.increment)% successful"

            on:
              failure:
                steps:
                  - task: KubernetesManifest@0
                    inputs:
                      action: 'reject'
                      kubernetesServiceConnection: 'AKS-Production'
                      namespace: '$(aksNamespace)'
                  - bash: echo "Canary deployment failed, rolled back"
              success:
                steps:
                  - bash: echo "Canary deployment completed successfully"
```

### Key Features
- ✅ **Smart Build**: Only builds changed services in monorepo
- ✅ **Multi-Stage**: Clear separation of build, package, deploy
- ✅ **Canary Deployment**: Progressive rollout (10% → 25% → 50% → 100%)
- ✅ **Automated Rollback**: Reverts on health check failure
- ✅ **Environment Protection**: Manual approval for production
- ✅ **Code Coverage**: Integrated test reporting

---

## Example 3: GitLab CI with Feature Branch Environments

### Scenario

Python data science team using GitLab. Need ephemeral environments for each feature branch, with Jupyter notebooks and GPU support for ML training.

### Requirements
- **Ephemeral Envs**: Spin up environment per PR
- **GPU Support**: ML training jobs need GPU runners
- **Data Pipeline**: Run ETL before training
- **Model Registry**: Push trained models to artifact registry
- **Cleanup**: Destroy environments when branch is deleted

### Pipeline Configuration (`.gitlab-ci.yml`)

```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DOCKER_DRIVER: overlay2
  K8S_NAMESPACE: "ml-${CI_COMMIT_REF_SLUG}"

cache:
  paths:
    - .cache/pip

stages:
  - test
  - build
  - deploy
  - train
  - cleanup

test:
  stage: test
  image: python:3.11
  before_script:
    - pip install -r requirements-dev.txt
  script:
    - pytest tests/ --cov=src --cov-report=xml --cov-report=term
    - pylint src/
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build-image:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - branches

deploy-preview:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl create namespace $K8S_NAMESPACE || true
    - |
      cat <<EOF | kubectl apply -f -
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: ml-app
        namespace: $K8S_NAMESPACE
      spec:
        replicas: 1
        selector:
          matchLabels:
            app: ml-app
        template:
          metadata:
            labels:
              app: ml-app
          spec:
            containers:
            - name: ml-app
              image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
              ports:
              - containerPort: 8888
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: ml-app
        namespace: $K8S_NAMESPACE
      spec:
        type: LoadBalancer
        ports:
        - port: 80
          targetPort: 8888
        selector:
          app: ml-app
      EOF
    - |
      JUPYTER_URL=$(kubectl get svc ml-app -n $K8S_NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
      echo "Jupyter available at: http://$JUPYTER_URL"
  environment:
    name: preview/$CI_COMMIT_REF_SLUG
    url: http://$CI_ENVIRONMENT_SLUG.ml.example.com
    on_stop: cleanup-preview
  only:
    - branches
  except:
    - main

train-model:
  stage: train
  tags:
    - gpu  # Use GPU-enabled runner
  image: tensorflow/tensorflow:latest-gpu
  script:
    - python scripts/etl.py  # Run data pipeline
    - python scripts/train_model.py --epochs 100
    - python scripts/evaluate_model.py
    - |
      # Push model to registry
      curl -X POST \
        -H "JOB-TOKEN: $CI_JOB_TOKEN" \
        -F "file=@model.h5" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/packages/generic/models/$CI_COMMIT_SHA/model.h5"
  artifacts:
    paths:
      - model.h5
      - metrics.json
    expire_in: 30 days
  only:
    - main

cleanup-preview:
  stage: cleanup
  image: bitnami/kubectl:latest
  script:
    - kubectl delete namespace $K8S_NAMESPACE || true
  when: manual
  environment:
    name: preview/$CI_COMMIT_REF_SLUG
    action: stop
```

### Key Features
- ✅ **Ephemeral Environments**: Kubernetes namespace per branch
- ✅ **GPU Support**: ML training on GPU-enabled runners
- ✅ **Model Registry**: Artifacts stored in GitLab package registry
- ✅ **Auto-Cleanup**: Manual trigger to destroy preview environment
- ✅ **Jupyter Access**: Dynamic URLs for data exploration
- ✅ **Pipeline Caching**: pip cache for faster builds

---

## Common DevOps Patterns

### Pattern 1: Pipeline as Code
- Store all pipeline config in version control
- Use YAML/JSON for declarative pipelines
- Template reusable pipeline components
- Review pipeline changes like code

### Pattern 2: Fail Fast
- Run fastest tests first (lint, unit tests)
- Parallel execution of independent stages
- Cancel jobs on first failure (PR pipelines)
- Clear error messages and logs

### Pattern 3: Artifact Promotion
- Build once, deploy many times
- Tag artifacts with immutable identifiers (git SHA)
- Progressive environment promotion (dev → staging → prod)
- Artifact signing and verification

### Pattern 4: Feature Flags + Deployment
- Deploy code with features disabled
- Enable features progressively
- Decouple deployment from release
- Instant feature rollback without redeployment

### Pattern 5: GitOps
- Git as single source of truth
- Automated sync between Git and runtime
- Pull-based deployment (Argo CD, Flux)
- Audit trail via Git history
