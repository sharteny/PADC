from dataclasses import dataclass, field
 
 
@dataclass
class Member:
    total_members = 0
    name: str
    _member_id: int = field(init=False)
    borrowed_books: dict = field(default_factory=dict)
    history: list = field(default_factory=list)
 
    def __post_init__(self):
        self.name = self.name.strip()
        Member.total_members += 1
        self._member_id = Member.total_members
    
    @property
    def member_id(self):
        return self._member_id

    @member_id.setter
    def member_id(self, value):
        self._member_id = value
        
    def __str__(self):
        return f"[ID: {self.member_id}] {self.name} | Borrowed: {len(self.borrowed_books)}"
 
    def __repr__(self):
        return f"Member(name={self.name!r}, member_id={self.member_id})"