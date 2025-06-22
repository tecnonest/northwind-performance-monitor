"""
Performance analyzer for comparing SQL vs GraphQL performance
"""

import asyncio
import json
import logging
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import statistics

import aiohttp
import psutil

from core.config import settings
from core.database import DatabaseManager
from core.cache import CacheManager

logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    """Analyzes and compares performance between SQL and GraphQL queries"""
    
    def __init__(self, db_manager: DatabaseManager, cache_manager: CacheManager):
        self.db_manager = db_manager
        self.cache_manager = cache_manager
        self.test_results = []
        self.test_status = "idle"
        
        # Test queries for performance comparison
        self.test_queries = self._get_test_queries()
    
    def _get_test_queries(self) -> Dict[str, Dict]:
        """Get predefined test queries for performance analysis"""
        return {
            "simple_select": {
                "sql": "SELECT customer_id, company_name, city, country FROM customers LIMIT 100;",
                "graphql": """
                    query {
                        customers(limit: 100) {
                            customer_id
                            company_name
                            city
                            country
                        }
                    }
                """,
                "description": "Simple SELECT query with LIMIT"
            },
            "customer_orders": {
                "sql": """
                    SELECT c.customer_id, c.company_name, o.order_id, o.order_date, o.freight
                    FROM customers c
                    JOIN orders o ON c.customer_id = o.customer_id
                    WHERE c.country = 'USA'
                    ORDER BY o.order_date DESC
                    LIMIT 1000;
                """,
                "graphql": """
                    query {
                        customers(where: {country: {_eq: "USA"}}) {
                            customer_id
                            company_name
                            orders(order_by: {order_date: desc}, limit: 1000) {
                                order_id
                                order_date
                                freight
                            }
                        }
                    }
                """,
                "description": "JOIN query with filtering and ordering"
            },
            "order_aggregation": {
                "sql": """
                    SELECT 
                        DATE_TRUNC('month', order_date) as month,
                        COUNT(*) as order_count,
                        SUM(freight) as total_freight,
                        AVG(freight) as avg_freight
                    FROM orders
                    WHERE order_date >= '2023-01-01'
                    GROUP BY DATE_TRUNC('month', order_date)
                    ORDER BY month;
                """,
                "graphql": """
                    query {
                        orders_aggregate(
                            where: {order_date: {_gte: "2023-01-01"}}
                        ) {
                            aggregate {
                                count
                                sum {
                                    freight
                                }
                                avg {
                                    freight
                                }
                            }
                        }
                    }
                """,
                "description": "Aggregation query with date filtering"
            },
            "complex_join": {
                "sql": """
                    SELECT 
                        c.company_name,
                        p.product_name,
                        cat.category_name,
                        s.company_name as supplier_name,
                        od.quantity,
                        od.unit_price,
                        od.line_total,
                        o.order_date
                    FROM customers c
                    JOIN orders o ON c.customer_id = o.customer_id
                    JOIN order_details od ON o.order_id = od.order_id
                    JOIN products p ON od.product_id = p.product_id
                    JOIN categories cat ON p.category_id = cat.category_id
                    JOIN suppliers s ON p.supplier_id = s.supplier_id
                    WHERE o.order_date >= '2024-01-01'
                    ORDER BY o.order_date DESC, od.line_total DESC
                    LIMIT 500;
                """,
                "graphql": """
                    query {
                        orders(
                            where: {order_date: {_gte: "2024-01-01"}},
                            order_by: [{order_date: desc}, {order_details: {line_total: desc}}],
                            limit: 500
                        ) {
                            order_date
                            customer {
                                company_name
                            }
                            order_details {
                                quantity
                                unit_price
                                line_total
                                product {
                                    product_name
                                    category {
                                        category_name
                                    }
                                    supplier {
                                        company_name
                                    }
                                }
                            }
                        }
                    }
                """,
                "description": "Complex multi-table JOIN query"
            },
            "pagination_test": {
                "sql": """
                    SELECT customer_id, company_name, contact_name, city, country
                    FROM customers
                    ORDER BY customer_id
                    OFFSET 1000 LIMIT 100;
                """,
                "graphql": """
                    query {
                        customers(
                            order_by: {customer_id: asc},
                            offset: 1000,
                            limit: 100
                        ) {
                            customer_id
                            company_name
                            contact_name
                            city
                            country
                        }
                    }
                """,
                "description": "Pagination performance test"
            }
        }
    
    async def execute_sql_query(self, query: str, use_cache: bool = False) -> Dict[str, Any]:
        """Execute SQL query and measure performance"""
        cache_hit = False
        cache_time = 0
        
        if use_cache:
            # Check cache first
            cached_result = await self.cache_manager.get_cached_query(query)
            if cached_result:
                return {
                    "data": cached_result["data"],
                    "execution_time_ms": cached_result["cache_retrieval_time_ms"],
                    "row_count": len(cached_result["data"]),
                    "cache_hit": True,
                    "query_type": "sql"
                }
        
        # Execute query
        start_time = time.time()
        try:
            result, execution_time = await self.db_manager.execute_query_async(query)
            
            response = {
                "data": result,
                "execution_time_ms": execution_time,
                "row_count": len(result),
                "cache_hit": False,
                "query_type": "sql"
            }
            
            # Cache result if caching is enabled
            if use_cache:
                await self.cache_manager.cache_query_result(query, result)
            
            return response
            
        except Exception as e:
            logger.error(f"SQL query execution failed: {e}")
            return {
                "error": str(e),
                "execution_time_ms": (time.time() - start_time) * 1000,
                "query_type": "sql"
            }
    
    async def execute_graphql_query(self, query: str, use_cache: bool = False) -> Dict[str, Any]:
        """Execute GraphQL query and measure performance"""
        if use_cache:
            # Check cache first
            cached_result = await self.cache_manager.get_cached_query(query)
            if cached_result:
                return {
                    "data": cached_result["data"],
                    "execution_time_ms": cached_result["cache_retrieval_time_ms"],
                    "cache_hit": True,
                    "query_type": "graphql"
                }
        
        # Execute GraphQL query
        start_time = time.time()
        try:
            headers = {
                "Content-Type": "application/json",
                "x-hasura-admin-secret": settings.HASURA_ADMIN_SECRET
            }
            
            payload = {"query": query}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    settings.HASURA_URL,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    execution_time = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        response_data = {
                            "data": result.get("data", {}),
                            "execution_time_ms": execution_time,
                            "cache_hit": False,
                            "query_type": "graphql"
                        }
                        
                        # Cache result if caching is enabled
                        if use_cache and "errors" not in result:
                            await self.cache_manager.cache_query_result(query, result.get("data", {}))
                        
                        if "errors" in result:
                            response_data["errors"] = result["errors"]
                        
                        return response_data
                    else:
                        error_text = await response.text()
                        return {
                            "error": f"HTTP {response.status}: {error_text}",
                            "execution_time_ms": execution_time,
                            "query_type": "graphql"
                        }
                        
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"GraphQL query execution failed: {e}")
            return {
                "error": str(e),
                "execution_time_ms": execution_time,
                "query_type": "graphql"
            }
    
    async def run_single_test(self, test_name: str, iterations: int = 10, 
                            use_cache: bool = False) -> Dict[str, Any]:
        """Run a single performance test with multiple iterations"""
        if test_name not in self.test_queries:
            raise ValueError(f"Unknown test: {test_name}")
        
        test_config = self.test_queries[test_name]
        sql_results = []
        graphql_results = []
        
        logger.info(f"Running test '{test_name}' with {iterations} iterations (cache: {use_cache})")
        
        # Run SQL tests
        for i in range(iterations):
            result = await self.execute_sql_query(test_config["sql"], use_cache)
            sql_results.append(result)
            
            # Small delay between iterations
            await asyncio.sleep(0.1)
        
        # Run GraphQL tests
        for i in range(iterations):
            result = await self.execute_graphql_query(test_config["graphql"], use_cache)
            graphql_results.append(result)
            
            # Small delay between iterations
            await asyncio.sleep(0.1)
        
        # Calculate statistics
        sql_times = [r["execution_time_ms"] for r in sql_results if "error" not in r]
        graphql_times = [r["execution_time_ms"] for r in graphql_results if "error" not in r]
        
        test_result = {
            "test_name": test_name,
            "description": test_config["description"],
            "iterations": iterations,
            "use_cache": use_cache,
            "timestamp": datetime.utcnow().isoformat(),
            "sql_stats": self._calculate_stats(sql_times) if sql_times else None,
            "graphql_stats": self._calculate_stats(graphql_times) if graphql_times else None,
            "sql_results": sql_results,
            "graphql_results": graphql_results
        }
        
        # Add comparison metrics
        if sql_times and graphql_times:
            sql_avg = statistics.mean(sql_times)
            graphql_avg = statistics.mean(graphql_times)
            
            test_result["comparison"] = {
                "sql_avg_ms": sql_avg,
                "graphql_avg_ms": graphql_avg,
                "performance_difference_percent": ((graphql_avg - sql_avg) / sql_avg) * 100,
                "faster_option": "sql" if sql_avg < graphql_avg else "graphql"
            }
        
        return test_result
    
    def _calculate_stats(self, times: List[float]) -> Dict[str, float]:
        """Calculate statistical metrics for execution times"""
        if not times:
            return {}
        
        return {
            "min_ms": min(times),
            "max_ms": max(times),
            "avg_ms": statistics.mean(times),
            "median_ms": statistics.median(times),
            "std_dev_ms": statistics.stdev(times) if len(times) > 1 else 0,
            "p95_ms": statistics.quantiles(times, n=20)[18] if len(times) >= 20 else max(times),
            "p99_ms": statistics.quantiles(times, n=100)[98] if len(times) >= 100 else max(times)
        }
    
    async def run_concurrent_test(self, test_name: str, concurrent_users: int = 10, 
                                duration_seconds: int = 60) -> Dict[str, Any]:
        """Run concurrent user simulation test"""
        logger.info(f"Running concurrent test '{test_name}' with {concurrent_users} users for {duration_seconds}s")
        
        self.test_status = "running_concurrent"
        
        if test_name not in self.test_queries:
            raise ValueError(f"Unknown test: {test_name}")
        
        test_config = self.test_queries[test_name]
        results = []
        start_time = time.time()
        
        async def user_simulation(user_id: int):
            """Simulate a single user's queries"""
            user_results = []
            user_start = time.time()
            
            while (time.time() - start_time) < duration_seconds:
                # Alternate between SQL and GraphQL
                if len(user_results) % 2 == 0:
                    result = await self.execute_sql_query(test_config["sql"])
                    result["user_id"] = user_id
                else:
                    result = await self.execute_graphql_query(test_config["graphql"])
                    result["user_id"] = user_id
                
                user_results.append(result)
                
                # Random delay between requests (0.5-2 seconds)
                await asyncio.sleep(random.uniform(0.5, 2.0))
            
            return user_results
        
        # Run concurrent users
        tasks = [user_simulation(i) for i in range(concurrent_users)]
        all_user_results = await asyncio.gather(*tasks)
        
        # Flatten results
        for user_results in all_user_results:
            results.extend(user_results)
        
        self.test_status = "idle"
        
        # Analyze results
        sql_results = [r for r in results if r.get("query_type") == "sql" and "error" not in r]
        graphql_results = [r for r in results if r.get("query_type") == "graphql" and "error" not in r]
        error_results = [r for r in results if "error" in r]
        
        return {
            "test_name": f"{test_name}_concurrent",
            "concurrent_users": concurrent_users,
            "duration_seconds": duration_seconds,
            "total_requests": len(results),
            "successful_requests": len(sql_results) + len(graphql_results),
            "error_rate_percent": (len(error_results) / len(results)) * 100 if results else 0,
            "requests_per_second": len(results) / duration_seconds,
            "sql_stats": self._calculate_stats([r["execution_time_ms"] for r in sql_results]),
            "graphql_stats": self._calculate_stats([r["execution_time_ms"] for r in graphql_results]),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def run_comprehensive_tests(self):
        """Run all performance tests"""
        logger.info("Starting comprehensive performance tests...")
        self.test_status = "running_comprehensive"
        self.test_results = []
        
        try:
            # Test scenarios
            scenarios = [
                {"cache": False, "iterations": 10},
                {"cache": True, "iterations": 10},
                {"cache": False, "iterations": 50},  # Load test
            ]
            
            for scenario in scenarios:
                for test_name in self.test_queries.keys():
                    test_result = await self.run_single_test(
                        test_name, 
                        iterations=scenario["iterations"],
                        use_cache=scenario["cache"]
                    )
                    self.test_results.append(test_result)
            
            # Run concurrent tests
            for test_name in ["simple_select", "customer_orders"]:
                concurrent_result = await self.run_concurrent_test(
                    test_name, 
                    concurrent_users=20, 
                    duration_seconds=60
                )
                self.test_results.append(concurrent_result)
            
            self.test_status = "completed"
            logger.info("Comprehensive performance tests completed")
            
        except Exception as e:
            self.test_status = "failed"
            logger.error(f"Comprehensive tests failed: {e}")
            raise
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get current system performance statistics"""
        # CPU and Memory stats
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database stats
        db_stats = await self.db_manager.get_table_stats()
        connection_stats = await self.db_manager.get_connection_stats()
        
        # Cache stats
        cache_stats = await self.cache_manager.get_cache_stats()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / (1024**3),
                "memory_total_gb": memory.total / (1024**3),
                "disk_percent": disk.percent,
                "disk_used_gb": disk.used / (1024**3),
                "disk_total_gb": disk.total / (1024**3)
            },
            "database": {
                "table_stats": db_stats,
                "connections": connection_stats
            },
            "cache": cache_stats
        }
    
    async def get_test_status(self) -> Dict[str, Any]:
        """Get current test execution status"""
        return {
            "status": self.test_status,
            "completed_tests": len(self.test_results),
            "last_update": datetime.utcnow().isoformat()
        }
    
    def get_test_results(self) -> List[Dict[str, Any]]:
        """Get all test results"""
        return self.test_results
        
    async def run_individual_test(self, test_name: str, iterations: int = 10, use_cache: bool = False) -> Dict[str, Any]:
        """Run a single performance test"""
        logger.info(f"Running individual test '{test_name}' with {iterations} iterations (cache: {use_cache})")
        
        if test_name not in self.test_queries:
            raise ValueError(f"Unknown test: {test_name}")
        
        self.test_status = "running_individual"
        
        try:
            test_config = self.test_queries[test_name]
            sql_query = test_config["sql"]
            graphql_query = test_config["graphql"]
            
            # Run SQL test
            sql_results = []
            for i in range(iterations):
                start_time = time.time()
                _, sql_time = await self.db_manager.execute_query_async(sql_query)
                sql_results.append(sql_time)
            
            # Run GraphQL test  
            graphql_results = []
            for i in range(iterations):
                result = await self.execute_graphql_query(graphql_query, use_cache)
                if "error" not in result:
                    graphql_results.append(result["execution_time_ms"] / 1000.0)  # Convert to seconds
                else:
                    graphql_results.append(0)
            
            # Calculate statistics
            avg_sql_time = sum(sql_results) / len(sql_results)
            avg_graphql_time = sum(graphql_results) / len(graphql_results)
            
            test_result = {
                "test_name": test_name,
                "timestamp": datetime.utcnow().isoformat(),
                "iterations": iterations,
                "use_cache": use_cache,
                "sql_time": avg_sql_time,
                "graphql_time": avg_graphql_time,
                "sql_times": sql_results,
                "graphql_times": graphql_results,
                "performance_ratio": avg_graphql_time / avg_sql_time if avg_sql_time > 0 else 0
            }
            
            self.test_results.append(test_result)
            self.test_status = "completed"
            
            logger.info(f"Individual test '{test_name}' completed. SQL: {avg_sql_time:.3f}s, GraphQL: {avg_graphql_time:.3f}s")
            
            return test_result
            
        except Exception as e:
            logger.error(f"Individual test '{test_name}' failed: {e}")
            self.test_status = "failed"
            raise
        finally:
            # Reset status after a delay
            await asyncio.sleep(2)
            self.test_status = "idle"
