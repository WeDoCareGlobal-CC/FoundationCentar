# Contributing to FoundationCentar

Thank you for your interest in contributing to FoundationCentar — the One-Click Agent Factory OS for autonomous multi-agent orchestration with CEO governance, bounded economics, evidence-first verification, and unified identity.

## Architecture Overview

FoundationCentar merges three systems:
- **AtlanTida OS** — Python/FastAPI orchestration layer
- **We Do Care Global Agentic Operations OS** — React/TypeScript control plane + AppDeploy backend
- **Daily Base AI Startup Factory** — Revenue/profit engine, worker campaigns, monetization

The system uses a hierarchical 10-agent topology:
```
Brain Agent (Global Router) → Chief Agents (Domain Leads) → Worker Agents (Skill Executors)
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 22+ / pnpm 11+
- Docker (for containerized deployment)

### Local Development

**Python API:**
```bash
cd FoundationCentar
pip install -r requirements.lock
python src/main.py --mode server
# API available at http://localhost:8000
```

**Frontend (React + Vite):**
```bash
cd frontend
npm install
npm run dev
# Frontend at http://localhost:5173
```

**Backend TypeScript (AppDeploy SDK):**
```bash
cd backend
npm install
npx tsc --noEmit  # Type check
```

**Full stack via Docker:**
```bash
docker build -t foundationcentar .
docker run -p 8080:8080 foundationcentar
# Full app at http://localhost:8080
```

## Adding a New Skill

Skills are organized into 9 domains. To add a new skill:

1. **Identify the domain** — Which of the 9 domains does this belong to? (ai-models, operations, marketing, hr, legal, sales, product, devops, research)

2. **Create the skill definition** — Add the skill to `src/skills/<domain>/<skill_name>.py` with:
   - Input parameters (required vs optional)
   - Execution logic
   - Output schema

3. **Register the skill** — Add it to the domain's skill registry in `src/skills/<domain>/__init__.py`

4. **Test locally** — Run the skill via the CLI or API to verify it works:
   ```bash
   python src/cli.py run-skill <domain>/<skill_name> --params '{"key": "value"}'
   ```

5. **Submit execution traces** — Run the skill through real workflows so the synthesis engine can capture trace data

### Skill Structure

```python
# src/skills/<domain>/<skill_name>.py
from src.engine import AgentEngine

class MyNewSkill:
    """One-line description of what this skill does."""

    def __init__(self, engine: AgentEngine):
        self.engine = engine

    def execute(self, param1: str, param2: int = None) -> dict:
        """Execute the skill and return structured output."""
        # Your logic here
        return {"status": "ok", "result": ...}
```

## Running Tests

```bash
# Python tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Frontend tests
cd frontend && npm run test

# All tests (via CI)
# Runs automatically on push/PR
```

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. Add your skill, fix, or feature **with tests**
3. Ensure all checks pass:
   - `ruff check src/` (Python linting)
   - `mypy src/ --ignore-missing-imports` (type checking)
   - `pytest tests/ --cov=src --cov-fail-under=80` (tests with ≥80% coverage)
   - Frontend: `npm run lint && npm run typecheck && npm run build`
   - Backend: `npx tsc --noEmit`
4. Update `CHANGELOG.md` under `[Unreleased]` with your changes
5. Submit a PR with a clear description of what domain/agents it touches
6. The maintainers will review and merge

## Code Style

- **Python**: Ruff (line length 100, py311 target) — config in `pyproject.toml`
- **TypeScript**: ESLint + Prettier — configs in `frontend/` and `backend/`
- **Conventional Commits**: Use `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:` prefixes

## Security

- Report security issues privately to `emirperla96@gmail.com`
- All dependencies are scanned in CI (bandit, safety, npm audit)
- Docker images run as non-root user (UID 1000)
- Base images are pinned by digest

## License

This project is licensed under the Apache-2.0 License. See `LICENSE` for details.

By contributing, you agree that your contributions will be licensed under the same license.