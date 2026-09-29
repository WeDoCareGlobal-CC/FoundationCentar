# FoundationCentar — Multi-stage Dockerfile
# Builds: Python FastAPI (orchestrator + telemetry) + React/Vite frontend + TypeScript backend (AppDeploy SDK)

# =============================================================================
# Stage 1: Build Frontend (React + Vite + TypeScript)
# =============================================================================
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm ci --prefer-offline --no-audit --no-fund 2>/dev/null || npm install --prefer-offline --no-audit --no-fund

# Copy frontend source
COPY frontend/ ./

# Build frontend (outputs to dist/)
RUN npm run build

# =============================================================================
# Stage 2: Build Backend TypeScript (AppDeploy SDK compatible)
# =============================================================================
FROM node:22-alpine AS backend-ts-builder

WORKDIR /app/backend

# Copy backend package files (if any - currently uses @appdeploy/sdk)
COPY backend/package.json backend/package-lock.json* ./ 2>/dev/null || true

# Install TypeScript/backend dependencies if package.json exists
RUN if [ -f package.json ]; then npm ci --prefer-offline --no-audit --no-fund 2>/dev/null || npm install --prefer-offline --no-audit --no-fund; fi

# Copy backend source
COPY backend/ ./

# TypeScript compilation (if tsconfig exists)
RUN if [ -f tsconfig.json ]; then npx tsc --noEmit; fi

# =============================================================================
# Stage 3: Python Runtime (FastAPI + Orchestrator + Telemetry)
# =============================================================================
FROM python:3.11-slim AS python-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy Python source
COPY src/ ./src/
COPY models.yaml ./

# =============================================================================
# Stage 4: Final Production Image
# =============================================================================
FROM python:3.11-slim AS production

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python runtime from stage 3
COPY --from=python-runtime /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=python-runtime /app/src ./src
COPY --from=python-runtime /app/models.yaml ./models.yaml
COPY --from=python-runtime /app/requirements.txt ./requirements.txt

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy backend TypeScript (for AppDeploy SDK runtime if needed)
COPY --from=backend-ts-builder /app/backend ./backend

# Copy config files
COPY config/ ./config/
COPY cron.json ./
COPY .zenodo.json ./
COPY CITATION.cff ./

# Create nginx config for serving frontend + proxying API
RUN mkdir -p /etc/nginx/conf.d
COPY <<'EOF' /etc/nginx/conf.d/default.conf
server {
    listen 8080;
    server_name localhost;
    root /app/frontend/dist;
    index index.html;

    # Frontend SPA routing
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy to Python FastAPI (port 8000)
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }

    # WebSocket proxy for realtime
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 86400;
    }

    # Health checks
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        access_log off;
    }

    # Static assets caching
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Supervisor config to run nginx + Python API
COPY <<'EOF' /etc/supervisor/conf.d/supervisord.conf
[supervisord]
nodaemon=true
user=root
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid

[program:nginx]
command=nginx -g "daemon off;"
stdout_logfile=/var/log/supervisor/nginx.log
stderr_logfile=/var/log/supervisor/nginx_err.log
autorestart=true
priority=10

[program:python-api]
command=python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 2
directory=/app
stdout_logfile=/var/log/supervisor/python_api.log
stderr_logfile=/var/log/supervisor/python_api_err.log
autorestart=true
priority=20
environment=PYTHONPATH=/app,PATH=/usr/local/bin:/usr/bin:/bin
EOF

# Create log directory
RUN mkdir -p /var/log/supervisor

# Expose ports
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
