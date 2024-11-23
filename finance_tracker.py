import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv


class Transaction:
    def __init__(self, amount, category, transaction_type, date=None):
        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    def __repr__(self):
        return f"{self.date} | {self.transaction_type} | ₹{self.amount} | {self.category}"


class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        self.transactions = []
        self.balance = 0

        # Labels
        self.balance_label = tk.Label(root, text=f"Balance: ₹{self.balance}", font=("Arial", 14))
        self.balance_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Amount
        self.amount_label = tk.Label(root, text="Amount (₹):")
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1)

        # Category
        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=2, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=2, column=1)

        # Type (Income/Expense)
        self.type_label = tk.Label(root, text="Type (Income/Expense):")
        self.type_label.grid(row=3, column=0)
        self.type_entry = tk.Entry(root)
        self.type_entry.grid(row=3, column=1)

        # Add Transaction Button
        self.add_button = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Transaction List Box
        self.transaction_listbox = tk.Listbox(root, width=50, height=10)
        self.transaction_listbox.grid(row=5, column=0, columnspan=2, pady=10)

        # Generate Report Button
        self.report_button = tk.Button(root, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=6, column=0, pady=10)

        # Export to CSV Button
        self.export_button = tk.Button(root, text="Export to CSV", command=self.export_to_csv)
        self.export_button.grid(row=6, column=1, pady=10)

    def add_transaction(self):
        try:
            # Get input values
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            transaction_type = self.type_entry.get().capitalize()

            if transaction_type not in ["Income", "Expense"]:
                raise ValueError("Transaction type must be 'Income' or 'Expense'.")

            # Create a transaction object and add it to the list
            transaction = Transaction(amount, category, transaction_type)
            self.transactions.append(transaction)

            # Update balance
            if transaction_type == "Income":
                self.balance += amount
            else:
                self.balance -= amount

            # Update the balance label
            self.balance_label.config(text=f"Balance: ₹{self.balance:.2f}")

            # Update the transaction listbox
            self.transaction_listbox.insert(tk.END, str(transaction))

            # Clear input fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.type_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def generate_report(self):
        total_income = sum(t.amount for t in self.transactions if t.transaction_type == "Income")
        total_expenses = sum(t.amount for t in self.transactions if t.transaction_type == "Expense")
        net_balance = total_income - total_expenses

        report = (
            f"Total Income: ₹{total_income:.2f}\n"
            f"Total Expenses: ₹{total_expenses:.2f}\n"
            f"Net Balance: ₹{net_balance:.2f}\n"
        )

        # Display report in a popup
        messagebox.showinfo("Report", report)

    def export_to_csv(self):
        with open('finance_report.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Type', 'Amount', 'Category'])
            for transaction in self.transactions:
                writer.writerow([transaction.date, transaction.transaction_type, transaction.amount, transaction.category])

        messagebox.showinfo("Export", "Data successfully exported to finance_report.csv")


# Set up the root Tkinter window
root = tk.Tk()
app = FinanceTrackerApp(root)

# Run the Tkinter event loop
root.mainloop()
