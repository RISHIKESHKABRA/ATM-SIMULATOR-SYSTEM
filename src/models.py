class Account:
    """Represents a bank account and handles business rules."""

    def __init__(
        self,
        account_number: str,
        name: str,
        pin: str,
        balance: float = 0.0,
        history: list = None,
    ):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = float(balance)
        self.history = (
            history if history is not None else [f"Account opened with ${self.balance:.2f}"]
        )

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.history.append(f"Deposited: +${amount:.2f}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.history.append(f"Withdrew: -${amount:.2f}")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pin": self.pin,
            "balance": self.balance,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, account_number: str, data: dict) -> "Account":
        return cls(
            account_number=account_number,
            name=data["name"],
            pin=data["pin"],
            balance=data["balance"],
            history=data.get("history", []),
        )
