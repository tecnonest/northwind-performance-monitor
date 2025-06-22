"""
Redis cache management for performance optimization
"""

import json
import logging
import time
from typing import Any, Dict, List, Optional, Union
import hashlib

import redis.asyncio as redis

from core.config import settings

logger = logging.getLogger(__name__)

class CacheManager:
    """Manages Redis cache operations"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            
            # Test connection
            await self.redis_client.ping()
            logger.info("Redis connection established")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
        logger.info("Redis connection closed")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check Redis health"""
        try:
            start_time = time.time()
            await self.redis_client.ping()
            latency = (time.time() - start_time) * 1000
            
            return {
                "status": "healthy",
                "latency_ms": round(latency, 2)
            }
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    def _generate_cache_key(self, prefix: str, query: str, params: List = None) -> str:
        """Generate a cache key from query and parameters"""
        cache_data = {
            "query": query,
            "params": params or []
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        cache_hash = hashlib.md5(cache_string.encode()).hexdigest()
        return f"{prefix}:{cache_hash}"
    
    async def get_cached_query(self, query: str, params: List = None) -> Optional[Dict[str, Any]]:
        """Get cached query result"""
        try:
            cache_key = self._generate_cache_key("query", query, params)
            
            start_time = time.time()
            cached_data = await self.redis_client.get(cache_key)
            retrieval_time = (time.time() - start_time) * 1000
            
            if cached_data:
                self.cache_stats["hits"] += 1
                result = json.loads(cached_data)
                result["cache_hit"] = True
                result["cache_retrieval_time_ms"] = round(retrieval_time, 2)
                return result
            else:
                self.cache_stats["misses"] += 1
                return None
                
        except Exception as e:
            logger.error(f"Error getting cached query: {e}")
            self.cache_stats["misses"] += 1
            return None
    
    async def cache_query_result(self, query: str, result: Dict[str, Any], 
                                params: List = None, ttl: int = None) -> bool:
        """Cache query result"""
        try:
            cache_key = self._generate_cache_key("query", query, params)
            cache_ttl = ttl or settings.CACHE_TTL_SECONDS
            
            cache_data = {
                "data": result,
                "cached_at": time.time(),
                "ttl": cache_ttl
            }
            
            start_time = time.time()
            await self.redis_client.setex(
                cache_key,
                cache_ttl,
                json.dumps(cache_data, default=str)
            )
            storage_time = (time.time() - start_time) * 1000
            
            self.cache_stats["sets"] += 1
            logger.debug(f"Cached query result in {storage_time:.2f}ms")
            return True
            
        except Exception as e:
            logger.error(f"Error caching query result: {e}")
            return False
    
    async def invalidate_cache_pattern(self, pattern: str) -> int:
        """Invalidate cache entries matching pattern"""
        try:
            keys = await self.redis_client.keys(pattern)
            if keys:
                deleted = await self.redis_client.delete(*keys)
                self.cache_stats["deletes"] += deleted
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Error invalidating cache: {e}")
            return 0
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        try:
            info = await self.redis_client.info("memory")
            
            total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
            hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "hits": self.cache_stats["hits"],
                "misses": self.cache_stats["misses"],
                "sets": self.cache_stats["sets"],
                "deletes": self.cache_stats["deletes"],
                "hit_rate_percent": round(hit_rate, 2),
                "memory_used_bytes": info.get("used_memory", 0),
                "memory_used_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return self.cache_stats
    
    async def clear_all_cache(self) -> bool:
        """Clear all cache entries"""
        try:
            await self.redis_client.flushdb()
            self.cache_stats = {
                "hits": 0,
                "misses": 0,
                "sets": 0,
                "deletes": 0
            }
            logger.info("All cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    async def warm_cache(self, queries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Warm cache with predefined queries"""
        warmed = 0
        failed = 0
        
        for query_info in queries:
            try:
                query = query_info["query"]
                params = query_info.get("params", [])
                ttl = query_info.get("ttl", settings.CACHE_TTL_SECONDS)
                
                # This would normally execute the query and cache result
                # For now, we'll just simulate caching
                cache_key = self._generate_cache_key("warm", query, params)
                await self.redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps({"warmed": True}, default=str)
                )
                warmed += 1
                
            except Exception as e:
                logger.error(f"Failed to warm cache for query: {e}")
                failed += 1
        
        return {
            "warmed": warmed,
            "failed": failed,
            "total": len(queries)
        }
