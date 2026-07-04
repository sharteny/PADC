from models.bank_account import BankAccount
from models.transaction import Transaction

class SavingsAccount(BankAccount):

    def __init__(self, owner, account_number, balance=0.0, minimum_balance=100.0):
        super().__init__(owner, account_number, balance)
        self.minimum_balance = minimum_balance
    
    def withdraw(self, amount):
        if not BankAccount.validate_amount(amount):
            raise ValueError("Withdrawal amount must be a positive number.")
        if self.balance - amount < self.minimum_balance:
            raise ValueError(
                f"Cannot withdraw ${amount:.2f}. "
                f"You must keep at least ${self.minimum_balance:.2f} in your savings account."
            )
        self.balance -= amount
        self.transactions.append(Transaction("withdrawal", amount))

    def apply_interest(self):
        interest = round(self.balance * BankAccount.interest_rate, 2)
        self.balance += interest
        self.transactions.append(Transaction("interest", interest))
        print(
            f"  Interest applied ({BankAccount.interest_rate * 100:.1f}%): "
            f"+${interest:.2f} | New balance: ${self.balance:.2f}"
        )

    def __str__(self):
        base = super().__str__()
        return base + f" | Min Balance: ${self.minimum_balance:.2f}"
 
    def __repr__(self):
        return (
            f"SavingsAccount(owner={self.owner!r}, "
            f"account_number={self.account_number!r}, "
            f"balance={self.balance}, "
            f"minimum_balance={self.minimum_balance})"
        )