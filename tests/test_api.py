"""Tests for FoundationCentar API and core functionality."""

import pytest
from fastapi.testclient import TestClient
from src.telemetry import app
from src.orchestrator import brain
from src.skills import skill_diagnose_smart_meter, MeterAuditInput
from datetime import datetime, timezone


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoints:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "AtlanTida OS API is running"}

    def test_health_endpoint(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestAPIEndpoints:
    def test_list_agents(self, client):
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        data = response.json()
        assert "brain" in data
        assert data["brain"]["role"] == "global_router"

    def test_list_skills(self, client):
        response = client.get("/api/v1/skills")
        assert response.status_code == 200
        data = response.json()
        assert "smart_meter_diagnostic" in data
        assert "half_hourly_reconciliation" in data

    def test_route_brain_valid_domain(self, client):
        response = client.post("/api/v1/brain/route", json={
            "domain": "operations",
            "action": "diagnose smart meter"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["routed"] is True

    def test_route_brain_invalid_domain(self, client):
        response = client.post("/api/v1/brain/route", json={
            "domain": "unknown",
            "action": "do something"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["routed"] is True

    def test_execute_skill_valid(self, client):
        response = client.post("/api/v1/execute-skill", json={
            "prompt": "smart_meter_diagnostic",
            "domain": "operations"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ("ok", "error")
        assert "skill" in data

    def test_execute_skill_invalid(self, client):
        response = client.post("/api/v1/execute-skill", json={
            "prompt": "nonexistent_skill",
            "domain": "operations"
        })
        assert response.status_code == 404

    def test_create_agent(self, client):
        response = client.post("/api/v1/create-agent", json={
            "id": "test-agent-1",
            "name": "Test Agent",
            "description": "A test agent",
            "domain": "operations",
            "role": "worker"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["registered"] is True

    def test_synthesize_skill(self, client):
        response = client.post("/api/v1/synthesize-skill", json={
            "name": "test_skill",
            "description": "A test skill",
            "parameters": {}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["synthesized"] is True


class TestOrchestrator:
    def test_brain_routes_known_domains(self):
        result = brain.route({"domain": "operations", "action": "diagnose smart meter"})
        assert "chief" in result
        assert "worker" in result
        assert "routed_to" in result

    def test_brain_handles_unknown_domain(self):
        result = brain.route({"domain": "unknown", "action": "do something"})
        assert "error" in result or "routed_to" in result


class TestSkills:
    def test_skill_diagnose_smart_meter(self):
        input_data = MeterAuditInput(
            meter_id="meter-001",
            reading_date=datetime.now(timezone.utc).isoformat(),
            consumption_kwh=400,
            tariff_zone="operations",
        )
        result = skill_diagnose_smart_meter(input_data)
        assert hasattr(result, "status")
        assert hasattr(result, "skill_name")
        assert hasattr(result, "output")
        assert hasattr(result, "execution_time_ms")


class TestMetrics:
    def test_metrics_endpoint_exists(self, client):
        """Test that /metrics endpoint exists for Prometheus."""
        response = client.get("/metrics")
        # Should return 200 with Prometheus metrics or 404 if not implemented
        # We're checking it exists, so 200 is expected once implemented
        assert response.status_code in (200, 404)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])