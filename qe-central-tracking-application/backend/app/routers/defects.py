from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/defects", tags=["defects"])


@router.post("", response_model=schemas.DefectOut)
def create_defect(payload: schemas.DefectCreate, db: Session = Depends(get_db)):
    defect = models.Defect(**payload.model_dump())
    db.add(defect)
    db.commit()
    db.refresh(defect)
    return defect


@router.get("", response_model=List[schemas.DefectOut])
def list_defects(
    category: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    detection_phase: Optional[str] = None,
    build_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Defect)
    if category:
        query = query.filter(models.Defect.category == category)
    if priority:
        query = query.filter(models.Defect.priority == priority)
    if status:
        query = query.filter(models.Defect.status == status)
    if detection_phase:
        query = query.filter(models.Defect.detection_phase == detection_phase)
    if build_id:
        query = query.filter(models.Defect.build_id == build_id)
    return query.order_by(models.Defect.detected_at.desc()).all()


@router.get("/priority-summary")
def priority_summary(category: Optional[str] = None, build_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Defect)
    if category:
        query = query.filter(models.Defect.category == category)
    if build_id:
        query = query.filter(models.Defect.build_id == build_id)
    summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for defect in query.all():
        summary[defect.priority] = summary.get(defect.priority, 0) + 1
    return summary


@router.get("/{defect_id}", response_model=schemas.DefectOut)
def get_defect(defect_id: int, db: Session = Depends(get_db)):
    defect = db.get(models.Defect, defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    return defect


@router.patch("/{defect_id}", response_model=schemas.DefectOut)
def update_defect(defect_id: int, payload: schemas.DefectUpdate, db: Session = Depends(get_db)):
    defect = db.get(models.Defect, defect_id)
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(defect, key, value)
    db.commit()
    db.refresh(defect)
    return defect
