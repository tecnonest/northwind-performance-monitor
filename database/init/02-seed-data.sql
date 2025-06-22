-- Insert sample seed data for lookup tables
-- This provides the foundation for generating millions of records

-- Insert Categories
INSERT INTO categories (category_name, description) VALUES
('Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
('Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings'),
('Dairy Products', 'Cheeses'),
('Grains/Cereals', 'Breads, crackers, pasta, and cereal'),
('Meat/Poultry', 'Prepared meats'),
('Produce', 'Dried fruit and bean curd'),
('Seafood', 'Seaweed and fish'),
('Electronics', 'Consumer electronics and gadgets'),
('Clothing', 'Apparel and accessories'),
('Books', 'Books and educational materials'),
('Sports', 'Sports equipment and gear'),
('Home & Garden', 'Home improvement and gardening supplies'),
('Health', 'Health and wellness products'),
('Beauty', 'Cosmetics and personal care'),
('Automotive', 'Car parts and accessories'),
('Toys', 'Toys and games'),
('Music', 'Musical instruments and accessories'),
('Office', 'Office supplies and equipment'),
('Pet Supplies', 'Pet food and accessories'),
('Travel', 'Travel accessories and luggage');

-- Insert Customer Demographics
INSERT INTO customer_demographics (customer_type_id, customer_desc) VALUES
('REGULAR', 'Regular customers with standard privileges'),
('PREMIUM', 'Premium customers with enhanced benefits'),
('VIP', 'VIP customers with exclusive access'),
('CORPORATE', 'Corporate bulk customers'),
('WHOLESALE', 'Wholesale partners'),
('RETAIL', 'Retail store customers'),
('ONLINE', 'Online-only customers'),
('MOBILE', 'Mobile app users'),
('ENTERPRISE', 'Enterprise-level customers'),
('STARTUP', 'Startup company customers');

-- Insert Regions
INSERT INTO region (region_description) VALUES
('Eastern'), ('Western'), ('Northern'), ('Southern'), ('Central'),
('Pacific'), ('Atlantic'), ('Mountain'), ('Great Lakes'), ('Southwest'),
('Southeast'), ('Northwest'), ('Midwest'), ('Northeast'), ('Gulf Coast');

-- Insert Territories
INSERT INTO territories (territory_id, territory_description, region_id) VALUES
('01581', 'Westboro', 1), ('01730', 'Bedford', 1), ('01833', 'Georgetow', 1),
('02116', 'Boston', 1), ('02139', 'Cambridge', 1), ('02184', 'Braintree', 1),
('02903', 'Providence', 1), ('03049', 'Hollis', 1), ('03801', 'Portsmouth', 1),
('06897', 'Wilton', 1), ('07960', 'Morristown', 1), ('08837', 'Edison', 1),
('10019', 'New York', 1), ('10038', 'New York', 1), ('11747', 'Mellvile', 1),
('14450', 'Fairport', 1), ('19428', 'Philadelphia', 1), ('19713', 'Neward', 1),
('20852', 'Rockville', 1), ('27403', 'Greensboro', 1), ('27511', 'Cary', 1),
('29202', 'Columbia', 1), ('30346', 'Atlanta', 1), ('31406', 'Savannah', 1),
('32859', 'Orlando', 1), ('33607', 'Tampa', 1), ('40222', 'Louisville', 1),
('44122', 'Beachwood', 1), ('45839', 'Findlay', 1), ('48084', 'Troy', 1),
('48304', 'Bloomfield Hills', 1), ('53404', 'Racine', 1), ('55113', 'Roseville', 1),
('55439', 'Minneapolis', 1), ('60179', 'Hoffman Estates', 1), ('60601', 'Chicago', 1),
('72716', 'Bentonville', 1), ('75234', 'Dallas', 1), ('78759', 'Austin', 1),
('80202', 'Denver', 1), ('80909', 'Colorado Springs', 1), ('85014', 'Phoenix', 1),
('85251', 'Scottsdale', 1), ('90405', 'Santa Monica', 1), ('94025', 'Menlo Park', 1),
('94105', 'San Francisco', 1), ('95008', 'Campbell', 1), ('95054', 'Santa Clara', 1),
('95060', 'Santa Cruz', 1), ('98004', 'Bellevue', 1), ('98052', 'Redmond', 1),
('98104', 'Seattle', 1);

-- Generate sample suppliers (1000 suppliers)
DO $$
DECLARE
    i INTEGER;
    company_names TEXT[] := ARRAY[
        'Tech Solutions Inc', 'Global Supply Co', 'Premium Products Ltd', 'Quality Distributors',
        'Reliable Sources Corp', 'International Trading', 'Excellence Suppliers', 'Prime Vendors LLC',
        'Superior Materials Co', 'Advanced Systems Inc', 'Professional Services', 'Elite Providers',
        'Standard Supply Chain', 'Modern Logistics Inc', 'Dynamic Distributors', 'Smart Solutions',
        'Innovative Products Co', 'Strategic Suppliers', 'Efficient Systems LLC', 'Optimal Resources'
    ];
    cities TEXT[] := ARRAY[
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
        'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
        'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis',
        'Seattle', 'Denver', 'Washington', 'Boston', 'El Paso', 'Nashville',
        'Detroit', 'Oklahoma City', 'Portland', 'Las Vegas', 'Memphis', 'Louisville', 'Baltimore'
    ];
    countries TEXT[] := ARRAY['USA', 'Canada', 'Mexico', 'UK', 'Germany', 'France', 'Italy', 'Spain', 'Japan', 'China'];
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO suppliers (
            company_name, contact_name, contact_title, address, city, region, 
            postal_code, country, phone, fax, homepage
        ) VALUES (
            company_names[1 + (i % array_length(company_names, 1))] || ' ' || i,
            'Contact ' || i,
            CASE (i % 5) 
                WHEN 0 THEN 'Sales Manager'
                WHEN 1 THEN 'Account Executive'
                WHEN 2 THEN 'Director'
                WHEN 3 THEN 'VP Sales'
                ELSE 'Representative'
            END,
            i || ' Business Blvd',
            cities[1 + (i % array_length(cities, 1))],
            CASE (i % 4)
                WHEN 0 THEN 'North'
                WHEN 1 THEN 'South'
                WHEN 2 THEN 'East'
                ELSE 'West'
            END,
            LPAD((10000 + (i % 90000))::text, 5, '0'),
            countries[1 + (i % array_length(countries, 1))],
            '+1-555-' || LPAD((1000 + (i % 9000))::text, 4, '0'),
            '+1-555-' || LPAD((2000 + (i % 9000))::text, 4, '0'),
            'https://www.supplier' || i || '.com'
        );
    END LOOP;
END $$;

-- Generate sample products (10,000 products)
DO $$
DECLARE
    i INTEGER;
    product_names TEXT[] := ARRAY[
        'Premium', 'Standard', 'Deluxe', 'Professional', 'Advanced', 'Basic', 'Ultimate',
        'Superior', 'Classic', 'Modern', 'Digital', 'Smart', 'Eco', 'Ultra', 'Mega',
        'Super', 'Master', 'Elite', 'Pro', 'Max', 'Plus', 'Special', 'Limited',
        'Signature', 'Custom', 'Original', 'New', 'Improved', 'Enhanced', 'Optimized'
    ];
    product_types TEXT[] := ARRAY[
        'Widget', 'Gadget', 'Device', 'Tool', 'System', 'Component', 'Module', 'Unit',
        'Instrument', 'Apparatus', 'Equipment', 'Machine', 'Product', 'Item', 'Solution',
        'Package', 'Kit', 'Set', 'Collection', 'Bundle', 'Assembly', 'Framework'
    ];
BEGIN
    FOR i IN 1..10000 LOOP
        INSERT INTO products (
            product_name, supplier_id, category_id, quantity_per_unit,
            unit_price, units_in_stock, units_on_order, reorder_level, discontinued
        ) VALUES (
            product_names[1 + (i % array_length(product_names, 1))] || ' ' ||
            product_types[1 + (i % array_length(product_types, 1))] || ' ' || i,
            1 + (i % 1000), -- supplier_id (1-1000)
            1 + (i % 20),   -- category_id (1-20)
            CASE (i % 5)
                WHEN 0 THEN '1 unit'
                WHEN 1 THEN '12 per box'
                WHEN 2 THEN '24 per case'
                WHEN 3 THEN '6 per pack'
                ELSE '1 dozen'
            END,
            ROUND((RANDOM() * 999 + 1)::numeric, 2), -- unit_price 1-1000
            FLOOR(RANDOM() * 100), -- units_in_stock 0-99
            FLOOR(RANDOM() * 50),  -- units_on_order 0-49
            FLOOR(RANDOM() * 20),  -- reorder_level 0-19
            CASE WHEN RANDOM() < 0.05 THEN TRUE ELSE FALSE END -- 5% discontinued
        );
    END LOOP;
END $$;

-- Generate sample shippers (50 shippers)
DO $$
DECLARE
    i INTEGER;
    shipper_names TEXT[] := ARRAY[
        'Express Delivery', 'Fast Transport', 'Quick Ship', 'Rapid Logistics', 'Speed Freight',
        'Lightning Express', 'Turbo Shipping', 'Rocket Delivery', 'Flash Transport', 'Swift Cargo'
    ];
BEGIN
    FOR i IN 1..50 LOOP
        INSERT INTO shippers (company_name, phone, email, website, base_shipping_cost) VALUES (
            shipper_names[1 + (i % array_length(shipper_names, 1))] || ' ' || i,
            '+1-800-' || LPAD((1000 + (i % 9000))::text, 4, '0'),
            'contact@shipper' || i || '.com',
            'https://www.shipper' || i || '.com',
            ROUND((RANDOM() * 50 + 5)::numeric, 2) -- base cost 5-55
        );
    END LOOP;
END $$;

-- Generate sample employees (1000 employees)
DO $$
DECLARE
    i INTEGER;
    first_names TEXT[] := ARRAY[
        'John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Mary',
        'William', 'Jennifer', 'James', 'Patricia', 'Richard', 'Elizabeth', 'Joseph',
        'Maria', 'Thomas', 'Susan', 'Christopher', 'Jessica', 'Charles', 'Karen',
        'Daniel', 'Nancy', 'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra'
    ];
    last_names TEXT[] := ARRAY[
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson'
    ];
    titles TEXT[] := ARRAY[
        'Sales Representative', 'Sales Manager', 'Account Executive', 'Regional Manager',
        'Vice President', 'Director of Sales', 'Senior Sales Rep', 'Territory Manager',
        'Sales Coordinator', 'Business Development', 'Key Account Manager', 'Sales Director'
    ];
BEGIN
    FOR i IN 1..1000 LOOP
        INSERT INTO employees (
            last_name, first_name, title, title_of_courtesy, birth_date, hire_date,
            address, city, region, postal_code, country, home_phone, extension,
            reports_to, salary, commission
        ) VALUES (
            last_names[1 + (i % array_length(last_names, 1))],
            first_names[1 + (i % array_length(first_names, 1))],
            titles[1 + (i % array_length(titles, 1))],
            CASE (i % 4)
                WHEN 0 THEN 'Mr.'
                WHEN 1 THEN 'Ms.'
                WHEN 2 THEN 'Dr.'
                ELSE 'Mrs.'
            END,
            DATE '1960-01-01' + (RANDOM() * 365 * 30)::int, -- ages 30-60
            DATE '2000-01-01' + (RANDOM() * 365 * 24)::int, -- hired 2000-2024
            i || ' Employee St',
            'City ' || (i % 100),
            CASE (i % 4)
                WHEN 0 THEN 'North'
                WHEN 1 THEN 'South'
                WHEN 2 THEN 'East'
                ELSE 'West'
            END,
            LPAD((10000 + (i % 90000))::text, 5, '0'),
            'USA',
            '+1-555-' || LPAD((3000 + (i % 9000))::text, 4, '0'),
            LPAD(((i % 9999) + 1)::text, 4, '0'),
            CASE WHEN i > 10 THEN (i % 10) + 1 ELSE NULL END, -- reports_to (creates hierarchy)
            ROUND((RANDOM() * 100000 + 30000)::numeric, 2), -- salary 30k-130k
            ROUND((RANDOM() * 0.1)::numeric, 4) -- commission 0-10%
        );
    END LOOP;
END $$;

-- Update table statistics after bulk inserts
ANALYZE;
