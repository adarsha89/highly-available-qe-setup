from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..categories import CATEGORIES

router = APIRouter(prefix="/api/quality-gates", tags=["quality-gates"])


@router.post("", response_model=schemas.QualityGateOut)
def record_gate_result(payload: schemas.QualityGateCreate, db: Session = Depends(get_db)):
    gate = models.QualityGate(**payload.model_dump())
    db.add(gate)
    db.commit()
    db.refresh(gate)
    return gate


@router.get("", response_model=List[schemas.QualityGateOut])
def list_gate_results(
    category: Optional[str] = None,
    gate_type: Optional[str] = None,
    status: Optional[str] = None,
    build_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.QualityGate)
    if category:
        query = query.filter(models.QualityGate.category == category)
    if gate_type:
        query = query.filter(models.QualityGate.gate_type == gate_type)
    if status:
        query = query.filter(models.QualityGate.status == status)
    if build_id:
        query = query.filter(models.QualityGate.build_id == build_id)
    return query.order_by(models.QualityGate.recorded_at.desc()).all()


@router.get("/summary")
def gate_summary(build_id: Optional[str] = None, db: Session = Depends(get_db)):
    summary = {}
    for category in CATEGORIES:
        query = db.query(models.QualityGate).filter(models.QualityGate.category == category)
        if build_id:
            query = query.filter(models.QualityGate.build_id == build_id)
        gates = query.all()
        total = len(gates)
        passed = sum(1 for gate in gates if gate.status == "pass")
        failed = sum(1 for gate in gates if gate.status == "fail")
        waived = sum(1 for gate in gates if gate.status == "waived")
        summary[category] = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "waived": waived,
            "pass_rate_percent": round(passed / total * 100, 2) if total else None,
        }
    return summary
