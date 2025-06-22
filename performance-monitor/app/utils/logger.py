"""
Logging configuration and utilities
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

from core.config import settings

def setup_logging():
    """Setup application logging configuration"""
    
    # Create logs directory if it doesn't exist
    log_dir = settings.LOG_OUTPUT_DIR
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'application.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Performance test specific handler
    perf_handler = RotatingFileHandler(
        os.path.join(log_dir, 'performance.log'),
        maxBytes=50*1024*1024,  # 50MB
        backupCount=3
    )
    perf_handler.setLevel(logging.INFO)
    perf_handler.setFormatter(detailed_formatter)
    
    # Add performance handler to performance logger
    perf_logger = logging.getLogger('performance')
    perf_logger.addHandler(perf_handler)
    
    # Error handler for critical issues
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'errors.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Silence some noisy loggers in development
    if settings.ENVIRONMENT == "development":
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("aiohttp").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    logging.info("Logging configuration initialized")

def get_performance_logger():
    """Get logger specifically for performance metrics"""
    return logging.getLogger('performance')

def log_performance_metric(test_name: str, metric_type: str, value: float, unit: str = "ms"):
    """Log a performance metric in a structured format"""
    perf_logger = get_performance_logger()
    
    metric_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "test_name": test_name,
        "metric_type": metric_type,
        "value": value,
        "unit": unit
    }
    
    perf_logger.info(f"METRIC: {metric_data}")

class PerformanceContextManager:
    """Context manager for timing operations"""
    
    def __init__(self, operation_name: str, logger: logging.Logger = None):
        self.operation_name = operation_name
        self.logger = logger or logging.getLogger(__name__)
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting {self.operation_name}...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(f"Completed {self.operation_name} in {duration:.2f} seconds")
        else:
            self.logger.error(f"Failed {self.operation_name} after {duration:.2f} seconds: {exc_val}")
        
        log_performance_metric(self.operation_name, "duration", duration * 1000, "ms")
    
    @property
    def duration_ms(self) -> float:
        """Get duration in milliseconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return 0.0
