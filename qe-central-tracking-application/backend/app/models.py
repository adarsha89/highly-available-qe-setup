from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base

# Shared category values across the app: api, web, mobile, database, performance, ai


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    suite_name = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    build_id = Column(String, index=True)
    status = Column(String, nullable=False)  # passed/failed/partial
    total_tests = Column(Integer, default=0)
    passed_tests = Column(Integer, default=0)
    failed_tests = Column(Integer, default=0)
    skipped_tests = Column(Integer, default=0)
    triggered_by = Column(String)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=False)
    duration_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)
    environment = Column(String, nullable=False, index=True)
    category = Column(String)
    status = Column(String, nullable=False)  # success/failed/rolled_back
    build_id = Column(String, index=True)
    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=False)
    duration_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Defect(Base):
    __tablename__ = "defects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False, index=True)
    priority = Column(String, nullable=False, index=True)  # critical/high/medium/low
    status = Column(String, default="open", index=True)  # open/in_progress/resolved/closed
    detected_by = Column(String, nullable=False)  # manual/automation
    detection_phase = Column(String, nullable=False, index=True)  # pre_release/production
    build_id = Column(String, index=True)
    linked_execution_id = Column(Integer, ForeignKey("executions.id"), nullable=True)
    introduced_at = Column(DateTime, nullable=True)
    detected_at = Column(DateTime, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False, index=True)
    automation_tool = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    runs = relationship("TestCaseRun", back_populates="test_case", cascade="all, delete-orphan")


class TestCaseRun(Base):
    __tablename__ = "test_case_runs"

    id = Column(Integer, primary_key=True, index=True)
    test_case_id = Column(Integer, ForeignKey("test_cases.id"), nullable=False)
    execution_id = Column(Integer, ForeignKey("executions.id"), nullable=True)
    status = Column(String, nullable=False)  # passed/failed
    is_flaky = Column(Boolean, default=False)
    run_at = Column(DateTime, default=datetime.utcnow)

    test_case = relationship("TestCase", back_populates="runs")


class QualityGate(Base):
    __tablename__ = "quality_gates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    gate_type = Column(String, nullable=False)  # manual/automated
    stage = Column(String)  # pre-commit/pr/ci/pre-release/post-release
    threshold = Column(String)
    actual_value = Column(String)
    status = Column(String, nullable=False, index=True)  # pass/fail/waived
    owner = Column(String)
    build_id = Column(String, index=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)


class CoverageMetric(Base):
    __tablename__ = "coverage_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    numerator = Column(Float, nullable=False)
    denominator = Column(Float, nullable=False)
    build_id = Column(String, index=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)
