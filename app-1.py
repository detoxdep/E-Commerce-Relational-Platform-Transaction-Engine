import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from db_manager import DBManager
import sys

RESTOCK_THRESHOLD = 50
class EcommerceApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Roger Arias and Irene Ramirez E-commerce Management System")
        self.geometry("800x600")
        self.current_user_id = None
        self.current_role = None

        self.db = DBManager()

        if not self.db.connect():
            messagebox.showerror("Connection Error", "FATAL: Could not connect to database. Check console for details (DBManager credentials).")

            try:
                self.destroy()
            except:
                sys.exit(1)
            return
        
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()
        self.columnconfigure(0, weight = 1)

        login_frame = ttk.Frame(self, padding = "30 30 30 30")
        login_frame.grid(row = 0, column = 0, sticky = "nsew")
        login_frame.columnconfigure(0, weight = 1)
        login_frame.columnconfigure(1, weight = 3)

        ttk.Label(login_frame, text = "System Login (Group Assignment)", font = ("Arial", 18, "bold")).grid(row = 0, column = 0, columnspan = 2, pady = 20)

        ttk.Label(login_frame, text = "Email:").grid(row = 1, column = 0, sticky = 'w', padx = 5, pady =5)
        self.email_entry = ttk.Entry(login_frame, width = 40)
        self.email_entry.grid(row = 1, column = 1, sticky = 'ew', padx = 5, pady = 5)

        ttk.Label(login_frame, text = "Password:").grid(row = 2, column = 0, sticky = 'w', padx = 5, pady = 5)
        self.password_entry = ttk.Entry(login_frame, show = "*", width = 40) 
        self.password_entry.grid(row = 2, column = 1, sticky = 'ew', padx =5, pady = 5)

        ttk.Button(login_frame, text = "Login", command = self.handle_login).grid(row = 3, column = 0, columnspan = 2, pady = 20)

        ttk.Label(login_frame, text = "Admin admin@ecommerce.com / securepassword", font = ("Arial", 10, "italic")).grid(row = 4, column = 0, columnspan = 2)
        ttk.Label(login_frame, text = "Customer: john.smith@email.com / anypassword", font = ("Arial", 10, "italic")).grid(row = 5, column = 0, columnspan = 2)

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        role, user_id = self.db.verify_login(email, password)

        if role:
            self.current_role = role
            self.current_user_id = user_id
            messagebox.showinfo("Login Success", f"Welcome, {role} (ID: {user_id})!")

            if role == "Admin":
                self.show_admin_dashboard()
            else:
                self.show_customer_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def show_admin_dashboard(self):
        self.clear_screen()
        self.title("Admin Dashboard")
        
        main_frame = ttk.Frame(self, padding = "10")
        main_frame.pack(fill = 'both', expand = True)

        ttk.Label(main_frame, text = "ADMIN DASHBOARD", font = ("Arial", 20, "bold")).pack(pady = 10)
        ttk.Label(main_frame, text = f"Logged in as: {self.current_role} (ID: {self.current_user_id})").pack(pady = 5)

        ttk.Button(main_frame, text = "View Restock Alerts", command = self.show_restock_alerts, width = 30).pack(pady = 10)
        ttk.Button(main_frame, text = "Manage Products (CRUD)", command = lambda: messagebox.showinfo("Feature", "Placeholder for full Product CRUD system")).pack(pady = 10)
        ttk.Button(main_frame, text = "Manage Orders", command = lambda: messagebox.showinfo("Feature", "Placeholder for Order status updates.")).pack(pady = 10)
        ttk.Button(main_frame, text = "Logout", command = self.show_login_screen, width = 30).pack(pady = 20)

    def show_restock_alerts(self):
        alerts = self.db.get_restock_alerts(RESTOCK_THRESHOLD)

        if alerts is None:
            messagebox.showerror("Error", "Could not fetch restock alerts.")
            return
        
        top = tk.Toplevel(self)
        top.title("Restock Alerts")
        top.geometry("500x300")

        ttk.Label(top, text = f"Products Below Stock Threshold ({RESTOCK_THRESHOLD})", font = ("Arial", 14, "bold")).pack(pady = 10)
        
        if not alerts:
            ttk.Label(top, text = "No products require immediate restock.").pack(pady = 20)
            return
        
        tree = ttk.Treeview(top, columns = ("ID", "Name", "Stock"), show = "headings")
        tree.heading("ID", text = "Product ID")
        tree.heading("Name", text = "Product Name")
        tree.heading("Stock", text = "Current Stock")
        tree.column("ID", width = 80, anchor = "center")
        tree.column("Name", width = 250)
        tree.column("Stock", width = 100, anchor = "center")
        
        for pid, name, stock in alerts:
            tree.insert("", tk.END, values = (pid, name, stock))

        tree.pack(fill = "both", expand = True, padx = 10, pady = 10)
        ttk.Button(top, text = "Close", command = top.destroy).pack(pady = 10)

    def show_customer_dashboard(self):
        
        self.clear_screen()
        self.title("Customer Dashboard")
        
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        ttk.Label(main_frame, text="CUSTOMER HOME", font=("Arial", 20, "bold")).pack(pady=10)
        ttk.Label(main_frame, text=f"Logged in as: Customer (ID: {self.current_user_id})").pack(pady=5)
        
        ttk.Button(main_frame, text="Browse and Place Order", command=self.show_product_browser, width=40).pack(pady=10)
        ttk.Button(main_frame, text="View My Orders", command=lambda: messagebox.showinfo("Feature", "Placeholder for viewing past orders.")).pack(pady=10)
        ttk.Button(main_frame, text="Logout", command=self.show_login_screen, width=40).pack(pady=20)
        
    def show_product_browser(self):
        
        self.clear_screen()
        self.title("Product Browser - Start New Order")
        
        sql = "SELECT productID, productName, price, stockQuantity FROM Products WHERE isActive = TRUE ORDER BY productID;"
        products_data = self.db._execute_query(sql, fetch=True)
        
        if products_data is None:
            ttk.Label(self, text="Error fetching product data.").pack(pady=50)
            ttk.Button(self, text="Back to Dashboard", command=self.show_customer_dashboard).pack(pady=10)
            return
        
        ttk.Label(self, text="Available Products", font=("Arial", 16, "bold")).pack(pady=10)
        
       
        self.cart = {} # {productID: {'name': str, 'price': float, 'quantity': int}}
        
        content_frame = ttk.Frame(self)
        content_frame.pack(fill='both', expand=True, padx=20)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)

        
        prod_frame = ttk.LabelFrame(content_frame, text="Product List")
        prod_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        tree = ttk.Treeview(prod_frame, columns=("ID", "Name", "Price", "Stock"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Price", text="Price")
        tree.heading("Stock", text="Stock")
        tree.column("ID", width=50, anchor='center')
        tree.column("Price", width=80, anchor='e')
        tree.column("Stock", width=80, anchor='center')
        
        for pid, name, price, stock in products_data:
            tree.insert("", tk.END, iid=pid, values=(pid, name, f"${price}", stock))
            
        tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        def add_to_cart():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a product first.")
                return
            
            pid, name, price_str, stock = tree.item(selected_item, 'values')
            pid = int(pid)
            price = float(price_str.replace('$', ''))
            stock = int(stock)
            
            quantity = simpledialog.askinteger("Quantity", f"Enter quantity for {name} (Max: {stock}):", parent=self, minvalue=1, maxvalue=stock)
            
            if quantity is not None:
                    
                if pid in self.cart:
                    self.cart[pid]['quantity'] += quantity
                else:
                    self.cart[pid] = {'name': name, 'price': price, 'quantity': quantity}
                self.update_cart_summary()

        ttk.Button(prod_frame, text="Add Selected to Cart", command=add_to_cart).pack(pady=5)
        
        cart_frame = ttk.LabelFrame(content_frame, text="Shopping Cart")
        cart_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        cart_frame.rowconfigure(0, weight=1)
        
        self.cart_tree = ttk.Treeview(cart_frame, columns=("Name", "Qty", "Subtotal"), show="headings")
        self.cart_tree.heading("Name", text="Product Name")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Subtotal", text="Subtotal")
        self.cart_tree.column("Qty", width=50, anchor='center')
        self.cart_tree.column("Subtotal", width=100, anchor='e')
        self.cart_tree.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        
        self.cart_total_label = ttk.Label(cart_frame, text="Total: $0.00", font=("Arial", 14, "bold"))
        self.cart_total_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        
        
        ttk.Button(cart_frame, text="Place Order", command=self.place_order_transaction).grid(row=2, column=0, pady=10)

        ttk.Button(self, text="Back to Dashboard", command=self.show_customer_dashboard).pack(pady=10)

    def update_cart_summary(self):
         
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
            
        total = 0.0
        for pid, item in self.cart.items():
            subtotal = item['price'] * item['quantity']
            total += subtotal
            self.cart_tree.insert("", tk.END, values=(item['name'], item['quantity'], f"${subtotal:.2f}"))

        self.cart_total_label.config(text=f"Total: ${total:.2f}")


    def place_order_transaction(self):
        
        if not self.cart:
            messagebox.showwarning("Order Failed", "Your cart is empty.")
            return

        
        address = simpledialog.askstring("Shipping", "Enter Shipping Address:", parent=self)
        if not address: return

        payment_method = simpledialog.askstring("Payment", "Enter Payment Method (e.g., Credit Card):", parent=self)
        if not payment_method: return

        new_order_id = self.db.place_new_order(self.current_user_id, address, payment_method)
        
        if not new_order_id:
            messagebox.showerror("Order Failed", "Could not start new order. Check database logs for constraint issues.")
            return

        
        all_items_added = True
        
        for pid, item in self.cart.items():
            
            success = self.db.add_order_item_and_update_stock(
                new_order_id, 
                pid, 
                item['quantity'], 
                item['price']
            )
            
            if not success:
                
                all_items_added = False
                messagebox.showwarning("Stock Failure", f"Failed to add {item['name']} due to low stock or error. Item skipped.")
        
        
        final_total = self.db.finalize_order_total(new_order_id)
        
        if final_total is not None and final_total > 0:
            messagebox.showinfo("Order Placed", 
                                f"Order {new_order_id} successfully placed!\nTotal Amount: ${final_total:.2f}\n{len(self.cart)} item(s) processed.")
            self.cart = {}
            self.show_customer_dashboard() # Refresh view
        else:
            messagebox.showwarning("Order Incomplete", f"Order {new_order_id} started but could not be finalized. Total is $0.00.")


if __name__ == "__main__":
    app = EcommerceApp()
    try:
        app.mainloop()
    finally:
        
        if hasattr(app, 'db'):
            app.db.close()



