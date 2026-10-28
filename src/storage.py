import json
import os
from typing import Dict
from src.models import Account


class JSONStorage:
    """Handles loading and persisting accounts using a JSON file."""

    def __init__(self, filepath: str = "bank_data.json"):
        self.filepath = filepath

    def load_accounts(self) -> Dict[str, Account]:
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, "r") as file:
                raw_data = json.load(file)
                return {
                    acc_num: Account.from_dict(acc_num, data)
                    for acc_num, data in raw_data.items()
                }
        except (json.JSONDecodeError, KeyError):
            return {}

    def save_accounts(self, accounts: Dict[str, Account]) -> None:
        raw_data = {
            acc_num: acc_obj.to_dict() for acc_num, acc_obj in accounts.items()
        }
        with open(self.filepath, "w") as file:
            json.dump(raw_data, file, indent=4)
