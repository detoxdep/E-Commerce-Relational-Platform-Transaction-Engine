--Create Tables--
CREATE TABLE Categories (
categoryID INT PRIMARY KEY,
categoryName VARCHAR(100),
description TEXT,
isActive BOOLEAN 
);

CREATE TABLE Products (
productID INT PRIMARY KEY,
productName VARCHAR(100),
categoryID INT,
price NUMERIC (10,2),
stockQuantity INT,
description TEXT,
brand VARCHAR(50),
weight NUMERIC(8,2),
isActive BOOLEAN,
FOREIGN KEY(categoryID) REFERENCES Categories(categoryID)
);

CREATE TABLE Customers (
customerID INT PRIMARY KEY,
firstName VARCHAR(100),
lastName VARCHAR(100),
email VARCHAR(150) UNIQUE,
phone VARCHAR(20),
dateOfBirth DATE,
registrationDate DATE,
isActive BOOLEAN
);

CREATE TABLE Orders (
orderID INT PRIMARY KEY,
customerID INT,
orderDate DATE,
totalAmount NUMERIC(12,2),
orderStatus VARCHAR(50),
shippingAddress VARCHAR(100),
paymentMethod VARCHAR(50),
FOREIGN KEY(customerID) REFERENCES Customers(customerID)
);

CREATE TABLE OrderItems (
orderID INT,
productID INT,
quantity INT,
unitPrice NUMERIC(10,2),
subtotal NUMERIC(12,2),
PRIMARY KEY(orderID, productID),
FOREIGN KEY(orderID) REFERENCES Orders(orderID),
FOREIGN KEY(productID) REFERENCES Products(productID)
);

CREATE TABLE Reviews (
reviewID INT PRIMARY KEY,
customerID INT,
productID INT,
rating INT,
reviewText TEXT,
reviewDate DATE,
isVerified BOOLEAN,
FOREIGN KEY(customerID) REFERENCES Customers(customerID),
FOREIGN KEY(productID) REFERENCES Products(productID),
CONSTRAINT check_rating CHECK(rating >= 1 AND rating <= 5)
);

--Inserting Data--
INSERT INTO Categories (categoryID, categoryName, description, isActive)
VALUES
(1, 'Electronics', 'Electronic devices and gadgets', TRUE),
(2, 'Clothing', 'Apparel and fashion items', TRUE),
(3, 'Books', 'Books and educational materials', TRUE),
(4, 'Home & Garden', 'Home improvement and gardening supplies', TRUE),
(5, 'Sports', 'Sports equipment and accessories', TRUE);

INSERT INTO Products (productID, productName, categoryID, price,
stockQuantity, description, brand, weight, isActive) VALUES
(101, 'iPhone 15 Pro', 1, 999.99, 50, 'Latest Apple smartphone', 'Apple', 0.19,
TRUE),
(102, 'Samsung Galaxy S24', 1, 899.99, 30, 'Premium Android smartphone',
'Samsung', 0.17, TRUE),
(103, 'MacBook Air M2', 1, 1299.99, 25, 'Lightweight laptop with M2 chip', 'Apple',
1.24, TRUE),
(104, 'Nike Air Max', 2, 129.99, 100, 'Comfortable running shoes', 'Nike', 0.8,
TRUE),
(105, 'Levi''s 501 Jeans', 2, 89.99, 75, 'Classic straight fit jeans', 'Levi''s', 0.6, TRUE),
(106, 'The Great Gatsby', 3, 12.99, 200, 'Classic American novel', 'Scribner', 0.3,
TRUE),
(107, 'Python Programming', 3, 49.99, 80, 'Learn Python programming',
'TechBooks', 1.2, TRUE),
(108, 'Coffee Maker', 4, 79.99, 40, 'Automatic drip coffee maker', 'Breville', 3.5,
TRUE),
(109, 'Yoga Mat', 5, 29.99, 60, 'Non-slip exercise mat', 'FitLife', 1.0, TRUE),
(110, 'Tennis Racket', 5, 149.99, 35, 'Professional tennis racket', 'Wilson', 0.3,
TRUE);

INSERT INTO Customers (customerID, firstName, lastName, email, phone, dateOfBirth, registrationDate, isActive) VALUES
(1001, 'John', 'Smith', 'john.smith@email.com', '555-0101', '1985-03-15', '2023-01-15', TRUE),
(1002, 'Emily', 'Johnson', 'emily.j@email.com', '555-0102', '1990-07-22', '2023-02-20', TRUE),
(1003, 'Michael', 'Brown', 'mbrown@email.com', '555-0103', '1988-11-10', '2023-03-10', TRUE),
(1004, 'Sarah', 'Davis', 'sarah.davis@email.com', '555-0104', '1992-05-30', '2023-04-05', TRUE),
(1005, 'David', 'Wilson', 'dwilson@email.com', '555-0105', '1987-09-18', '2023-05-12', TRUE),
(1006, 'Lisa', 'Martinez', 'lisa.m@email.com', '555-0106', '1991-12-03', '2023-06-08',FALSE);

INSERT INTO Orders (orderID, customerID, orderDate, totalAmount, orderStatus, shippingAddress, paymentMethod) VALUES
(2001, 1001, '2024-01-15', 1129.98, 'Delivered', '123 Main St, City, State 12345', 'Credit Card'),
(2002, 1002, '2024-01-20', 219.98, 'Shipped', '456 Oak Ave, City, State 12346', 'PayPal'),
(2003, 1003, '2024-02-01', 999.99, 'Delivered', '789 Pine St, City, State 12347', 'Credit Card'),
(2004, 1001, '2024-02-15', 89.99, 'Processing', '123 Main St, City, State 12345', 'Debit Card'),
(2005, 1004, '2024-03-01', 1379.98, 'Shipped', '321 Elm St, City, State 12348', 'Credit Card'),
(2006, 1002, '2024-03-10', 62.98, 'Delivered', '456 Oak Ave, City, State 12346', 'PayPal'),
(2007, 1005, '2024-03-15', 179.98, 'Pending', '654 Maple Dr, City, State 12349', 'Credit Card');

INSERT INTO OrderItems (orderID, productID, quantity, unitPrice, subtotal)
VALUES
(2001, 101, 1, 999.99, 999.99),
(2001, 104, 1, 129.99, 129.99),
(2002, 104, 1, 129.99, 129.99),
(2002, 105, 1, 89.99, 89.99),
(2003, 101, 1, 999.99, 999.99),
(2004, 105, 1, 89.99, 89.99),
(2005, 103, 1, 1299.99, 1299.99),
(2005, 108, 1, 79.99, 79.99),
(2006, 106, 3, 12.99, 38.97),
(2006, 109, 1, 29.99, 29.99),
(2007, 110, 1, 149.99, 149.99),
(2007, 109, 1, 29.99, 29.99);

INSERT INTO Reviews (reviewID, customerID, productID, rating, reviewText,
reviewDate, isVerified) VALUES
(3001, 1001, 101, 5, 'Excellent phone! Battery life is amazing.', '2024-01-25', TRUE),
(3002, 1002, 104, 4, 'Very comfortable shoes, great for running.', '2024-01-30', TRUE),
(3003, 1003, 101, 5, 'Love the camera quality!', '2024-02-10', TRUE),
(3004, 1001, 104, 5, 'Perfect fit and very durable.', '2024-02-05', TRUE),
(3005, 1004, 103, 5, 'Fast performance and great design.', '2024-03-15', TRUE),
(3006, 1002, 106, 4, 'Classic book, good condition.', '2024-03-20', TRUE),
(3007, 1005, 110, 3, 'Good racket but a bit heavy for my preference.', '2024-03-25', FALSE);

--View the Tables--
SELECT * FROM Categories;
SELECT * FROM Customers;
SELECT * FROM Orders;
SELECT * FROM OrderItems;
SELECT * FROM Products;
SELECT * FROM Reviews;


--SQL Questions--
/*
1. Retrieve all records from the Categories table.
2. Fetch only the product names and prices of all products.
3. Find all active customers.
4. List all orders with 'Pending' status.
5. Get the total number of products in the store.
6. Get the average price of all products.
7. Find the most expensive product.
8. Find the number of products in each category.
9. List the products ordered by each customer.
10. Retrieve orders that are currently being processed (status: 'Processing' or 'Shipped').
11. Get the total amount spent by each customer.
12. Find customers who have placed more than 1 order.
13. Find products that have never been ordered.
14. Calculate the total quantity sold for each product.
15. Get a list of all reviews along with customer and product information.
16. For each category, show the total revenue generated from products in that category.
17. Get the average rating for each product that has been reviewed.
18. For each payment method, calculate the total amount and number of orders.
19. Find the top 3 best-selling products by quantity.
20. Display customers who have both ordered products and written reviews.
21. Find products with low stock (less than 50 units).
22. Find customers who registered in 2023 and have made at least one purchase.
*/

--SQL Answers--
--1
SELECT * FROM Categories;
--2
SELECT productName, price FROM Products;
--3
SELECT * FROM Customers WHERE isActive = TRUE;
--4
SELECT * FROM Orders WHERE orderStatus LIKE 'Pending';
--5
SELECT COUNT(*) AS Products FROM Products;
--6
SELECT AVG(price) FROM Products;
--7
SELECT MAX(price) FROM Products;
--8
SELECT c.categoryName, COUNT(*) AS num_products 
FROM Categories c 
JOIN Products p ON c.categoryID = p.categoryID 
GROUP BY categoryName;
--9
SELECT c.firstName, c.lastName, p.ProductName 
FROM Customers c 
JOIN Orders o ON c.customerID = o.customerID
JOIN OrderItems oi ON o.orderID = oi.orderID
JOIN Products p ON oi.productID = p.productID;
--10
SELECT * FROM Orders WHERE orderStatus = 'Processing' OR orderStatus = 'Shipped';
--11
SELECT c.firstName, c.lastName, SUM(oi.subtotal) AS totalSpent
FROM Customers c
JOIN Orders o ON c.customerID = o.customerID
JOIN OrderItems oi ON o.orderID = oi.orderID
GROUP BY c.firstName, c.lastName;
--12
SELECT c.firstName, c.lastName, COUNT(DISTINCT o.orderID) AS num_orders
FROM Customers c
JOIN Orders o ON c.customerID = o.customerID
GROUP BY c.firstName, c.lastName
HAVING COUNT(DISTINCT o.orderID) > 1;
--13
SELECT p.productName
FROM Products p
LEFT JOIN OrderItems oi ON p.productID = oi.productID
WHERE oi.orderID IS NULL;
--14
SELECT p.productName, SUM(oi.quantity) AS num_sold
FROM Products p
JOIN OrderItems oi ON p.productID = oi.productID
GROUP BY p.productName;
--15
SELECT c.firstName, c.lastName, p.productName, r.reviewText
FROM Reviews r
JOIN Products p ON p.productID = r.productID
JOIN Customers c ON c.customerID = r.customerID; 
--16
SELECT ca.categoryName, SUM(oi.subtotal) AS totalRevenue
FROM Categories ca
JOIN Products p ON ca.categoryID = p.categoryID
JOIN OrderItems oi ON p.productID = oi.productID
JOIN Orders o ON oi.orderID = o.orderID
GROUP BY ca.categoryName;
--17
SELECT p.productName, AVG(r.rating) AS avgRating
From Products p
JOIN Reviews r ON p.productID = r.productID
GROUP BY p.productName;
--18
SELECT o.paymentMethod, SUM(o.totalAmount) AS total_amount, COUNT(o.paymentMethod) AS num_of_orders
FROM Orders o
GROUP BY o.paymentMethod;
--19
SELECT p.productName, SUM(oi.quantity) AS quantity
FROM Products p
JOIN OrderItems oi ON p.productID = oi.productID
GROUP BY p.productName
ORDER BY quantity DESC LIMIT 3;
--20
SELECT c.firstName, c.lastName
FROM Customers c
LEFT JOIN Orders o ON c.customerID = o.customerID
LEFT JOIN Reviews r ON c.customerID = r.customerID
WHERE o.orderID IS NOT NULL AND r.reviewID IS NOT NULL
GROUP BY c.firstName, c.lastName;
--21
SELECT p.productName, p.stockQuantity AS low_stock 
FROM Products p
WHERE p.stockQuantity < 50;
--22
SELECT c.firstName, c.lastName, c.registrationDate, COUNT(o.orderID) AS num_of_orders
FROM Customers c
JOIN Orders o ON c.customerID = o.customerID
WHERE c.registrationDate BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY c.firstName, c.lastName, c.registrationDate
HAVING COUNT(o.orderID) > 0;

--Reflection--
/*
What was the most challenging query for you, and why?

	The hardest part for me was mapping out which tables I needed to join to achieve the desrired outcome.

Did you face any unexpected errors while executing your SQL?

	It was mainly syntax errors that I was able to resolve quickly with the error message I got in the output.

What’s one thing you learned while working on this?

	I learn how to show a desire amount from a list using the LIMIT function.
*/

-------Assignmemt 3-------

--Constraints--

--1
ALTER TABLE OrderItems
ADD CONSTRAINT fk_order_id_cascade
FOREIGN KEY (orderID)
REFERENCES Orders(orderID)
ON DELETE CASCADE;

--2
ALTER TABLE Orders
ADD CONSTRAINT check_total_amount_positive
CHECK (totalAmount > 0);

--3
ALTER TABLE Products
ADD CONSTRAINT check_stock_quantity_non_negative
CHECK (stockQuantity >= 0);

--4
ALTER TABLE Products
ADD CONSTRAINT check_price_positive
CHECK (price > 0);

--5 (Already done in inital DDL but here for completeness)
ALTER TABLE Reviews
ADD CONSTRAINT check_rating_range
CHECK (rating >= 1 AND rating <= 5);

--6
ALTER TABLE Customers
ADD CONSTRAINT check_registration_date_not_future
CHECK (registrationDate <= CURRENT_DATE);

--7 (Already done in inital DDL but here for completeness)
ALTER TABLE Customers
ADD CONSTRAINT unique_customer_email
UNIQUE (email);

--Testing Constarints--

--1
INSERT INTO Orders (orderID, customerID, orderDate, totalAmount, orderStatus, shippingAddress, paymentMethod)
VALUES (9999, 1001, '2024-04-01', -50.00, 'Pending', 'Test Address', 'Credit Card');

SELECT * FROM Orders WHERE totalAmount < 0;

-- 2
INSERT INTO Products (productID, productName, categoryID, price, stockQuantity, description, brand, weight, isActive)
VALUES (9999, 'Bad Stock Product', 1, 10.00, -10, 'Test Desc', 'Test Brand', 0.1, TRUE);

SELECT * FROM Products WHERE stockQuantity < 0;


-- 3
INSERT INTO Products (productID, productName, categoryID, price, stockQuantity, description, brand, weight, isActive)
VALUES (9998, 'Zero Price Product', 1, 0.00, 10, 'Test Desc', 'Test Brand', 0.1, TRUE);

SELECT * FROM Products WHERE price <= 0;


-- 4
INSERT INTO Reviews (reviewID, customerID, productID, rating, reviewText, reviewDate, isVerified)
VALUES (9999, 1001, 101, 6, 'Bad rating test', '2024-04-01', TRUE);

SELECT * FROM Reviews WHERE rating > 5 OR rating < 1;


-- 5
INSERT INTO Customers (customerID, firstName, lastName, email, phone, dateOfBirth, registrationDate, isActive)
VALUES (9999, 'Future', 'Customer', 'future@email.com', '555-0199', '1995-01-01', '2026-12-31', TRUE);

SELECT * FROM Customers WHERE registrationDate > CURRENT_DATE;


-- 6
INSERT INTO Customers (customerID, firstName, lastName, email, phone, dateOfBirth, registrationDate, isActive)
VALUES (9998, 'Duplicate', 'Email', 'john.smith@email.com', '555-0188', '1996-01-01', '2024-04-01', TRUE);

SELECT * FROM Customers WHERE customerID = 9998;

--High-Value Customers View--

-- 1. Create HighValueCustomersView
CREATE VIEW HighValueCustomersView AS
SELECT
    c.customerID,
    c.firstName,
    c.lastName,
    c.email,
    SUM(o.totalAmount) AS totalOrderAmount,
    COUNT(o.orderID) AS orderCount
FROM
    Customers c
JOIN
    Orders o ON c.customerID = o.customerID
GROUP BY
    c.customerID, c.firstName, c.lastName, c.email
HAVING
    COUNT(o.orderID) > 0; 
    
-- Verify the view structure and data
SELECT * FROM HighValueCustomersView;

-- 2. Query the view to list customers who have spent more than $500 in total
SELECT
	customerID,
	firstName,
	lastName,
	totalOrderAmount
FROM
	HighValueCustomersView
WHERE
	totalOrderAmount > 500.00
ORDER BY
	totalOrderAmount DESC;

-- 3. Create LowStockProductsView
CREATE VIEW LowStockProductsView AS
SELECT
    p.productID,
    p.productName,
    c.categoryName,
    p.stockQuantity,
    p.price
FROM
    Products p
JOIN
    Categories c ON p.categoryID = c.categoryID
WHERE
    p.stockQuantity < 50;
    
-- Verify the view structure and data
SELECT * FROM LowStockProductsView;

-- 4. Query the view to find 'Electronics' products that are low in stock
SELECT
    productID,
    productName,
    stockQuantity,
    price
FROM
    LowStockProductsView
WHERE
    categoryName = 'Electronics';

--Create Indexes--

--1
CREATE UNIQUE INDEX idx_customer_email ON Customers (email);
--Speeds up customer login and search by email. Enforces email uniqueness faster than a full table scan.

--2
CREATE INDEX idx_orders_customerid_orderdate ON Orders (customerID, orderDate);
-- Optimizes queries that filter orders by a specific customer ID AND a date range. It sorts by customer first.

--3
CREATE INDEX idx_reviews_productid ON Reviews (productID);

SELECT
    r.reviewID,
    r.rating,
    r.reviewText,
    c.firstName,
    c.lastName
FROM
    Reviews r
JOIN
    Customers c ON r.customerID = c.customerID
WHERE
    r.productID = 101;

--Improves performance when retrieving all reviews for a single product ID, avoiding a full table scan on Reviews.

--4
CREATE INDEX idx_orderitems_orderid_productid ON OrderItems (orderID, productID);
--Ensures fast lookups when searching for a specific product within a specific order, as well as efficient FK validation.

--Normalization--
--Inside of word document

--Reflection--
/*
What was the most challenging query for you, and why?

	The hardest part for me was understa

Did you face any unexpected errors while executing your SQL?

	It was mainly syntax errors that I was able to resolve quickly with the error message I got in the output.

What’s one thing you learned while working on this?

	I learn how to show a desire amount from a list using the LIMIT function.
*/

-------Assignmemt 4-------
-- 1. FUNCTION: placeOrder
-- Creates a new order record and returns the new orderID.
CREATE OR REPLACE FUNCTION placeOrder(
    p_customerID INT,
    p_shippingAddress VARCHAR,
    p_paymentMethod VARCHAR
)
RETURNS INT AS $$
DECLARE
    new_orderID INT;
BEGIN
    -- Insert the new order record. totalAmount starts at 0.00
    INSERT INTO Orders (
        customerID,
        orderDate,
        totalAmount,
        orderStatus,
        shippingAddress,
        paymentMethod
    )
    VALUES (
        p_customerID,
        CURRENT_DATE, -- Uses the current date of execution
        0.00,
        'Pending', -- Default status
        p_shippingAddress,
        p_paymentMethod
    )
    -- RETURNING is a PostgreSQL feature that retrieves the new ID
    RETURNING orderID INTO new_orderID;

    -- Return the generated order ID to the application
    RETURN new_orderID;
END;
$$ LANGUAGE plpgsql;

-- 2. FUNCTION: calculateOrderTotal
-- Computes the sum of all OrderItems subtotals for a given order and updates Orders.totalAmount.
CREATE OR REPLACE FUNCTION calculateOrderTotal(
    p_orderID INT
)
RETURNS NUMERIC(12,2) AS $$
DECLARE
    calculated_total NUMERIC(12,2);
BEGIN
    -- Calculate the sum of all subtotals for the order
    SELECT SUM(subtotal)
    INTO calculated_total
    FROM OrderItems
    WHERE orderID = p_orderID;

    -- Update the totalAmount in the Orders table
    UPDATE Orders
    SET totalAmount = COALESCE(calculated_total, 0.00) -- Use 0.00 if sum is NULL (empty order)
    WHERE orderID = p_orderID;

    -- Return the calculated total for verification in the application
    RETURN COALESCE(calculated_total, 0.00);
END;
$$ LANGUAGE plpgsql;

-- 3. FUNCTION: checkProductStock
-- Returns TRUE if stockQuantity is >= requestedQuantity, FALSE otherwise.
CREATE OR REPLACE FUNCTION checkProductStock(
    p_productID INT,
    p_requestedQuantity INT
)
RETURNS BOOLEAN AS $$
DECLARE
    current_stock INT;
BEGIN
    -- Retrieve the current stock quantity for the product
    SELECT stockQuantity INTO current_stock
    FROM Products
    WHERE productID = p_productID;

    -- If no product is found (stock is NULL), or if the requested quantity exceeds stock, return FALSE
    IF current_stock IS NULL OR p_requestedQuantity > current_stock THEN
        RETURN FALSE;
    ELSE
        -- Stock is sufficient
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 4. FUNCTION: getRestockAlerts
-- Returns a table of products whose stock is below the specified threshold.
CREATE OR REPLACE FUNCTION getRestockAlerts(
    p_threshold INT
)
RETURNS TABLE (
    product_id INT,
    product_name VARCHAR,
    current_stock INT
) AS $$
BEGIN
    -- Return the query result directly
    RETURN QUERY
    SELECT
        productID,
        productName,
        stockQuantity
    FROM
        Products
    WHERE
        stockQuantity < p_threshold
    ORDER BY
        stockQuantity ASC; -- Order by lowest stock first
END;
$$ LANGUAGE plpgsql;

CREATE SEQUENCE orders_orderid_seq START WITH 2008 INCREMENT BY 1;

-- 2. Set the orderID column to automatically use this sequence as its default value
ALTER TABLE Orders
ALTER COLUMN orderID SET DEFAULT nextval('orders_orderid_seq');

-- 1. Drop the existing constraint that enforces > 0
ALTER TABLE Orders
DROP CONSTRAINT check_total_amount_positive;

-- 2. Add the new constraint that allows >= 0 (non-negative)
ALTER TABLE Orders
ADD CONSTRAINT check_total_amount_non_negative
CHECK (totalAmount >= 0);