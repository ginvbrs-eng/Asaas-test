# ASAAS Platform - Setup, Troubleshooting, and CI/CD Runbook

This document is the full project tutorial: how the project was created, how to run it, issues we hit, how we fixed them, and how image publishing works with GitHub Actions and Docker Hub.

## 1) Project structure

```text
Asaas/
- backend/
- frontend/
- mobile/
- infrastructure/
- docker-compose.yml
- docker-compose.vps.yml
- docker-compose.images.yml
- .github/workflows/build-and-push-images.yml
```

## 2) Local development startup

### Start all services

```bash
docker compose up --build
```

### Main local URLs

- Frontend: `http://localhost`
- API health: `http://api.localhost/health`
- MinIO console: `http://minio.localhost`
- Traefik dashboard: `http://localhost:8081/dashboard/`
- Elasticsearch endpoint (internal Docker network): `http://elasticsearch:9200`

## 2.1) MinIO account reference

Use this as your quick reference for local/dev access:

- Console URL: `http://minio.localhost`
- Username: `asaas`
- Password: `asaas123456`
- API endpoint (internal Docker network): `minio:9000`

Security note:
- These are development defaults from `docker-compose.yml`.
- For production, replace them with strong credentials and store them in environment variables/secrets.

## 3) Major issues we faced and the fixes

### Issue A: `tls: bad record MAC` while pulling Docker images

Symptoms:
- Docker image pulls failed randomly (`postgres`, `redis`, `traefik`, `minio`).

Fix applied:
1. Kept only required active network adapter.
2. Disabled offload on active Wi-Fi adapter.
3. Restarted WSL and Docker service.

Windows PowerShell (Admin):

```powershell
Disable-NetAdapter -Name "Ethernet 4" -Confirm:$false
Disable-NetAdapterLso -Name "Wi-Fi 3"
Disable-NetAdapterChecksumOffload -Name "Wi-Fi 3"
wsl --shutdown
Restart-Service com.docker.service
```

### Issue B: Port conflict on `8080`

Error:
- `bind: Only one usage of each socket address...`

Fix applied:
- Changed Traefik dashboard mapping from `8080:8080` to `8081:8080`.

### Issue C: Frontend build failed at `npm ci` (network instability)

Fix applied:
- Added npm retry/timeouts in `frontend/Dockerfile`.
- Added `frontend/.dockerignore` to reduce Docker context size.

### Issue D: Frontend build error `No QueryClient set`

Fix applied:
- Added global React Query provider.
- Files:
  - `frontend/components/providers/QueryProvider.tsx`
  - `frontend/app/layout.tsx`

### Issue E: MinIO startup failure `decodeXLHeaders: Unknown xl meta version 3`

Cause:
- Existing MinIO volume data was incompatible with pinned older image.

Fix applied:
- Switched MinIO image back to a compatible image for existing volume data.

### Issue F: GitHub push rejected because file > 100MB

Error:
- `frontend/node_modules/@next/swc-win32-x64-msvc/next-swc.win32-x64-msvc.node is 129.57 MB`

Fix applied:

```bash
git rm -r --cached frontend/node_modules
git add .gitignore
git commit --amend --no-edit
git push -u origin main --force-with-lease
```

### Issue G: Git identity missing

Fix applied:

```bash
git config user.name "ginvbrs-eng"
git config user.email "ginvbrs-eng@users.noreply.github.com"
```

### Issue H: GitHub Actions validation error (`secrets` in matrix)

Cause:
- `secrets.*` cannot be used inside `strategy.matrix` expressions.

Fix applied:
- Kept matrix static (`service/context/dockerfile`).
- Used `secrets` only in steps.

### Issue I: GitHub Actions login error (`Username and password required`)

Cause:
- Missing repository secrets for Docker Hub.

Fix applied:
- Added required GitHub repository secrets:
  - `DOCKERHUB_USERNAME`
  - `DOCKERHUB_TOKEN`

### Issue J: Add Elasticsearch service for search

Requirement:
- Add Elasticsearch container for search features and make it available to backend.

Fix applied:
- Added `elasticsearch` service in `docker-compose.yml`.
- Added persistent volume `elasticsearch_data`.
- Added backend env `ELASTICSEARCH_URL=http://elasticsearch:9200`.
- Added backend dependency on Elasticsearch health check.

## 4) GitHub Actions - current behavior

Workflow file:
- `.github/workflows/build-and-push-images.yml`

Current trigger mode:
- Manual only via `workflow_dispatch`.
- Automatic `push` trigger is kept commented for later use.

Current image targets:
- `docker.io/<DOCKERHUB_USERNAME>/asaas-backend`
- `docker.io/<DOCKERHUB_USERNAME>/asaas-frontend`

Current tags:
- `latest`
- `sha-<short>`

## 5) Docker Hub token (secret key) and GitHub secrets setup

This is how we generated and connected the Docker secret key/token.

### Step 1: Create Docker Hub repositories

In Docker Hub website, create:
- `asaas-backend`
- `asaas-frontend`

### Step 2: Generate Docker Hub Access Token

In Docker Hub:
1. Go to `Account Settings`.
2. Open `Security`.
3. Click `New Access Token`.
4. Give it a name (example: `github-actions-asaas`).
5. Copy the token value immediately (it is shown once).

Important:
- This token is the secret key used by CI.
- Do not use your account password in CI.

### Step 3: Add secrets in GitHub repository

In GitHub repo:
1. `Settings` -> `Secrets and variables` -> `Actions`.
2. Add repository secret:
   - Name: `DOCKERHUB_USERNAME`
   - Value: your Docker Hub username (example: `ginvbrs`)
3. Add repository secret:
   - Name: `DOCKERHUB_TOKEN`
   - Value: the access token created in Step 2

### Step 4: Run workflow manually

1. Push workflow file to `main`.
2. Open `Actions` tab.
3. Select `Build and Push Images`.
4. Click `Run workflow`.

## 6) Team usage with prebuilt images

We prepared `docker-compose.images.yml` so team members can run images directly.

```yaml
services:
  backend:
    image: ginvbrs/asaas-backend:latest
    build: null
    volumes: []

  frontend:
    image: ginvbrs/asaas-frontend:latest
    build: null
```

Team commands:

```bash
docker compose -f docker-compose.yml -f docker-compose.images.yml pull
docker compose -f docker-compose.yml -f docker-compose.images.yml up -d
```

If images are private:

```bash
docker login -u <dockerhub_user>
```

## 7) Team Git workflow

### First day setup

```bash
git clone https://github.com/ginvbrs-eng/Asaas.git
cd Asaas
git config user.name "Member Name"
git config user.email "member@email.com"
```

### For each task

```bash
git checkout main
git pull origin main
git checkout -b feature/<task-name>
# make changes
git add .
git commit -m "feat: ..."
git push -u origin feature/<task-name>
```

Then open a Pull Request into `main`.

## 8) Re-enable automatic workflow later

In `.github/workflows/build-and-push-images.yml`, uncomment this block:

```yaml
push:
  branches:
    - main
  tags:
    - "v*"
```

Keep `workflow_dispatch` if you want both manual and automatic modes.

## 9) Useful commands

```bash
# compose status
docker compose ps

# follow logs
docker compose logs -f backend frontend traefik minio

# rebuild one service
docker compose build frontend

# git remotes
git remote -v

# current branch with tracking
git branch -vv
```

---

Quick recovery checklist when something fails:
1. `docker compose ps`
2. `docker compose logs`
3. `git status`
4. GitHub Actions logs
