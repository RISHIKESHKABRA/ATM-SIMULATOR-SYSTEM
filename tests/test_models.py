import unittest
from src.models import Account


class TestAccountModel(unittest.TestCase):

    def setUp(self):
        self.account = Account("100001", "John Doe", "1234", 100.0)

    def test_deposit_valid(self):
        self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)
        self.assertIn("Deposited: +$50.00", self.account.history[-1])

    def test_deposit_invalid(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-10.0)

    def test_withdraw_valid(self):
        self.account.withdraw(40.0)
        self.assertEqual(self.account.balance, 60.0)
        self.assertIn("Withdrew: -$40.00", self.account.history[-1])

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(200.0)

    def test_to_and_from_dict(self):
        data = self.account.to_dict()
        reconstructed = Account.from_dict("100001", data)
        self.assertEqual(reconstructed.name, "John Doe")
        self.assertEqual(reconstructed.balance, 100.0)


if __name__ == "__main__":
    unittest.main()
