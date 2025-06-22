"""
Northwind Performance Monitor Application
A comprehensive performance testing suite for GraphQL vs SQL comparison
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi import Request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from core.config import settings
from core.database import DatabaseManager
from core.cache import CacheManager
from core.performance import PerformanceAnalyzer
from core.data_generator import DataGenerator
from core.metrics import http_requests_total, http_request_duration_seconds, system_cpu_usage, system_memory_usage
from api.routes import performance, reports, admin
from utils.logger import setup_logging
import psutil
import time

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global managers
db_manager = None
cache_manager = None
performance_analyzer = None
data_generator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global db_manager, cache_manager, performance_analyzer, data_generator
    
    logger.info("Starting Northwind Performance Monitor...")
    
    try:
        # Initialize managers
        db_manager = DatabaseManager()
        cache_manager = CacheManager()
        performance_analyzer = PerformanceAnalyzer(db_manager, cache_manager)
        data_generator = DataGenerator(db_manager)
        
        # Test connections
        await db_manager.connect()
        await cache_manager.connect()
        
        logger.info("All services connected successfully")
        
        # Store in app state
        app.state.db_manager = db_manager
        app.state.cache_manager = cache_manager
        app.state.performance_analyzer = performance_analyzer
        app.state.data_generator = data_generator
        
        # Start system metrics collection
        app.state.metrics_task = asyncio.create_task(update_system_metrics())
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    finally:
        # Cleanup
        logger.info("Shutting down services...")
        if hasattr(app.state, 'metrics_task'):
            app.state.metrics_task.cancel()
        if db_manager:
            await db_manager.disconnect()
        if cache_manager:
            await cache_manager.disconnect()

async def update_system_metrics():
    """Background task to update system metrics"""
    while True:
        try:
            # Update CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            system_cpu_usage.set(cpu_percent)
            
            # Update memory usage
            memory = psutil.virtual_memory()
            system_memory_usage.set(memory.percent)
            
            # Sleep for 10 seconds before next update
            await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Error updating system metrics: {e}")
            await asyncio.sleep(10)

# Create FastAPI app
app = FastAPI(
    title="Northwind Performance Monitor",
    description="GraphQL vs SQL Performance Analysis Suite",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add metrics middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect HTTP request metrics"""
    start_time = time.time()
    
    # Call the endpoint
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Extract path template instead of full path
    endpoint = request.url.path
    method = request.method
    status_code = str(response.status_code)
    
    # Record metrics
    http_requests_total.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
    
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(performance.router, prefix="/api/v1/performance", tags=["performance"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = await app.state.db_manager.health_check()
        
        # Check cache connection
        cache_status = await app.state.cache_manager.health_check()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": db_status,
                "cache": cache_status
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/api/v1/stats")
async def get_system_stats():
    """Get current system statistics"""
    try:
        stats = await app.state.performance_analyzer.get_system_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get system stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")

@app.post("/api/v1/generate-data")
async def generate_data(background_tasks: BackgroundTasks):
    """Start data generation process"""
    try:
        # Start data generation in background
        background_tasks.add_task(
            app.state.data_generator.generate_all_data
        )
        
        return {
            "status": "started",
            "message": "Data generation started in background",
            "estimated_time": "30-60 minutes"
        }
    except Exception as e:
        logger.error(f"Failed to start data generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to start data generation")

@app.post("/api/v1/run-performance-tests")
async def run_performance_tests(background_tasks: BackgroundTasks):
    """Run comprehensive performance tests"""
    try:
        # Start performance tests in background
        background_tasks.add_task(
            app.state.performance_analyzer.run_comprehensive_tests
        )
        
        return {
            "status": "started",
            "message": "Performance tests started in background",
            "estimated_time": "15-30 minutes"
        }
    except Exception as e:
        logger.error(f"Failed to start performance tests: {e}")
        raise HTTPException(status_code=500, detail="Failed to start performance tests")

@app.get("/api/v1/test-status")
async def get_test_status():
    """Get current test execution status"""
    try:
        status = await app.state.performance_analyzer.get_test_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get test status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get test status")

@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("ENVIRONMENT") == "development" else False,
        log_level="info"
    )
