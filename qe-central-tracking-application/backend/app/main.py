"""QE Central Tracking Application - High Availability Backend API & Dashboard.

Collects quality gates, test execution metrics, deployments, defects, coverage,
and flakiness across API, Web, Mobile, Database, Performance, and AI categories.
Includes AI-driven insights, Prometheus scraping metrics, and Kubernetes health probes.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
import os
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import uvicorn

from .database import Base, engine, get_db
from .models import Execution
from .routers import (
    ai_insights,
    coverage,
    defects,
    deployments,
    executions,
    flakiness,
    metrics,
    quality_gates,
)
from .seed import seed

logger = logging.getLogger("qe-tracking")
logging.basicConfig(level=logging.INFO)

# Prometheus Metrics
TEST_RUNS_TOTAL = Counter(
    "qe_test_runs_total",
    "Total number of test suite runs tracked",
    ["suite", "environment", "status"],
)
TEST_DURATION_SECONDS = Gauge(
    "qe_test_duration_seconds",
    "Duration of test suite executions in seconds",
    ["suite"],
)
ACTIVE_SERVICES_GAUGE = Gauge(
    "qe_ha_active_services",
    "Health status of tracked HA services (1 = Healthy, 0 = Degraded)",
    ["service"],
)

# Ensure tables exist at import time
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema
    Base.metadata.create_all(bind=engine)
    # Auto-seed if database is empty
    try:
        seed()
    except Exception as e:
        logger.warning("Auto-seed check encountered: %s", e)
    ACTIVE_SERVICES_GAUGE.labels(service="tracker-backend").set(1)
    yield


app = FastAPI(
    title="QE Central Tracking Application",
    version="2.0.0",
    description="Central tracking and analysis platform for automation data, quality gates, and HA resilience.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Tracking Routers
app.include_router(executions.router)
app.include_router(deployments.router)
app.include_router(defects.router)
app.include_router(flakiness.router)
app.include_router(quality_gates.router)
app.include_router(coverage.router)
app.include_router(metrics.router)
app.include_router(ai_insights.router)


# --- Observability & Health Endpoints ---
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check(db: Session = Depends(get_db)):
    """Liveness and Readiness probe for Kubernetes, Docker Compose, and HA monitoring."""
    ACTIVE_SERVICES_GAUGE.labels(service="tracker-backend").set(1)
    total_executions = db.query(Execution).count()
    return {
        "status": "HEALTHY",
        "service": "qe-central-tracking-application",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": "connected",
        "total_executions": total_executions,
    }


@app.get("/metrics")
def get_metrics():
    """Prometheus scraping endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# --- Backward Compatible Telemetry Endpoints (/api/v1) ---
legacy_router = APIRouter(prefix="/api/v1", tags=["telemetry-v1"])


class LegacyTestRunCreate(BaseModel):
    suite: str = Field(..., json_schema_extra={"example": "qe-base-api-verification"})
    environment: str = Field(default="ci", json_schema_extra={"example": "ci"})
    status: str = Field(default="PASSED", json_schema_extra={"example": "PASSED"})
    total_tests: int = Field(default=0, ge=0)
    passed_tests: int = Field(default=0, ge=0)
    failed_tests: int = Field(default=0, ge=0)
    duration_seconds: float = Field(default=0.0, ge=0.0)
    metadata: Optional[Dict[str, Any]] = None


class LegacyTestRun(LegacyTestRunCreate):
    id: int
    created_at: datetime


def _infer_category(suite_name: str) -> str:
    name = suite_name.lower()
    for cat in ["web", "mobile", "database", "performance", "ai"]:
        if cat in name:
            return cat
    return "api"


@legacy_router.post("/runs", response_model=LegacyTestRun, status_code=status.HTTP_201_CREATED)
def create_legacy_test_run(run: LegacyTestRunCreate, db: Session = Depends(get_db)):
    """Backward compatible ingestion endpoint for Jenkins pipelines and telemetry exporters."""
    cat = _infer_category(run.suite)
    now = datetime.now(timezone.utc)

    norm_status = run.status.lower()
    if norm_status not in ["passed", "failed", "partial"]:
        norm_status = "passed" if "pass" in norm_status else "failed"

    execution = Execution(
        category=cat,
        suite_name=run.suite,
        environment=run.environment,
        build_id=(run.metadata or {}).get("build_id", "ci-build"),
        status=norm_status,
        total_tests=run.total_tests,
        passed_tests=run.passed_tests,
        failed_tests=run.failed_tests,
        skipped_tests=max(0, run.total_tests - (run.passed_tests + run.failed_tests)),
        triggered_by=(run.metadata or {}).get("source", "legacy-telemetry"),
        started_at=now,
        finished_at=now,
        duration_seconds=run.duration_seconds,
        created_at=now,
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)

    # Emit Prometheus metrics
    TEST_RUNS_TOTAL.labels(
        suite=run.suite, environment=run.environment, status=run.status
    ).inc()
    TEST_DURATION_SECONDS.labels(suite=run.suite).set(run.duration_seconds)

    return LegacyTestRun(
        id=execution.id,
        suite=execution.suite_name,
        environment=execution.environment,
        status=run.status,
        total_tests=execution.total_tests,
        passed_tests=execution.passed_tests,
        failed_tests=execution.failed_tests,
        duration_seconds=execution.duration_seconds or 0.0,
        metadata=run.metadata,
        created_at=execution.created_at,
    )


@legacy_router.get("/runs", response_model=List[LegacyTestRun])
def list_legacy_test_runs(limit: int = 50, db: Session = Depends(get_db)):
    executions = db.query(Execution).order_by(Execution.created_at.desc()).limit(limit).all()
    results = []
    for e in executions:
        results.append(
            LegacyTestRun(
                id=e.id,
                suite=e.suite_name,
                environment=e.environment,
                status=e.status.upper(),
                total_tests=e.total_tests,
                passed_tests=e.passed_tests,
                failed_tests=e.failed_tests,
                duration_seconds=e.duration_seconds or 0.0,
                metadata={"build_id": e.build_id, "category": e.category},
                created_at=e.created_at,
            )
        )
    return results


@legacy_router.get("/runs/{run_id}", response_model=LegacyTestRun)
def get_legacy_test_run(run_id: int, db: Session = Depends(get_db)):
    e = db.get(Execution, run_id)
    if not e:
        raise HTTPException(status_code=404, detail="Test run not found")
    return LegacyTestRun(
        id=e.id,
        suite=e.suite_name,
        environment=e.environment,
        status=e.status.upper(),
        total_tests=e.total_tests,
        passed_tests=e.passed_tests,
        failed_tests=e.failed_tests,
        duration_seconds=e.duration_seconds or 0.0,
        metadata={"build_id": e.build_id, "category": e.category},
        created_at=e.created_at,
    )


@legacy_router.get("/stats")
def get_legacy_stats(db: Session = Depends(get_db)):
    executions = db.query(Execution).all()
    total = len(executions)
    passed = sum(1 for e in executions if e.status.lower() in ["passed", "pass"])
    failed = total - passed
    return {
        "total_runs": total,
        "passed_runs": passed,
        "failed_runs": failed,
        "pass_rate_percentage": round((passed / total * 100), 2) if total > 0 else 100.0,
    }


# Webhook receiver for Alertmanager
@legacy_router.post("/alerts")
@legacy_router.post("/alerts/critical")
def receive_alert(alert_payload: Dict[str, Any]):
    logger.info("Received alert from Alertmanager: %s", alert_payload.get("status", "unknown"))
    return {"status": "received", "alerts_count": len(alert_payload.get("alerts", []))}


app.include_router(legacy_router)


# Mount frontend static files
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
candidate_frontend_paths = [
    os.path.join(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)), "frontend"),
    os.path.join(os.path.dirname(CURRENT_FILE_DIR), "frontend"),
    os.path.join("/app", "frontend"),
]

for frontend_path in candidate_frontend_paths:
    if os.path.isdir(frontend_path):
        app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
        logger.info("Mounted frontend static files from %s", frontend_path)
        break


if __name__ == "__main__":
    port = int(os.environ.get("TRACKER_PORT", 8000))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=False)
