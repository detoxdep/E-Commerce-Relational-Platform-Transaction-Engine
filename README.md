==============================================================================
POSTGRESQL-BACKED E-COMMERCE MANAGEMENT SYSTEM
Course: COP 3703 - Introduction to Databases (Fall 2025)
University of North Florida — School of Computing
==============================================================================
================================================================================

PROJECT OVERVIEW
================================================================================
The E-Commerce Management System is a database-driven desktop application
designed to manage an online storefront's retail operations, customer pipelines,
and backend warehouse inventory. The system interfaces directly with a relational
PostgreSQL instance using Python's raw database adapter pipeline (psycopg2).

A central feature of the application is a robust, multi-step transaction framework
enforcing full ACID compliance (specifically Atomicity). If a customer builds a shopping
cart containing multiple products, the system processes item modifications and drops
inventory counts synchronously. If any individual product breaks warehouse supply limits,
the system executes a complete state rollback to insulate the database from fractional,
corrupted order logs.

Core Architecture Highlights:

Persistent Relational Storage: Full schema mapping across five primary system
tables (Categories, Products, Customers, Orders, and OrderItems).

PL/pgSQL Server Extensions: Implements server-side procedural functions
(place_new_order, add_order_item_and_update_stock, finalize_order_total,
and getRestockAlerts) to handle server logic near the physical rows.

Role-Based Access Control (RBAC): Provides localized authentication splitting
users into a "Customer Dashboard" (for shopping, tracking orders, and evaluating costs)
or an "Admin Dashboard" (for evaluating warehouse supply metrics and low-stock warnings).

Mock Isolation Automated Testing: Features a rigorous programmatic validation matrix
implemented under Python's unittest framework to check database behavior across regular
and boundary transaction profiles.

================================================================================
2. SYSTEM COMPONENT & FILE STRUCTURE
The project directory contains the following core modules and database assets:

├── Arias_EcommerceAssignment3.sql     # Master DDL Schema, Sequences, and PL/pgSQL functions
├── db_manager.py                       # Connection layer and parameterized transaction backend
├── app.py                              # Client GUI application engine managed via Tkinter/ttk
├── unittests-1.py                      # Integration testing suite verifying backend components
└── README.txt                          # Operation and implementation blueprint (this file)

================================================================================
3. DATABASE SCHEMA & ROUTINE BLUEPRINTS
Relational Tables Layout

Categories: Groups merchant inventory (categoryID, categoryName, description, isActive).

Products: Tracks physical items for sale (productID, productName, categoryID, price, stockQuantity, brand, weight, isActive).

Customers: Stores client demographic listings (customerID, firstName, lastName, email, phone, dateOfBirth, registrationDate, isActive).

Orders: High-level transaction mapping tracking totals (orderID, customerID, orderDate, totalAmount, orderStatus, shippingAddress, paymentMethod).

OrderItems: Composite intersection bridge resolving many-to-many relationship rows (orderID, productID, quantity, unitPrice, subtotal).

Core PL/pgSQL Functions

place_new_order(p_customerID, p_shippingAddress, p_paymentMethod): Spawns a clean
header row inside the Orders table, bound to an auto-incrementing identity sequence.

add_order_item_and_update_stock(p_orderID, p_productID, p_quantity, p_unitPrice): Evaluates
available stock. If satisfied, updates inventory quantities and appends records to the
OrderItems table.

finalize_order_total(p_orderID): Aggregates calculated values from downstream
line elements, commits the math, and injects the absolute total into the parent record.

getRestockAlerts(p_threshold): Dynamically builds tabular rows isolating items falling
beneath specified warehouse safety limits.

================================================================================
4. LOGICAL ARCHITECTURE & TRANSACTION MANAGEMENT
Database connections are initialized securely through python context hooks, explicitly
disabling global autocommit modes (self.conn.autocommit = False) to pass execution controls
to application drivers.

When a customer submits a multi-item cart purchase, the interaction runs across a protected
transaction sequence:

An explicit transaction boundary is opened.

The parent order registry row is established using place_new_order.

The engine loops through line records, passing calls to add_order_item_and_update_stock.

If a product check returns a programmatic FALSE indicator (due to insufficient warehouse
quantities or data anomalies), the script trips an alert loop flag.

If flags remain clean, finalize_order_total executes, and a final database COMMIT settles the transaction.

If any line operation fails, the application issues a defensive database ROLLBACK, restoring
original table indices and purging partial entries.

================================================================================
5. TESTING MATRIX AND AUTOMATION SUITE
System logic verification is driven automatically by unittests-1.py. Tests run
directly against active database rows to track constraint responses and verify system performance:

test_01_successful_admin_login / test_02_successful_customer_login
Asserts authentication pathing and verifies character assignments for target role keys.

test_03_invalid_login_fails
Confirms the validation layer returns proper None identifiers under malformed user inputs.

test_04_get_restock_alerts
Validates backend performance for tabular lookups against target low-supply rows.

test_05_customer_order_transaction_success
Tracks multi-step transaction progression: exercises line appending, stock deductions,
and total calculation validations across a nominal customer profile.

test_06_transaction_rollback_on_low_stock
Simulates a boundary constraint failure by requesting quantities exceeding warehouse inventory.
Verifies that partial table rows roll back fully, leaving starting inventory metrics unaffected.

================================================================================
6. PIPELINE INSTRUCTIONS & EXECUTION
Step 1: Environment Dependencies Setup
Ensure you are running an environment containing Python (3.10+) and a local or remote
PostgreSQL server instance. Install the explicit driver bindings via the command terminal:
$ pip install psycopg2

Step 2: Database Migration Execution
Connect to your PostgreSQL server instance using a query interface tool (e.g., pgAdmin or psql terminal).
Execute the complete schema blueprint text script to generate tables, relational indices,
sequences, and server functions:
$ psql -U postgres -d Assignment2 -f Arias_EcommerceAssignment3.sql

Step 3: Verification Layer Validation
Before booting the interface components, verify back-end transaction operations and code lines
by running the automated testing suite:
$ python unittests-1.py

Step 4: Launching the Graphical User Interface (GUI App)
Execute the application runner file to start the system window dashboard interface:
$ python app.py

================================================================================
7. CREDENTIALS AND TARGET WORKSPACE PARAMETERS
Local Database Configuration Defaults:

Host Address: localhost

Target Port: 5432

Target Instance DB: Assignment2

Target Username: postgres

Default Admin Credentials:

User Email: admin@ecommerce.com

Secure Password: securepassword
================================================================================
