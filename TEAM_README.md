# ASAAS Team Guide (Daily Workflow and Operations)

This document is for all team members working on ASAAS. It explains exactly what to do on day one, what to do every day, how to push safely, how to use CI/CD, and how to run the project with Docker images.

## 1) Purpose

Use this guide to ensure everyone works the same way:
- consistent Git flow
- predictable releases
- safe collaboration on `main`
- fast troubleshooting

---

## 2) Access you need

Before you start, make sure you have access to:
- GitHub repository: `https://github.com/ginvbrs-eng/Asaas`
- Docker Hub images:
  - `ginvbrs/asaas-backend`
  - `ginvbrs/asaas-frontend`
- Local tools installed:
  - Git
  - Docker Desktop (or Docker Engine)
  - VS Code (recommended)

If Docker Hub repositories are private, run:

```bash
docker login -u <dockerhub_username>
```

---

## 3) Day 1 setup (new team member)

### Step 1: Clone repository

```bash
git clone https://github.com/ginvbrs-eng/Asaas.git
cd Asaas
```

### Step 2: Configure Git identity

```bash
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

### Step 3: Verify your setup

```bash
git remote -v
git branch -vv
docker --version
```

### Step 4: Start project locally

Option A: Build locally

```bash
docker compose up --build
```

Option B: Use prebuilt team images (faster)

```bash
docker compose -f docker-compose.yml -f docker-compose.images.yml pull
docker compose -f docker-compose.yml -f docker-compose.images.yml up -d
```

### Step 5: Validate services

- Frontend: `http://localhost`
- API health: `http://api.localhost/health`
- MinIO: `http://minio.localhost`
- Traefik dashboard: `http://localhost:8081/dashboard/`
- Elasticsearch (internal): `http://elasticsearch:9200`

If your task depends on search/indexing:

```bash
docker compose exec backend sh -lc "echo $ELASTICSEARCH_URL"
```

---

## 4) Daily workflow (every day)

### Morning sync

```bash
git checkout main
git pull origin main
```

### Start a new task branch

Use clear branch names:
- `feature/<name>`
- `fix/<name>`
- `chore/<name>`

Example:

```bash
git checkout -b feature/inventory-filter
```

### Work, test, commit

```bash
git add .
git commit -m "feat: add inventory filter by org"
```

### Push your branch

```bash
git push -u origin feature/inventory-filter
```

---

## 5) Before opening PR (quality checklist)

Run this checklist every time:

1. Code compiles/runs locally
2. No sensitive data committed (`.env`, tokens, secrets)
3. `node_modules` is not tracked
4. Docker services are healthy
5. Scope is small and focused
6. Commit message is clear

Quick checks:

```bash
git status
git diff --name-only
docker compose ps
```

---

## 6) CI/CD with GitHub Actions

Workflow file:
- `.github/workflows/build-and-push-images.yml`

Current mode:
- Manual trigger (`workflow_dispatch`)
- Automatic push trigger currently commented

### Run CI manually

1. Go to GitHub -> `Actions`
2. Open `Build and Push Images`
3. Click `Run workflow`

### What CI does

- builds backend image
- builds frontend image
- pushes to Docker Hub:
  - `ginvbrs/asaas-backend`
  - `ginvbrs/asaas-frontend`
- tags include:
  - `latest`
  - `sha-<short>`

---

## 7) Team release workflow (recommended)

### Standard release

1. Merge approved PR into `main`
2. Run workflow manually
3. Confirm new images are pushed
4. Team pulls latest images

### Safer release (recommended for production)

Use immutable SHA tag instead of only `latest`.

Example:

```bash
docker pull ginvbrs/asaas-backend:sha-abc1234
docker pull ginvbrs/asaas-frontend:sha-abc1234
```

---

## 8) Example: full task cycle

### Scenario
You need to add a new API endpoint.

### Commands

```bash
# 1) sync main
git checkout main
git pull origin main

# 2) create branch
git checkout -b feature/new-report-endpoint

# 3) implement changes
# ... edit files ...

# 4) run local stack
docker compose up --build

# 5) commit
git add .
git commit -m "feat(api): add new report endpoint"

# 6) push
git push -u origin feature/new-report-endpoint
```

Then create PR, request review, and merge after approval.

---

## 9) Troubleshooting quick reference

### A) `tls: bad record MAC` during image pulls
- Check network adapter/offload settings
- Restart WSL + Docker

### B) `port already in use`
- Find conflicting process/service
- Change local exposed port if needed

### C) `Username and password required` in GitHub Actions
- Ensure GitHub secrets exist:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`

### D) `Run workflow` button missing
- Confirm workflow is on `main`
- Confirm Actions are enabled
- Confirm `workflow_dispatch` exists

### E) GitHub push rejected due to large file
- Ensure `node_modules` is ignored
- Remove tracked large files from index/history

---

## 10) Security rules

Do not commit:
- `.env`
- API keys
- access tokens
- private certificates

Do:
- use GitHub secrets for CI
- use environment variables
- rotate Docker Hub token if leaked

---

## 11) Team commands cheatsheet

```bash
# Sync main
git checkout main && git pull origin main

# New branch
git checkout -b feature/<task>

# Push branch
git push -u origin feature/<task>

# Start local stack
docker compose up --build

# Start from prebuilt images
docker compose -f docker-compose.yml -f docker-compose.images.yml up -d

# View logs
docker compose logs -f backend frontend

# Service status
docker compose ps
```

---

## 12) Ownership and communication

For every task:
- assign owner
- keep PR small
- request at least one review
- document notable decisions in PR description

This keeps delivery fast and avoids regressions.
