from dataclasses import dataclass
from datetime import datetime
 
@dataclass
class Loan:

    action: str
    isbn: str
    book_title: str
    date: str
    due_date: str = ""
    late_fee: float = 0.0
 
    def __str__(self):
        if self.action == "borrowed":
            return f"Borrowed '{self.book_title}' on {self.date} | Due: {self.due_date}"
        fee_text = f"${self.late_fee:.2f} late fee" if self.late_fee > 0 else "on time"
        return f"Returned '{self.book_title}' on {self.date} | {fee_text}"