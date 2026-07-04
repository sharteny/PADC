from models.bank_account import BankAccount
from models.transaction import Transaction

class CheckingAccount (BankAccount):
    VERDRAFT_FEE = 35.0

    def __init__(self, owner, account_number, balance=0.0, overdraft_limit=500.0):
        super().__init__(owner, account_number, balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if not BankAccount.validate_amount(amount):
            raise ValueError("Withdrawal amount must be a positive number.")
        if self.balance - amount < -self.overdraft_limit:
            raise ValueError(
                f"Cannot withdraw ${amount:.2f}. "
                f"This exceeds your overdraft limit of ${self.overdraft_limit:.2f}."
            )
        self.balance -= amount
        self.transactions.append(Transaction("withdrawal", amount))
 
        if self.balance < 0:
            self.balance -= CheckingAccount.OVERDRAFT_FEE
            self.transactions.append(Transaction("overdraft fee", CheckingAccount.OVERDRAFT_FEE))
            print(f"  Overdraft! Fee of ${CheckingAccount.OVERDRAFT_FEE:.2f} charged.")
 