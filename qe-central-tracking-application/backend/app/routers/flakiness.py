from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/flakiness", tags=["flakiness"])


@router.post("/test-cases", response_model=schemas.TestCaseOut)
def register_test_case(payload: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    existing = db.query(models.TestCase).filter(models.TestCase.name == payload.name).first()
    if existing:
        return existing
    test_case = models.TestCase(**payload.model_dump())
    db.add(test_case)
    db.commit()
    db.refresh(test_case)
    return test_case


@router.get("/test-cases", response_model=List[schemas.TestCaseOut])
def list_test_cases(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.TestCase)
    if category:
        query = query.filter(models.TestCase.category == category)
    return query.all()


@router.post("/runs", response_model=schemas.TestCaseRunOut)
def record_run(payload: schemas.TestCaseRunCreate, db: Session = Depends(get_db)):
    test_case = db.get(models.TestCase, payload.test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    run = models.TestCaseRun(**payload.model_dump())
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@router.get("")
def flakiness_summary(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.TestCase)
    if category:
        query = query.filter(models.TestCase.category == category)
    results = []
    for test_case in query.all():
        total = len(test_case.runs)
        flaky = sum(1 for run in test_case.runs if run.is_flaky)
        results.append(
            {
                "test_case_id": test_case.id,
                "name": test_case.name,
                "category": test_case.category,
                "total_runs": total,
                "flaky_runs": flaky,
                "flaky_rate_percent": round(flaky / total * 100, 2) if total else None,
            }
        )
    return results


@router.get("/{test_case_id}")
def flakiness_detail(test_case_id: int, db: Session = Depends(get_db)):
    test_case = db.get(models.TestCase, test_case_id)
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    total = len(test_case.runs)
    flaky = sum(1 for run in test_case.runs if run.is_flaky)
    return {
        "test_case_id": test_case.id,
        "name": test_case.name,
        "category": test_case.category,
        "total_runs": total,
        "flaky_runs": flaky,
        "flaky_rate_percent": round(flaky / total * 100, 2) if total else None,
        "runs": [
            {"id": run.id, "status": run.status, "is_flaky": run.is_flaky, "run_at": run.run_at}
            for run in test_case.runs
        ],
    }
