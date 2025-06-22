# Setup Guide

## Prerequisites

- Docker 20.0+ and Docker Compose 2.0+
- At least 8GB RAM available for containers
- 50GB free disk space for data generation
- Network access for downloading images

## Quick Start

1. **Clone and Navigate**
```bash
git clone <repository-url>
cd webapitest
```

2. **Run Setup Script**
```bash
./setup.sh
```

3. **Access Dashboard**
- Open http://localhost:8000 in your browser
- The setup script will show all available endpoints

## Manual Setup

If you prefer manual setup or encounter issues:

### 1. Start Services
```bash
docker-compose up -d
```

### 2. Wait for Services
```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Verify Health
```bash
curl http://localhost:8000/health
curl http://localhost:8080/healthz
```

## Service Configuration

### PostgreSQL Database
- **Port**: 5432
- **Database**: northwind
- **User**: postgres
- **Password**: postgres
- **Connection String**: `postgres://postgres:postgres@localhost:5432/northwind`

### Hasura GraphQL Engine
- **Port**: 8080
- **Admin Secret**: `hasura-admin-secret`
- **GraphQL Endpoint**: http://localhost:8080/v1/graphql
- **Console**: http://localhost:8080/console

### Redis Cache
- **Port**: 6379
- **No authentication** (development setup)
- **Connection String**: `redis://localhost:6379`

### Performance Monitor
- **Port**: 8000
- **Web Interface**: http://localhost:8000
- **API Base**: http://localhost:8000/api/v1

### Monitoring Stack
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **PostgreSQL Exporter**: http://localhost:9187/metrics
- **Redis Exporter**: http://localhost:9121/metrics

## Data Generation

### Option 1: Web Interface
1. Go to http://localhost:8000
2. Click "Generate Data" button
3. Monitor progress in the dashboard

### Option 2: Command Line
```bash
docker-compose exec performance-monitor python /app/scripts/generate_data.py
```

### Expected Data Volumes
- **Customers**: 100,000 records
- **Orders**: 5,000,000 records
- **Order Details**: 5,000,000+ records
- **Products**: 10,000 records
- **Employees**: 1,000 records
- **Suppliers**: 1,000 records
- **Categories**: 20 records
- **Shippers**: 50 records

**Total**: 10+ million records
**Estimated Time**: 30-60 minutes
**Disk Space**: ~10-15GB

## Performance Testing

### Option 1: Web Interface
1. Ensure data generation is complete
2. Go to http://localhost:8000
3. Run individual tests or comprehensive suite

### Option 2: Command Line
```bash
docker-compose exec performance-monitor python /app/scripts/run_performance_tests.py
```

### Test Types
- **Simple Queries**: Basic SELECT operations
- **Complex JOINs**: Multi-table relationships
- **Aggregations**: COUNT, SUM, AVG operations
- **Concurrent Load**: Multiple simultaneous users
- **Cache Performance**: With and without Redis

## Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check Docker resources
docker system df
docker system prune

# Check ports
netstat -tulpn | grep -E "(5432|6379|8000|8080|3000|9090)"

# Restart services
docker-compose down
docker-compose up -d
```

#### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Test connection
docker-compose exec postgres psql -U postgres -d northwind -c "SELECT 1;"
```

#### Performance Monitor Issues
```bash
# Check application logs
docker-compose logs performance-monitor

# Restart service
docker-compose restart performance-monitor
```

#### Memory Issues
```bash
# Check memory usage
docker stats

# Adjust memory limits in docker-compose.yml
# Increase system memory or reduce concurrent operations
```

### Log Locations
- **Application logs**: `./logs/application.log`
- **Performance logs**: `./logs/performance.log`
- **Error logs**: `./logs/errors.log`
- **Docker logs**: `docker-compose logs [service]`

### Data Persistence
- **PostgreSQL data**: `postgres_data` volume
- **Redis data**: `redis_data` volume (not persistent by default)
- **Grafana data**: `grafana_data` volume
- **Prometheus data**: `prometheus_data` volume
- **Reports**: `./reports/` directory
- **Logs**: `./logs/` directory

## Environment Variables

Create `.env` file to customize settings:

```bash
# Database
POSTGRES_URL=postgres://postgres:postgres@postgres:5432/northwind

# GraphQL
HASURA_URL=http://hasura:8080/v1/graphql
HASURA_ADMIN_SECRET=hasura-admin-secret

# Cache
REDIS_URL=redis://redis:6379
CACHE_TTL_SECONDS=300

# Performance
MAX_CONCURRENT_REQUESTS=100
TEST_DURATION_SECONDS=300
BATCH_SIZE=10000

# Paths
REPORT_OUTPUT_DIR=/app/reports
LOG_OUTPUT_DIR=/app/logs
```

## Security Notes

⚠️ **This setup is for development/testing only**

- Database has default credentials
- Redis has no authentication
- Hasura admin secret is hardcoded
- Services are exposed on all interfaces

For production deployment:
- Change all default credentials
- Enable authentication/authorization
- Use environment variables for secrets
- Configure proper firewall rules
- Enable TLS/SSL encryption
