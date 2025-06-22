# Northwind Performance Analysis Project Makefile

.PHONY: help setup start stop restart logs clean status test generate-data performance-test

# Default target
help:
	@echo "Northwind Performance Analysis Project"
	@echo "====================================="
	@echo ""
	@echo "Available commands:"
	@echo "  setup          - Initial project setup and start all services"
	@echo "  start          - Start all services"
	@echo "  stop           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  status         - Show service status"
	@echo "  logs           - Show logs for all services"
	@echo "  logs-follow    - Follow logs in real-time"
	@echo "  generate-data  - Generate 10M+ test records"
	@echo "  performance-test - Run comprehensive performance tests"
	@echo "  test           - Run quick health checks"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  clean-data     - Clean up generated data only"
	@echo "  backup         - Create database backup"
	@echo "  restore        - Restore database from backup"
	@echo ""
	@echo "Monitoring:"
	@echo "  dashboard      - Open main dashboard"
	@echo "  grafana        - Open Grafana dashboard"
	@echo "  hasura         - Open Hasura console"
	@echo "  prometheus     - Open Prometheus"
	@echo ""
	@echo "Development:"
	@echo "  shell          - Access performance monitor shell"
	@echo "  db-shell       - Access PostgreSQL shell"
	@echo "  redis-shell    - Access Redis shell"

# Setup and service management
setup:
	@echo "🚀 Setting up Northwind Performance Analysis Project..."
	@./setup.sh

start:
	@echo "🐳 Starting all services..."
	@docker-compose up -d
	@echo "✅ Services started"

stop:
	@echo "🛑 Stopping all services..."
	@docker-compose down
	@echo "✅ Services stopped"

restart:
	@echo "🔄 Restarting all services..."
	@docker-compose restart
	@echo "✅ Services restarted"

status:
	@echo "📊 Service Status:"
	@docker-compose ps

logs:
	@docker-compose logs

logs-follow:
	@docker-compose logs -f

# Data operations
generate-data:
	@echo "📊 Generating 10M+ test records..."
	@docker-compose exec performance-monitor python3 /app/scripts/generate_data.py

performance-test:
	@echo "🧪 Running comprehensive performance tests..."
	@docker-compose exec performance-monitor python3 /app/scripts/run_performance_tests.py

test:
	@echo "🔍 Running health checks..."
	@curl -f http://localhost:8000/health || echo "❌ Performance Monitor not responding"
	@curl -f http://localhost:8080/healthz || echo "❌ Hasura not responding"
	@docker-compose exec postgres pg_isready -U postgres || echo "❌ PostgreSQL not ready"
	@docker-compose exec redis redis-cli ping || echo "❌ Redis not responding"

# Cleanup operations
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	@docker-compose down -v --remove-orphans
	@docker system prune -f
	@echo "✅ Cleanup complete"

clean-data:
	@echo "🧹 Cleaning up generated data..."
	@docker-compose exec postgres psql -U postgres -d northwind -c "TRUNCATE customers, orders, order_details RESTART IDENTITY CASCADE;"
	@docker-compose exec redis redis-cli FLUSHALL
	@echo "✅ Data cleanup complete"

# Backup and restore
backup:
	@echo "💾 Creating database backup..."
	@mkdir -p ./backups
	@docker-compose exec postgres pg_dump -U postgres northwind > ./backups/northwind_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in ./backups/"

restore:
	@echo "📥 Restoring database from backup..."
	@read -p "Enter backup file path: " backup_file; \
	docker-compose exec -T postgres psql -U postgres northwind < $$backup_file
	@echo "✅ Database restored"

# Quick access to dashboards
dashboard:
	@echo "🌐 Opening main dashboard..."
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:8000')" 2>/dev/null || echo "Please open http://localhost:8000 in your browser"

grafana:
	@echo "📊 Opening Grafana dashboard..."
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:3000')" 2>/dev/null || echo "Please open http://localhost:3000 in your browser"

hasura:
	@echo "🔧 Opening Hasura console..."
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:8080')" 2>/dev/null || echo "Please open http://localhost:8080 in your browser"

prometheus:
	@echo "📈 Opening Prometheus..."
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:9090')" 2>/dev/null || echo "Please open http://localhost:9090 in your browser"

# Development shells
shell:
	@echo "🐚 Accessing performance monitor shell..."
	@docker-compose exec performance-monitor bash

db-shell:
	@echo "🐚 Accessing PostgreSQL shell..."
	@docker-compose exec postgres psql -U postgres -d northwind

redis-shell:
	@echo "🐚 Accessing Redis shell..."
	@docker-compose exec redis redis-cli

# Docker operations
build:
	@echo "🔨 Building all containers..."
	@docker-compose build

pull:
	@echo "⬇️ Pulling latest images..."
	@docker-compose pull

# Monitoring operations
metrics:
	@echo "📊 Current system metrics:"
	@curl -s http://localhost:8000/api/v1/stats | python3 -m json.tool

cache-stats:
	@echo "💾 Cache statistics:"
	@docker-compose exec redis redis-cli info memory

db-stats:
	@echo "🗄️ Database statistics:"
	@docker-compose exec postgres psql -U postgres -d northwind -c "SELECT schemaname, tablename, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC;"

# Development helpers
dev-setup:
	@echo "🛠️ Setting up development environment..."
	@cp .env.example .env
	@echo "✅ Environment file created. Edit .env as needed."

update:
	@echo "⬆️ Updating project..."
	@git pull
	@docker-compose build
	@docker-compose up -d
	@echo "✅ Project updated"

# Quick tests
quick-test:
	@echo "⚡ Running quick performance test..."
	@curl -X POST http://localhost:8000/api/v1/performance/run-test/simple_select

load-test:
	@echo "🏋️ Running load test..."
	@curl -X POST http://localhost:8000/api/v1/performance/run-concurrent-test/simple_select

# Report generation
report:
	@echo "📋 Generating performance report..."
	@curl -X POST http://localhost:8000/api/v1/reports/generate

# Environment info
info:
	@echo "ℹ️ Environment Information:"
	@echo "Docker version: $(shell docker --version)"
	@echo "Docker Compose version: $(shell docker-compose --version)"
	@echo "Available memory: $(shell free -h | grep '^Mem:' | awk '{print $$2}')"
	@echo "Available disk space: $(shell df -h . | tail -1 | awk '{print $$4}')"
	@echo ""
	@echo "Service URLs:"
	@echo "  Main Dashboard:    http://localhost:8000"
	@echo "  Hasura Console:    http://localhost:8080"
	@echo "  Grafana:           http://localhost:3000"
	@echo "  Prometheus:        http://localhost:9090"
