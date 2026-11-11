"""Generates a quality-metrics summary and improvement recommendations from stored data.

Uses whichever AI provider is configured (see app/ai/provider.py). When no provider is
configured, or the configured one has no API key, falls back to a deterministic
rule-based analysis built directly from the aggregated metrics snapshot.
"""

import json
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from .ai.provider import RuleBasedProvider, get_provider
from .analytics import build_dashboard_snapshot

THRESHOLDS = {
    "gate_pass_rate_percent": 80,
    "flaky_rate_percent": 5,
    "dde_percent": 70,
    "production_leakage_percent": 20,
    "critical_defect_detection_percent": 90,
    "avg_defect_detection_time_hours": 72,
    "coverage_percent": 80,
}


def _rule_based_insights(snapshot: dict):
    recommendations = []
    category_notes = []

    for category, data in snapshot["categories"].items():
        total_defects = data["defects"]["total"]
        gate_rate = data["gate_pass_rate_percent"]
        flaky_rate = data["flaky_rate_percent"]
        dde = data["dde_percent"]
        leakage = data["production_leakage_percent"]
        critical_rate = data["critical_defect_detection_percent"]
        detection_time = data["avg_defect_detection_time_hours"]

        if total_defects == 0 and data["gates_total"] == 0 and data["executions"]["total"] == 0:
            continue

        category_notes.append(
            f"{category.upper()}: {total_defects} defects, "
            f"gate pass rate {gate_rate if gate_rate is not None else 'n/a'}%, "
            f"flaky rate {flaky_rate if flaky_rate is not None else 'n/a'}%, "
            f"DDE {dde if dde is not None else 'n/a'}%."
        )

        if gate_rate is not None and gate_rate < THRESHOLDS["gate_pass_rate_percent"]:
            recommendations.append(
                f"[{category}] Quality gate pass rate is {gate_rate}% — investigate and fix failing gates "
                "before the next release."
            )
        if flaky_rate is not None and flaky_rate > THRESHOLDS["flaky_rate_percent"]:
            recommendations.append(
                f"[{category}] Flaky test rate is {flaky_rate}% — quarantine unstable tests and stabilize "
                "test data/environment."
            )
        if dde is not None and dde < THRESHOLDS["dde_percent"]:
            recommendations.append(
                f"[{category}] Defect Detection Efficiency is {dde}% — expand pre-release automated/manual "
                "test coverage."
            )
        if leakage is not None and leakage > THRESHOLDS["production_leakage_percent"]:
            recommendations.append(
                f"[{category}] Production defect leakage is {leakage}% — strengthen regression and UAT gates."
            )
        if critical_rate is not None and critical_rate < THRESHOLDS["critical_defect_detection_percent"]:
            recommendations.append(
                f"[{category}] Only {critical_rate}% of critical defects are caught pre-release — add "
                "targeted critical-path tests."
            )
        if detection_time is not None and detection_time > THRESHOLDS["avg_defect_detection_time_hours"]:
            recommendations.append(
                f"[{category}] Average defect detection time is {detection_time}h — add earlier monitoring/"
                "alerting in this pipeline stage."
            )
        for metric_name, pct in data["coverage"].items():
            if pct is not None and pct < THRESHOLDS["coverage_percent"]:
                label = metric_name.replace("_", " ").title()
                recommendations.append(f"[{category}] {label} is {pct}% — raise it toward an 80%+ target.")

    if not recommendations:
        recommendations.append("All tracked metrics are within healthy thresholds — maintain current cadence.")

    summary = "Quality metrics summary across tracked categories:\n" + "\n".join(category_notes)
    return summary, recommendations


def _llm_insights(provider, snapshot: dict):
    prompt = (
        "You are a quality engineering analytics assistant. Given this JSON snapshot of automation and "
        "quality metrics across API, Web, Mobile, Database, Performance, and AI categories, respond ONLY "
        "with JSON of the form "
        '{"summary": "<3-5 sentence summary of overall quality health>", '
        '"recommendations": ["<specific, prioritized improvement action>", ...]}.\n\n'
        f"Snapshot:\n{json.dumps(snapshot, default=str)}"
    )
    raw = provider.generate(prompt)
    try:
        parsed = json.loads(raw)
        return parsed.get("summary", raw), parsed.get("recommendations", [])
    except (json.JSONDecodeError, TypeError):
        return raw, []


def generate_insights(db: Session, build_id: Optional[str] = None) -> dict:
    snapshot = build_dashboard_snapshot(db, build_id)
    provider = get_provider()

    provider_label = provider.name
    if isinstance(provider, RuleBasedProvider):
        summary, recommendations = _rule_based_insights(snapshot)
    else:
        try:
            summary, recommendations = _llm_insights(provider, snapshot)
            if not recommendations:
                _, recommendations = _rule_based_insights(snapshot)
        except Exception:
            # e.g. no local Ollama server running, or an API call failed — stay available.
            summary, recommendations = _rule_based_insights(snapshot)
            provider_label = f"{provider.name} (unreachable, fell back to rule_based)"

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "provider": provider_label,
        "summary": summary,
        "recommendations": recommendations,
        "data_snapshot": snapshot,
    }
