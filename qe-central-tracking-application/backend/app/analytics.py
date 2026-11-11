"""Shared aggregation logic for per-category quality metrics.

Used by both the /api/metrics dashboard endpoint and the AI insights module so
the two always report consistent numbers from the same queries.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from . import models
from .categories import CATEGORIES


def _pct(numerator: int, denominator: int) -> Optional[float]:
    if not denominator:
        return None
    return round(numerator / denominator * 100, 2)


def category_metrics(db: Session, category: str, build_id: Optional[str] = None) -> dict:
    defects_q = db.query(models.Defect).filter(models.Defect.category == category)
    if build_id:
        defects_q = defects_q.filter(models.Defect.build_id == build_id)
    defects = defects_q.all()
    total_defects = len(defects)
    pre_release = sum(1 for d in defects if d.detection_phase == "pre_release")
    production = sum(1 for d in defects if d.detection_phase == "production")
    automation_detected = sum(1 for d in defects if d.detected_by == "automation")
    critical_defects = [d for d in defects if d.priority == "critical"]
    critical_pre_release = sum(1 for d in critical_defects if d.detection_phase == "pre_release")
    timed_defects = [d for d in defects if d.introduced_at is not None]
    avg_detection_hours = None
    if timed_defects:
        total_hours = sum((d.detected_at - d.introduced_at).total_seconds() / 3600 for d in timed_defects)
        avg_detection_hours = round(total_hours / len(timed_defects), 2)

    priority_breakdown = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for d in defects:
        priority_breakdown[d.priority] = priority_breakdown.get(d.priority, 0) + 1

    gates_q = db.query(models.QualityGate).filter(models.QualityGate.category == category)
    if build_id:
        gates_q = gates_q.filter(models.QualityGate.build_id == build_id)
    gates = gates_q.all()
    gates_passed = sum(1 for g in gates if g.status == "pass")
    gates_failed = sum(1 for g in gates if g.status == "fail")
    gates_waived = sum(1 for g in gates if g.status == "waived")

    runs_q = (
        db.query(models.TestCaseRun)
        .join(models.TestCase)
        .filter(models.TestCase.category == category)
    )
    runs = runs_q.all()
    flaky_runs = sum(1 for r in runs if r.is_flaky)

    exec_q = db.query(models.Execution).filter(models.Execution.category == category)
    if build_id:
        exec_q = exec_q.filter(models.Execution.build_id == build_id)
    executions = exec_q.all()
    exec_passed_total = sum(e.passed_tests for e in executions)
    exec_total_tests = sum(e.total_tests for e in executions)

    coverage_q = db.query(models.CoverageMetric).filter(models.CoverageMetric.category == category)
    if build_id:
        coverage_q = coverage_q.filter(models.CoverageMetric.build_id == build_id)
    latest_coverage: dict = {}
    for metric in coverage_q.all():
        existing = latest_coverage.get(metric.metric_name)
        if existing is None or metric.recorded_at > existing.recorded_at:
            latest_coverage[metric.metric_name] = metric
    coverage = {
        name: _pct(metric.numerator, metric.denominator) for name, metric in latest_coverage.items()
    }

    return {
        "defects": {"total": total_defects, **priority_breakdown},
        "dde_percent": _pct(pre_release, total_defects),
        "automation_dde_percent": _pct(automation_detected, total_defects),
        "production_leakage_percent": _pct(production, total_defects),
        "critical_defect_detection_percent": _pct(critical_pre_release, len(critical_defects)),
        "avg_defect_detection_time_hours": avg_detection_hours,
        "flaky_rate_percent": _pct(flaky_runs, len(runs)),
        "gates_total": len(gates),
        "gates_passed": gates_passed,
        "gates_failed": gates_failed,
        "gates_waived": gates_waived,
        "gate_pass_rate_percent": _pct(gates_passed, len(gates)),
        "coverage": coverage,
        "executions": {
            "total": len(executions),
            "test_pass_rate_percent": _pct(exec_passed_total, exec_total_tests),
        },
    }


def build_dashboard_snapshot(db: Session, build_id: Optional[str] = None) -> dict:
    deployments_q = db.query(models.Deployment)
    if build_id:
        deployments_q = deployments_q.filter(models.Deployment.build_id == build_id)
    deployments = deployments_q.all()
    successful_deployments = sum(1 for d in deployments if d.status == "success")
    deployment_summary = {
        "count": len(deployments),
        "avg_duration_seconds": (
            round(sum(d.duration_seconds or 0 for d in deployments) / len(deployments), 2)
            if deployments
            else None
        ),
        "success_rate_percent": _pct(successful_deployments, len(deployments)),
    }

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "build_id": build_id,
        "categories": {category: category_metrics(db, category, build_id) for category in CATEGORIES},
        "deployments": deployment_summary,
    }
