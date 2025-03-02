import pytest


class Wallet:
    def __init__(self, filename="wallet.txt"):
        self.filename = filename
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                lines = file.readlines()
                self.balance = float(lines[0].strip())
                self.transactions = [line.strip() for line in lines[1:]]
        except (FileNotFoundError, ValueError, IndexError):
            self.balance = 0
            self.transactions = []

    def save_data(self):
        with open(self.filename, "w") as file:
            file.write(f"{self.balance}\n")
            for transaction in self.transactions:
                file.write(f"{transaction}\n")

    def add_transaction(self, amount, description=""):
        self.transactions.append(f"{amount} {description}")
        self.balance += amount
        self.save_data()
        print(f"Транзакція додана: {amount} ({description})")

    def show_balance(self):
        print(f"Баланс: {self.balance}")

    def show_transactions(self):
        print("Історія транзакцій:")
        for transaction in self.transactions:
            print(transaction)


if __name__ == "__main__":
    wallet = Wallet()
    while True:
        print(
            "\n1. Додати транзакцію\n2. Переглянути баланс\n3. Історія транзакцій\n4. Вийти"
        )
        choice = input("Виберіть опцію: ")
        if choice == "1":
            amount = float(input("Введіть суму: "))
            description = input("Опис: ")
            wallet.add_transaction(amount, description)
        elif choice == "2":
            wallet.show_balance()
        elif choice == "3":
            wallet.show_transactions()
        elif choice == "4":
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")


@pytest.fixture
def test_wallet(tmp_path):
    test_file = tmp_path / "test_wallet.txt"
    return Wallet(filename=str(test_file))


def test_initial_balance(test_wallet):
    assert test_wallet.balance == 0


def test_add_transaction(test_wallet):
    test_wallet.add_transaction(100, "Доход")
    assert test_wallet.balance == 100
    assert test_wallet.transactions == ["100 Доход"]


def test_add_multiple_transactions(test_wallet):
    test_wallet.add_transaction(100, "Доход")
    test_wallet.add_transaction(-50, "Витрати")
    assert test_wallet.balance == 50
    assert test_wallet.transactions == ["100 Доход", "-50 Витрати"]


def test_save_and_load(test_wallet):
    test_wallet.add_transaction(200, "Зарплата")
    test_wallet.load_data()
    assert test_wallet.balance == 200
    assert "200 Зарплата" in test_wallet.transactions
