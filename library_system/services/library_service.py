import json
import os 
from datetime import datetime

from models.book import Book, FictionBook, NonFictionBook
from models.member import Member
from models.loan import Loan


DATA_FILE = "data/library.json"


class LibraryService:
    _total_books = 0
    _total_members = 0

    def __init__(self):
        self._books = []
        self._members = []
        self.load_data()

    @classmethod
    def get_statistics(cls):
        return {
            "Total book titles added": cls._total_books,
            "Total members registered": cls._total_members,
        }

    def add_book(self, book):
        for existing in self._books:
            if existing.isbn == book.isbn:
                raise ValueError(f"A book with ISBN '{book.isbn}' already exists.")
        self._books.append(book)
        LibraryService._total_books += 1
        self.save_data()

    def find_book(self, isbn):
        for book in self._books:
            if book.isbn == isbn:
                return book
        return None

    def search_books(self, query):
        query_lower = query.lower()
        results = []
        for book in self._books:
            if query_lower in book.title.lower() or query_lower in book.author.lower():
                results.append(book)
        return results

    def display_all_books(self):
        if not self._books:
            print("  No books in the catalogue yet.")
            return
        for i, book in enumerate(self.books, start=1):
            print(f"  {i}. {book}")

    def add_member(self, member):
        for existing in self._members:
            if existing.member_id == member.member_id:
                raise ValueError(f"Member ID {member.member_id} is already registered.")
        self._members.append(member)
        LibraryService._total_members += 1
        self.save_data()

    def find_member(self, member_id):
        for member in self._members:
            if str(member.member_id) == str(member_id):
                return member
        return None

    def display_all_members(self):
        if not self._members:
            print("  No members registered yet.")
            return
        for i, member in enumerate(self._members, start=1):
            print(f"  {i}. {member}")

    def borrow_book(self, member_id, isbn):
        member = self.find_member(member_id)
        if member is None:
            raise ValueError(f"No member found with ID '{member_id}'.")

        book = self.find_book(isbn)
        if book is None:
            raise ValueError(f"No book found with ISBN '{isbn}'.")

        if isbn in member.borrowed_books:
            raise ValueError(f"{member.name} already has a copy of '{book.title}'.")

        due_date = book.borrow()
        due_str = due_date.strftime("%Y-%m-%d")

        member.borrowed_books[isbn] = due_str
        member.history.append(Loan(
            action="borrowed",
            isbn=isbn,
            book_title=book.title,
            date=datetime.now().strftime("%Y-%m-%d"),
            due_date=due_str,
        ))

        self.save_data()
        print(f"  '{book.title}' borrowed by {member.name}. Due: {due_str}")

    def return_book(self, member_id, isbn):
        member = self.find_member(member_id)
        if member is None:
            raise ValueError(f"No member found with ID '{member_id}'.")

        book = self.find_book(isbn)
        if book is None:
            raise ValueError(f"No book found with ISBN '{isbn}'.")

        if isbn not in member.borrowed_books:
            raise ValueError(f"{member.name} does not have '{book.title}' checked out.")

        due_date = datetime.strptime(member.borrowed_books[isbn], "%Y-%m-%d")
        late_fee = self._calculate_late_fee(due_date)

        book.return_book()
        del member.borrowed_books[isbn]
        member.history.append(Loan(
            action="returned",
            isbn=isbn,
            book_title=book.title,
            date=datetime.now().strftime("%Y-%m-%d"),
            late_fee=late_fee,
        ))

        self.save_data()
        print(f"  '{book.title}' returned by {member.name}.", end=" ")
        if late_fee > 0:
            print(f"Late fee: ${late_fee:.2f}")
        else:
            print("Returned on time!")

    @staticmethod
    def _calculate_late_fee(due_date):
        days_late = (datetime.now() - due_date).days
        if days_late <= 0:
            return 0.0
        return round(days_late * 0.25, 2)

    def show_statistics(self):
        total_copies = 0
        available_copies = 0
        for book in self.books:
            total_copies += book.copies
            available_copies += book.available_copies

        stats = LibraryService.get_statistics()

        print(f"\n  --- Library Statistics ---")
        for label, value in stats.items():
            print(f"  {label}: {value}")
        print(f"  Unique titles in catalogue: {len(self.books)}")
        print(f"  Total physical copies:      {total_copies}")
        print(f"  Copies available right now: {available_copies}")
        print(f"  Copies currently on loan:   {total_copies - available_copies}")
        print(f"  Registered members:         {len(self.members)}")

    def save_data(self):
        books_data = []
        for book in self.books:
            entry = {
                "type": type(book).__name__,
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "copies": book.copies,
                "available_copies": book.available_copies,
            }
            if isinstance(book, FictionBook):
                entry["sub_genre"] = book.sub_genre
            elif isinstance(book, NonFictionBook):
                entry["subject"] = book.subject
            books_data.append(entry)

        members_data = []
        for member in self.members:
            history_data = []
            for loan in member.history:
                history_data.append({
                    "action": loan.action,
                    "isbn": loan.isbn,
                    "book_title": loan.book_title,
                    "date": loan.date,
                    "due_date": loan.due_date,
                    "late_fee": loan.late_fee,
                })
            members_data.append({
                "name": member.name,
                "member_id": member.member_id,
                "borrowed_books": member.borrowed_books,
                "history": history_data,
            })

        data = {
            "total_books": LibraryService._total_books,
            "total_members": LibraryService._total_members,
            "books": books_data,
            "members": members_data,
        }

        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            LibraryService._total_books = data.get("total_books", 0)
            LibraryService._total_members = data.get("total_members", 0)

            for entry in data.get("books", []):
                book_type = entry["type"]
                if book_type == "FictionBook":
                    book = FictionBook(
                        entry["title"], entry["author"], entry["isbn"],
                        entry["copies"], entry.get("sub_genre", "General")
                    )
                elif book_type == "NonFictionBook":
                    book = NonFictionBook(
                        entry["title"], entry["author"], entry["isbn"],
                        entry["copies"], entry.get("subject", "General")
                    )
                else:
                    book = Book(entry["title"], entry["author"], entry["isbn"], entry["copies"])
                book.available_copies = entry["available_copies"]
                self._books.append(book)

            for entry in data.get("members", []):
                member = Member(entry["name"])
                member.member_id = entry["member_id"]
                Member.total_members = max(Member.total_members, member.member_id)
                member.borrowed_books = entry.get("borrowed_books", {})
                for loan_data in entry.get("history", []):
                    member.history.append(Loan(
                        action=loan_data["action"],
                        isbn=loan_data["isbn"],
                        book_title=loan_data["book_title"],
                        date=loan_data["date"],
                        due_date=loan_data.get("due_date", ""),
                        late_fee=loan_data.get("late_fee", 0.0),
                    ))
                self._members.append(member)

            print("  Data loaded from library.json.")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Could not load data: {e}. Starting fresh.")