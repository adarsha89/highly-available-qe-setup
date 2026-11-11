from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models
from ..analytics import build_dashboard_snapshot
from ..database import get_db

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


def _defects_query(db: Session, category: Optional[str], build_id: Optional[str]):
    query = db.query(models.Defect)
    if category:
        query = query.filter(models.Defect.category == category)
    if build_id:
        query = query.filter(models.Defect.build_id == build_id)
    return query


@router.get("/dde")
def defect_detection_efficiency(category: Optional[str] = None, build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = _defects_query(db, category, build_id)
    total = query.count()
    pre_release = query.filter(models.Defect.detection_phase == "pre_release").count()
    dde = (pre_release / total * 100) if total else None
    return {
        "pre_release_defects": pre_release,
        "total_defects": total,
        "dde_percent": round(dde, 2) if dde is not None else None,
    }


@router.get("/automation-dde")
def automation_dde(category: Optional[str] = None, build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = _defects_query(db, category, build_id)
    total = query.count()
    automation = query.filter(models.Defect.detected_by == "automation").count()
    value = (automation / total * 100) if total else None
    return {
        "automation_detected_defects": automation,
        "total_defects": total,
        "automation_dde_percent": round(value, 2) if value is not None else None,
    }


@router.get("/production-leakage")
def production_defect_leakage(category: Optional[str] = None, build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = _defects_query(db, category, build_id)
    total = query.count()
    production = query.filter(models.Defect.detection_phase == "production").count()
    value = (production / total * 100) if total else None
    return {
        "production_defects": production,
        "total_defects": total,
        "production_leakage_percent": round(value, 2) if value is not None else None,
    }


@router.get("/critical-defect-detection")
def critical_defect_detection(category: Optional[str] = None, build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = _defects_query(db, category, build_id).filter(models.Defect.priority == "critical")
    total_critical = query.count()
    detected_pre_release = query.filter(models.Defect.detection_phase == "pre_release").count()
    value = (detected_pre_release / total_critical * 100) if total_critical else None
    return {
        "critical_detected_pre_release": detected_pre_release,
        "total_critical_defects": total_critical,
        "critical_defect_detection_percent": round(value, 2) if value is not None else None,
    }


@router.get("/defect-detection-time")
def defect_detection_time(category: Optional[str] = None, build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = _defects_query(db, category, build_id).filter(models.Defect.introduced_at.isnot(None))
    defects = query.all()
    if not defects:
        return {"sample_size": 0, "avg_detection_time_hours": None}
    total_hours = sum((d.detected_at - d.introduced_at).total_seconds() / 3600 for d in defects)
    return {"sample_size": len(defects), "avg_detection_time_hours": round(total_hours / len(defects), 2)}


@router.get("/flaky-rate")
def flaky_rate(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.TestCaseRun).join(models.TestCase)
    if category:
        query = query.filter(models.TestCase.category == category)
    total = query.count()
    flaky = query.filter(models.TestCaseRun.is_flaky.is_(True)).count()
    value = (flaky / total * 100) if total else None
    return {
        "flaky_runs": flaky,
        "total_runs": total,
        "flaky_rate_percent": round(value, 2) if value is not None else None,
    }


@router.get("/dashboard")
def dashboard_summary(build_id: Optional[str] = None, db: Session = Depends(get_db)):
    return build_dashboard_snapshot(db, build_id)
