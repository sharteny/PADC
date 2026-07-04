
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from services.bank_service import Bank
from models.bank_account import BankAccount
from utils.validators import get_nonempty_input, get_float_input, get_int_input

def action_create_account(bank):
    print("\n-- Create Account --")
    print("  1. Savings  (earns interest, has minimum balance)")
    print("  2. Checking (allows overdraft with a fee)")
    choice = get_int_input("  Choose type (1-2): ", 1, 2)
    owner = get_nonempty_input("  Owner name: ")
 
    try:
        if choice == 1:
            balance = get_float_input("  Initial deposit: $")
            min_bal = get_float_input("  Minimum balance: $")
            bank.create_account("savings", owner, balance, minimum_balance=min_bal)
        else:
            balance = get_float_input("  Initial deposit: $")
            overdraft = get_float_input("  Overdraft limit: $")
            bank.create_account("checking", owner, balance, overdraft_limit=overdraft)
    except ValueError as e:
        print(f"  Error: {e}")

def action_deposit(bank):
    print("\n-- Deposit --")
    number = get_nonempty_input("  Account number: ")
    account = bank.find_account(number)
    if account is None:
        print(f"  No account found with number '{number}'.")
        return
    amount = get_float_input("  Amount: $")
    try:
        account.deposit(amount)
        bank.save_data()
        print(f"  Deposited ${amount:.2f}. New balance: ${account.balance:.2f}")
    except ValueError as e:
        print(f"  Error: {e}")

def action_withdraw(bank):
    print("\n-- Withdraw --")
    number = get_nonempty_input("  Account number: ")
    account = bank.find_account(number)
    if account is None:
        print(f"  No account found with number '{number}'.")
        return
    amount = get_float_input("  Amount: $")
    try:
        account.withdraw(amount)
        bank.save_data()
        print(f"  Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}")
    except ValueError as e:
        print(f"  Error: {e}")

def action_check_balance(bank):
    print("\n-- Check Balance --")
    number = get_nonempty_input("  Account number: ")
    account = bank.find_account(number)
    if account is None:
        print(f"  No account found with number '{number}'.")
        return
    account.get_balance()

def action_transfer(bank):
    print("\n-- Transfer --")
    from_number = get_nonempty_input("  From account number: ")
    to_number = get_nonempty_input("  To account number: ")
    from_account = bank.find_account(from_number)
    to_account = bank.find_account(to_number)
    if from_account is None:
        print(f"  No account found with number '{from_number}'.")
        return
    if to_account is None:
        print(f"  No account found with number '{to_number}'.")
        return
    amount = get_float_input("  Amount: $")
    try:
        from_account.transfer(amount, to_account)
        bank.save_data()
        print(f"  Transferred ${amount:.2f} from {from_account.account_number} to {to_account.account_number}.")
    except ValueError as e:
        print(f"  Error: {e}")

def action_apply_interest(bank):
    print("\n-- Apply Interest --")
    number = get_nonempty_input("  Account number: ")
    account = bank.find_account(number)
    if account is None:
        print(f"  No account found with number '{number}'.")
        return
    from models.savings_account import SavingsAccount
    if not isinstance(account, SavingsAccount):
        print("  Only savings accounts earn interest.")
        return
    account.apply_interest()
    bank.save_data()

def action_show_transactions(bank):
    print("\n-- Transaction History --")
    number = get_nonempty_input("  Account number: ")
    account = bank.find_account(number)
    if account is None:
        print(f"  No account found with number '{number}'.")
        return
    print(f"  Transactions for account {account.account_number} ({account.owner}):")
    account.show_transactions()
 
def action_change_interest_rate(bank):
    print("\n-- Change Interest Rate --")
    print(f"  Current rate: {BankAccount.interest_rate * 100:.2f}%")
    raw = input("  New rate (e.g. enter 5 for 5%): ").strip()
    try:
        rate = float(raw) / 100
        BankAccount.set_interest_rate(rate)
        bank.save_data()
        print(f"  Interest rate updated to {rate * 100:.2f}%.")
    except ValueError as e:
        print(f"  Error: {e}")

def action_display_accounts(bank):
    print("\n-- All Accounts --")
    bank.display_all_accounts()

def action_statistics(bank):
    bank.show_statistics()

def print_menu():
    print(f"\n{'='*40}")
    print(f"   {BankAccount.bank_name} — Main Menu")
    print(f"{'='*40}")
    print("  1.  Create account")
    print("  2.  Deposit")
    print("  3.  Withdraw")
    print("  4.  Check balance")
    print("  5.  Transfer")
    print("  6.  Apply interest (savings only)")
    print("  7.  Transaction history")
    print("  8.  Change interest rate")
    print("  9.  View all accounts")
    print("  10. Statistics")
    print("  0.  Quit")
    print(f"{'='*40}")

def main():
    bank = Bank()
    print(f"Welcome to {BankAccount.bank_name}!")
 
    while True:
        print_menu()
        choice = input("  Your choice: ").strip()
 
        if choice == "1":
            action_create_account(bank)
        elif choice == "2":
            action_deposit(bank)
        elif choice == "3":
            action_withdraw(bank)
        elif choice == "4":
            action_check_balance(bank)
        elif choice == "5":
            action_transfer(bank)
        elif choice == "6":
            action_apply_interest(bank)
        elif choice == "7":
            action_show_transactions(bank)
        elif choice == "8":
            action_change_interest_rate(bank)
        elif choice == "9":
            action_display_accounts(bank)
        elif choice == "10":
            action_statistics(bank)
        elif choice == "0":
            bank.save_data()
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()