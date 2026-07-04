from enum import Enum
 
class BookStatus(Enum):
    AVAILABLE = "Available"
    BORROWED = "Borrowed"
 
class MembershipType(Enum):
    REGULAR = "Regular"
    PREMIUM = "Premium"