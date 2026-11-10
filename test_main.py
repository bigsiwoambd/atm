import unittest
from decimal import Decimal

from main import ATM, parse_amount


class ParseAmountTests(unittest.TestCase):
    def test_accepts_valid_amount(self):
        self.assertEqual(parse_amount("12.50"), Decimal("12.50"))
        self.assertEqual(parse_amount("7"), Decimal("7"))

    def test_rejects_invalid_amount(self):
        for value in ("", "abc", "0", "-1", "1.001", "NaN", "Infinity"):
            with self.subTest(value=value):
                self.assertIsNone(parse_amount(value))


class ATMTests(unittest.TestCase):
    def test_deposit_increases_balance(self):
        atm = ATM(Decimal("10.00"))

        self.assertTrue(atm.deposit(Decimal("2.50")))
        self.assertEqual(atm.balance, Decimal("12.50"))

    def test_withdrawal_updates_balance_or_rejects_insufficient_funds(self):
        atm = ATM(Decimal("10.00"))

        self.assertTrue(atm.withdraw(Decimal("3.25")))
        self.assertEqual(atm.balance, Decimal("6.75"))
        self.assertFalse(atm.withdraw(Decimal("7.00")))
        self.assertEqual(atm.balance, Decimal("6.75"))


if __name__ == "__main__":
    unittest.main()
