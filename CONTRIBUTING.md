# Contributing to Atlantida OS

Thank you for your interest in contributing. This guide covers how to work with the 10-agent topology, add new skills, run the Three.js PWA locally, and understand skill synthesis from execution traces.

## Architecture Overview

Atlantida OS uses a hierarchical 10-agent collective:

```
Brain Agent (Global Router) -> Chief Agents (Domain Leads) -> Worker Agents (Skill Executors) -> Deterministic State Machines -> Skill Synthesis & Execution Traces
```

- **Brain Agent**: Routes requests to the right chief based on domain
- **Chief Agents**: 9 domain leads (Marketing, Finance, Operations, HR, Legal, Sales, Product, DevOps, Research)
- **Worker Agents**: Execute specific skills within a domain
- **Deterministic State Machines**: Encode workflows as reproducible state transitions
- **Skill Synthesis Engine**: Generates reusable skills (currently 76) from execution traces

## Adding a New Skill

Skills are organized into 9 domains. To add a new skill:

1. **Identify the domain** - Which of the 9 domains does this belong to? (ai-models, operations, marketing, hr, legal, sales, product, devops, research)
2. **Create the skill definition** - Add the skill to `src/skills/<domain>/<skill_name>.py` with:
   - Input parameters (required vs optional)
   - Execution logic
   - Output schema
3. **Register the skill** - Add it to the domain's skill registry in `src/skills/<domain>/__init__.py`
4. **Test locally** - Run the skill via the CLI or API to verify it works
5. **Submit execution traces** - Run the skill through real workflows so the synthesis engine can capture trace data

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

## Running the Three.js PWA Locally

The 3D Neural Command Center is a Three.js-based PWA for visualizing multi-agent DAGs.

### Prerequisites
- Node.js 18+ / npm 9+
- Git

### Setup
```bash
# Clone the repo
git clone https://github.com/emirperla96-lab/atlantida-os.git
cd atlantida-os

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The PWA will be available at `http://localhost:3000`. It connects to the backend API for real-time agent state visualization.

### Building for Production
```bash
npm run build
```

The built PWA is served as a Progressive Web App with offline support.

## Skill Synthesis from Execution Traces

The system automatically synthesizes skills from execution traces:

1. **Trace Collection**: Every executed workflow generates a trace (timestamp, agent chain, inputs, outputs, state transitions)
2. **Pattern Recognition**: The synthesis engine analyzes traces to find recurring patterns across domains
3. **Skill Generation**: Recurring patterns are converted into reusable parameterized skills
4. **Registration**: New skills are registered into the appropriate domain's skill registry

### How to Trigger Synthesis
- Run workflows through the Brain Agent API (`POST /api/v1/brain/route`)
- Traces are stored in the SQLite database (`/data/traces.db`)
- The synthesis engine runs periodically or can be triggered manually

## CLI Tools

The system exposes CLI tools for local development:

```bash
# List all available skills
python src/cli.py list-skills

# Execute a specific skill
python src/cli.py run-skill <domain>/<skill_name> --params '{"key": "value"}'

# View execution traces
python src/cli.py traces --domain marketing --limit 10

# Synthesize skills from recent traces
python src/cli.py synthesize --domain all --since 7d
```

## Pull Request Process

1. Fork the repo and create your branch from `main`
2. Add your skill, fix, or feature with tests
3. Ensure the CLI works (`python src/cli.py list-skills` shows your new skill)
4. Submit a PR with a clear description of what domain/agents it touches
5. The maintainers will review and merge

## Code of Conduct

Please be respectful and constructive. This project is maintained by a small team - clear, specific PRs get faster reviews.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
