import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

DATA_FILE = "bank_data.json"


class BankingSystemApp:

    def __init__(self, root):
        self.root = root
        self.root.title("GUI Banking System")
        self.root.geometry("450x550")
        self.root.resizable(False, False)

        self.accounts = self.load_data()
        self.current_acc = None

        # Custom Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.create_login_screen()

    # --- Data Persistence ---
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.accounts, file, indent=4)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Screens ---
    def create_login_screen(self):
        self.clear_screen()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Secure Banking Portal", font=("Helvetica", 16, "bold")
        ).pack(pady=15)

        ttk.Label(frame, text="Account Number:").pack(anchor=tk.W, pady=(10, 0))
        self.acc_entry = ttk.Entry(frame, width=30)
        self.acc_entry.pack(pady=5)

        ttk.Label(frame, text="PIN:").pack(anchor=tk.W, pady=(10, 0))
        self.pin_entry = ttk.Entry(frame, show="*", width=30)
        self.pin_entry.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.login).pack(
            fill=tk.X, pady=(20, 5)
        )
        ttk.Button(
            frame, text="Create New Account", command=self.create_signup_screen
        ).pack(fill=tk.X, pady=5)

    def create_signup_screen(self):
        self.clear_screen()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame, text="Register New Account", font=("Helvetica", 16, "bold")
        ).pack(pady=15)

        ttk.Label(frame, text="Full Name:").pack(anchor=tk.W, pady=(5, 0))
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.pack(pady=5)

        ttk.Label(frame, text="4-Digit PIN:").pack(anchor=tk.W, pady=(5, 0))
        self.new_pin_entry = ttk.Entry(frame, show="*", width=30)
        self.new_pin_entry.pack(pady=5)

        ttk.Label(frame, text="Initial Deposit ($):").pack(
            anchor=tk.W, pady=(5, 0)
        )
        self.deposit_entry = ttk.Entry(frame, width=30)
        self.deposit_entry.pack(pady=5)

        ttk.Button(
            frame, text="Register Account", command=self.register_account
        ).pack(fill=tk.X, pady=(20, 5))
        ttk.Button(
            frame, text="Back to Login", command=self.create_login_screen
        ).pack(fill=tk.X, pady=5)

    def create_dashboard_screen(self):
        self.clear_screen()

        acc_data = self.accounts[self.current_acc]

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text=f"Welcome, {acc_data['name']}",
            font=("Helvetica", 14, "bold"),
        ).pack(anchor=tk.W)
        ttk.Label(
            frame,
            text=f"Account No: {self.current_acc}",
            font=("Helvetica", 10),
        ).pack(anchor=tk.W, pady=(0, 15))

        self.balance_label = ttk.Label(
            frame,
            text=f"Balance: ${acc_data['balance']:.2f}",
            font=("Helvetica", 16, "bold"),
            foreground="#2e7d32",
        )
        self.balance_label.pack(pady=10)

        # Amount Input
        ttk.Label(frame, text="Enter Amount ($):").pack(
            anchor=tk.W, pady=(10, 0)
        )
        self.amount_entry = ttk.Entry(frame, width=30)
        self.amount_entry.pack(pady=5)

        # Action Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Deposit", command=self.deposit).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5)
        )
        ttk.Button(btn_frame, text="Withdraw", command=self.withdraw).pack(
            side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0)
        )

        # Transactions List
        ttk.Label(
            frame, text="Recent Transactions:", font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(15, 5))

        self.tx_listbox = tk.Listbox(frame, height=6)
        self.tx_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.update_tx_history()

        ttk.Button(frame, text="Logout", command=self.logout).pack(
            fill=tk.X, pady=(15, 0)
        )

    # --- Business Logic ---
    def register_account(self):
        name = self.name_entry.get().strip()
        pin = self.new_pin_entry.get().strip()
        deposit_str = self.deposit_entry.get().strip()

        if not name or not pin or not deposit_str:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be a 4-digit number.")
            return

        try:
            deposit = float(deposit_str)
            if deposit < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid initial deposit amount."
            )
            return

        acc_num = str(100000 + len(self.accounts) + 1)
        self.accounts[acc_num] = {
            "name": name,
            "pin": pin,
            "balance": deposit,
            "history": [f"Account opened with ${deposit:.2f}"],
        }
        self.save_data()

        messagebox.showinfo(
            "Success",
            f"Account created successfully!\nYour Account Number is: {acc_num}",
        )
        self.create_login_screen()

    def login(self):
        acc_num = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if acc_num in self.accounts and self.accounts[acc_num]["pin"] == pin:
            self.current_acc = acc_num
            self.create_dashboard_screen()
        else:
            messagebox.showerror("Error", "Invalid Account Number or PIN.")

    def deposit(self):
        try:
            amount = float(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Enter a valid positive amount to deposit."
            )
            return

        self.accounts[self.current_acc]["balance"] += amount
        self.accounts[self.current_acc]["history"].append(
            f"Deposited: +${amount:.2f}"
        )
        self.save_data()
        self.refresh_dashboard()

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Enter a valid positive amount to withdraw."
            )
            return

        current_balance = self.accounts[self.current_acc]["balance"]
        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient balance.")
            return

        self.accounts[self.current_acc]["balance"] -= amount
        self.accounts[self.current_acc]["history"].append(
            f"Withdrew: -${amount:.2f}"
        )
        self.save_data()
        self.refresh_dashboard()

    def refresh_dashboard(self):
        balance = self.accounts[self.current_acc]["balance"]
        self.balance_label.config(text=f"Balance: ${balance:.2f}")
        self.amount_entry.delete(0, tk.END)
        self.update_tx_history()

    def update_tx_history(self):
        self.tx_listbox.delete(0, tk.END)
        history = self.accounts[self.current_acc]["history"]
        for item in reversed(history[-10:]):  # Show last 10 entries
            self.tx_listbox.insert(tk.END, item)

    def logout(self):
        self.current_acc = None
        self.create_login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingSystemApp(root)
    root.mainloop()
