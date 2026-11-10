"""A small, in-memory console ATM for learning and demonstration."""

from decimal import Decimal, InvalidOperation


DEMO_PIN = "1234"
STARTING_BALANCE = Decimal("1000.00")
CENT = Decimal("0.01")
MAX_PIN_ATTEMPTS = 3


def parse_amount(value):
    """Return a positive amount with at most two decimal places, or None."""
    try:
        amount = Decimal(value.strip())
        if not amount.is_finite() or amount <= 0:
            return None
        if amount != amount.quantize(CENT):
            return None
    except (InvalidOperation, ValueError):
        return None
    return amount


class ATM:
    def __init__(self, balance=STARTING_BALANCE):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0 or amount != amount.quantize(CENT):
            return False
        self.balance += amount
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount != amount.quantize(CENT):
            return False
        if amount > self.balance:
            return False
        self.balance -= amount
        return True


def authenticate():
    for attempt in range(MAX_PIN_ATTEMPTS):
        pin = input("Enter your 4-digit PIN: ").strip()
        if pin == DEMO_PIN:
            return True
        remaining = MAX_PIN_ATTEMPTS - attempt - 1
        if remaining:
            print(f"Incorrect PIN. {remaining} attempt(s) remaining.")
    print("Too many incorrect attempts. Goodbye.")
    return False


def read_amount(prompt):
    amount = parse_amount(input(prompt))
    if amount is None:
        print("Please enter a valid amount greater than zero, with up to 2 decimal places.")
    return amount


def run_atm():
    print("Welcome to the Console ATM")
    if not authenticate():
        return

    atm = ATM()
    print("\nLogin successful.")
    while True:
        print("\n1. Check balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"Your balance is ${atm.balance:.2f}")
        elif choice == "2":
            amount = read_amount("Amount to deposit: $")
            if amount is not None:
                atm.deposit(amount)
                print(f"Deposit successful. New balance: ${atm.balance:.2f}")
        elif choice == "3":
            amount = read_amount("Amount to withdraw: $")
            if amount is not None:
                if atm.withdraw(amount):
                    print(f"Withdrawal successful. New balance: ${atm.balance:.2f}")
                else:
                    print("Insufficient funds.")
        elif choice == "4":
            print("Thank you for using the Console ATM. Goodbye!")
            return
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_atm()
