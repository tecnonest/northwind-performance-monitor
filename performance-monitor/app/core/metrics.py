"""
Prometheus metrics for the performance monitor application
"""

from prometheus_client import Counter, Histogram, Gauge, Info

# Application info
app_info = Info('northwind_app_info', 'Application information')
app_info.info({'version': '1.0.0', 'environment': 'production'})

# HTTP metrics
http_requests_total = Counter(
    'northwind_http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'northwind_http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'endpoint']
)

# Database metrics
db_queries_total = Counter(
    'northwind_db_queries_total',
    'Total number of database queries',
    ['query_type', 'status']
)

db_query_duration_seconds = Histogram(
    'northwind_db_query_duration_seconds',
    'Duration of database queries in seconds',
    ['query_type']
)

db_connections_active = Gauge(
    'northwind_db_connections_active',
    'Number of active database connections'
)

# Cache metrics
cache_operations_total = Counter(
    'northwind_cache_operations_total',
    'Total number of cache operations',
    ['operation', 'status']
)

cache_hit_rate = Gauge(
    'northwind_cache_hit_rate',
    'Cache hit rate as a percentage'
)

# Performance test metrics
performance_tests_total = Counter(
    'northwind_performance_tests_total',
    'Total number of performance tests executed',
    ['test_type', 'status']
)

performance_test_duration_seconds = Histogram(
    'northwind_performance_test_duration_seconds',
    'Duration of performance tests in seconds',
    ['test_type']
)

# System metrics
system_cpu_usage = Gauge(
    'northwind_system_cpu_usage_percent',
    'Current CPU usage percentage'
)

system_memory_usage = Gauge(
    'northwind_system_memory_usage_percent', 
    'Current memory usage percentage'
)

system_disk_usage = Gauge(
    'northwind_system_disk_usage_percent',
    'Current disk usage percentage'
)
