# Deployment Guide

> From localhost to production in under an hour.

This guide covers the recommended deployment pattern: **Netlify for frontend + backend** using serverless functions. This is the same pattern we use for all production agents.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [Option 1: Netlify (Recommended)](#option-1-netlify-recommended)
4. [Option 2: Docker Self-Hosted](#option-2-docker-self-hosted)
5. [Option 3: Railway](#option-3-railway)
6. [Option 4: Vercel](#option-4-vercel-coming-soon)
7. [Production Checklist](#production-checklist)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with your fork of this repo
- [ ] Anthropic API key ([get one here](https://console.anthropic.com/))
- [ ] Node.js 18+ installed locally
- [ ] Python 3.11+ installed locally

**Estimated time:** 30-45 minutes for first deployment

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Your Users                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Netlify Edge                            │
│  ┌─────────────────────┐    ┌────────────────────────────┐ │
│  │   Static Frontend   │    │   Serverless Functions     │ │
│  │   (React + Vite)    │    │   (FastAPI via Mangum)     │ │
│  │                     │    │                            │ │
│  │   /                 │◄──►│   /api/*                   │ │
│  │   /assets/*         │    │   /.netlify/functions/*    │ │
│  └─────────────────────┘    └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Anthropic API                           │
│                   (Claude models)                           │
└─────────────────────────────────────────────────────────────┘
```

**Why this architecture:**
- **Fast**: Frontend served from CDN edge locations
- **Cheap**: Pay only for function invocations
- **Scalable**: Automatic scaling, no server management
- **Simple**: One platform for frontend + backend

---

## Option 1: Netlify (Recommended)

This is our production deployment pattern. Netlify handles everything.

### Step 1: Fork the Repository

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/jai-agent-accelerator.git
cd jai-agent-accelerator
```

### Step 2: Install Netlify CLI

```bash
npm install -g netlify-cli
netlify login
```

### Step 3: Create netlify.toml

Create `netlify.toml` in the project root:

```toml
[build]
  # Build the frontend
  command = "cd apps/web && npm install && npm run build"
  publish = "apps/web/dist"

[build.environment]
  # Node version for build
  NODE_VERSION = "18"
  # Python version for functions
  PYTHON_VERSION = "3.11"

[functions]
  # Python functions directory
  directory = "apps/agent/netlify/functions"

  # Bundle with included files
  included_files = ["apps/agent/src/**"]

# API routes proxy to functions
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/agent/:splat"
  status = 200

# SPA fallback
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Step 4: Create the Netlify Function

Create the function wrapper at `apps/agent/netlify/functions/agent.py`:

```python
"""
Netlify serverless function wrapper for the PMM Agent.

This wraps our FastAPI app with Mangum for AWS Lambda compatibility
(which Netlify Functions use under the hood).
"""
import sys
from pathlib import Path

# Add the agent source to Python path
agent_src = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(agent_src))

from mangum import Mangum
from pmm_agent.server import app

# Create the handler that Netlify will invoke
handler = Mangum(app, lifespan="off")
```

Create the requirements file at `apps/agent/netlify/functions/requirements.txt`:

```
mangum>=0.17.0
anthropic>=0.18.0
langchain>=0.1.0
langchain-anthropic>=0.1.0
langgraph>=0.0.20
fastapi>=0.109.0
pydantic>=2.0.0
httpx>=0.26.0
```

### Step 5: Update Frontend Environment

Create `apps/web/.env.production`:

```bash
VITE_API_URL=
# Leave empty - relative URLs work with Netlify redirects
```

### Step 6: Initialize and Deploy

```bash
# Initialize Netlify project
netlify init

# When prompted:
# - Create & configure a new site
# - Choose your team
# - Set site name (e.g., my-pmm-agent)

# Set environment variables
netlify env:set ANTHROPIC_API_KEY sk-ant-your-key-here

# Deploy to production
netlify deploy --prod
```

### Step 7: Verify Deployment

```bash
# Check health endpoint
curl https://your-site.netlify.app/api/health

# Expected response:
# {"status": "ok", "agent": "jai-agent-accelerator", "version": "1.0.0"}
```

Open `https://your-site.netlify.app` — your agent is live!

### Netlify Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `MODEL` | No | Model to use (default: `claude-sonnet-4-20250514`) |
| `MAX_TOKENS` | No | Max response tokens (default: `8192`) |
| `LOG_LEVEL` | No | Logging level (default: `INFO`) |

### Automatic Deployments

Once connected to GitHub, Netlify automatically deploys:
- **Production**: On push to `main` branch
- **Preview**: On pull requests

No additional configuration needed.

---

## Option 2: Docker Self-Hosted

For teams that need to self-host or have specific infrastructure requirements.

### Step 1: Build and Run

```bash
# From project root
docker-compose up --build

# Or build individually
docker build -t pmm-agent-backend ./apps/agent
docker build -t pmm-agent-frontend ./apps/web

# Run with environment variables
docker run -p 8123:8123 \
  -e ANTHROPIC_API_KEY=sk-ant-your-key \
  pmm-agent-backend

docker run -p 3003:3003 \
  -e VITE_API_URL=http://localhost:8123 \
  pmm-agent-frontend
```

### Step 2: Docker Compose Configuration

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./apps/agent
    ports:
      - "8123:8123"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - MODEL=claude-sonnet-4-20250514
      - LOG_LEVEL=INFO
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8123/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./apps/web
    ports:
      - "3003:3003"
    environment:
      - VITE_API_URL=http://backend:8123
    depends_on:
      - backend

  # Optional: nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
      - frontend
```

### Step 3: Production Docker Tips

**Use multi-stage builds** for smaller images:

```dockerfile
# apps/agent/Dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir build && python -m build

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/dist/*.whl .
RUN pip install --no-cache-dir *.whl
COPY src/ ./src/
CMD ["uvicorn", "pmm_agent.server:app", "--host", "0.0.0.0", "--port", "8123"]
```

**Set resource limits** in docker-compose:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

---

## Option 3: Railway

Railway offers simple deployment with automatic HTTPS and scaling.

### Step 1: Install Railway CLI

```bash
npm i -g @railway/cli
railway login
```

### Step 2: Create Railway Project

```bash
cd apps/agent
railway init

# When prompted:
# - Create new project
# - Name: pmm-agent-backend
```

### Step 3: Configure Railway

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn pmm_agent.server:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 30
  }
}
```

### Step 4: Deploy

```bash
# Set environment variables
railway variables set ANTHROPIC_API_KEY=sk-ant-your-key

# Deploy
railway up

# Get your URL
railway domain
```

### Step 5: Deploy Frontend

```bash
cd apps/web
railway init  # New project for frontend

# Set API URL
railway variables set VITE_API_URL=https://your-backend.railway.app

railway up
```

---

## Option 4: Vercel (Coming Soon)

Vercel deployment documentation is in development. The pattern will be:

- **Frontend**: Zero-config Vite deployment
- **Backend**: Vercel Serverless Functions (Python runtime)

Check back for updates or join the Discord for early access.

---

## Production Checklist

### Security

- [ ] **API Key Security**: Never commit keys to git
- [ ] **CORS Configuration**: Restrict to your domains only
- [ ] **Rate Limiting**: Implement request limits
- [ ] **Input Validation**: Validate all user inputs
- [ ] **HTTPS Only**: Enforce TLS everywhere

### Performance

- [ ] **Response Caching**: Cache common queries
- [ ] **Conversation Truncation**: Limit history length
- [ ] **Model Selection**: Use Haiku for simple tasks
- [ ] **Cold Start Optimization**: Keep functions warm

### Monitoring

- [ ] **Health Checks**: Automated uptime monitoring
- [ ] **Error Tracking**: Sentry or similar
- [ ] **Usage Metrics**: Track tokens and costs
- [ ] **Alerting**: Set up cost and error alerts

### Cost Control

- [ ] **Budget Alerts**: Set spending limits
- [ ] **Usage Dashboards**: Monitor token consumption
- [ ] **Prompt Optimization**: Minimize input tokens
- [ ] **Caching Strategy**: Reduce duplicate calls

---

## Environment Variables Reference

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | `sk-ant-...` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `MAX_TOKENS` | Maximum response tokens | `8192` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` |
| `API_KEY` | Internal API key for auth | None |

### Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://api.example.com` |

---

## Troubleshooting

### "Function timeout"

**Symptom**: Requests fail after 10 seconds on Netlify

**Solution**: Netlify has a 10-second function timeout on free tier. Upgrade to Pro for 26 seconds, or implement streaming responses.

### "Module not found"

**Symptom**: Python imports fail in serverless function

**Solution**: Ensure `included_files` in `netlify.toml` includes your source:

```toml
[functions]
  included_files = ["apps/agent/src/**"]
```

### "CORS error"

**Symptom**: Frontend can't reach backend

**Solution**: Check `ALLOWED_ORIGINS` environment variable and ensure your frontend domain is included.

### "Cold start latency"

**Symptom**: First request takes 5+ seconds

**Solution**: This is normal for serverless. Options:
1. Implement a "keep warm" scheduled function
2. Upgrade to provisioned concurrency (AWS)
3. Use a long-running server (Railway, Fly.io)

### "Out of memory"

**Symptom**: Function crashes with memory error

**Solution**: Increase memory allocation. On Netlify:

```toml
[functions]
  [functions.agent]
    memory = 1024  # MB
```

---

## Getting Help

- **Discord**: Join our community for real-time help
- **GitHub Issues**: Report bugs and request features
- **Office Hours**: Pro/Team tiers get direct access

---

## Next Steps

After deployment:

1. **Monitor costs**: Check Anthropic dashboard daily for first week
2. **Set up alerts**: Configure budget notifications
3. **Collect feedback**: Add a feedback mechanism
4. **Iterate**: Use the [Methodology](METHODOLOGY.md) to improve your agent

---

Built with [LangChain](https://langchain.com) • Deployed with [Netlify](https://netlify.com)
