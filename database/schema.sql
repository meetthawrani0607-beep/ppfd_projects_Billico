-- =====================================================
-- Billico Database Schema
-- Smart Inventory Automation Platform
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS billico CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE billico;

-- =====================================================
-- Table: users
-- Store user account information
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: suppliers
-- Store supplier/vendor information
-- =====================================================
CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(150),
    email VARCHAR(120),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT,
    
    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_created_by (created_by),
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: categories
-- Store product categories
-- =====================================================
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default categories
INSERT INTO categories (name, description) VALUES
    ('Electronics', 'Electronic items and devices'),
    ('Groceries', 'Food and grocery items'),
    ('Stationery', 'Office and school supplies'),
    ('Hardware', 'Hardware and tools'),
    ('Clothing', 'Apparel and accessories'),
    ('Furniture', 'Furniture items'),
    ('Other', 'Miscellaneous items');

-- =====================================================
-- Table: inventory_items
-- Store inventory product information
-- =====================================================
CREATE TABLE IF NOT EXISTS inventory_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(200) NOT NULL,
    description TEXT,
    sku VARCHAR(100) UNIQUE,
    category_id INT,
    quantity INT NOT NULL DEFAULT 0,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    reorder_level INT DEFAULT 10,
    supplier_id INT,
    location VARCHAR(100),
    
    -- Stock status indicators
    stock_status ENUM('healthy', 'medium', 'low', 'out_of_stock') DEFAULT 'healthy',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_restocked TIMESTAMP NULL,
    
    -- User tracking
    created_by INT,
    updated_by INT,
    
    -- Indexes for performance
    INDEX idx_item_name (item_name),
    INDEX idx_sku (sku),
    INDEX idx_category (category_id),
    INDEX idx_supplier (supplier_id),
    INDEX idx_stock_status (stock_status),
    INDEX idx_quantity (quantity),
    INDEX idx_created_at (created_at),
    
    -- Foreign keys
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: stock_transactions
-- Track all stock movements (add/remove/adjust)
-- =====================================================
CREATE TABLE IF NOT EXISTS stock_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    transaction_type ENUM('purchase', 'sale', 'adjustment', 'return', 'damage') NOT NULL,
    quantity_change INT NOT NULL,
    quantity_before INT NOT NULL,
    quantity_after INT NOT NULL,
    unit_price DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    reference_number VARCHAR(100),
    notes TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    
    INDEX idx_item (item_id),
    INDEX idx_type (transaction_type),
    INDEX idx_date (transaction_date),
    INDEX idx_reference (reference_number),
    
    FOREIGN KEY (item_id) REFERENCES inventory_items(id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: upload_logs
-- Track bill/receipt uploads and OCR processing
-- =====================================================
CREATE TABLE IF NOT EXISTS upload_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT,
    file_type VARCHAR(50),
    
    -- OCR Processing status
    ocr_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    ocr_text TEXT,
    ocr_confidence DECIMAL(5, 2),
    
    -- Extracted data
    extracted_data JSON,
    items_extracted INT DEFAULT 0,
    items_added INT DEFAULT 0,
    
    -- Bill information
    bill_number VARCHAR(100),
    bill_date DATE,
    supplier_name VARCHAR(200),
    total_amount DECIMAL(10, 2),
    
    -- Processing timestamps
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_started TIMESTAMP NULL,
    processing_completed TIMESTAMP NULL,
    
    -- Error handling
    error_message TEXT,
    
    INDEX idx_user (user_id),
    INDEX idx_status (ocr_status),
    INDEX idx_upload_time (upload_time),
    INDEX idx_bill_number (bill_number),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Table: alerts
-- Store system alerts and notifications
-- =====================================================
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    alert_type ENUM('low_stock', 'out_of_stock', 'high_value', 'system') NOT NULL,
    item_id INT,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    severity ENUM('info', 'warning', 'critical') DEFAULT 'info',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP NULL,
    
    INDEX idx_user (user_id),
    INDEX idx_type (alert_type),
    INDEX idx_read (is_read),
    INDEX idx_created (created_at),
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES inventory_items(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Triggers
-- =====================================================

-- Trigger to update stock_status based on quantity
DELIMITER //

CREATE TRIGGER update_stock_status_insert
BEFORE INSERT ON inventory_items
FOR EACH ROW
BEGIN
    IF NEW.quantity = 0 THEN
        SET NEW.stock_status = 'out_of_stock';
    ELSEIF NEW.quantity <= NEW.reorder_level THEN
        SET NEW.stock_status = 'low';
    ELSEIF NEW.quantity <= (NEW.reorder_level * 2) THEN
        SET NEW.stock_status = 'medium';
    ELSE
        SET NEW.stock_status = 'healthy';
    END IF;
END//

CREATE TRIGGER update_stock_status_update
BEFORE UPDATE ON inventory_items
FOR EACH ROW
BEGIN
    IF NEW.quantity = 0 THEN
        SET NEW.stock_status = 'out_of_stock';
    ELSEIF NEW.quantity <= NEW.reorder_level THEN
        SET NEW.stock_status = 'low';
    ELSEIF NEW.quantity <= (NEW.reorder_level * 2) THEN
        SET NEW.stock_status = 'medium';
    ELSE
        SET NEW.stock_status = 'healthy';
    END IF;
END//

DELIMITER ;

-- =====================================================
-- Views for easier querying
-- =====================================================

-- View: Low stock items
CREATE OR REPLACE VIEW low_stock_items AS
SELECT 
    i.id,
    i.item_name,
    i.quantity,
    i.reorder_level,
    i.stock_status,
    c.name AS category_name,
    s.name AS supplier_name
FROM inventory_items i
LEFT JOIN categories c ON i.category_id = c.id
LEFT JOIN suppliers s ON i.supplier_id = s.id
WHERE i.stock_status IN ('low', 'out_of_stock')
ORDER BY i.quantity ASC;

-- View: Inventory summary
CREATE OR REPLACE VIEW inventory_summary AS
SELECT 
    i.id,
    i.item_name,
    i.sku,
    i.quantity,
    i.unit_price,
    i.quantity * i.unit_price AS total_value,
    i.stock_status,
    i.reorder_level,
    c.name AS category_name,
    s.name AS supplier_name,
    i.last_restocked,
    i.updated_at
FROM inventory_items i
LEFT JOIN categories c ON i.category_id = c.id
LEFT JOIN suppliers s ON i.supplier_id = s.id
ORDER BY i.updated_at DESC;

-- =====================================================
-- Sample Data (Optional - for testing)
-- =====================================================

-- Sample supplier
INSERT INTO suppliers (name, contact_person, email, phone, address, city, state, country)
VALUES 
    ('ABC Wholesale', 'John Doe', 'john@abcwholesale.com', '555-0100', '123 Main St', 'New York', 'NY', 'USA'),
    ('XYZ Distributors', 'Jane Smith', 'jane@xyzdist.com', '555-0200', '456 Oak Ave', 'Los Angeles', 'CA', 'USA');

-- =====================================================
-- Indexes for Optimization
-- =====================================================

-- Composite indexes for common queries
CREATE INDEX idx_item_category_status ON inventory_items(category_id, stock_status);
CREATE INDEX idx_transaction_item_date ON stock_transactions(item_id, transaction_date);
CREATE INDEX idx_upload_user_status ON upload_logs(user_id, ocr_status);

-- =====================================================
-- Completion Message
-- =====================================================
-- Database schema created successfully!
-- Total tables: 8 (users, suppliers, categories, inventory_items, stock_transactions, upload_logs, alerts)
-- Total views: 2 (low_stock_items, inventory_summary)
-- Total triggers: 2 (auto stock status update)
-- =====================================================
