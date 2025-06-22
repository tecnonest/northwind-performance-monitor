"""
Configuration settings for the performance monitor application
"""

import os
from typing import Optional
from pydantic import BaseModel

class Settings(BaseModel):
    """Application settings"""
    
    # Database settings
    POSTGRES_URL: str = os.getenv(
        "POSTGRES_URL", 
        "postgres://postgres:postgres@postgres:5432/northwind"
    )
    
    # GraphQL settings
    HASURA_URL: str = os.getenv(
        "HASURA_URL", 
        "http://hasura:8080/v1/graphql"
    )
    HASURA_ADMIN_SECRET: str = os.getenv(
        "HASURA_ADMIN_SECRET", 
        "hasura-admin-secret"
    )
    
    # Redis settings
    REDIS_URL: str = os.getenv(
        "REDIS_URL", 
        "redis://redis:6379"
    )
    
    # Prometheus settings
    PROMETHEUS_URL: str = os.getenv(
        "PROMETHEUS_URL", 
        "http://prometheus:9090"
    )
    
    # Application settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Performance test settings
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "100"))
    TEST_DURATION_SECONDS: int = int(os.getenv("TEST_DURATION_SECONDS", "300"))
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
    
    # Data generation settings
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "10000"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # Reporting settings
    REPORT_OUTPUT_DIR: str = os.getenv("REPORT_OUTPUT_DIR", "/app/reports")
    LOG_OUTPUT_DIR: str = os.getenv("LOG_OUTPUT_DIR", "/app/logs")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
