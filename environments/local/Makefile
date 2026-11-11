.PHONY: help up down restart logs ps test clean

help:
	@echo "Available commands:"
	@echo "  make up       - Start all local QE platform services"
	@echo "  make down     - Stop all local services"
	@echo "  make restart  - Restart local services"
	@echo "  make logs     - Tail logs from all containers"
	@echo "  make ps       - List running platform containers"
	@echo "  make test     - Run integration & failover test suites"
	@echo "  make clean    - Remove local containers, volumes, and temporary caches"

up:
	bash setup.sh

down:
	bash stop.sh

restart:
	docker compose restart

logs:
	docker compose logs -f

ps:
	docker compose ps

test:
	pytest ../../tests/

clean:
	bash stop.sh --clean
