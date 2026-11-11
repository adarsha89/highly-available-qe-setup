from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..insights import generate_insights

router = APIRouter(prefix="/api/ai", tags=["ai-insights"])


@router.get("/insights")
def get_insights(build_id: Optional[str] = None, db: Session = Depends(get_db)):
    return generate_insights(db, build_id)
