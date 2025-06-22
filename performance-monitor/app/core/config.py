"""
Configuration settings for the performance monitor application
"""

import os

class Settings:
    """Application settings"""
    
    def __init__(self):
        # Database settings
        self.POSTGRES_URL = os.getenv(
            "POSTGRES_URL", 
            "postgres://postgres:postgres@postgres:5432/northwind"
        )
        
        # GraphQL settings
        self.HASURA_URL = os.getenv(
            "HASURA_URL", 
            "http://hasura:8080/v1/graphql"
        )
        self.HASURA_ADMIN_SECRET = os.getenv(
            "HASURA_ADMIN_SECRET", 
            "hasura-admin-secret"
        )
        
        # Redis settings
        self.REDIS_URL = os.getenv(
            "REDIS_URL", 
            "redis://redis:6379"
        )
        
        # Prometheus settings
        self.PROMETHEUS_URL = os.getenv(
            "PROMETHEUS_URL", 
            "http://prometheus:9090"
        )
        
        # Application settings
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Performance test settings
        self.MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "100"))
        self.TEST_DURATION_SECONDS = int(os.getenv("TEST_DURATION_SECONDS", "300"))
        self.CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "300"))
        
        # Data generation settings
        self.BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10000"))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
        
        # Reporting settings
        self.REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "/app/reports")
        self.LOG_OUTPUT_DIR = os.getenv("LOG_OUTPUT_DIR", "/app/logs")

# Global settings instance
settings = Settings()
