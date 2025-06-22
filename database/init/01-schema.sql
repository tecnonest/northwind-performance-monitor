-- Northwind Database Schema
-- Optimized for 10+ Million Records Performance Testing

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(15) NOT NULL,
    description TEXT,
    picture BYTEA,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers table
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    contact_name VARCHAR(30),
    contact_title VARCHAR(30),
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    phone VARCHAR(24),
    fax VARCHAR(24),
    homepage TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(40) NOT NULL,
    supplier_id INTEGER REFERENCES suppliers(supplier_id),
    category_id INTEGER REFERENCES categories(category_id),
    quantity_per_unit VARCHAR(20),
    unit_price DECIMAL(10,2) DEFAULT 0,
    units_in_stock INTEGER DEFAULT 0,
    units_on_order INTEGER DEFAULT 0,
    reorder_level INTEGER DEFAULT 0,
    discontinued BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE customers (
    customer_id VARCHAR(5) PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    contact_name VARCHAR(30),
    contact_title VARCHAR(30),
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    phone VARCHAR(24),
    fax VARCHAR(24),
    email VARCHAR(100),
    registration_date DATE DEFAULT CURRENT_DATE,
    customer_type VARCHAR(20) DEFAULT 'Regular',
    credit_limit DECIMAL(10,2) DEFAULT 10000.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    last_name VARCHAR(20) NOT NULL,
    first_name VARCHAR(10) NOT NULL,
    title VARCHAR(30),
    title_of_courtesy VARCHAR(25),
    birth_date DATE,
    hire_date DATE,
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    home_phone VARCHAR(24),
    extension VARCHAR(4),
    photo BYTEA,
    notes TEXT,
    reports_to INTEGER REFERENCES employees(employee_id),
    photo_path VARCHAR(255),
    salary DECIMAL(10,2),
    commission DECIMAL(5,4) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shippers table
CREATE TABLE shippers (
    shipper_id SERIAL PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    phone VARCHAR(24),
    email VARCHAR(100),
    website VARCHAR(100),
    base_shipping_cost DECIMAL(8,2) DEFAULT 10.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(5) REFERENCES customers(customer_id),
    employee_id INTEGER REFERENCES employees(employee_id),
    order_date DATE DEFAULT CURRENT_DATE,
    required_date DATE,
    shipped_date DATE,
    ship_via INTEGER REFERENCES shippers(shipper_id),
    freight DECIMAL(10,2) DEFAULT 0,
    ship_name VARCHAR(40),
    ship_address VARCHAR(60),
    ship_city VARCHAR(15),
    ship_region VARCHAR(15),
    ship_postal_code VARCHAR(10),
    ship_country VARCHAR(15),
    order_status VARCHAR(20) DEFAULT 'Pending',
    payment_method VARCHAR(20) DEFAULT 'Credit Card',
    discount_percent DECIMAL(5,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Details table
CREATE TABLE order_details (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    unit_price DECIMAL(10,2) NOT NULL DEFAULT 0,
    quantity INTEGER NOT NULL DEFAULT 1,
    discount DECIMAL(4,3) NOT NULL DEFAULT 0,
    line_total DECIMAL(12,2) GENERATED ALWAYS AS (
        (unit_price * quantity) * (1 - discount)
    ) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id, product_id)
);

-- Customer Demographics table (for analysis)
CREATE TABLE customer_demographics (
    customer_type_id VARCHAR(10) PRIMARY KEY,
    customer_desc TEXT
);

-- Customer Customer Demo (many-to-many)
CREATE TABLE customer_customer_demo (
    customer_id VARCHAR(5) REFERENCES customers(customer_id),
    customer_type_id VARCHAR(10) REFERENCES customer_demographics(customer_type_id),
    PRIMARY KEY (customer_id, customer_type_id)
);

-- Region table
CREATE TABLE region (
    region_id SERIAL PRIMARY KEY,
    region_description VARCHAR(50) NOT NULL
);

-- Territories table
CREATE TABLE territories (
    territory_id VARCHAR(20) PRIMARY KEY,
    territory_description VARCHAR(50) NOT NULL,
    region_id INTEGER REFERENCES region(region_id)
);

-- Employee Territories (many-to-many)
CREATE TABLE employee_territories (
    employee_id INTEGER REFERENCES employees(employee_id),
    territory_id VARCHAR(20) REFERENCES territories(territory_id),
    PRIMARY KEY (employee_id, territory_id)
);

-- Performance optimization indexes
-- Primary indexes for foreign keys
CREATE INDEX idx_products_supplier_id ON products(supplier_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_employee_id ON orders(employee_id);
CREATE INDEX idx_orders_ship_via ON orders(ship_via);
CREATE INDEX idx_order_details_order_id ON order_details(order_id);
CREATE INDEX idx_order_details_product_id ON order_details(product_id);

-- Date-based indexes for time-series queries
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_shipped_date ON orders(shipped_date);
CREATE INDEX idx_orders_required_date ON orders(required_date);

-- Composite indexes for common queries
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);
CREATE INDEX idx_orders_employee_date ON orders(employee_id, order_date);
CREATE INDEX idx_order_details_composite ON order_details(order_id, product_id);

-- Text search indexes
CREATE INDEX idx_customers_company_name ON customers(company_name);
CREATE INDEX idx_products_product_name ON products(product_name);
CREATE INDEX idx_suppliers_company_name ON suppliers(company_name);

-- Status and type indexes
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_customers_type ON customers(customer_type);
CREATE INDEX idx_products_discontinued ON products(discontinued);

-- Partial indexes for active records
CREATE INDEX idx_active_products ON products(product_id) WHERE discontinued = FALSE;
CREATE INDEX idx_shipped_orders ON orders(order_id) WHERE shipped_date IS NOT NULL;

-- Statistics collection for query optimization
CREATE INDEX idx_orders_freight ON orders(freight);
CREATE INDEX idx_order_details_quantity ON order_details(quantity);
CREATE INDEX idx_order_details_unit_price ON order_details(unit_price);

-- Update statistics
ANALYZE;
