
import sys
import os
 
from models.book import Book, FictionBook, NonFictionBook
from models.member import Member
from services.library_service import LibraryService
 
def get_nonempty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")
 
 
def get_int_input(prompt, min_val, max_val):
    while True:
        raw = input(prompt).strip()
        if raw.isdigit():
            value = int(raw)
            if min_val <= value <= max_val:
                return value
        print(f"  Please enter a number between {min_val} and {max_val}.")
 
def action_add_book(library):
    print("\n-- Add Book --")
    print("  1. Fiction")
    print("  2. Non-Fiction")
    print("  3. General")
    choice = get_int_input("  Choose type (1-3): ", 1, 3)
 
    title = get_nonempty_input("  Title: ")
    author = get_nonempty_input("  Author: ")
    isbn = get_nonempty_input("  ISBN: ")
 
    if not Book.validate_isbn(isbn):
        print("  Error: ISBN must be at least 10 digits.")
        return
 
    copies = get_int_input("  Number of copies: ", 1, 50)
 
    try:
        if choice == 1:
            sub_genre = get_nonempty_input("  Sub-genre (e.g. Thriller, Romance): ")
            book = FictionBook(title, author, isbn, copies, sub_genre)
        elif choice == 2:
            subject = get_nonempty_input("  Subject (e.g. History, Science): ")
            book = NonFictionBook(title, author, isbn, copies, subject)
        else:
            book = Book(title, author, isbn, copies)
 
        library.add_book(book)
        print(f"  Book added: {book}")
    except ValueError as e:
        print(f"  Error: {e}")
 
 
def action_display_books(library):
    print("\n-- All Books --")
    library.display_all_books()
 
 
def action_search_books(library):
    print("\n-- Search Books --")
    query = get_nonempty_input("  Search by title or author: ")
    results = library.search_books(query)
    if not results:
        print("  No books found.")
    else:
        print(f"  Found {len(results)} result(s):")
        for book in results:
            print(f"    - {book}")
 
 
def action_add_member(library):
    print("\n-- Register Member --")
    name = get_nonempty_input("  Member name: ")
    try:
        member = Member(name)
        library.add_member(member)
        print(f"  Member registered: {member}")
    except ValueError as e:
        print(f"  Error: {e}")
 
 
def action_display_members(library):
    print("\n-- All Members --")
    library.display_all_members()
 
 
def action_borrow_book(library):
    print("\n-- Borrow a Book --")
    member_id = get_nonempty_input("  Member ID: ")
    isbn = get_nonempty_input("  Book ISBN: ")
    try:
        library.borrow_book(member_id, isbn)
    except ValueError as e:
        print(f"  Error: {e}")
 
def action_return_book(library):
    print("\n-- Return a Book --")
    member_id = get_nonempty_input("  Member ID: ")
    isbn = get_nonempty_input("  Book ISBN: ")
    try:
        library.return_book(member_id, isbn)
    except ValueError as e:
        print(f"  Error: {e}")
 
def action_member_history(library):
    print("\n-- Member History --")
    member_id = get_nonempty_input("  Member ID: ")
    member = library.find_member(member_id)
    if member is None:
        print(f"  No member found with ID '{member_id}'.")
        return
    print(f"\n  {member}")
    if not member.history:
        print("  No transaction history yet.")
        return
    for loan in member.history:
        print(f"    - {loan}")
 
def action_statistics(library):
    library.show_statistics()
 
def print_menu():
    print("\n" + "=" * 40)
    print("      Library Management System")
    print("=" * 40)
    print("  1.  Add a book")
    print("  2.  Display all books")
    print("  3.  Search for a book")
    print("  4.  Register a member")
    print("  5.  Display all members")
    print("  6.  Borrow a book")
    print("  7.  Return a book")
    print("  8.  View member history")
    print("  9.  Library statistics")
    print("  0.  Quit")
    print("=" * 40)
 
 
def main():
    library = LibraryService()
    print("Welcome to the Library Management System!")
 
    while True:
        print_menu()
        choice = input("  Your choice: ").strip()
 
        if choice == "1":
            action_add_book(library)
        elif choice == "2":
            action_display_books(library)
        elif choice == "3":
            action_search_books(library)
        elif choice == "4":
            action_add_member(library)
        elif choice == "5":
            action_display_members(library)
        elif choice == "6":
            action_borrow_book(library)
        elif choice == "7":
            action_return_book(library)
        elif choice == "8":
            action_member_history(library)
        elif choice == "9":
            action_statistics(library)
        elif choice == "0":
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice. Please try again.")
 
 
if __name__ == "__main__":
    main()