import tkinter as tk
import uuid

class Cart:
    def __init__(self,db, user, root):
        self.items = {}
        self.db = db
        self.user = user
        self.root = root
    def add_item(self, item):
        if item['name'] in self.items:
            self.items[item['name']] += 1
        else:
            self.items[item['name']] = 1

    def get_total_cost(self):
        total = 0
        for item_name, quantity in self.items.items():
            item = self.db.get_item_by_name(item_name)
            total += item['price'] * quantity
        return total
    
    def confirm_purchase(self):
        purchases = {item_name: quantity for item_name, quantity in self.items.items()}
        self.db.update_user_purchases(self.user, purchases)
        self.print_receipt()
        self.items = {}  # Clear the cart

    def print_receipt(self):
        receipt_window = tk.Toplevel(self.root)
        tk.Label(receipt_window, text="Receipt", font=("Arial", 24)).pack()
        tk.Label(receipt_window, text="-----------------------------").pack()
        for item_name, quantity in self.items.items():
            tk.Label(receipt_window, text=f"Item: {item_name}").pack()
            tk.Label(receipt_window, text=f"Quantity: {quantity}").pack()
            tk.Label(receipt_window, text="-----------------------------").pack()
        total_cost = self.get_total_cost()
        tk.Label(receipt_window, text=f"Total cost: {total_cost}").pack()

class Merchandise:
    def __init__(self, root, db, dashboard, cart, user, barber=None):
        self.root = root
        self.db = db
        self.cart = cart
        self.user = user
        self.barber = barber
        self.dashboard = dashboard
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.cart_frame = tk.Frame(self.root)
        self.cart_frame.pack()
        if barber:
            self.create_item_fields()
        else:
            self.create_widgets()

    def create_widgets(self):
        self.merchandise_list = self.db.get_merchandise()
        for item in self.merchandise_list:
            tk.Label(self.frame, text=item['name']).pack()
            tk.Button(self.frame, text='Add to Cart', command=lambda i=item: self.add_to_cart(i)).pack()
        tk.Button(self.frame, text='Confirm Purchase', command=lambda: self.cart.confirm_purchase()).pack()
        tk.Button(self.frame, text='Back', command=self.back).pack()

    def buy(self, item):
        self.db.add_merchandise(item)
    def back(self):
        # Destroy the current frame and the cart frame, then display the main dashboard
        self.frame.destroy()
        self.cart_frame.destroy()
        self.dashboard.display_dashboard()

    def back_from_merch(self):
        self.frame.destroy()
        self.dashboard.display_dashboard()

    def add_to_cart(self, item):
        self.cart.add_item(item)
        self.display_cart()

    def display_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        for item_name, quantity in self.cart.items.items():
            tk.Label(self.cart_frame, text=f"{item_name}: {quantity}").pack()  # Changed self.frame to self.cart_frame
        total_cost = self.cart.get_total_cost()
        tk.Label(self.cart_frame, text=f"Total cost: {total_cost}").pack()  # Changed self.frame to self.cart_frame

    def create_item_fields(self):
        tk.Label(self.frame, text="Name: ").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()

        tk.Label(self.frame, text="Price: ").pack()
        self.price_entry = tk.Entry(self.frame)
        self.price_entry.pack()

        tk.Label(self.frame, text="Stock: ").pack()
        self.stock_entry = tk.Entry(self.frame)
        self.stock_entry.pack()

        tk.Label(self.frame, text="Details: ").pack()
        self.details_entry = tk.Entry(self.frame)
        self.details_entry.pack()

        tk.Button(self.frame, text='Add Item', command=self.add_item).pack()
        tk.Button(self.frame, text='Back', command=self.back_from_merch).pack()


    def add_item(self):
        item = {
            "itemID": str(uuid.uuid4()),
            "name": self.name_entry.get(),
            "price": float(self.price_entry.get()),
            "stock": int(self.stock_entry.get()),
            "details": self.details_entry.get()
        }
        self.db.add_merchandise(item)
        self.frame.pack_forget()
        self.dashboard.display_dashboard()