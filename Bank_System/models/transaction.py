from dataclasses import dataclass
from datetime import datetime
 
 
@dataclass
class Transaction:
 
    action: str
    amount: float
    date: str = ""
 
    def __post_init__(self):
        if not self.date:
            self.date = datetime.now().strftime("%Y-%m-%d %H:%M")
 
    def __str__(self):
        return f"{self.date} | {self.action:<12} | ${self.amount:.2f}"