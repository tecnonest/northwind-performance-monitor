# Project Structure

```
webapitest/
├── README.md                           # Project overview and quick start
├── docker-compose.yml                  # Docker services orchestration
├── setup.sh                           # Automated setup script
├── .env.example                        # Environment variables template
│
├── database/                           # PostgreSQL configuration
│   ├── init/
│   │   ├── 01-schema.sql              # Database schema definition
│   │   └── 02-seed-data.sql           # Initial seed data
│   └── config/
│       └── postgresql.conf            # Optimized PostgreSQL settings
│
├── cache/                              # Redis configuration
│   └── redis.conf                     # Redis performance settings
│
├── hasura/                             # Hasura GraphQL configuration
│   ├── config.yaml                    # Hasura project config
│   ├── metadata/                      # GraphQL schema metadata
│   │   └── databases/
│   │       └── default/
│   │           └── tables/
│   │               └── tables.yaml    # Table relationships & permissions
│   └── migrations/                    # Database migrations (auto-generated)
│
├── performance-monitor/                # Performance testing application
│   ├── Dockerfile                     # Performance monitor container
│   ├── requirements.txt               # Python dependencies
│   ├── app/
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── core/                      # Core application modules
│   │   │   ├── config.py              # Configuration management
│   │   │   ├── database.py            # Database connection & operations
│   │   │   ├── cache.py               # Redis cache management
│   │   │   ├── performance.py         # Performance analysis engine
│   │   │   └── data_generator.py      # 10M+ records data generator
│   │   ├── api/                       # REST API endpoints
│   │   │   └── routes/
│   │   │       ├── performance.py     # Performance testing endpoints
│   │   │       ├── reports.py         # Report generation endpoints
│   │   │       └── admin.py           # Administrative endpoints
│   │   └── utils/
│   │       └── logger.py              # Logging configuration
│   ├── templates/
│   │   └── dashboard.html             # Web dashboard interface
│   ├── static/                        # Static web assets (CSS, JS, images)
│   └── scripts/
│       ├── generate_data.py           # Standalone data generation
│       └── run_performance_tests.py   # Standalone performance testing
│
├── monitoring/                         # Monitoring and observability
│   ├── prometheus/                    # Prometheus configuration
│   │   ├── prometheus.yml             # Scraping configuration
│   │   └── rules/
│   │       └── performance.yml        # Alerting rules
│   └── grafana/                       # Grafana configuration
│       ├── provisioning/
│       │   ├── dashboards/
│       │   │   └── dashboard.yml      # Dashboard provisioning
│       │   └── datasources/
│       │       └── prometheus.yml     # Prometheus datasource
│       └── dashboards/                # Pre-built dashboards
│           ├── performance-overview.json
│           ├── database-metrics.json
│           └── cache-analysis.json
│
├── docs/                              # Documentation
│   ├── SETUP.md                      # Detailed setup instructions
│   ├── PERFORMANCE.md                 # Performance analysis guide
│   ├── API.md                         # API documentation
│   ├── DEVELOPMENT.md                 # Development guide
│   └── TROUBLESHOOTING.md             # Common issues and solutions
│
├── reports/                           # Generated performance reports
│   └── (auto-generated files)
│
├── logs/                              # Application logs
│   ├── application.log                # General application logs
│   ├── performance.log                # Performance-specific logs
│   └── errors.log                     # Error logs
│
└── data/                              # Data exports and backups
    └── (auto-generated files)
```

## Key Features by Directory

### Database (`database/`)
- **Complete Northwind Schema**: All tables with relationships and constraints
- **Performance Optimized**: Indexes, constraints, and PostgreSQL tuning
- **10M+ Records Support**: Schema designed for massive datasets
- **Seed Data**: Initial categories, suppliers, employees for testing

### Cache (`cache/`)
- **Redis Configuration**: Optimized for high-throughput caching
- **Memory Management**: LRU eviction and memory limits
- **Performance Tuning**: Disabled persistence for speed in testing

### GraphQL (`hasura/`)
- **Complete Schema**: All table relationships and permissions
- **Hasura Metadata**: Tracked tables, relationships, permissions
- **Query Optimization**: Automatic query planning and execution
- **Real-time Subscriptions**: WebSocket support for live data

### Performance Monitor (`performance-monitor/`)
- **FastAPI Application**: Modern Python web framework
- **Async Operations**: Non-blocking database and cache operations
- **Web Dashboard**: Beautiful Bootstrap-based interface
- **REST API**: Comprehensive API for all operations
- **Data Generation**: Faker-based realistic data creation
- **Performance Analysis**: Statistical analysis and comparison

### Monitoring (`monitoring/`)
- **Prometheus**: Metrics collection from all services
- **Grafana**: Beautiful dashboards for visualization
- **Alerting**: Performance threshold monitoring
- **Exporters**: PostgreSQL, Redis, and system metrics

### Documentation (`docs/`)
- **Setup Guide**: Step-by-step installation and configuration
- **Performance Guide**: Analysis methodology and interpretation
- **API Documentation**: Complete endpoint documentation
- **Troubleshooting**: Common issues and solutions

## Service Architecture

### Core Services
1. **PostgreSQL**: Primary data storage with performance optimization
2. **Redis**: High-speed caching layer
3. **Hasura**: GraphQL API engine with automatic optimization
4. **Performance Monitor**: Custom analysis and web interface

### Monitoring Stack
1. **Prometheus**: Metrics collection and storage
2. **Grafana**: Visualization and dashboards
3. **Exporters**: Service-specific metric collection
4. **Node Exporter**: System-level metrics

### Data Flow
```
Client Request → Performance Monitor → [SQL Direct | GraphQL via Hasura] → PostgreSQL
                      ↓                           ↓
                 Redis Cache ←----- Cache Check/Store
                      ↓
              Prometheus Metrics ← Performance Data
                      ↓
                Grafana Dashboard ← Visualization
```

## Performance Testing Workflow

### 1. Environment Setup
- Docker Compose orchestration
- Service health verification
- Initial seed data loading

### 2. Data Generation
- 100,000 customers
- 5,000,000 orders
- 5,000,000+ order details
- 10,000 products
- Supporting reference data

### 3. Performance Analysis
- SQL direct query testing
- GraphQL query testing
- Cache performance analysis
- Concurrent user simulation
- Resource utilization monitoring

### 4. Results & Reporting
- Statistical analysis
- Performance comparison
- Optimization recommendations
- Automated report generation

## Customization Points

### Environment Variables
- Database connection settings
- Cache configuration
- Test parameters
- Output directories

### Test Scenarios
- Custom query definitions
- Load testing parameters
- Concurrent user simulation
- Cache strategies

### Monitoring & Alerting
- Custom Prometheus rules
- Grafana dashboard customization
- Alert notification settings
- Performance thresholds

### Data Generation
- Record count configuration
- Data distribution settings
- Realistic data patterns
- Custom data generators
