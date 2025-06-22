#!/usr/bin/env python3
"""
Data generation script for creating 10+ million records
Can be run independently or via the web interface
"""

import asyncio
import logging
import sys
import os
from datetime import datetime

# Add app directory to path
sys.path.append('/app')

from core.config import settings
from core.database import DatabaseManager
from core.data_generator import DataGenerator
from utils.logger import setup_logging

async def main():
    """Main data generation function"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting data generation process...")
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        await db_manager.connect()
        
        # Initialize data generator
        data_generator = DataGenerator(db_manager)
        
        # Check current data counts
        summary = await data_generator.get_data_summary()
        logger.info(f"Current data summary: {summary}")
        
        total_records = sum(summary.values())
        if total_records > 1000000:  # 1M records
            response = input(f"Database already contains {total_records:,} records. Continue? (y/N): ")
            if response.lower() != 'y':
                logger.info("Data generation cancelled by user")
                return
        
        # Start data generation
        start_time = datetime.now()
        await data_generator.generate_all_data()
        end_time = datetime.now()
        
        duration = end_time - start_time
        logger.info(f"Data generation completed in {duration.total_seconds():.2f} seconds")
        
        # Final summary
        final_summary = await data_generator.get_data_summary()
        logger.info(f"Final data summary: {final_summary}")
        
        total_final = sum(final_summary.values())
        logger.info(f"Total records generated: {total_final:,}")
        
    except Exception as e:
        logger.error(f"Data generation failed: {e}")
        sys.exit(1)
    finally:
        if 'db_manager' in locals():
            await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
