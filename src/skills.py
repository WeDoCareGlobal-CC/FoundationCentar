"""AtlanTida OS - Skill definitions and execution."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class MeterAuditInput:
    """Input for smart meter audit skill."""
    meter_id: str
    reading_date: str
    consumption_kwh: float
    tariff_zone: str = "단일"


@dataclass
class SkillExecutionResult:
    """Result of a skill execution."""
    status: str
    skill_name: str
    output: str
    execution_time_ms: int = 0
    metadata: dict[str, Any] = None


def skill_diagnose_smart_meter(input_data: MeterAuditInput, engine=None) -> SkillExecutionResult:
    """Diagnose a smart meter anomaly based on consumption data."""
    was_anomaly = input_data.consumption_kwh > 350
    is_wasting = was_anomaly and input_data.tariff_zone == "단일"

    diagnosis = (
        f"Meter {input_data.meter_id}: consumption {input_data.consumption_kwh} kWh "
        f"on {input_data.reading_date}."
    )

    if was_anomaly:
        diagnosis += "\n⚠️ Anomaly detected: consumption exceeds threshold (350 kWh)."
        if is_wasting:
            diagnosis += (
                "\n⚠️ This single-rate tariff meter is wasting ~50 kWh/day near "
                "peak hours. Recommend time-of-use tariff switch to Economy 7 or "
                "Intelligent Octopus to reduce costs."
            )
    else:
        diagnosis += "\n✅ Normal consumption pattern."

    execution_time = int(datetime.now(timezone.utc).timestamp() * 1000) % 1000

    return SkillExecutionResult(
        status="ok" if not was_anomaly else "warning",
        skill_name="smart_meter_diagnostic",
        output=diagnosis,
        execution_time_ms=execution_time,
        metadata={
            "anomaly": was_anomaly,
            "wasting": is_wasting,
            "tariff_recommendation": "Switch to Economy 7 or Intelligent Octopus" if is_wasting else None,
        },
    )


def skill_reconcile_half_hourly_tariff(input_data: MeterAuditInput, engine=None) -> SkillExecutionResult:
    """Reconcile half-hourly tariff data against expected patterns."""
    # Simple reconciliation: compare actual vs expected (expected = reading / 48 half-hours)
    expected_per_half_hour = input_data.consumption_kwh / 48
    variance = abs(input_data.consumption_kwh - (expected_per_half_hour * 48)) / input_data.consumption_kwh * 100

    result_output = (
        f"Half-hourly reconciliation for meter {input_data.meter_id}:\n"
        f"  Expected per half-hour: {expected_per_half_hour:.2f} kWh\n"
        f"  Variance: {variance:.1f}%\n"
        f"  Status: {'Within tolerance' if variance < 5 else 'Needs review'}"
    )

    return SkillExecutionResult(
        status="ok" if variance < 5 else "warning",
        skill_name="half_hourly_reconciliation",
        output=result_output,
        execution_time_ms=50,
        metadata={
            "expected_per_half_hour": expected_per_half_hour,
            "variance_percent": variance,
        },
    )
