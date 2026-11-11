# QE Central Tracking Application

Central tracking and analysis application for quality engineering data, telemetry, and metrics across:
- **API**
- **Web**
- **Mobile**
- **Database**
- **Performance**
- **AI Automation & LLM Evaluation**

Implements and monitors all quality gates catalogued in `quality_gates.txt`.

## Architecture & Features

- **Backend**: FastAPI + SQLAlchemy (`backend/app`), exposing REST APIs for all QE domains and Prometheus metrics (`/metrics`).
- **Database**: SQLite by default (`tracker.db`), configurable via `DATABASE_URL` (PostgreSQL, MySQL, etc.).
- **Frontend**: Responsive single-page dashboard (`frontend/`), served natively by FastAPI at `/` or via Nginx reverse proxy at port `3000`.
- **AI Insights**: Configurable multi-provider engine (Ollama `llama3.1`, Anthropic `claude-sonnet-5`, OpenAI `gpt-4o-mini`, or automatic rule-based fallback).
- **High Availability & Observability**: Kubernetes health and readiness probes (`/health`), Prometheus scrape targets (`/metrics`), Alertmanager webhook receivers (`/api/v1/alerts`), and backward-compatible v1 telemetry endpoints (`/api/v1/runs`).

## API Endpoints

| Category | Method & Endpoint | Description |
|---|---|---|
| **Health & Probes** | `GET /health` | Liveness and readiness probe for Kubernetes and Docker |
| **Observability** | `GET /metrics` | Prometheus metrics scrape endpoint |
| **Executions** | `POST/GET /api/executions`, `GET /api/executions/{id}` | Test suite runs by category and build |
| **Deployments** | `POST/GET /api/deployments`, `GET /api/deployments/stats`, `GET /api/deployments/{id}` | Service deployment tracking and MTTR/duration stats |
| **Defects** | `POST/GET /api/defects`, `PATCH /api/defects/{id}`, `GET /api/defects/priority-summary` | Defect triage, phase detection, and severity distribution |
| **Flakiness** | `POST /api/flakiness/test-cases`, `POST /api/flakiness/runs`, `GET /api/flakiness` | Test flakiness rates and quarantine indicators |
| **Quality Gates** | `POST/GET /api/quality-gates`, `GET /api/quality-gates/summary` | Manual and automated gate pass/fail tracking |
| **Coverage** | `POST/GET /api/coverage`, `GET /api/coverage/summary` | Requirement, code, flow, and API endpoint coverage |
| **Derived Metrics** | `GET /api/metrics/dde`, `/automation-dde`, `/production-leakage`, `/flaky-rate`, `/dashboard` | DDE, Leakage, and category dashboard metrics |
| **AI Insights** | `GET /api/ai/insights?build_id=...` | AI summary and actionable recommendations |
| **Legacy Telemetry** | `POST/GET /api/v1/runs`, `GET /api/v1/runs/{id}`, `GET /api/v1/stats` | Backward-compatible ingestion for CI/CD pipelines |

## Local Development & Running

### Running with Docker Compose

```bash
docker compose -f environments/local/docker-compose.yml up -d --build tracker-backend tracker-frontend
```

- Dashboard UI: `http://localhost:3000` (Nginx) or `http://localhost:8000` (FastAPI)
- Swagger Docs: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/health`
- Prometheus Metrics: `http://localhost:8000/metrics`

### Running Standalone

```bash
cd qe-central-tracking-application
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
