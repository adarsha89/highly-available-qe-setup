from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ---------- Executions ----------
class ExecutionBase(BaseModel):
    category: str
    suite_name: str
    environment: str
    build_id: Optional[str] = None
    status: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    triggered_by: Optional[str] = None
    started_at: datetime
    finished_at: datetime


class ExecutionCreate(ExecutionBase):
    pass


class ExecutionOut(ExecutionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    duration_seconds: Optional[float] = None
    created_at: datetime


# ---------- Deployments ----------
class DeploymentBase(BaseModel):
    service_name: str
    environment: str
    category: Optional[str] = None
    status: str
    build_id: Optional[str] = None
    started_at: datetime
    finished_at: datetime


class DeploymentCreate(DeploymentBase):
    pass


class DeploymentOut(DeploymentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    duration_seconds: Optional[float] = None
    created_at: datetime


# ---------- Defects ----------
class DefectBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    priority: str
    status: str = "open"
    detected_by: str
    detection_phase: str
    build_id: Optional[str] = None
    linked_execution_id: Optional[int] = None
    introduced_at: Optional[datetime] = None
    detected_at: datetime
    resolved_at: Optional[datetime] = None


class DefectCreate(DefectBase):
    pass


class DefectUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    resolved_at: Optional[datetime] = None


class DefectOut(DefectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


# ---------- Test cases / flakiness ----------
class TestCaseBase(BaseModel):
    name: str
    category: str
    automation_tool: Optional[str] = None


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseOut(TestCaseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class TestCaseRunBase(BaseModel):
    test_case_id: int
    execution_id: Optional[int] = None
    status: str
    is_flaky: bool = False


class TestCaseRunCreate(TestCaseRunBase):
    pass


class TestCaseRunOut(TestCaseRunBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    run_at: datetime


# ---------- Quality gates ----------
class QualityGateBase(BaseModel):
    name: str
    category: str
    gate_type: str
    stage: Optional[str] = None
    threshold: Optional[str] = None
    actual_value: Optional[str] = None
    status: str
    owner: Optional[str] = None
    build_id: Optional[str] = None


class QualityGateCreate(QualityGateBase):
    pass


class QualityGateOut(QualityGateBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    recorded_at: datetime


# ---------- Coverage metrics ----------
class CoverageMetricBase(BaseModel):
    metric_name: str
    category: str
    numerator: float
    denominator: float
    build_id: Optional[str] = None


class CoverageMetricCreate(CoverageMetricBase):
    pass


class CoverageMetricOut(CoverageMetricBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    recorded_at: datetime
