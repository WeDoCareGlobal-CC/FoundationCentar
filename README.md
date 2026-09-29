# FoundationCentar — One-Click Agent Factory OS

[![CI](https://github.com/we-do-care-global/FoundationCentar/actions/workflows/ci.yml/badge.svg)](https://github.com/we-do-care-global/FoundationCentar/actions/workflows/ci.yml)
[![Release](https://github.com/we-do-care-global/FoundationCentar/actions/workflows/release.yml/badge.svg)](https://github.com/we-do-care-global/FoundationCentar/actions/workflows/release.yml)
[![Validate](https://github.com/we-do-care-global/FoundationCentar/actions/workflows/validate.yml/badge.svg)](https://github.com/we-do-care-global/FoundationCentar/actions/workflows/validate.yml)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&label=Container&color=2496ED)](https://ghcr.io/we-do-care-global/FoundationCentar)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![10-Agent Orchestration](https://img.shields.io/badge/10--Agent%20Orchestration-00C853?logo=robot&logoColor=white)
![76 Skills](https://img.shields.io/badge/76-Skills-8E24AA?logo=code&logoColor=white)

**FoundationCentar** is a production-grade, 24/7 autonomous cloud AI operating platform — a **One-Click Agent Factory** that orchestrates multi-agent workflows with human governance, bounded economics, and evidence-first verification.

> **Merged from**: AtlanTida OS (Python/FastAPI orchestration) + We Do Care Global Agentic Operations OS (React/TypeScript control plane + AppDeploy backend)

---

## System Architecture

### Authority Hierarchy
```
Human CEO → AI Lead → Team Leads (Chiefs) → Workers → Verifier → Outcome → Learning
```

### Core Loops
| Loop | Flow |
|---|---|
| **Economic** | Mission → Budget → Execution → Cost → Evidence → Verification → Revenue/Outcome → Learning |
| **Local AI** | Cloud Control Plane → Mission Package → Local AI Runtime → Worker Execution → Receipt → Verifier → Control Plane |
| **Research/Release** | GitHub commit → GitHub release → Zenodo archive/DOI |

---

## Unified Repository Structure

```
FoundationCentar/
├── src/                          # Python: Orchestrator + FastAPI Telemetry
│   ├── orchestrator.py           # Brain → Chiefs → Workers + AtState state machines
│   ├── skills.py                 # Smart meter diagnostic, half-hourly reconciliation
│   ├── telemetry.py              # 9 FastAPI endpoints (agents, skills, routing, execution)
│   ├── main.py                   # CLI / Server / Daemon entry points
│   └── __init__.py               # Package exports
├── frontend/                     # React + Vite + TypeScript (Control Plane UI)
│   ├── src/App.tsx               # CEO Dashboard: actions, approvals, missions, org, audit, learning
│   ├── src/main.tsx              # Entry point
│   └── dist/                     # Built assets (served by nginx)
├── backend/                      # TypeScript: AppDeploy SDK backend
│   ├── index.ts                  # Control plane API: actions, approvals, OAuth, bridge, sync
│   └── realtime-subscribers.ts   # WebSocket realtime updates
├── config/                       # Configuration
│   └── integrations.example.json # GitHub/ORCID/Zenodo + local AI bridge config
├── docs/                         # Architecture & operations docs
│   ├── ARCHITECTURE.md           # Authority hierarchy, loops, identity
│   ├── ONE_CLICK_FACTORY.md      # Operating loop, task boundary, expansion, emergency
│   └── UNIFIED_IDENTITY.md       # Google → GitHub/ORCID/Zenodo OAuth flow
├── models.yaml                   # Model registry: Chief→model mapping (NVIDIA NIM + vLLM fallbacks)
├── cron.json                     # Scheduled sync (every 6h, Sarajevo TZ)
├── .zenodo.json                  # Zenodo metadata for DOI minting
├── CITATION.cff                  # Citation file format
├── Dockerfile                    # Multi-stage: frontend + backend + Python + nginx + supervisor
├── requirements.txt              # fastapi, uvicorn, pydantic
└── .github/workflows/            # CI: validate, release, docker build/push to GHCR
```

---

## Quickstart

### Local Development (Python API only)
```bash
# Clone
git clone https://github.com/we-do-care-global/FoundationCentar.git
cd FoundationCentar

# Python API (port 8000)
pip install -r requirements.txt
python src/main.py --mode server

# Test endpoints
curl http://localhost:8000/health
# → {"status": "ok", "version": "1.0.0"}

curl http://localhost:8000/api/v1/agents
# → Brain + 9 Chiefs + Workers

curl -X POST http://localhost:8000/api/v1/brain/route \
  -H "Content-Type: application/json" \
  -d '{"action": "diagnose smart meter", "domain": "operations"}'
```

### Full Stack (Docker - Production)
```bash
# Build multi-stage image (frontend + backend + Python + nginx)
docker build -t foundationcentar .

# Run on port 8080 (nginx proxies /api/* to Python :8000)
docker run -p 8080:8080 foundationcentar

# Frontend: http://localhost:8080
# API:      http://localhost:8080/api/...
```

---

## Model Registry (`models.yaml`)

Maps each Chief/Worker role to **primary + fallback** model endpoints (OpenAI-compatible):

| Role | Primary | Fallback |
|---|---|---|
| **Brain** (Global Router) | NVIDIA NIM: `nemotron-3-ultra-550b` | NIM: `nemotron-3-super-120b` → vLLM: `Qwen3-235B-A22B` |
| **Chief Operations** | vLLM: `Qwen-AgentWorld-35B-A3B` | vLLM: `Qwen3-30B` → NIM: `nemotron-70b` |
| **Chief DevOps** | vLLM: `Qwen3-Coder-32B` | vLLM: `Qwen2.5-Coder-32B` → NIM: `codestral-22b` |
| **Chief Research** | vLLM: `Qwen3-30B-A3B-Thinking` | NIM: `nemotron-3-ultra` → NIM: `nemotron-3-super` |
| **Chief Finance/Legal** | NIM: `llama-3.1-405b` | NIM: `nemotron-70b` → vLLM: `Qwen3-32B` |
| **Chief Marketing/Sales** | vLLM: `Qwen3-32B` | NIM: `mistral-large-2` |
| **Workers (default)** | vLLM: `Qwen3-14B` | vLLM: `Mixtral-8x22B` → NIM: `mixtral-8x22b` |

> **vLLM ports**: 8001–8013 (see `models.yaml:vllm_ports`) — deploy via `docker-compose.yml` (add separately)

---

## CEO Control Plane (Frontend)

The React dashboard (`frontend/src/App.tsx`) provides:

| Tab | Purpose |
|---|---|
| **Dashboard** | KPI metrics (verified revenue, tracked cost, profit, bound budgets), running missions, org chart, governance |
| **Missions** | List all missions with status, cost/budget, verification |
| **Org Chart** | Human CEO → AI Lead → 4 Department Leads → Workers |
| **Timeline** | Workflow execution timeline |
| **Learning** | Optimization versions, scores, optimization notes |
| **Audit** | Append-only ledger: actions, decisions, costs, outcomes |

### CEO Actions (One-Click)
- **Start Research** — Regulatory & Knowledge mission
- **Start Workflow** — Product & Engineering mission
- **Execute Mission** — Operations & Finance mission
- **Approve / Reject** — Governance decisions on proposals
- **Pause / Resume** — Execution control
- **Expand Team** — Capability-gap → Agent Spec → sandbox → promotion
- **Learn & Optimize** — Rebalance routing, verifier thresholds
- **Retire Agent** — Safe decommissioning after reassignment
- **Emergency Stop** — Halt all execution, preserve state

---

## Backend API (AppDeploy SDK)

TypeScript backend (`backend/index.ts`) exposes:

| Endpoint | Auth | Purpose |
|---|---|---|
| `GET /api/control-plane` | ✓ | Full state: missions, approvals, audit, learning, agents |
| `GET /api/integrations` | ✓ | GitHub/ORCID/Zenodo connection status |
| `POST /api/integrations/:provider/start` | ✓ | OAuth flow start (GitHub/ORCID/Zenodo) |
| `GET /api/oauth/:provider/callback` | — | OAuth callback, encrypts & stores tokens |
| `DELETE /api/integrations/:provider` | ✓ | Disconnect provider |
| `POST /api/actions` | ✓ | CEO actions (research/workflow/execute/expand/retire/learn/stop/pause/resume) |
| `POST /api/approvals/decision` | ✓ | Approve/reject pending proposals |
| `GET /api/bridge/config` | — | Local AI bridge protocol spec |
| `POST /api/bridge/receipt` | ✓ | Receive worker receipt from local runtime |
| `GET /api/sync/status` | ✓ | GitHub/Zenodo/ORCID sync status |
| `POST /api/sync/run` | ✓ | Trigger unified account sync |
| `WS /api/realtime/subscribe` | — | Realtime entity updates |

---

## Unified Identity

- **Google** = Primary AppDeploy identity (CEO)
- **GitHub/ORCID/Zenodo** = OAuth connections linked to same AppDeploy user ID
- **Secrets required**: `APP_ENCRYPTION_KEY`, `GITHUB_CLIENT_ID/SECRET`, `ORCID_CLIENT_ID/SECRET`, `ZENODO_CLIENT_ID/SECRET`
- **Tokens** encrypted server-side (AES-256-GCM) before persistence; browser sees only connection status

---

## Deployment

| Target | Command |
|---|---|
| **Docker (local)** | `docker build -t foundationcentar . && docker run -p 8080:8080 foundationcentar` |
| **GHCR** | `ghcr.io/we-do-care-global/FoundationCentar` (auto on push to `main`) |
| **Fly.io / Cloud** | Requires Cloudflare API token + secrets |

### CI/CD (`.github/workflows/`)
- `validate.yml` — Lint, typecheck, test on PR
- `release.yml` — Version bump, tag, Docker build/push on release
- `ci.yml` — Docker build/push to GHCR on `main` push

---

## License

Apache-2.0 — see [LICENSE](LICENSE) / [LICENSE-OS](LICENSE-OS) for details.

---

## Citation

If you use this software, please cite the repository and its Zenodo release:

```bibtex
@software{we_do_care_global_foundationcentar,
  title = {We Do Care Global — Agentic Operations OS},
  author = {We Do Care Global},
  url = {https://github.com/we-do-care-global/FoundationCentar},
  license = {Apache-2.0}
}
```

DOI: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX) (minted on release)
