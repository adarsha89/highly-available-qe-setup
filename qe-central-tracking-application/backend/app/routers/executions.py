from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/executions", tags=["executions"])


@router.post("", response_model=schemas.ExecutionOut)
def create_execution(payload: schemas.ExecutionCreate, db: Session = Depends(get_db)):
    duration = (payload.finished_at - payload.started_at).total_seconds()
    execution = models.Execution(**payload.model_dump(), duration_seconds=duration)
    db.add(execution)
    db.commit()
    db.refresh(execution)
    return execution


@router.get("", response_model=List[schemas.ExecutionOut])
def list_executions(
    category: Optional[str] = None,
    build_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Execution)
    if category:
        query = query.filter(models.Execution.category == category)
    if build_id:
        query = query.filter(models.Execution.build_id == build_id)
    if status:
        query = query.filter(models.Execution.status == status)
    return query.order_by(models.Execution.started_at.desc()).all()


@router.get("/{execution_id}", response_model=schemas.ExecutionOut)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    execution = db.get(models.Execution, execution_id)
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution
