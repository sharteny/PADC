from dataclasses import dataclass

@dataclass
class Grade:

    course_code: str
    score: float

    def get_letter(self):
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"

    def get_gpa_points(self):
        if self.score >= 90:
            return 4.0
        elif self.score >= 80:
            return 3.0
        elif self.score >= 70:
            return 2.0
        elif self.score >= 60:
            return 1.0
        else:
            return 0.0

    def __str__(self):
        return f"{self.course_code}: {self.score:.1f} ({self.get_letter()})"

    def __repr__(self):
        return f"Grade(course_code={self.course_code!r}, score={self.score})"