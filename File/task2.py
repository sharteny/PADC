#!/usr/bin/python3
import json

def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_and_exit(expenses):
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file, indent=4)
    print("Expenses saved. Goodbye!")

def add_expense(expenses):
    category = input("Enter expense category: ")
    try:
        amount = float(input("Enter expense amount: "))
        if amount <= 0:
            print("Amount cannot be zero or negative.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    date = input("Enter expense date (YYYY-MM-DD): ")
    expenses.append({"category": category, "amount": amount, "date": date})
    print("Expense added successfully.")

def view_expenses(expenses):
    if not expenses:
        print("No expenses to display.")
    else:
        for i, expense in enumerate(expenses, start=1):
            print(f"{i}. Category: {expense['category']}, Amount: {expense['amount']}, Date: {expense['date']}")

def view_summary(expenses, mode):
    summary = {}
    for expense in expenses:
        if mode == "category":
            key = expense["category"]
        elif mode == "month":
            key = expense["date"][:7]
        else:
            print("Invalid mode. Please choose 'category' or 'month'.")
            return
        summary[key] = summary.get(key, 0) + expense["amount"]
    for key, total in summary.items():
        print(f"{key}: {total}")

def delete_expense(expenses):
    view_expenses(expenses)
    if expenses:
        try:
            index = int(input("Enter the index of the expense to delete: ")) - 1
            if 0 <= index < len(expenses):
                expenses.pop(index)
                print("Expense deleted successfully.")
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    expenses = load_expenses()
    while True:
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View summary by category/month")
        print("4. Delete expense")
        print("5. Save & Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            print("View summary by:")
            print("1. Category")
            print("2. Month")
            mode_choice = input("Enter your choice: ")
            if mode_choice == '1':
                view_summary(expenses, "category")
            elif mode_choice == '2':
                view_summary(expenses, "month")
            else:
                print("Invalid choice. Please try again.")
        elif choice == '4':
            delete_expense(expenses)
        elif choice == '5':
            save_and_exit(expenses)
            break
        else:
            print("Invalid choice. Please try again.")

main()
