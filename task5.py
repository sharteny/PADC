#!/usr/bin/python3
import json
from datetime import date 

def  new_entry(entries):
    title = input("Enter entry title: ")
    today = str(date.today())
    entry = input("Enter entry content: ")
    entries.append({"title":title, "date":today, "entry":entry})

def view_all_entries(entries):
    if not entries:
        print("No entries to display.")
    else:
        for entry in entries:
            print(f"Title: {entry['title']}, Date: {entry['date']}, Entry: {entry['entry']}")

def search_by_keyword(entries):
    keyword = input("Enter keyword to search for: ")
    results = []
    for entry in entries:
        if keyword in entry['title'] or keyword in entry['entry']:
            results.append(entry)
    if not results:
        print("No entries found.")
    else:
        for entry in results:
            print(f"Title: {entry['title']}, Date: {entry['date']}, Entry: {entry['entry']}")

def search_by_date(entries):
    date_str = input("Enter date to search for (YYYY-MM-DD): ")
    results = []
    for entry in entries:
        if entry['date'] == date_str:
            results.append(entry)
    if not results:
        print("No entries found.")
    else:
        for entry in results:
            print(f"Title: {entry['title']}, Date: {entry['date']}, Entry: {entry['entry']}")

def view_stats(entries):
    print("Total entries:", len(entries))
    stats = {}
    for entry in entries:
        month = entry["date"][:7]
        stats[month] = stats.get(month, 0) + 1
    for month, count in stats.items():
        print(month, "→", count)

def load_file():
    try:
        with open("entries.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_file(entries):
    with open("entries.json", "w") as file:
        json.dump(entries, file, indent=4)

def main():
    entries = load_file()
    while True:
        print("1. New Entry")
        print("2. View All Entries")
        print("3. Search by Keyword")
        print("4. Search by Date")
        print("5. View Stats")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            new_entry(entries)
            save_file(entries)
        elif choice == "2":
            view_all_entries(entries)
        elif choice == "3":
            search_by_keyword(entries)
        elif choice == "4":
            search_by_date(entries)
        elif choice == "5":
            view_stats(entries)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()