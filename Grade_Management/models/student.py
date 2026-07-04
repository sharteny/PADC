from models.grade import Grade

class Student:

    def __init__(self, student_id, name):
        self.student_id = student_id.strip()
        self.name = name.strip()
        self.grades = []
        self.attendance = {}

    def add_grade(self, course_code, score):
        for grade in self.grades:
            if grade.course_code == course_code:
                grade.score = score
                return
        self.grades.append(Grade(course_code, score))

    def get_grade(self, course_code):
        for grade in self.grades:
            if grade.course_code == course_code:
                return grade
        return None

    def calculate_average(self):
        if not self.grades:
            return 0.0
        total = 0.0
        for grade in self.grades:
            total += grade.score
        return round(total / len(self.grades), 2)

    def calculate_gpa(self, courses):
        total_points = 0.0
        total_credits = 0
        for grade in self.grades:
            if grade.course_code in courses:
                credit = courses[grade.course_code].credits
                total_points += grade.get_gpa_points() * credit
                total_credits += credit
        if total_credits == 0:
            return 0.0
        return round(total_points / total_credits, 2)
 
    def mark_attendance(self, course_code, present):
        if course_code not in self.attendance:
            self.attendance[course_code] = []
        self.attendance[course_code].append(present)

    def get_attendance_rate(self, course_code):
        records = self.attendance.get(course_code, [])
        if not records:
            return None
        return round(sum(records) / len(records) * 100, 1)

    @classmethod
    def from_dict(cls, data):
        student = cls(data["student_id"], data["name"])
        for g in data.get("grades", []):
            student.grades.append(Grade(g["course_code"], g["score"]))
        student.attendance = data.get("attendance", {})
        return student

    @classmethod
    def from_string(cls, text):
        parts = text.split(",")
        if len(parts) != 2:
            raise ValueError("String must be in the format 'student_id,name'.")
        return cls(parts[0].strip(), parts[1].strip())
 
    @staticmethod
    def validate_name(name):
        cleaned = name.strip().replace(" ", "")
        return len(cleaned) > 0 and cleaned.isalpha()

    @staticmethod
    def validate_score(score):
        return isinstance(score, (int, float)) and 0 <= score <= 100
 
    def to_dict(self):
        return {
            "type": type(self).__name__,
            "student_id": self.student_id,
            "name": self.name,
            "grades": [{"course_code": g.course_code, "score": g.score} for g in self.grades],
            "attendance": self.attendance,
        }

    def __str__(self):
        avg = self.calculate_average()
        return (
            f"[{self.student_id}] {self.name} | "
            f"Avg: {avg:.1f} | "
            f"Courses: {len(self.grades)} | "
            f"Type: {type(self).__name__}"
        )

    def __repr__(self):
        return f"Student(student_id={self.student_id!r}, name={self.name!r})"

class UndergraduateStudent(Student):

    def __init__(self, student_id, name, year=1):
        super().__init__(student_id, name)
        self.year = year

    def is_on_probation(self, courses):
        return self.calculate_gpa(courses) < 2.0

    @classmethod
    def from_dict(cls, data):
        student = cls(data["student_id"], data["name"], data.get("year", 1))
        for g in data.get("grades", []):
            student.grades.append(Grade(g["course_code"], g["score"]))
        student.attendance = data.get("attendance", {})
        return student

    @classmethod
    def from_string(cls, text):
        parts = text.split(",")
        if len(parts) != 3:
            raise ValueError("Format must be 'student_id,name,year'.")
        return cls(parts[0].strip(), parts[1].strip(), int(parts[2].strip()))

    def to_dict(self):
        data = super().to_dict()
        data["year"] = self.year
        return data

    def __str__(self):
        base = super().__str__()
        return base + f" | Year {self.year}"

    def __repr__(self):
        return f"UndergraduateStudent(id={self.student_id!r}, name={self.name!r}, year={self.year})"

class GraduateStudent(Student):

    def __init__(self, student_id, name, supervisor="TBA"):
        super().__init__(student_id, name)
        self.supervisor = supervisor.strip()

    @classmethod
    def from_dict(cls, data):
        student = cls(data["student_id"], data["name"], data.get("supervisor", "TBA"))
        for g in data.get("grades", []):
            student.grades.append(Grade(g["course_code"], g["score"]))
        student.attendance = data.get("attendance", {})
        return student

    @classmethod
    def from_string(cls, text):
        parts = text.split(",")
        if len(parts) != 3:
            raise ValueError("Format must be 'student_id,name,supervisor'.")
        return cls(parts[0].strip(), parts[1].strip(), parts[2].strip())

    def to_dict(self):
        data = super().to_dict()
        data["supervisor"] = self.supervisor
        return data

    def __str__(self):
        base = super().__str__()
        return base + f" | Supervisor: {self.supervisor}"

    def __repr__(self):
        return f"GraduateStudent(id={self.student_id!r}, name={self.name!r})"