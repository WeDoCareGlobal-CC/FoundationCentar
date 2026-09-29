"""AtlanTida OS - Core Orchestrator."""

import asyncio
import random
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AtState:
    """Deterministic state machine for agent execution."""
    agent_id: str
    domain: str
    status: str = "idle"
    last_executed: datetime | None = None
    execution_count: int = 0
    errors: list[str] = field(default_factory=list)

    def transition(self, new_status: str) -> None:
        self.status = new_status
        self.last_executed = datetime.now()
        if new_status == "running":
            self.execution_count += 1

    def record_error(self, error: str) -> None:
        self.errors.append(error)
        self.status = "error"


class Brain:
    """Global router - routes requests to appropriate Chief agent."""

    def __init__(self):
        self.domains = {
            "marketing": "Chief_Marketing",
            "finance": "Chief_Finance",
            "operations": "Chief_Ops",
            "hr": "Chief_HR",
            "legal": "Chief_Legal",
            "sales": "Chief_Sales",
            "product": "Chief_Product",
            "devops": "Chief_DevOps",
            "research": "Chief_Research",
        }
        self.chiefs: dict[str, "Chief"] = {}

    def register_chief(self, domain: str, chief: "Chief") -> None:
        self.chiefs[domain] = chief

    def route(self, request: dict[str, Any]) -> str:
        """Route a request to the appropriate chief based on domain."""
        domain = request.get("domain", "general")
        chief_name = self.domains.get(domain, "Chief_General")
        if domain in self.chiefs:
            return self.chiefs[domain].handle(request)
        return f"Routed to {chief_name} - domain '{domain}'"


class Chief:
    """Domain lead - manages workers in its domain."""

    def __init__(self, name: str, domain: str, workers: list["Worker"] | None = None):
        self.name = name
        self.domain = domain
        self.workers = workers or []
        self.state = AtState(agent_id=name, domain=domain)

    def add_worker(self, worker: "Worker") -> None:
        self.workers.append(worker)

    def handle(self, request: dict[str, Any]) -> str:
        self.state.transition("running")
        result = f"{self.name} received request for {self.domain}: {request.get('action', 'unknown')}"
        # Route to best worker
        if self.workers:
            best_worker = max(self.workers, key=lambda w: w.match_score(request))
            result += f"\n  -> Delegated to {best_worker.name} (match: {best_worker.match_score(request):.0%})"
            result += f"\n  -> {best_worker.execute(request)}"
        else:
            result += "\n  -> No workers available, queued for synthesis"
        self.state.transition("idle")
        return result


class Worker:
    """Skill executor - executes specific skills within a domain."""

    def __init__(self, name: str, domain: str, skills: list[str]):
        self.name = name
        self.domain = domain
        self.skills = skills
        self.state = AtState(agent_id=name, domain=domain)

    def match_score(self, request: dict[str, Any]) -> float:
        """How well this worker matches the request (0.0 to 1.0)."""
        action = request.get("action", "")
        return 0.5 + (len(set(action.lower().split()) & set(s.lower() for s in self.skills)) * 0.1)

    def execute(self, request: dict[str, Any]) -> str:
        self.state.transition("running")
        action = request.get("action", "default")
        result = f"{self.name} executed '{action}' using skills: {self.skills}"
        self.state.transition("idle")
        return result


# Instantiate the Brain
brain = Brain()


class Chief_Ops(Chief):
    def __init__(self):
        super().__init__("Chief_Ops", "operations", [
            Worker("Worker_Diagnostic", "operations", ["diagnose", "health", "monitor"]),
            Worker("Worker_AutoScale", "operations", ["scale", "deploy", "infra"]),
        ])
        brain.register_chief("operations", self)


class Chief_Infra(Chief):
    def __init__(self):
        super().__init__("Chief_Infra", "infrastructure", [
            Worker("Worker_Cloudflare", "infrastructure", ["cloudflare", "edge", "cdn"]),
            Worker("Worker_FlyIO", "infrastructure", ["fly.io", "deploy", "daemon"]),
        ])
        brain.register_chief("infrastructure", self)


class Chief_General(Chief):
    def __init__(self):
        super().__init__("Chief_General", "general", [
            Worker("Worker_Default", "general", ["general", "default", "fallback"]),
        ])
        brain.register_chief("general", self)


class Worker_SmartMeterDiag(Worker):
    def __init__(self):
        super().__init__("Worker_SmartMeterDiag", "operations", ["smart_meter", "diagnose"])


class Worker_CloudflareEdge(Worker):
    def __init__(self):
        super().__init__("Worker_CloudflareEdge", "infrastructure", ["cloudflare", "edge"])


class Worker_DataProcessor(Worker):
    def __init__(self):
        super().__init__("Worker_DataProcessor", "data", ["process", "transform", "analyze"])


def run_cyclical_execution(interval_seconds: int = 300) -> None:
    """Run cyclical execution loop for all chiefs."""
    print(f"AtlanTida OS: Starting cyclical execution every {interval_seconds}s...")
    round_num = 0
    try:
        while True:
            round_num += 1
            print(f"\n--- Round {round_num} ---")
            for domain, chief in brain.chiefs.items():
                print(f"[{domain}] {chief.name}: {chief.state.status}")
            print(f"Round {round_num} complete at {datetime.now().isoformat()}")
            asyncio.run(asyncio.sleep(interval_seconds))
    except KeyboardInterrupt:
        print("\nAtlanTida OS: Shutting down gracefully.")


if __name__ == "__main__":
    # Demo: route a few requests
    print("AtlanTida OS v1.0.0 - Brain Agent Online")
    print("=" * 50)

    test_requests = [
        {"domain": "operations", "action": "diagnose smart meter"},
        {"domain": "marketing", "action": "create campaign"},
        {"domain": "infrastructure", "action": "deploy to fly.io"},
        {"domain": "unknown", "action": "do something"},
    ]

    for req in test_requests:
        result = brain.route(req)
        print(f"\nRequest: {req}")
        print(f"Result: {result}")

    print("\n" + "=" * 50)
    print("AtlanTida OS: Ready. Run run_cyclical_execution() for daemon mode.")
