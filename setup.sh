#!/bin/bash

# Northwind Performance Analysis Project Setup Script
# This script initializes and starts the entire performance testing environment

set -e

echo "🚀 Northwind Performance Analysis Setup"
echo "========================================"

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p reports logs data

# Set proper permissions
chmod 755 reports logs data

echo "✅ Directories created"

# Start the services
echo "🐳 Starting Docker services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

# Wait for PostgreSQL
echo "   Waiting for PostgreSQL..."
until docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do
    printf '.'
    sleep 2
done
echo " ✅ PostgreSQL is ready"

# Wait for Redis
echo "   Waiting for Redis..."
until docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; do
    printf '.'
    sleep 2
done
echo " ✅ Redis is ready"

# Wait for Hasura
echo "   Waiting for Hasura..."
until curl -f http://localhost:8080/healthz > /dev/null 2>&1; do
    printf '.'
    sleep 2
done
echo " ✅ Hasura is ready"

# Wait for Performance Monitor
echo "   Waiting for Performance Monitor..."
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    printf '.'
    sleep 2
done
echo " ✅ Performance Monitor is ready"

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📊 Access Points:"
echo "   • Main Dashboard:     http://localhost:8000"
echo "   • Hasura Console:     http://localhost:8080"
echo "   • Grafana Dashboard:  http://localhost:3000 (admin/admin)"
echo "   • Prometheus:         http://localhost:9090"
echo ""
echo "📋 Next Steps:"
echo "   1. Open http://localhost:8000 to access the main dashboard"
echo "   2. Click 'Generate Data' to create 10M+ test records (30-60 minutes)"
echo "   3. Run performance tests to compare SQL vs GraphQL"
echo "   4. View detailed metrics in Grafana dashboard"
echo ""
echo "🛠️ Useful Commands:"
echo "   • View logs:          docker-compose logs -f [service]"
echo "   • Stop services:      docker-compose down"
echo "   • Restart services:   docker-compose restart"
echo "   • View status:        docker-compose ps"
echo ""
echo "📖 For detailed documentation, see README.md"
