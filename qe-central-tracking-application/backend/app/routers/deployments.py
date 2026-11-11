from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/deployments", tags=["deployments"])


@router.post("", response_model=schemas.DeploymentOut)
def create_deployment(payload: schemas.DeploymentCreate, db: Session = Depends(get_db)):
    duration = (payload.finished_at - payload.started_at).total_seconds()
    deployment = models.Deployment(**payload.model_dump(), duration_seconds=duration)
    db.add(deployment)
    db.commit()
    db.refresh(deployment)
    return deployment


@router.get("", response_model=List[schemas.DeploymentOut])
def list_deployments(
    environment: Optional[str] = None,
    service_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Deployment)
    if environment:
        query = query.filter(models.Deployment.environment == environment)
    if service_name:
        query = query.filter(models.Deployment.service_name == service_name)
    return query.order_by(models.Deployment.started_at.desc()).all()


@router.get("/stats")
def deployment_stats(environment: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Deployment)
    if environment:
        query = query.filter(models.Deployment.environment == environment)
    deployments = query.all()
    if not deployments:
        return {"count": 0, "avg_duration_seconds": None, "success_rate_percent": None}
    avg_duration = sum(d.duration_seconds or 0 for d in deployments) / len(deployments)
    successful = sum(1 for d in deployments if d.status == "success")
    return {
        "count": len(deployments),
        "avg_duration_seconds": round(avg_duration, 2),
        "success_rate_percent": round(successful / len(deployments) * 100, 2),
    }


@router.get("/{deployment_id}", response_model=schemas.DeploymentOut)
def get_deployment(deployment_id: int, db: Session = Depends(get_db)):
    deployment = db.get(models.Deployment, deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment
