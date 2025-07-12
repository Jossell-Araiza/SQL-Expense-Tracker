-- Clean up existing tables if they exist (already in your file)
DROP TABLE IF EXISTS expenses CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- Create table for expense categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Create table for users (basic for now; expand for auth later)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Create table for expenses
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    expense_date DATE NOT NULL DEFAULT CURRENT_DATE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE RESTRICT
);

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
('Food', 'Dining and groceries'),
('Transportation', 'Fuel, public transit, etc.'),
('Entertainment', 'Movies, concerts, etc.'),
('Bills', 'Utilities, rent, etc.'),
('Other', 'Miscellaneous expenses');

-- Insert sample users (use hashed passwords in production; placeholders here)
INSERT INTO users (username, email, password_hash) VALUES
('john_doe', 'john@example.com', '$2b$12$ZLf00wvjHCGOmw6kwGuUru1tjcdASMYsmAmttWQwXl86qw95Rpqna'),
('jane_smith', 'jane@example.com', '$2b$12$A5JmtNMCkk/FCsGqgsuDiOmVj6UH4bML6fHXb1ppfSRoOvVop45Ce');

-- Insert sample expenses
INSERT INTO expenses (user_id, category_id, amount, expense_date, description) VALUES
(1, 1, 45.50, '2025-07-01', 'Grocery shopping'),
(1, 2, 20.00, '2025-07-02', 'Bus pass'),
(2, 3, 15.00, '2025-07-03', 'Movie ticket'),
(2, 4, 120.00, '2025-07-01', 'Electricity bill');

-- Sample Queries for Testing (optional, but good for verification)
-- Monthly spending by category for a user
SELECT 
    c.name AS category,
    EXTRACT(YEAR FROM e.expense_date) AS year,
    EXTRACT(MONTH FROM e.expense_date) AS month,
    SUM(e.amount) AS total_amount
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = 1
GROUP BY c.name, year, month
ORDER BY year DESC, month DESC, total_amount DESC;

-- Recent expenses for a user
SELECT 
    e.expense_id,
    c.name AS category,
    e.amount,
    e.expense_date,
    e.description
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE e.user_id = 1
ORDER BY e.expense_date DESC
LIMIT 10;