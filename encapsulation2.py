# encapsulation.py

class BankAccount:
    # Part 3: Static (class) variable
    total_accounts = 0

    def __init__(self, holder_name: str, initial_balance: float = 0.0):
        self.holder_name = holder_name  # public attribute (allowed)

        # Generate unique incremental account number (ID 1, ID 2, ...)
        BankAccount.total_accounts += 1
        self.__account_number = BankAccount.total_accounts  # private

        # Private balance (cannot be directly modified from outside)
        if initial_balance < 0:
            initial_balance = 0.0
        self.__balance = float(initial_balance)

    # ---------- Internal (protected) helper for subclasses ----------
    def _set_balance(self, new_balance: float) -> None:
        """Protected method: intended for subclasses only."""
        self.__balance = float(new_balance)

    # ---------- Required public methods ----------
    def get_balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float) -> None:
        # Reject negative and zero deposits
        if amount <= 0:
            print("Transaction denied")
            return
        self.__balance += float(amount)

    def withdraw(self, amount: float) -> None:
        # Must check amount > 0 AND sufficient funds
        if amount <= 0:
            print("Transaction denied")
            return

        if self.__balance >= amount:
            self.__balance -= float(amount)
        else:
            print("Transaction denied")

    # Optional helper (not required, but useful for testing)
    def get_account_number(self) -> int:
        return self.__account_number


class SavingsAccount(BankAccount):
    def __init__(self, holder_name: str, initial_balance: float = 0.0, interest_rate: float = 0.05):
        super().__init__(holder_name, initial_balance)
        self.interest_rate = float(interest_rate)

    def apply_interest(self) -> None:
        # Increases balance based on the rate
        interest = self.get_balance() * self.interest_rate
        # Reuse existing validated method (DRY)
        self.deposit(interest)


class VIPAccount(BankAccount):
    def __init__(self, holder_name: str, initial_balance: float = 0.0, overdraft_limit: float = -1000.0):
        super().__init__(holder_name, initial_balance)
        self.overdraft_limit = float(overdraft_limit)

    # Polymorphism: override withdraw to allow negative balance down to overdraft_limit
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            print("Transaction denied")
            return

        new_balance = self.get_balance() - float(amount)

        # VIP can go negative, but not below overdraft_limit
        if new_balance >= self.overdraft_limit:
            self._set_balance(new_balance)
        else:
            print("Transaction denied")


# -------------------- Simple tests (optional, but good evidence) --------------------
if __name__ == "__main__":
    acc1 = BankAccount("Paulette", 100.0)
    acc2 = SavingsAccount("Mercedes", 200.0, 0.05)
    acc3 = VIPAccount("Danny", 50.0, -1000.0)

    print("Account numbers:", acc1.get_account_number(), acc2.get_account_number(), acc3.get_account_number())
    print("Total accounts:", BankAccount.total_accounts)

    # Encapsulation evidence: cannot access private attributes directly
    try:
        print(acc1.__balance)  # should fail
    except AttributeError as e:
        print("Access Denied:", e)

    # Validation evidence
    acc1.deposit(-10)          # denied
    acc1.withdraw(9999)        # denied (insufficient funds)
    acc1.withdraw(20)          # ok
    print("acc1 balance:", acc1.get_balance())

    # Savings interest
    acc2.apply_interest()
    print("acc2 (savings) balance:", acc2.get_balance())

    # VIP overdraft behavior
    acc3.withdraw(900)         # allowed if within overdraft_limit
    print("acc3 (vip) balance:", acc3.get_balance())
    acc3.withdraw(5000)        # denied if exceeds overdraft_limit
    print("acc3 (vip) balance:", acc3.get_balance())
