from dataclasses import dataclass, field

@dataclass
class Course:

    course_code: str
    name: str
    credits: int

    def __post_init__(self):
        self.course_code = self.course_code.strip().upper()
        self.name = self.name.strip()

    @staticmethod
    def validate_credits(credits):
        return isinstance(credits, int) and credits > 0

    @staticmethod
    def validate_code(code):
        cleaned = code.strip().replace(" ", "")
        return len(cleaned) > 0 and cleaned.isalnum()

    def __str__(self):
        return f"[{self.course_code}] {self.name} ({self.credits} credit(s))"

    def __repr__(self):
        return f"Course(code={self.course_code!r}, name={self.name!r}, credits={self.credits})"
