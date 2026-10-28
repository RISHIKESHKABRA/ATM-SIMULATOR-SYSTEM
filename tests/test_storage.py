import os
import unittest
from src.models import Account
from src.storage import JSONStorage


class TestJSONStorage(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_bank_data.json"
        self.storage = JSONStorage(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        accounts = {"100001": Account("100001", "Alice", "1111", 500.0)}
        self.storage.save_accounts(accounts)

        loaded = self.storage.load_accounts()
        self.assertIn("100001", loaded)
        self.assertEqual(loaded["100001"].name, "Alice")
        self.assertEqual(loaded["100001"].balance, 500.0)


if __name__ == "__main__":
    unittest.main()
