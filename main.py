import tkinter as tk
from tkinter import messagebox, ttk


class MenuItem:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock


class Order:
    def __init__(self):
        self.items = []
        self.total_price = 0

    def add_item(self, item):
        if item.stock > 0:
            self.items.append(item)
            self.total_price += item.price
            item.stock -= 1
        else:
            messagebox.showwarning("Out of Stock", f"{item.name} is out of stock!")

    def display_order(self):
        order_summary = "\n".join([f"{item.name} - ₹{item.price}" for item in self.items])
        order_summary += f"\nTotal: ₹{self.total_price}"
        return order_summary

    def clear_order(self):
        self.items.clear()
        self.total_price = 0


class CafeManagementSystem:
    def __init__(self):
        self.menu = [
            MenuItem("Espresso", 100, 10),
            MenuItem("Cappuccino", 150, 8),
            MenuItem("Latte", 180, 5),
            MenuItem("Croissant", 80, 15),
            MenuItem("Muffin", 90, 12),
        ]
        self.current_order = Order()

    def place_order(self, index):
        item = self.menu[index]
        self.current_order.add_item(item)

    def generate_bill(self):
        if self.current_order.items:
            order_details = self.current_order.display_order()
            messagebox.showinfo("Order Summary", order_details)
            self.current_order.clear_order()  
        else:
            messagebox.showwarning("No Order", "No items in the order. Please add items first.")

    def get_menu(self):
        return self.menu


class CafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interactive Café Management System")
        self.geometry("600x600")
        self.system = CafeManagementSystem()


        self.tab_control = ttk.Notebook(self)
        

        self.order_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.order_tab, text='Order')

        self.billing_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.billing_tab, text='Billing')

        self.tab_control.pack(expand=1, fill="both")


        self.build_order_tab()
        self.build_billing_tab()


    def build_order_tab(self):
        self.menu_label = tk.Label(self.order_tab, text="Select items to add to your order", font=("Arial", 14))
        self.menu_label.pack(pady=10)

        self.order_listbox = tk.Listbox(self.order_tab, height=10)
        self.order_listbox.pack(pady=5)

        for index, item in enumerate(self.system.get_menu()):
            self.order_listbox.insert(tk.END, f"{item.name} - ₹{item.price} (Stock: {item.stock})")

        self.add_button = tk.Button(self.order_tab, text="Add to Order", command=self.add_to_order)
        self.add_button.pack(pady=5)

        self.current_order_label = tk.Label(self.order_tab, text="Current Order:", font=("Arial", 12))
        self.current_order_label.pack(pady=5)

        self.current_order_text = tk.Text(self.order_tab, height=10, width=40)
        self.current_order_text.pack(pady=5)

        self.clear_button = tk.Button(self.order_tab, text="Clear Order", command=self.clear_order)
        self.clear_button.pack(pady=5)

    def add_to_order(self):
        selected_index = self.order_listbox.curselection()
        if selected_index:
            item_index = selected_index[0]
            self.system.place_order(item_index)
            self.update_order_display()

    def update_order_display(self):
        self.current_order_text.delete(1.0, tk.END)
        order_summary = self.system.current_order.display_order()
        self.current_order_text.insert(tk.END, order_summary)

    def clear_order(self):
        self.system.current_order.clear_order()
        self.update_order_display()


    def build_billing_tab(self):
        self.bill_label = tk.Label(self.billing_tab, text="Billing Section", font=("Arial", 14))
        self.bill_label.pack(pady=10)

        self.generate_bill_button = tk.Button(self.billing_tab, text="Generate Bill", command=self.generate_bill)
        self.generate_bill_button.pack(pady=5)

    def generate_bill(self):
        self.system.generate_bill()


if __name__ == "__main__":
    app = CafeApp()
    app.mainloop()
