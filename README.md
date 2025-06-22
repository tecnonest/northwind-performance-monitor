# 🚀 Northwind Performance Monitor

A comprehensive performance monitoring and testing suite for comparing SQL vs GraphQL performance with real-time metrics, interactive dashboards, and containerized monitoring stack.

![Performance Monitor](https://img.shields.io/badge/Performance-Monitor-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-orange)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-red)

## 📋 Features

### 🔍 Performance Testing
- **SQL vs GraphQL Comparison**: Side-by-side performance analysis
- **Individual Test Execution**: Run specific performance tests
- **Concurrent User Simulation**: Multi-user load testing
- **Comprehensive Test Suites**: Automated test execution
- **Real-time Performance Metrics**: Live monitoring during tests

### 📊 Monitoring & Visualization
- **Interactive Web UI**: Real-time charts and status monitoring
- **Grafana Dashboards**: Professional monitoring dashboards
- **Prometheus Metrics**: Time-series metrics collection
- **System Resource Monitoring**: CPU, Memory, Disk usage
- **Database Performance**: Connection pools, query performance
- **Cache Analytics**: Redis hit/miss ratios and performance

### 🐳 Containerized Stack
- **Docker Compose**: One-command deployment
- **PostgreSQL**: High-performance database with Northwind data
- **Redis**: Caching layer for performance optimization  
- **Hasura**: GraphQL API engine
- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and alerting
- **FastAPI**: Modern Python web framework

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   Performance   │    │   Grafana       │
│   (Chart.js)    │◄───┤   Monitor       ├───►│   Dashboards    │
│                 │    │   (FastAPI)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌────────┼────────┐
                       ▼        ▼        ▼
                 ┌──────────┐ ┌─────┐ ┌─────────┐
                 │PostgreSQL│ │Redis│ │ Hasura  │
                 │          │ │     │ │(GraphQL)│
                 └──────────┘ └─────┘ └─────────┘
                       │        │        │
                       └────────┼────────┘
                                ▼
                       ┌─────────────────┐
                       │   Prometheus    │
                       │   (Metrics)     │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- 8GB+ RAM recommended

### 1. Clone the Repository
```bash
git clone https://github.com/tecnonest/northwind-performance-monitor.git
cd northwind-performance-monitor
```

### 2. Start the Stack
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. Access the Applications

| Service | URL | Credentials |
|---------|-----|-------------|
| **Performance Monitor UI** | http://localhost:8000 | - |
| **Grafana Dashboards** | http://localhost:3000 | admin/admin |
| **Hasura Console** | http://localhost:8080 | - |
| **Prometheus** | http://localhost:9090 | - |

## 📈 Available Dashboards

### 1. Performance Overview
- HTTP request rates and response times
- System resource utilization
- Test execution status
- **URL**: http://localhost:3000/d/northwind-overview

### 2. Database Performance  
- Query execution times
- Connection pool status
- Database size and statistics
- **URL**: http://localhost:3000/d/northwind-database

### 3. Cache Performance
- Redis hit/miss ratios
- Memory usage and keyspace statistics
- Cache operation rates
- **URL**: http://localhost:3000/d/northwind-cache

### 4. GraphQL vs SQL Comparison
- Side-by-side performance metrics
- Response time comparisons
- Query type analysis
- **URL**: http://localhost:3000/d/northwind-comparison

## 🧪 Running Performance Tests

### Via Web UI
1. Open http://localhost:8000
2. Navigate to "Performance Tests" section
3. Click on individual test buttons or "Run All Tests"
4. Monitor progress in "Test Status" section
5. View results in real-time charts

### Via API
```bash
# Run individual test
curl -X POST http://localhost:8000/api/v1/performance/run-test/simple_select

# Run comprehensive tests
curl -X POST http://localhost:8000/api/v1/run-performance-tests

# Check test status
curl http://localhost:8000/api/v1/performance/test-status

# Get test results
curl http://localhost:8000/api/v1/performance/results
```

### Available Test Types
- **simple_select**: Basic SELECT queries
- **customer_orders**: JOIN queries with filtering
- **order_aggregation**: GROUP BY and aggregation
- **complex_join**: Multi-table complex JOINs
- **pagination_test**: LIMIT/OFFSET performance

## 📊 Metrics & Monitoring

### Custom Metrics
- `northwind_http_request_duration_seconds`: HTTP request latencies
- `northwind_http_requests_total`: Total HTTP requests
- `northwind_test_execution_total`: Performance test counters
- `northwind_database_query_duration_seconds`: Database query times

### System Metrics
- CPU, Memory, Disk usage (Node Exporter)
- PostgreSQL metrics (Postgres Exporter)
- Redis metrics (Redis Exporter)

## 🛠️ Development

### Project Structure
```
├── performance-monitor/          # FastAPI application
│   ├── app/
│   │   ├── main.py              # Application entry point
│   │   ├── core/                # Core modules
│   │   ├── api/                 # API routes
│   │   └── templates/           # HTML templates
├── monitoring/                   # Monitoring configuration
│   ├── grafana/                 # Grafana dashboards & config
│   ├── prometheus/              # Prometheus configuration
│   └── sql/                     # Database initialization
├── docker-compose.yml           # Service orchestration
└── Makefile                     # Development commands
```

### Local Development
```bash
# Install dependencies
cd performance-monitor
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
black app/
isort app/
```

### Environment Variables
```bash
# Database
POSTGRES_DB=northwind
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Redis
REDIS_URL=redis://redis:6379

# Hasura
HASURA_GRAPHQL_DATABASE_URL=postgresql://postgres:password@postgres:5432/northwind
HASURA_GRAPHQL_ADMIN_SECRET=admin_secret
```

## 🐳 Docker Services

| Service | Image | Purpose |
|---------|-------|---------|
| **performance-monitor** | Custom FastAPI | Main application |
| **postgres** | postgres:15-alpine | Database |
| **redis** | redis:7-alpine | Caching |
| **hasura** | hasura/graphql-engine | GraphQL API |
| **prometheus** | prom/prometheus | Metrics collection |
| **grafana** | grafana/grafana | Visualization |
| **postgres-exporter** | postgres_exporter | Database metrics |
| **redis-exporter** | redis_exporter | Cache metrics |
| **node-exporter** | node_exporter | System metrics |

## 📚 API Documentation

### Interactive API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints
- `GET /api/v1/stats` - System and database statistics
- `POST /api/v1/performance/run-test/{test_name}` - Run individual test
- `GET /api/v1/performance/test-status` - Test execution status
- `GET /api/v1/performance/results` - Test results
- `GET /metrics` - Prometheus metrics

## 🔧 Configuration

### Grafana Dashboards
Dashboards are automatically provisioned from `monitoring/grafana/dashboards/`

### Prometheus Targets
Configured in `monitoring/prometheus/prometheus.yml`

### Database Schema
Northwind sample database is loaded automatically from `monitoring/sql/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Northwind Database**: Classic sample database
- **FastAPI**: Modern Python web framework
- **Grafana**: Beautiful monitoring dashboards
- **Prometheus**: Reliable metrics collection
- **Docker**: Containerization platform

## 📞 Support

- 📧 Issues: [GitHub Issues](https://github.com/tecnonest/northwind-performance-monitor/issues)
- 📖 Documentation: Check this README and API docs
- 💬 Discussions: [GitHub Discussions](https://github.com/tecnonest/northwind-performance-monitor/discussions)

---

**Made with ❤️ for the open source community**
