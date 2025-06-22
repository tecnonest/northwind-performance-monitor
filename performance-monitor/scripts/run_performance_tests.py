#!/usr/bin/env python3
"""
Performance testing script for running comprehensive tests
Can be run independently or via the web interface
"""

import asyncio
import logging
import sys
import json
from datetime import datetime

# Add app directory to path
sys.path.append('/app')

from core.config import settings
from core.database import DatabaseManager
from core.cache import CacheManager
from core.performance import PerformanceAnalyzer
from utils.logger import setup_logging

async def main():
    """Main performance testing function"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting performance testing process...")
    
    try:
        # Initialize managers
        db_manager = DatabaseManager()
        cache_manager = CacheManager()
        
        await db_manager.connect()
        await cache_manager.connect()
        
        # Initialize performance analyzer
        performance_analyzer = PerformanceAnalyzer(db_manager, cache_manager)
        
        # Run comprehensive tests
        logger.info("Running comprehensive performance tests...")
        await performance_analyzer.run_comprehensive_tests()
        
        # Get results
        results = performance_analyzer.get_test_results()
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"/app/reports/performance_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {results_file}")
        
        # Print summary
        print("\n" + "="*60)
        print("PERFORMANCE TEST SUMMARY")
        print("="*60)
        
        for result in results:
            if 'comparison' in result:
                comp = result['comparison']
                print(f"\nTest: {result['test_name']}")
                print(f"  SQL Average:     {comp['sql_avg_ms']:.2f}ms")
                print(f"  GraphQL Average: {comp['graphql_avg_ms']:.2f}ms")
                print(f"  Faster Option:   {comp['faster_option']}")
                print(f"  Difference:      {comp['performance_difference_percent']:.1f}%")
        
        print("\n" + "="*60)
        print(f"Detailed results saved to: {results_file}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Performance testing failed: {e}")
        sys.exit(1)
    finally:
        if 'db_manager' in locals():
            await db_manager.disconnect()
        if 'cache_manager' in locals():
            await cache_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
