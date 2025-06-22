"""
Data generator for creating 10+ million records in Northwind database
"""

import asyncio
import logging
import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

from faker import Faker

from core.config import settings
from core.database import DatabaseManager

logger = logging.getLogger(__name__)
fake = Faker()

class DataGenerator:
    """Generates large datasets for performance testing"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.batch_size = settings.BATCH_SIZE
        
    def generate_customer_id(self, index: int) -> str:
        """Generate unique customer ID"""
        return f"C{index:05d}"
    
    def generate_customers_batch(self, start_id: int, batch_size: int) -> List[List]:
        """Generate a batch of customer records"""
        customers = []
        
        for i in range(batch_size):
            customer_id = self.generate_customer_id(start_id + i)
            
            customer = [
                customer_id,
                fake.company(),
                fake.name(),
                fake.job(),
                fake.street_address(),
                fake.city(),
                fake.state_abbr() if random.random() > 0.3 else None,
                fake.postcode(),
                fake.country(),
                fake.phone_number(),
                fake.phone_number() if random.random() > 0.7 else None,
                fake.email(),
                fake.date_between(start_date='-5y', end_date='today'),
                random.choice(['Regular', 'Premium', 'VIP', 'Corporate']),
                round(random.uniform(1000, 50000), 2),
                datetime.now(),
                datetime.now()
            ]
            customers.append(customer)
        
        return customers
    
    async def generate_customers(self, total_customers: int = 100000):
        """Generate customer records"""
        logger.info(f"Generating {total_customers} customers...")
        
        columns = [
            'customer_id', 'company_name', 'contact_name', 'contact_title',
            'address', 'city', 'region', 'postal_code', 'country', 'phone',
            'fax', 'email', 'registration_date', 'customer_type', 'credit_limit',
            'created_at', 'updated_at'
        ]
        
        total_batches = (total_customers + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_id = batch_num * self.batch_size + 1
            current_batch_size = min(self.batch_size, total_customers - batch_num * self.batch_size)
            
            # Generate batch data
            batch_data = self.generate_customers_batch(start_id, current_batch_size)
            
            # Insert batch
            try:
                execution_time = await self.db_manager.execute_bulk_insert(
                    'customers', columns, batch_data
                )
                
                logger.info(f"Inserted customers batch {batch_num + 1}/{total_batches} "
                          f"({current_batch_size} records) in {execution_time:.2f}ms")
                
            except Exception as e:
                logger.error(f"Failed to insert customers batch {batch_num + 1}: {e}")
                raise
        
        logger.info(f"Completed generating {total_customers} customers")
    
    def generate_orders_batch(self, start_id: int, batch_size: int, 
                            customer_ids: List[str], employee_ids: List[int],
                            shipper_ids: List[int]) -> List[List]:
        """Generate a batch of order records"""
        orders = []
        
        for i in range(batch_size):
            order_date = fake.date_between(start_date='-2y', end_date='today')
            required_date = order_date + timedelta(days=random.randint(1, 30))
            shipped_date = order_date + timedelta(days=random.randint(0, 20)) if random.random() > 0.1 else None
            
            order = [
                start_id + i,  # order_id will be auto-generated, but we track for reference
                random.choice(customer_ids),
                random.choice(employee_ids),
                order_date,
                required_date,
                shipped_date,
                random.choice(shipper_ids),
                round(random.uniform(5.0, 500.0), 2),  # freight
                fake.company(),  # ship_name
                fake.street_address(),  # ship_address
                fake.city(),
                fake.state_abbr() if random.random() > 0.3 else None,
                fake.postcode(),
                fake.country(),
                random.choice(['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']),
                random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash']),
                round(random.uniform(0, 20), 2),  # discount_percent
                round(random.uniform(0, 50), 2),  # tax_amount
                datetime.now(),
                datetime.now()
            ]
            orders.append(order)
        
        return orders
    
    async def generate_orders(self, total_orders: int = 5000000):
        """Generate order records"""
        logger.info(f"Generating {total_orders} orders...")
        
        # Get existing reference data
        customers_query = "SELECT customer_id FROM customers LIMIT 100000"
        employees_query = "SELECT employee_id FROM employees"
        shippers_query = "SELECT shipper_id FROM shippers"
        
        customers_result, _ = await self.db_manager.execute_query_async(customers_query)
        employees_result, _ = await self.db_manager.execute_query_async(employees_query)
        shippers_result, _ = await self.db_manager.execute_query_async(shippers_query)
        
        customer_ids = [row['customer_id'] for row in customers_result]
        employee_ids = [row['employee_id'] for row in employees_result]
        shipper_ids = [row['shipper_id'] for row in shippers_result]
        
        if not customer_ids or not employee_ids or not shipper_ids:
            raise ValueError("Missing reference data. Ensure customers, employees, and shippers exist.")
        
        columns = [
            'customer_id', 'employee_id', 'order_date', 'required_date',
            'shipped_date', 'ship_via', 'freight', 'ship_name', 'ship_address',
            'ship_city', 'ship_region', 'ship_postal_code', 'ship_country',
            'order_status', 'payment_method', 'discount_percent', 'tax_amount',
            'created_at', 'updated_at'
        ]
        
        total_batches = (total_orders + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            start_id = batch_num * self.batch_size + 1
            current_batch_size = min(self.batch_size, total_orders - batch_num * self.batch_size)
            
            # Generate batch data
            batch_data = self.generate_orders_batch(
                start_id, current_batch_size, customer_ids, employee_ids, shipper_ids
            )
            
            # Insert batch
            try:
                execution_time = await self.db_manager.execute_bulk_insert(
                    'orders', columns, batch_data
                )
                
                logger.info(f"Inserted orders batch {batch_num + 1}/{total_batches} "
                          f"({current_batch_size} records) in {execution_time:.2f}ms")
                
            except Exception as e:
                logger.error(f"Failed to insert orders batch {batch_num + 1}: {e}")
                raise
        
        logger.info(f"Completed generating {total_orders} orders")
    
    def generate_order_details_batch(self, order_ids: List[int], product_ids: List[int], 
                                   batch_size: int) -> List[List]:
        """Generate a batch of order detail records"""
        order_details = []
        
        for _ in range(batch_size):
            order_id = random.choice(order_ids)
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 50)
            unit_price = round(random.uniform(1.0, 1000.0), 2)
            discount = round(random.uniform(0, 0.25), 3)
            
            order_detail = [
                order_id,
                product_id,
                unit_price,
                quantity,
                discount,
                datetime.now()
            ]
            order_details.append(order_detail)
        
        return order_details
    
    async def generate_order_details(self, total_order_details: int = 5000000):
        """Generate order detail records"""
        logger.info(f"Generating {total_order_details} order details...")
        
        # Get existing reference data
        orders_query = "SELECT order_id FROM orders"
        products_query = "SELECT product_id FROM products"
        
        orders_result, _ = await self.db_manager.execute_query_async(orders_query)
        products_result, _ = await self.db_manager.execute_query_async(products_query)
        
        order_ids = [row['order_id'] for row in orders_result]
        product_ids = [row['product_id'] for row in products_result]
        
        if not order_ids or not product_ids:
            raise ValueError("Missing reference data. Ensure orders and products exist.")
        
        columns = [
            'order_id', 'product_id', 'unit_price', 'quantity', 'discount', 'created_at'
        ]
        
        total_batches = (total_order_details + self.batch_size - 1) // self.batch_size
        
        for batch_num in range(total_batches):
            current_batch_size = min(self.batch_size, total_order_details - batch_num * self.batch_size)
            
            # Generate batch data
            batch_data = self.generate_order_details_batch(
                order_ids, product_ids, current_batch_size
            )
            
            # Insert batch
            try:
                execution_time = await self.db_manager.execute_bulk_insert(
                    'order_details', columns, batch_data
                )
                
                logger.info(f"Inserted order details batch {batch_num + 1}/{total_batches} "
                          f"({current_batch_size} records) in {execution_time:.2f}ms")
                
            except Exception as e:
                logger.error(f"Failed to insert order details batch {batch_num + 1}: {e}")
                raise
        
        logger.info(f"Completed generating {total_order_details} order details")
    
    async def generate_all_data(self):
        """Generate all data according to specifications"""
        try:
            logger.info("Starting comprehensive data generation...")
            start_time = datetime.now()
            
            # Generate customers (100,000)
            await self.generate_customers(100000)
            
            # Generate orders (5,000,000)
            await self.generate_orders(5000000)
            
            # Generate order details (5,000,000+)
            await self.generate_order_details(5000000)
            
            # Update statistics for better query planning
            await self.update_table_statistics()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"Data generation completed in {duration.total_seconds():.2f} seconds")
            
            # Get final counts
            summary = await self.get_data_summary()
            logger.info(f"Data generation summary: {summary}")
            
        except Exception as e:
            logger.error(f"Data generation failed: {e}")
            raise
    
    async def update_table_statistics(self):
        """Update table statistics for query optimization"""
        logger.info("Updating table statistics...")
        
        tables = ['customers', 'orders', 'order_details', 'products', 'employees', 'suppliers']
        
        for table in tables:
            try:
                query = f"ANALYZE {table};"
                await self.db_manager.execute_query_async(query)
                logger.info(f"Updated statistics for {table}")
            except Exception as e:
                logger.error(f"Failed to update statistics for {table}: {e}")
    
    async def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of generated data"""
        summary = {}
        
        tables = [
            'customers', 'orders', 'order_details', 'products', 
            'employees', 'suppliers', 'categories', 'shippers'
        ]
        
        for table in tables:
            try:
                query = f"SELECT COUNT(*) as count FROM {table};"
                result, _ = await self.db_manager.execute_query_async(query)
                summary[table] = result[0]['count']
            except Exception as e:
                logger.error(f"Failed to get count for {table}: {e}")
                summary[table] = 0
        
        return summary
