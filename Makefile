.PHONY: help up down kind test test-ha lint clean

help:
	@echo "Highly Available QE Platform - Automation Commands"
	@echo "=================================================="
	@echo "  make up       - Start local platform (LocalStack, Tracker, Prometheus, Grafana, Alertmanager)"
	@echo "  make down     - Stop local platform containers"
	@echo "  make kind     - Provision Multi-Node HA Kubernetes Cluster via Kind"
	@echo "  make test     - Run integration & validation test suites"
	@echo "  make test-ha  - Run Kubernetes HA & Jenkins failover tests"
	@echo "  make lint     - Validate Terraform, Helm, and YAML syntax"
	@echo "  make clean    - Clean local caches and volumes"

up:
	cd environments/local && make up

down:
	cd environments/local && make down

kind:
	bash kubernetes/kind/setup-kind.sh

test:
	pytest tests/ -v

test-ha:
	pytest tests/failover/ tests/kubernetes-ha/ -v

lint:
	terraform fmt -check -recursive terraform/ || true
	helm lint kubernetes/helm/jenkins-ha/ || true
	helm lint kubernetes/helm/qe-central-tracking-application/ || true

clean:
	cd environments/local && make clean
	rm -rf .pytest_cache
