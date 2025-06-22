"""
Database connection and query management
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from contextlib import asynccontextmanager

import asyncpg
import psycopg2
from psycopg2.extras import RealDictCursor

from core.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.connection_pool: Optional[asyncpg.Pool] = None
        self.sync_connection = None
        
    async def connect(self):
        """Establish database connections"""
        try:
            # Create async connection pool
            self.connection_pool = await asyncpg.create_pool(
                settings.POSTGRES_URL,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            
            # Create sync connection for specific operations
            self.sync_connection = psycopg2.connect(settings.POSTGRES_URL)
            
            logger.info("Database connections established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    async def disconnect(self):
        """Close database connections"""
        if self.connection_pool:
            await self.connection_pool.close()
        if self.sync_connection:
            self.sync_connection.close()
        logger.info("Database connections closed")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            async with self.connection_pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1")
                return {
                    "status": "healthy" if result == 1 else "unhealthy",
                    "latency_ms": 0  # Will be measured in actual implementation
                }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    async def execute_query_async(self, query: str, params: List = None) -> Tuple[List[Dict], float]:
        """Execute query asynchronously and measure execution time"""
        start_time = time.time()
        try:
            async with self.connection_pool.acquire() as conn:
                if params:
                    rows = await conn.fetch(query, *params)
                else:
                    rows = await conn.fetch(query)
                
                execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Convert to list of dicts
                result = [dict(row) for row in rows]
                return result, execution_time
                
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"Query execution failed: {e}")
            raise
    
    def execute_query_sync(self, query: str, params: List = None) -> Tuple[List[Dict], float]:
        """Execute query synchronously and measure execution time"""
        start_time = time.time()
        try:
            with self.sync_connection.cursor(cursor_factory=RealDictCursor) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                rows = cursor.fetchall()
                execution_time = (time.time() - start_time) * 1000
                
                # Convert to list of dicts
                result = [dict(row) for row in rows]
                return result, execution_time
                
        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            logger.error(f"Sync query execution failed: {e}")
            self.sync_connection.rollback()
            raise
    
    async def execute_bulk_insert(self, table: str, columns: List[str], data: List[List]) -> float:
        """Execute bulk insert operation"""
        start_time = time.time()
        try:
            async with self.connection_pool.acquire() as conn:
                # Use COPY for bulk inserts
                await conn.copy_records_to_table(
                    table,
                    records=data,
                    columns=columns
                )
                
                execution_time = (time.time() - start_time) * 1000
                return execution_time
                
        except Exception as e:
            logger.error(f"Bulk insert failed: {e}")
            raise
    
    async def get_table_stats(self) -> Dict[str, Any]:
        """Get table statistics"""
        try:
            # Simple table stats query that should work
            query = """
            SELECT 
                table_name,
                table_schema
            FROM information_schema.tables 
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_name;
            """
            
            result, _ = await self.execute_query_async(query)
            
            # Get basic database size info
            size_query = "SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;"
            size_result, _ = await self.execute_query_async(size_query)
            
            return {
                "tables": result,
                "database_size": size_result[0]["db_size"] if size_result else "Unknown",
                "table_count": len(result)
            }
        except Exception as e:
            logger.error(f"Error getting table stats: {e}")
            return {
                "tables": [],
                "database_size": "Unknown",
                "table_count": 0,
                "error": str(e)
            }
    
    async def get_index_usage(self) -> Dict[str, Any]:
        """Get index usage statistics"""
        query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            idx_tup_read,
            idx_tup_fetch,
            idx_scan
        FROM pg_stat_user_indexes
        ORDER BY idx_scan DESC;
        """
        
        result, _ = await self.execute_query_async(query)
        return result
    
    async def get_slow_queries(self, limit: int = 10) -> Dict[str, Any]:
        """Get slow queries from pg_stat_statements"""
        query = """
        SELECT 
            query,
            calls,
            total_time,
            mean_time,
            max_time,
            stddev_time,
            rows
        FROM pg_stat_statements
        ORDER BY mean_time DESC
        LIMIT $1;
        """
        
        result, _ = await self.execute_query_async(query, [limit])
        return result
    
    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get database connection statistics"""
        query = """
        SELECT 
            state,
            COUNT(*) as count
        FROM pg_stat_activity
        WHERE datname = current_database()
        GROUP BY state;
        """
        
        result, _ = await self.execute_query_async(query)
        return result
