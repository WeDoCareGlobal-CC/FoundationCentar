"""AtlanTida OS - Telemetry API (FastAPI)."""

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Prometheus metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])
SKILL_EXECUTIONS = Counter("skill_executions_total", "Total skill executions", ["skill", "status"])
SKILL_DURATION = Histogram("skill_execution_duration_seconds", "Skill execution duration", ["skill"])

app = FastAPI(
    title="AtlanTida OS Telemetry",
    description="Real-time agent health monitoring and skill execution tracking",
    version="1.0.0",
)


class SkillRequest(BaseModel):
    prompt: str
    domain: str = "general"


class ChiefInput(BaseModel):
    action: str
    domain: str = "general"
    params: dict[str, Any] | None = None


class NewAgent(BaseModel):
    id: str
    name: str
    description: str
    domain: str = "general"
    role: str = "worker"


class CreateSkillRequest(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any] | None = None


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
async def root():
    return {"message": "AtlanTida OS API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/v1/agents")
async def list_agents():
    """List all registered agents (Brain + Chiefs + Workers)."""
    from orchestrator import brain
    agents = {"brain": {"name": "Brain", "role": "global_router"}}
    for domain, chief in brain.chiefs.items():
        agents[domain] = {
            "name": chief.name,
            "role": chief.domain,
            "workers": [w.name for w in chief.workers],
        }
    return agents


@app.get("/api/v1/skills")
async def list_skills():
    """List all available skills."""
    from skills import skill_diagnose_smart_meter, skill_reconcile_half_hourly_tariff
    return {
        "smart_meter_diagnostic": skill_diagnose_smart_meter.__doc__,
        "half_hourly_reconciliation": skill_reconcile_half_hourly_tariff.__doc__,
    }


@app.post("/api/v1/brain/route")
async def route_brain(request: ChiefInput):
    """Route a request through the Brain agent."""
    from orchestrator import brain
    result = brain.route({"domain": request.domain, "action": request.action})
    return {"routed": True, "result": result}


@app.post("/api/v1/execute-skill")
async def execute_skill(request: SkillRequest):
    """Execute a skill by name."""
    from skills import (
        MeterAuditInput,
        skill_diagnose_smart_meter,
        skill_reconcile_half_hourly_tariff,
    )

    skills = {
        "smart_meter_diagnostic": skill_diagnose_smart_meter,
        "half_hourly_reconciliation": skill_reconcile_half_hourly_tariff,
    }

    skill_name = request.prompt
    if skill_name not in skills:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")

    # Create a mock input
    input_data = MeterAuditInput(
        meter_id="meter-001",
        reading_date=datetime.now(timezone.utc).isoformat(),
        consumption_kwh=400,
        tariff_zone=request.domain,
    )

    result = skills[skill_name](input_data)
    return {
        "status": result.status,
        "skill": result.skill_name,
        "output": result.output,
        "execution_time_ms": result.execution_time_ms,
    }


@app.post("/api/v1/create-agent")
async def create_agent(request: NewAgent):
    """Register a new agent in the system."""
    # This is a simplified registration - real impl would be more complex
    return {
        "registered": True,
        "agent": request.model_dump(),
        "message": f"Agent {request.name} registered in domain {request.domain}",
    }


@app.post("/api/v1/synthesize-skill")
async def synthesize_skill(request: CreateSkillRequest):
    """Synthesize a new skill from execution traces."""
    # Placeholder - real implementation would analyze traces
    return {
        "synthesized": True,
        "skill": request.name,
        "message": f"Skill {request.name} synthesized from trace patterns",
    }


@app.get("/api/v1/traces")
async def list_traces(domain: str | None = None, limit: int = 10):
    """List recent execution traces."""
    # Placeholder - real impl would query the trace database
    return {
        "traces": [],
        "domain": domain,
        "limit": limit,
    }
