# GraphQL Performance Analysis Project with Northwind Database

A comprehensive Docker-based performance analysis system comparing PostgreSQL direct queries vs GraphQL API performance using Hasura, with Redis caching and real-time monitoring.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Grafana       │    │   Prometheus    │    │ Performance     │
│   Dashboard     │◄───┤   Metrics       │◄───┤ Monitor         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                        ▲                        ▲
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Hasura        │    │   Redis         │    │ PostgreSQL      │
│   GraphQL       │◄───┤   Cache         │◄───┤ Northwind       │
│   Engine        │    │   Layer         │    │ 10M+ Records    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

```bash
# Method 1: Automated Setup (Recommended)
./setup.sh

# Method 2: Manual Setup
docker-compose up -d

# Wait for services to start (about 2-3 minutes)
docker-compose logs -f

# Method 3: Using Makefile
make setup                 # Complete setup
make status               # Check service status
make generate-data        # Create 10M+ records (30-60 min)
make performance-test     # Run comprehensive tests
make dashboard           # Open web interface
```

## 🌐 Access URLs

- **Main Dashboard**: http://localhost:8000
- **Hasura Console**: http://localhost:8080 (Admin Secret: `hasura-admin-secret`)
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
  - **Performance Overview**: Real-time system metrics
  - **Database Performance**: PostgreSQL monitoring
  - **Cache Performance**: Redis monitoring  
  - **GraphQL vs SQL Comparison**: Performance analysis
- **Prometheus**: http://localhost:9090

## 📊 Performance Metrics

- **Query Execution Times**: SQL vs GraphQL comparison
- **Cache Performance**: Hit/miss ratios and TTL optimization
- **Concurrent Load**: Multi-user simulation
- **Resource Usage**: CPU, Memory, I/O metrics
- **Index Impact**: Performance with/without proper indexing

## 🔧 Services

| Service | Port | Purpose |
|---------|------|---------|
| PostgreSQL | 5432 | Northwind database with 10M+ records |
| Hasura | 8080 | GraphQL API engine |
| Redis | 6379 | Cache layer |
| Grafana | 3000 | Performance dashboard |
| Prometheus | 9090 | Metrics collection |
| Performance Monitor | 8000 | Custom analysis tools |

## 📈 Test Scenarios

1. **Cold Start Performance**: First-time queries
2. **Warm Cache Performance**: Cached query responses
3. **Complex Queries**: Multi-table JOINs and aggregations
4. **Concurrent Users**: Simultaneous request handling
5. **CRUD Operations**: Insert/Update/Delete performance

## 📋 Data Distribution

- **Customers**: 100,000 records
- **Products**: 10,000 records
- **Orders**: 5,000,000 records
- **Order Details**: 5,000,000+ records
- **Employees**: 1,000 records
- **Categories**: 100 records
- **Suppliers**: 1,000 records
- **Shippers**: 50 records

## 🛠️ Development

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for detailed setup and development instructions.

## 📊 Sample Performance Results

| Query Type | SQL (ms) | GraphQL (ms) | Cache Hit (ms) | Improvement |
|------------|----------|--------------|----------------|-------------|
| Simple Select | 2.3 | 4.1 | 0.8 | 65% faster |
| Complex Join | 145.2 | 178.9 | 12.3 | 91% faster |
| Aggregation | 89.4 | 112.7 | 5.2 | 95% faster |

## 📚 Documentation

- [Setup Guide](docs/SETUP.md)
- [Performance Analysis](docs/PERFORMANCE.md)
- [API Documentation](docs/API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
