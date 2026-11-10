import unittest
from decimal import Decimal
from datetime import date
from unittest.mock import patch

from main import ATM, authenticate, parse_amount, parse_birth_date


class ParseAmountTests(unittest.TestCase):
    def test_accepts_valid_amount(self):
        self.assertEqual(parse_amount("12.50"), Decimal("12.50"))
        self.assertEqual(parse_amount("7"), Decimal("7"))

    def test_rejects_invalid_amount(self):
        for value in ("", "abc", "0", "-1", "1.001", "NaN", "Infinity"):
            with self.subTest(value=value):
                self.assertIsNone(parse_amount(value))


class ParseBirthDateTests(unittest.TestCase):
    def test_accepts_valid_birth_date(self):
        self.assertEqual(parse_birth_date("2000-01-01"), date(2000, 1, 1))

    def test_rejects_invalid_or_future_birth_date(self):
        for value in ("", "01-01-2000", "2001-02-29", "2999-01-01"):
            with self.subTest(value=value):
                self.assertIsNone(parse_birth_date(value))


class AuthenticationTests(unittest.TestCase):
    @patch("builtins.input", return_value="2000-01-01")
    def test_accepts_demo_birth_date(self, _mock_input):
        self.assertTrue(authenticate())

    @patch("builtins.input", side_effect=["1990-05-10"] * 3)
    def test_rejects_three_incorrect_birth_dates(self, mock_input):
        self.assertFalse(authenticate())
        self.assertEqual(mock_input.call_count, 3)


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
