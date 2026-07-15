import json
import os
 
from models.bank_account import BankAccount
from models.savings_account import SavingsAccount
from models.checking_account import CheckingAccount
from models.transaction import Transaction
 
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "bank.json")

class Bank:

    def __init__(self):
        self._accounts = []
        self._next_number = 1001
        self.load_data()

    @property
    def accounts(self):
        return self._accounts

    @property
    def next_number(self):
        return self._next_number

    @next_number.setter
    def next_number(self, value):
        self._next_number = value

    def create_account(self, account_type, owner, initial_balance=0.0, **kwargs):
        account_number = str(self._next_number)
        self._next_number += 1
 
        if account_type == "savings":
            min_bal = kwargs.get("minimum_balance", 100.0)
            account = SavingsAccount(owner, account_number, initial_balance, min_bal)
        elif account_type == "checking":
            limit = kwargs.get("overdraft_limit", 500.0)
            account = CheckingAccount(owner, account_number, initial_balance, limit)
        else:
            raise ValueError(f"Unknown account type: '{account_type}'.")
 
        self._accounts.append(account)
        self.save_data()
        print(f"  Account created! Number: {account_number} | Owner: {owner}")
        return account

    def display_all_accounts(self):
        if not self._accounts:
            print("  No accounts yet.")
            return
        for i, account in enumerate(self._accounts, start=1):
            print(f"  {i}. {account}")

    def find_account(self, account_number):
        for account in self._accounts:
            if account.account_number == str(account_number):
                return account
        return None

    def show_statistics(self):
        total_balance = 0.0
        savings_count = 0
        checking_count = 0
 
        for account in self._accounts:
            total_balance += account.balance
            if isinstance(account, SavingsAccount):
                savings_count += 1
            elif isinstance(account, CheckingAccount):
                checking_count += 1
 
        print(f"\n  --- {BankAccount.bank_name} Statistics ---")
        print(f"  Total accounts ever created : {BankAccount.total_accounts}")
        print(f"  Savings accounts            : {savings_count}")
        print(f"  Checking accounts           : {checking_count}")
        print(f"  Total balance across all    : ${total_balance:.2f}")
        print(f"  Current interest rate       : {BankAccount.interest_rate * 100:.2f}%")

    def save_data(self):
        accounts_data = []
        for account in self._accounts:
            entry = {
                "type": type(account).__name__,
                "owner": account.owner,
                "account_number": account.account_number,
                "balance": account.balance,
                "transactions": [
                    {"action": t.action, "amount": t.amount, "date": t.date}
                    for t in account.transactions
                ],
            }
            if isinstance(account, SavingsAccount):
                entry["minimum_balance"] = account.minimum_balance
            elif isinstance(account, CheckingAccount):
                entry["overdraft_limit"] = account.overdraft_limit
            accounts_data.append(entry)
 
        data = {
            "next_number": self._next_number,
            "total_accounts": BankAccount.total_accounts,
            "interest_rate": BankAccount.interest_rate,
            "accounts": accounts_data,
        }
 
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
 
            self._next_number = data.get("next_number", 1001)
            BankAccount.interest_rate = data.get("interest_rate", 0.03)
            BankAccount.total_accounts = 0
 
            for entry in data.get("accounts", []):
                if entry["type"] == "SavingsAccount":
                    account = SavingsAccount(
                        entry["owner"],
                        entry["account_number"],
                        entry["balance"],
                        entry.get("minimum_balance", 100.0),
                    )
                elif entry["type"] == "CheckingAccount":
                    account = CheckingAccount(
                        entry["owner"],
                        entry["account_number"],
                        entry["balance"],
                        entry.get("overdraft_limit", 500.0),
                    )
                else:
                    continue
 
                for t in entry.get("transactions", []):
                    account.transactions.append(
                        Transaction(t["action"], t["amount"], t["date"])
                    )
                self.accounts.append(account)
 
            print(f"  Data loaded. {len(self.accounts)} account(s) restored.")
        except FileNotFoundError:
            return
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Could not load data: {e}. Starting fresh.")
 