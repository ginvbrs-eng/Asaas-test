# Infrastructure (Production Images)

## 1) Configure GitHub
- Push this repository to GitHub.
- In repo settings, allow GitHub Actions to write packages.
- Add repository variable `NEXT_PUBLIC_API_URL` (example: `https://api.yourdomain.com`).

## 2) Images published automatically
Workflow: `.github/workflows/build-and-push-images.yml`
- Builds backend + frontend images.
- Pushes to GHCR with tags: `latest`, branch, tag, and commit SHA.

Images:
- `ghcr.io/<owner>/asaas-backend:<tag>`
- `ghcr.io/<owner>/asaas-frontend:<tag>`

## 3) VPS deploy with fixed images
Use compose override with image tags:

```bash
export LETSENCRYPT_EMAIL=admin@yourdomain.com
export BACKEND_IMAGE=ghcr.io/<owner>/asaas-backend:latest
export FRONTEND_IMAGE=ghcr.io/<owner>/asaas-frontend:latest

docker compose -f docker-compose.yml -f docker-compose.vps.yml pull
docker compose -f docker-compose.yml -f docker-compose.vps.yml up -d
```

## 4) Safer production strategy
Prefer immutable tags (commit SHA or release tag) instead of `latest`:

```bash
export BACKEND_IMAGE=ghcr.io/<owner>/asaas-backend:sha-abc1234
export FRONTEND_IMAGE=ghcr.io/<owner>/asaas-frontend:sha-abc1234
```
