#!/usr/bin/make -f

# Configurare compose
COMPOSE=docker compose
COMPOSE_FILE=-f docker-compose.yml -f docker-compose.local.yml
COMPOSE_PROD=-f docker-compose.yml -f docker-compose.prod.yml

default: help

help: ## Display this help screen
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

# Development commands
build: ## Build containers for development
	$(COMPOSE) $(COMPOSE_FILE) build
.PHONY: build

up: ## Start development environment
	$(COMPOSE) $(COMPOSE_FILE) up
.PHONY: up

up-d: ## Start development environment in detached mode
	$(COMPOSE) $(COMPOSE_FILE) up -d
.PHONY: up-d

down: ## Stop development environment
	$(COMPOSE) $(COMPOSE_FILE) down
.PHONY: down

down-v: ## Stop development environment and remove volumes
	$(COMPOSE) $(COMPOSE_FILE) down -v
.PHONY: down-v

# Linting commands
lint: ## Run ruff linter
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend ruff check budget/
.PHONY: lint

lint-fix: ## Fix linting issues automatically
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend ruff check --fix budget/
.PHONY: lint-fix

format: ## Format code using ruff
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend ruff format budget/
.PHONY: format

# Database commands
makemigrations: ## Create new migrations
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py makemigrations
.PHONY: makemigrations

migrate: ## Apply migrations
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py migrate
.PHONY: migrate

migrateq: ## Apply Django-Q migrations
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py migrate django_q
.PHONY: migrateq

migrations: makemigrations migrate ## Create and apply migrations
.PHONY: migrations

createsuperuser: ## Create a superuser
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py createsuperuser
.PHONY: createsuperuser

createdefaultsuperuser: ## Create a superuser
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py createdefaultsuperuser
.PHONY: createdefaultsuperuser

seed: ## Seed database with random data
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py seed
.PHONY: seed

clear: ## Clear database except for superusers
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py clear
.PHONY: clear

seeddemo: ## Seed database with demo data
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py seeddemo
.PHONY: seeddemo

cleardemo: ## Clear demo data
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py cleardemo
.PHONY: cleardemo

# Testing
test: ## Run tests
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python -m pytest budget/
.PHONY: test

# Logs
logs: ## View logs from all containers
	$(COMPOSE) $(COMPOSE_FILE) logs -f
.PHONY: logs

# Production commands
build-prod: ## Build containers for production
	$(COMPOSE) $(COMPOSE_PROD) build
.PHONY: build-prod

up-prod: ## Start production environment (detached)
	$(COMPOSE) $(COMPOSE_PROD) up -d
.PHONY: up-prod

down-prod: ## Stop production environment
	$(COMPOSE) $(COMPOSE_PROD) down
.PHONY: down-prod

# Django-Q commands
qcluster: ## Start Django-Q cluster
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py qcluster
.PHONY: qcluster

qmonitor: ## Monitor Django-Q cluster
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py qmonitor
.PHONY: qmonitor

qinfo: ## Show Django-Q info
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py qinfo
.PHONY: qinfo

qhealth: ## Check Django-Q health
	$(COMPOSE) $(COMPOSE_FILE) run --rm backend python budget/manage.py qhealth
.PHONY: qhealth
