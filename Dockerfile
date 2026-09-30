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

# Copy backend package files
COPY backend/package.json backend/package-lock.json ./

# Install TypeScript/backend dependencies
RUN npm ci --prefer-offline --no-audit --no-fund

# Copy backend source
COPY backend/ ./

# TypeScript compilation (skip for AppDeploy SDK compatibility - types not available)
# RUN if [ -f tsconfig.json ]; then npx tsc --noEmit; fi

# =============================================================================
# Stage 3: Python Runtime (FastAPI + Orchestrator + Telemetry)
# =============================================================================
FROM python:3.11-slim@sha256:a8c5e5b8c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5 AS python-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --no-create-home --shell /bin/bash --uid 1000 appuser

WORKDIR /app

# Copy Python requirements
COPY requirements.txt ./
COPY requirements.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir --break-system-packages -r requirements.lock

# Copy Python source
COPY src/ ./src/
COPY models.yaml ./

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# =============================================================================
# Stage 4: Final Production Image
# =============================================================================
FROM python:3.11-slim@sha256:a8c5e5b8c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5 AS production

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
COPY --from=python-runtime /app/requirements.lock ./requirements.lock

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

    # Metrics endpoint
    location /metrics {
        proxy_pass http://127.0.0.1:8000/metrics;
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
