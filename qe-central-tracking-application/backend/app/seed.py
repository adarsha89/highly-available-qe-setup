"""Populates the database with sample data across all categories for demo/testing.

Run with: python -m backend.app.seed
"""

from datetime import datetime, timedelta

from . import models
from .database import Base, SessionLocal, engine

BUILD_ID = "build-1042"


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Execution).count() > 0:
            print("Database already has data — skipping seed.")
            return

        now = datetime.utcnow()

        execution_specs = [
            ("api", "api-regression-suite", "staging", "passed", 120, 118, 2, 0),
            ("web", "web-e2e-suite", "staging", "passed", 80, 72, 8, 0),
            ("mobile", "mobile-smoke-suite", "staging", "partial", 40, 30, 8, 2),
            ("database", "db-migration-tests", "staging", "passed", 25, 25, 0, 0),
            ("performance", "load-test-checkout", "staging", "passed", 10, 9, 1, 0),
            ("ai", "llm-eval-suite", "staging", "partial", 50, 38, 12, 0),
        ]
        executions = {}
        for category, suite, env, status, total, passed, failed, skipped in execution_specs:
            started = now - timedelta(hours=6)
            execution = models.Execution(
                category=category,
                suite_name=suite,
                environment=env,
                build_id=BUILD_ID,
                status=status,
                total_tests=total,
                passed_tests=passed,
                failed_tests=failed,
                skipped_tests=skipped,
                triggered_by="ci-pipeline",
                started_at=started,
                finished_at=started + timedelta(minutes=35),
                duration_seconds=35 * 60,
            )
            db.add(execution)
            executions[category] = execution
        db.flush()

        deployment_specs = [
            ("checkout-service", "staging", "api", "success"),
            ("web-frontend", "staging", "web", "success"),
            ("mobile-api-gateway", "production", "mobile", "success"),
            ("reporting-db", "staging", "database", "failed"),
            ("payments-service", "production", "performance", "success"),
            ("fraud-detection-ai", "production", "ai", "success"),
        ]
        for service, env, category, status in deployment_specs:
            started = now - timedelta(hours=8)
            finished = started + timedelta(minutes=12 if status == "success" else 25)
            db.add(
                models.Deployment(
                    service_name=service,
                    environment=env,
                    category=category,
                    status=status,
                    build_id=BUILD_ID,
                    started_at=started,
                    finished_at=finished,
                    duration_seconds=(finished - started).total_seconds(),
                )
            )

        defect_specs = [
            ("api", "critical", "automation", "pre_release", 50, 4),
            ("api", "medium", "manual", "pre_release", 30, 10),
            ("web", "high", "automation", "production", 60, 6),
            ("web", "low", "manual", "pre_release", 20, 5),
            ("mobile", "critical", "manual", "production", 90, 3),
            ("mobile", "medium", "automation", "pre_release", 15, 8),
            ("database", "high", "automation", "pre_release", 10, 2),
            ("performance", "medium", "automation", "pre_release", 8, 3),
            ("performance", "critical", "manual", "production", 40, 1),
            ("ai", "high", "automation", "pre_release", 12, 5),
            ("ai", "medium", "manual", "production", 20, 4),
        ]
        for category, priority, detected_by, phase, introduced_hours_ago, detected_hours_ago in defect_specs:
            introduced_at = now - timedelta(hours=introduced_hours_ago)
            detected_at = now - timedelta(hours=detected_hours_ago)
            db.add(
                models.Defect(
                    title=f"{category.upper()} {priority} defect ({phase})",
                    description="Seed data for demo purposes.",
                    category=category,
                    priority=priority,
                    status="open",
                    detected_by=detected_by,
                    detection_phase=phase,
                    build_id=BUILD_ID,
                    linked_execution_id=executions[category].id,
                    introduced_at=introduced_at,
                    detected_at=detected_at,
                )
            )

        test_case_specs = [
            ("api_login_flow", "api", "pytest", [True, True, False, True, True]),
            ("web_checkout_flow", "web", "playwright", [True, False, True, False, True]),
            ("mobile_push_notification", "mobile", "appium", [True, True, True, False, False]),
            ("db_migration_rollback", "database", "pytest", [True, True, True, True, True]),
            ("perf_checkout_load", "performance", "locust", [True, True, False, True, True]),
            ("ai_hallucination_eval", "ai", "custom-eval", [True, False, False, True, False]),
        ]
        for name, category, tool, run_results in test_case_specs:
            test_case = models.TestCase(name=name, category=category, automation_tool=tool)
            db.add(test_case)
            db.flush()
            for i, passed in enumerate(run_results):
                db.add(
                    models.TestCaseRun(
                        test_case_id=test_case.id,
                        execution_id=executions[category].id,
                        status="passed" if passed else "failed",
                        is_flaky=not passed,
                        run_at=now - timedelta(hours=i),
                    )
                )

        gate_specs = [
            ("API contract validation", "api", "automated", "ci", "pass"),
            ("API security scan (SAST/DAST)", "api", "automated", "ci", "pass"),
            ("API manual UAT sign-off", "api", "manual", "pre-release", "pass"),
            ("Web E2E regression suite", "web", "automated", "ci", "pass"),
            ("Web accessibility scan", "web", "automated", "ci", "fail"),
            ("Web exploratory testing sign-off", "web", "manual", "pre-release", "pass"),
            ("Mobile device-farm matrix", "mobile", "automated", "ci", "fail"),
            ("Mobile app-store compliance review", "mobile", "manual", "pre-release", "pass"),
            ("DB migration automation", "database", "automated", "ci", "pass"),
            ("DB schema peer review", "database", "manual", "pr", "pass"),
            ("Performance load test gate", "performance", "automated", "ci", "pass"),
            ("Performance sign-off review", "performance", "manual", "pre-release", "pass"),
            ("AI eval pipeline gate", "ai", "automated", "ci", "fail"),
            ("AI guardrail/safety check", "ai", "automated", "ci", "pass"),
            ("AI human-in-the-loop PR review", "ai", "manual", "pr", "pass"),
        ]
        for name, category, gate_type, stage, status in gate_specs:
            db.add(
                models.QualityGate(
                    name=name,
                    category=category,
                    gate_type=gate_type,
                    stage=stage,
                    threshold="pass",
                    actual_value=status,
                    status=status,
                    owner="qe-team",
                    build_id=BUILD_ID,
                    recorded_at=now,
                )
            )

        coverage_specs = [
            ("requirement_coverage", "api", 42, 50),
            ("automation_coverage", "api", 45, 50),
            ("code_coverage", "web", 68, 100),
            ("ui_flow_coverage", "web", 18, 25),
            ("automation_coverage", "mobile", 20, 40),
            ("regression_suite_coverage", "database", 30, 30),
            ("risk_based_coverage", "performance", 7, 10),
            ("automation_coverage", "ai", 22, 40),
        ]
        for metric_name, category, numerator, denominator in coverage_specs:
            db.add(
                models.CoverageMetric(
                    metric_name=metric_name,
                    category=category,
                    numerator=numerator,
                    denominator=denominator,
                    build_id=BUILD_ID,
                    recorded_at=now,
                )
            )

        db.commit()
        print("Seed data inserted.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
