import tkinter as tk
from tkinter import messagebox, ttk
from src.models import Account
from src.storage import JSONStorage


class BankingApp:

    def __init__(self, root: tk.Tk, storage: JSONStorage):
        self.root = root
        self.storage = storage
        self.accounts = self.storage.load_accounts()
        self.current_account: Account = None

        self.root.title("GUI Banking System")
        self.root.geometry("450x550")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
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

        ttk.Button(frame, text="Login", command=self.handle_login).pack(
            fill=tk.X, pady=(20, 5)
        )
        ttk.Button(
            frame,
            text="Create New Account",
            command=self.show_registration_screen,
        ).pack(fill=tk.X, pady=5)

    def show_registration_screen(self):
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
            frame, text="Register Account", command=self.handle_registration
        ).pack(fill=tk.X, pady=(20, 5))
        ttk.Button(
            frame, text="Back to Login", command=self.show_login_screen
        ).pack(fill=tk.X, pady=5)

    def show_dashboard_screen(self):
        self.clear_screen()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text=f"Welcome, {self.current_account.name}",
            font=("Helvetica", 14, "bold"),
        ).pack(anchor=tk.W)
        ttk.Label(
            frame,
            text=f"Account No: {self.current_account.account_number}",
            font=("Helvetica", 10),
        ).pack(anchor=tk.W, pady=(0, 15))

        self.balance_label = ttk.Label(
            frame,
            text=f"Balance: ${self.current_account.balance:.2f}",
            font=("Helvetica", 16, "bold"),
            foreground="#2e7d32",
        )
        self.balance_label.pack(pady=10)

        ttk.Label(frame, text="Enter Amount ($):").pack(
            anchor=tk.W, pady=(10, 0)
        )
        self.amount_entry = ttk.Entry(frame, width=30)
        self.amount_entry.pack(pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Deposit", command=self.handle_deposit).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5)
        )
        ttk.Button(
            btn_frame, text="Withdraw", command=self.handle_withdraw
        ).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

        ttk.Label(
            frame, text="Recent Transactions:", font=("Helvetica", 10, "bold")
        ).pack(anchor=tk.W, pady=(15, 5))
        self.tx_listbox = tk.Listbox(frame, height=6)
        self.tx_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.refresh_tx_history()

        ttk.Button(frame, text="Logout", command=self.handle_logout).pack(
            fill=tk.X, pady=(15, 0)
        )

    def handle_login(self):
        acc_num = self.acc_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if acc_num in self.accounts and self.accounts[acc_num].pin == pin:
            self.current_account = self.accounts[acc_num]
            self.show_dashboard_screen()
        else:
            messagebox.showerror("Error", "Invalid Account Number or PIN.")

    def handle_registration(self):
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
            messagebox.showerror("Error", "Enter a valid initial deposit.")
            return

        acc_num = str(100000 + len(self.accounts) + 1)
        new_acc = Account(
            account_number=acc_num, name=name, pin=pin, balance=deposit
        )
        self.accounts[acc_num] = new_acc
        self.storage.save_accounts(self.accounts)

        messagebox.showinfo(
            "Success", f"Account Created!\nAccount Number: {acc_num}"
        )
        self.show_login_screen()

    def handle_deposit(self):
        try:
            amount = float(self.amount_entry.get().strip())
            self.current_account.deposit(amount)
            self.storage.save_accounts(self.accounts)
            self.update_dashboard()
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def handle_withdraw(self):
        try:
            amount = float(self.amount_entry.get().strip())
            self.current_account.withdraw(amount)
            self.storage.save_accounts(self.accounts)
            self.update_dashboard()
        except ValueError as err:
            messagebox.showerror("Error", str(err))

    def update_dashboard(self):
        self.balance_label.config(
            text=f"Balance: ${self.current_account.balance:.2f}"
        )
        self.amount_entry.delete(0, tk.END)
        self.refresh_tx_history()

    def refresh_tx_history(self):
        self.tx_listbox.delete(0, tk.END)
        for tx in reversed(self.current_account.history[-10:]):
            self.tx_listbox.insert(tk.END, tx)

    def handle_logout(self):
        self.current_account = None
        self.show_login_screen()
