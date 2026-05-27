import unittest
from db_manager import DBManager # Import your DBManager class
import random
import time

# --- TEST CONSTANTS ---
# Use fixed high IDs to ensure they don't clash with real data
TEST_PRODUCT_ID = 99999
TEST_CUSTOMER_ID = 99999
ADMIN_EMAIL = "admin@ecommerce.com" 
CUSTOMER_EMAIL = "john.smith@email.com" # Use a known customer email from your data

# Generate a unique email every time to prevent conflicts if cleanup fails
TEST_EMAIL = f"test_user_{int(time.time())}@{random.randint(100, 999)}.com" 

# List to track all test order IDs created during the tests
TEST_ORDER_IDS = []

class TestDBManager(unittest.TestCase):
    """
    Tests the core database interaction and transaction logic in DBManager.
    These tests are integration tests because they interact with the actual database.
    """
    
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests: Initializes the DBManager and sets up test data."""
        cls.db = DBManager()
        if not cls.db.connect():
            raise Exception("Database connection failed in setUpClass. Check credentials.")
            
        # --- 1. SET UP TEST CUSTOMER ---
        # Note: We use ON CONFLICT to ensure the customer is present, updating the email 
        # to the unique TEST_EMAIL each time for login testing.
        cls.db._execute_query(
            """
            INSERT INTO Customers (customerID, firstName, lastName, email, registrationDate, isActive)
            VALUES (%s, 'Test', 'User', %s, CURRENT_DATE, TRUE)
            ON CONFLICT (customerID) DO UPDATE SET email = EXCLUDED.email; 
            """, 
            (TEST_CUSTOMER_ID, TEST_EMAIL), 
            commit=True
        )

        # --- 2. SET UP TEST PRODUCT (for restock alert and transactions) ---
        cls.db._execute_query(
            """
            INSERT INTO Products (productID, productName, categoryID, price, stockQuantity, isActive)
            VALUES (%s, 'Test Low Stock Item', 1, 10.00, 40, TRUE) 
            ON CONFLICT (productID) DO UPDATE SET stockQuantity = 40;
            """, 
            (TEST_PRODUCT_ID,), 
            commit=True
        )
        print(f"\nTest Customer Set Up: ID {TEST_CUSTOMER_ID}, Email: {TEST_EMAIL}")


    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests: Cleans up test data and closes the connection."""
        print("\n--- Cleaning up test data ---")
        
        # Foreign Key Cleanup Order: OrderItems -> Orders -> Customers/Products

        # 1. Clean up OrderItems related to the test product or any order created by tests
        if TEST_ORDER_IDS:
            # Delete order items for all orders created during tests
            cls.db._execute_query("DELETE FROM OrderItems WHERE orderID IN %s;", (tuple(TEST_ORDER_IDS),), commit=True)
            
        # Delete items that might reference the test product (just in case)
        cls.db._execute_query("DELETE FROM OrderItems WHERE productID = %s;", (TEST_PRODUCT_ID,), commit=True)
            
        # *** FIX ADDED HERE *** # 2. Clean up ALL Orders associated with the test customer ID=99999
        cls.db._execute_query("DELETE FROM Orders WHERE customerID = %s;", (TEST_CUSTOMER_ID,), commit=True)

        # 3. Clean up Test Customer (Now safe to delete as Orders are gone)
        cls.db._execute_query("DELETE FROM Customers WHERE customerID = %s;", (TEST_CUSTOMER_ID,), commit=True)

        # 4. Clean up Test Product
        cls.db._execute_query("DELETE FROM Products WHERE productID = %s;", (TEST_PRODUCT_ID,), commit=True)
        
        cls.db.close()
        print("Test environment cleaned up and DB connection closed.")

    # =====================================================================
    # TEST 1: LOGIN VERIFICATION
    # =====================================================================
    def test_01_verify_admin_login(self):
        """Tests login success for an Admin user."""
        role, user_id = self.db.verify_login(ADMIN_EMAIL, "securepassword")
        self.assertEqual(role, "Admin", "Admin login should return 'Admin' role.")
        self.assertIsNotNone(user_id, "Admin login should return a valid user ID.")

    def test_02_verify_customer_login(self):
        """Tests login success for a Customer user (using the setup test user)."""
        # We test the dynamically generated email here:
        role, user_id = self.db.verify_login(TEST_EMAIL, "anypassword")
        self.assertEqual(role, "Customer", "Customer login should return 'Customer' role.")
        # Fix for previous error: assertIs changed to assertEqual for value comparison
        self.assertEqual(user_id, TEST_CUSTOMER_ID, "Customer login should return the correct test user ID.")

    def test_03_verify_invalid_login(self):
        """Tests login failure for a non-existent user."""
        role, user_id = self.db.verify_login("nonexistent@user.com", "badpass")
        self.assertIsNone(role, "Invalid login should return None role.")
        self.assertIsNone(user_id, "Invalid login should return None user ID.")
        
    # =====================================================================
    # TEST 2: ADMIN FEATURE (RESTOCK)
    # =====================================================================
    def test_04_get_restock_alerts(self):
        """Tests that the low-stock product is correctly identified."""
        alerts = self.db.get_restock_alerts(threshold=50)
        found_test_product = any(pid == TEST_PRODUCT_ID for pid, name, stock in alerts)
        self.assertTrue(found_test_product, f"Test product (ID: {TEST_PRODUCT_ID}) with stock < 50 should be in the restock alerts.")

    # =====================================================================
    # TEST 3: CUSTOMER TRANSACTION (ORDER)
    # =====================================================================
    def test_05_place_order_transaction(self):
        """
        Tests the entire order placement flow (place_new_order, add_item, finalize).
        """
        initial_stock = 40
        order_quantity = 5
        
        # 1. Place Order
        new_order_id = self.db.place_new_order(TEST_CUSTOMER_ID, "123 Test St", "Test Card")
        global TEST_ORDER_IDS
        TEST_ORDER_IDS.append(new_order_id) # Track the order for teardown
        
        self.assertIsNotNone(new_order_id, "Should successfully create a new order ID.")

        # 2. Add Item and Update Stock
        item_added = self.db.add_order_item_and_update_stock(
            new_order_id, TEST_PRODUCT_ID, order_quantity, unit_price=10.00
        )
        self.assertTrue(item_added, "Should successfully add the item and update stock.")

        # 3. Finalize Total
        final_total = self.db.finalize_order_total(new_order_id)
        expected_total = order_quantity * 10.00
        self.assertEqual(final_total, expected_total, f"Final total should be ${expected_total}")

        # 4. Verify Stock Reduction
        self.db.cursor.execute("SELECT stockQuantity FROM Products WHERE productID = %s;", (TEST_PRODUCT_ID,))
        updated_stock = self.db.cursor.fetchone()[0]
        expected_stock = initial_stock - order_quantity
        self.assertEqual(updated_stock, expected_stock, f"Stock should be reduced from {initial_stock} to {expected_stock}.")

    def test_06_transaction_rollback_on_low_stock(self):
        """Tests that an item order fails and stock is NOT changed if quantity exceeds stock."""
        # Note: This test reads the current stock, which was reduced by test_05.
        self.db.cursor.execute("SELECT stockQuantity FROM Products WHERE productID = %s;", (TEST_PRODUCT_ID,))
        initial_stock = self.db.cursor.fetchone()[0] 
        order_quantity = initial_stock + 1 # Attempt to order 1 more than available
        
        # 1. Place Order
        new_order_id = self.db.place_new_order(TEST_CUSTOMER_ID, "123 Rollback St", "Rollback Card")
        global TEST_ORDER_IDS
        TEST_ORDER_IDS.append(new_order_id) # Track the order for teardown

        # 2. Attempt to Add Item (This should fail and rollback its transaction)
        item_added = self.db.add_order_item_and_update_stock(
            new_order_id, TEST_PRODUCT_ID, order_quantity, unit_price=10.00
        )
        self.assertFalse(item_added, "Item addition should fail due to low stock.")

        # 3. Verify Stock is UNCHANGED
        self.db.cursor.execute("SELECT stockQuantity FROM Products WHERE productID = %s;", (TEST_PRODUCT_ID,))
        final_stock = self.db.cursor.fetchone()[0]
        self.assertEqual(final_stock, initial_stock, "Stock should remain unchanged after a failed low-stock transaction attempt.")


if __name__ == '__main__':
    unittest.main()
