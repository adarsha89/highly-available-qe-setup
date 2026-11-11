from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/coverage", tags=["coverage"])


@router.post("", response_model=schemas.CoverageMetricOut)
def record_coverage(payload: schemas.CoverageMetricCreate, db: Session = Depends(get_db)):
    metric = models.CoverageMetric(**payload.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


@router.get("", response_model=List[schemas.CoverageMetricOut])
def list_coverage(
    category: Optional[str] = None,
    metric_name: Optional[str] = None,
    build_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.CoverageMetric)
    if category:
        query = query.filter(models.CoverageMetric.category == category)
    if metric_name:
        query = query.filter(models.CoverageMetric.metric_name == metric_name)
    if build_id:
        query = query.filter(models.CoverageMetric.build_id == build_id)
    return query.order_by(models.CoverageMetric.recorded_at.desc()).all()


@router.get("/summary")
def coverage_summary(build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.CoverageMetric)
    if build_id:
        query = query.filter(models.CoverageMetric.build_id == build_id)
    latest_by_key = {}
    for metric in query.all():
        key = (metric.category, metric.metric_name)
        if key not in latest_by_key or metric.recorded_at > latest_by_key[key].recorded_at:
            latest_by_key[key] = metric
    results = []
    for (category, metric_name), metric in latest_by_key.items():
        pct = round(metric.numerator / metric.denominator * 100, 2) if metric.denominator else None
        results.append(
            {
                "category": category,
                "metric_name": metric_name,
                "numerator": metric.numerator,
                "denominator": metric.denominator,
                "coverage_percent": pct,
                "recorded_at": metric.recorded_at,
            }
        )
    return results
