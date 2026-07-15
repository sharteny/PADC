from models.transaction import Transaction

class BankAccount:
    total_accounts = 0
    bank_name = "My_Bank"
    interest_rate = 0.03

    def __init__(self, owner, account_number, balance=0.0):
        BankAccount.total_accounts +=1
        self._owner = owner.strip()
        self._balance = balance
        self._account_number = account_number
        self._transactions = []
    
    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def transactions(self):
        return self._transactions

    def deposit(self, amount):
        if not BankAccount.validate_amount(amount):
            raise ValueError("Deposit amount must be a positive number.")
        self._balance += amount
        self._transactions.append(Transaction("deposit", amount))
    
    def withdraw(self, amount):
        if not BankAccount.validate_amount(amount):
            raise ValueError("Withdrawal amount must be a positive number.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        self._transactions.append(Transaction("withdrawal", amount))
    
    def get_balance(self):
         print(f"   Balance: ${self._balance:.2f}")

    @staticmethod
    def validate_amount(amount):
        return isinstance(amount, (int, float)) and amount > 0

    def transfer(self, amount, target_account):
        if not BankAccount.validate_amount(amount):
            raise ValueError("Transfer amount must be a positive number.")
        self.withdraw(amount)
        target_account.deposit(amount)
 
    def show_transactions(self):
        if not self._transactions:
            print("  No transactions yet.")
            return
        for t in self._transactions:
            print(f"  {t}")
 

    @classmethod
    def set_interest_rate(cls, new_rate):
        if not isinstance(new_rate, (int, float)) or new_rate < 0:
            raise ValueError("Interest rate must be a non-negative number.")
        cls.interest_rate = new_rate
    
    def __str__(self):
        return (
            f"[{self._account_number}] {self._owner} | "
            f"Balance: ${self._balance:.2f} | "
            f"Type: {type(self).__name__}"
        )
    
    def __repr__(self):
        return (
            f"{type(self).__name__}("
            f"owner={self._owner!r}, "
            f"account_number={self._account_number!r}, "
            f"balance={self._balance})"
        )
