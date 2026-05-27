import psycopg2
from psycopg2 import sql 

class DBManager:
    def __init__(self):
        self.DB_HOST = "localhost"
        self.DB_NAME = "Assignment2"
        self.DB_USER = "postgres"
        self.DB_PASS = "medrano12"
        self.DB_PORT = "5432"

        self.conn = None
        self.cursor = None
    
    def connect(self):
        try: 
            self.conn = psycopg2.connect(
                host = self.DB_HOST,
                database = self.DB_NAME,
                user = self.DB_USER,
                password = self.DB_PASS,
                port = self.DB_PORT
            )
            self.cursor = self.conn.cursor()
            return True
        except psycopg2.OperationalError as e:
            print(f"ERROR: Failed to connect to database.")
            print(f"Details: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("\nConnection closed.")

    def _execute_query(self, query, params = None, fetch = False, commit = False):
        if not self.conn:
            print("Database connection is not active.")
            return None

        try:
            self.cursor.execute(query, params)
            if commit:
                self.conn.commit()
            if fetch:
                return self.cursor.fetchall()
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"Database operation failed: {e}")
            return None

    def verify_login(self, email, password):
        if email == "admin@ecommerce.com" and password == "securepassword":
            return ("Admin", 0)
         
        sql_query = """
        SELECT customerID, firstName, isActive
        FROM Customers
        WHERE email = %s;
        """
        result = self._execute_query(sql_query, (email,), fetch = True)

        if result and result[0][2]:
            customer_id, first_name, _ = result[0]
            return ("Customer", customer_id)
        
        return (None, None)
    
    def check_stock_availability(self, product_id, quantity):
        sql_call = "SELECT checkProductStock(%s, %s);"
        result = self._execute_query(sql_call, (product_id, quantity), fetch = True)

        if result:
            return result[0][0]
        return False
    
    def place_new_order(self, customer_id, address, payment_method):
        sql_call = "SELECT placeOrder(%s, %s, %s);"
        result = self._execute_query(sql_call, (customer_id, address, payment_method), fetch = True)

        if result:
            return result[0][0]
        return None
    
    def finalize_order_total(self, order_id):
        sql_call = "SELECT calculateOrderTotal(%s);"
        result = self._execute_query(sql_call, (order_id,), fetch = True, commit = True)

        if result:
            return result[0][0]
        return None
    
    def get_restock_alerts(self, threshold = 50):
        sql_call = "SELECT * FROM getRestockAlerts(%s);"
        return self._execute_query(sql_call, (threshold,), fetch = True)
        
        
    def add_order_item_and_update_stock(self, order_id, product_id, quantity, unit_price):
        if not self.conn: return False

        subtotal = quantity * unit_price

        try:
            if not self.check_stock_availability(product_id, quantity):
                print(f"ERROR: Insufficient stock for product {product_id}.")
                return False
            
            insert_item_sql = """
            INSERT INTO OrderItems (orderID, productID, quantity, unitPrice, subtotal)
            VALUES (%s, %s, %s, %s, %s);
            """
            self.cursor.execute(insert_item_sql, (order_id, product_id, quantity, unit_price, subtotal))

            update_stock_sql = """
            UPDATE Products
            SET stockQuantity = stockQuantity - %s
            WHERE productID = %s;
            """
            self.cursor.execute(update_stock_sql, (quantity, product_id))

            self.conn.commit()
            print(f"Item added to order {order_id} and stock was updated.")
            return True

        except Exception as e:
            self.conn.rollback()
            print(f"Failed to add item to order {order_id}. Transaction rolled back. Error: {e}")
            return False
        
if __name__ == '__main__':
    manager = DBManager()

    if manager.connect():
        print("\n---Testing Login ---")

        role, uid = manager.verify_login("admin@ecommerce.com", "securepassword")
        print(f"Admin Test Results: Role = {role}, ID = {uid}")

        role, uid = manager.verify_login("john.doe@example.com", "anypassword")
        print(f"Customer Test Result: Role = {role}, ID = {uid}")

        print("\n--- Testing Stored Procedures ---")

        alerts = manager.get_restock_alerts(50)
        if alerts is not None:
            print(f"Restock Alerts Found ({len(alerts)}: {alerts})")

        customer_id_example = 1
        product_id_example = 101
        quantity_example = 1
        unit_price_example = 50.00

        new_order_id = manager.place_new_order(
            customer_id_example,
            "123 Main St, Anytown",
            "Credit Card",
        )
        print(f"\nOrder placed. New OrderID: {new_order_id}")

        if new_order_id:
            manager.add_order_item_and_update_stock(
                new_order_id,
                product_id_example,
                quantity_example,
                unit_price_example
            )

            final_total = manager.finalize_order_total(new_order_id)
            print(f"Order {new_order_id} total updated to: ${final_total}")

        manager.close()
        
            

         



