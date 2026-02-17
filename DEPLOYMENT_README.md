# ASAAS Deployment Guide (VPS / Cloud) - Step by Step

This guide explains exactly how to deploy ASAAS on a VPS or cloud VM using Docker Compose, Traefik, Let's Encrypt, and prebuilt Docker Hub images.

## 1) Prerequisites

Before deployment, make sure you have:
- A VPS/cloud server (Ubuntu 22.04+ recommended)
- A domain name (or subdomains) pointing to your server IP
- Docker and Docker Compose installed on the server
- Access to Docker Hub images:
  - `ginvbrs/asaas-backend`
  - `ginvbrs/asaas-frontend`

Recommended minimum server size:
- 2 vCPU
- 4 GB RAM
- 40+ GB disk

## 2) Domain DNS setup

Create these DNS A records to your VPS public IP:
- `app.yourdomain.com`
- `api.yourdomain.com`
- `minio.yourdomain.com`

Wait until DNS is propagated.

## 2.1) DNS setup for Hostinger + Google Cloud (recommended path)

If your VPS is on Google Cloud and your domain DNS is managed in Hostinger:

1. In Google Cloud Console (`Compute Engine -> VM instances`), copy your VM **External IP**.
2. In Hostinger hPanel (`Domains -> your domain -> DNS Zone`), create these `A` records:
   - `app` -> `<GCP_EXTERNAL_IP>`
   - `api` -> `<GCP_EXTERNAL_IP>`
   - `minio` -> `<GCP_EXTERNAL_IP>`
3. TTL: keep default (or `300`).
4. Save and wait for propagation.

Validate DNS:

```bash
nslookup app.yourdomain.com
nslookup api.yourdomain.com
nslookup minio.yourdomain.com
```

All three should resolve to the same Google Cloud VM external IP.

## 2.2) Cloudflare alternative (optional)

Use this only if your domain nameservers are pointed to Cloudflare.

1. In Cloudflare `DNS`, create the same three `A` records:
   - `app` -> `<VPS_PUBLIC_IP>`
   - `api` -> `<VPS_PUBLIC_IP>`
   - `minio` -> `<VPS_PUBLIC_IP>`
2. Initially set records to **DNS only** (not proxied) while issuing Let's Encrypt certificates.
3. After certificates are working, you can enable proxy mode if needed.

Important:
- Do not manage the same DNS records in both Hostinger and Cloudflare at the same time.
- Use one active DNS provider only (the one your nameservers currently point to).

## 3) Server initial setup

SSH into your server:

```bash
ssh root@<SERVER_IP>
```

Install Docker + Compose (Ubuntu):

```bash
apt update
apt install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
systemctl enable docker
systemctl start docker
```

## 4) Get project files on server

```bash
mkdir -p /opt/asaas
cd /opt/asaas
git clone https://github.com/ginvbrs-eng/Asaas.git .
```

## 5) Create production environment file

Use the template:

```bash
cp .env.vps.example .env.vps
```

Edit values:

```bash
nano .env.vps
```

Set:

```env
WEB_DOMAIN=app.yourdomain.com
API_DOMAIN=api.yourdomain.com
MINIO_DOMAIN=minio.yourdomain.com
LETSENCRYPT_EMAIL=admin@yourdomain.com
BACKEND_IMAGE=ginvbrs/asaas-backend:latest
FRONTEND_IMAGE=ginvbrs/asaas-frontend:latest
```

## 6) Prepare Let's Encrypt storage

```bash
mkdir -p letsencrypt
touch letsencrypt/acme.json
chmod 600 letsencrypt/acme.json
```

## 7) Optional: Docker Hub login (only if images are private)

```bash
docker login -u <dockerhub_user>
```

## 8) Pull and start production stack

```bash
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps pull
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps up -d
```

## 9) Validate deployment

Check running services:

```bash
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps ps
```

Check logs:

```bash
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps logs -f traefik backend frontend minio
```

Open URLs:
- `https://app.yourdomain.com`
- `https://api.yourdomain.com/health`
- `https://minio.yourdomain.com`

## 10) Update to latest images (routine)

When new images are pushed by CI:

```bash
cd /opt/asaas
git pull origin main
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps pull
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps up -d
```

## 11) Rollback strategy (recommended)

Use immutable tags (SHA/version) instead of only `latest`.

Example rollback:
1. Edit `.env.vps`:

```env
BACKEND_IMAGE=ginvbrs/asaas-backend:sha-abc1234
FRONTEND_IMAGE=ginvbrs/asaas-frontend:sha-abc1234
```

2. Restart with pinned tags:

```bash
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps pull
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps up -d
```

## 12) Security hardening checklist

- Replace default secrets in compose/env files
- Use strong MinIO credentials (do not keep defaults in production)
- Use SSH keys (disable password login)
- Enable firewall (`ufw`) and allow only required ports (22, 80, 443)
- Keep server packages and Docker updated
- Use branch protections on GitHub main branch

## 13) Common issues and quick fixes

### A) TLS cert not issued
- Ensure DNS records are correct and propagated
- Ensure ports 80/443 are open
- Check traefik logs

### B) API not reachable
- Check backend container is `Up`
- Check traefik router labels and domain names in `.env.vps`

### C) `pull access denied`
- Docker Hub image name/tag is wrong, or not logged in for private images

### D) Empty response from domain
- Check `docker compose ... ps`
- Check traefik logs
- Ensure domain points to correct server IP

---

## 14) One-command deploy script (optional)

You can create a small helper script:

```bash
cat > deploy.sh <<'SH'
#!/usr/bin/env bash
set -e

docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps pull
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps up -d
docker compose -f docker-compose.yml -f docker-compose.vps.yml --env-file .env.vps ps
SH

chmod +x deploy.sh
./deploy.sh
```

