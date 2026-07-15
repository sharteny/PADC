
from dataclasses import dataclass, field
from datetime import datetime, timedelta
 
 
@dataclass
class Book:
    title: str
    author: str
    isbn: str
    copies: int = 1
    _available_copies: int = field(default=0, init=False)
 
    def __post_init__(self):
        self._available_copies = self.copies
 
    @property
    def available_copies(self):
        return self._available_copies

    @available_copies.setter
    def available_copies(self, value):
        self._available_copies = value

    def is_available(self):
        return self._available_copies > 0
 
    def borrow(self):
        if not self.is_available():
            raise ValueError(f"No copies of '{self.title}' are available right now.")
        self._available_copies -= 1
        due_date = datetime.now() + timedelta(days=14)
        return due_date
 
    def return_book(self):
        if self._available_copies >= self.copies:
            raise ValueError("All copies are already on the shelf.")
        self._available_copies += 1
 
    @staticmethod
    def validate_isbn(isbn):
        cleaned = isbn.replace("-", "")
        return cleaned.isdigit() and len(cleaned) >= 10
 
    def __str__(self):
        status = f"{self._available_copies}/{self.copies} available"
        return f'"{self.title}" by {self.author} | ISBN: {self.isbn} | {status}'
 
    def __repr__(self):
        return f"Book(title={self.title!r}, author={self.author!r}, isbn={self.isbn!r})"
 
 
class FictionBook(Book):

    def __init__(self, title, author, isbn, copies=1, sub_genre="General"):
        super().__init__(title, author, isbn, copies)
        self.sub_genre = sub_genre
 
    def __str__(self):
        base = super().__str__()
        return base + f" | Fiction ({self.sub_genre})"
 
    def __repr__(self):
        return f"FictionBook(title={self.title!r}, author={self.author!r}, sub_genre={self.sub_genre!r})"
 
 
class NonFictionBook(Book):
 
    def __init__(self, title, author, isbn, copies=1, subject="General"):
        super().__init__(title, author, isbn, copies)
        self.subject = subject
 
    def __str__(self):
        base = super().__str__()
        return base + f" | Non-Fiction ({self.subject})"
 
    def __repr__(self):
        return f"NonFictionBook(title={self.title!r}, author={self.author!r}, subject={self.subject!r})"