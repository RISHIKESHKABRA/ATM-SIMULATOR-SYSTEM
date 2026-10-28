import tkinter as tk
from src.gui import BankingApp
from src.storage import JSONStorage


def main():
    root = tk.Tk()
    storage = JSONStorage(filepath="bank_data.json")
    _ = BankingApp(root, storage)
    root.mainloop()


if __name__ == "__main__":
    main()
