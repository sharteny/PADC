import json
import os
from datetime import date
from models.student import Student, UndergraduateStudent, GraduateStudent
from models.course import Course

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "school.json") 

class SchoolService:

    school_name = "Python Academy"
    total_students = 0
    total_courses = 0
 
    def __init__(self, name="Python Academy"):
        SchoolService.school_name = name
        self.students = {}
        self.courses = {}
        self.load_data()

    @classmethod
    def get_class_stats(cls):
        return {
            "School": cls.school_name,
            "Total students ever registered": cls.total_students,
            "Total courses ever added": cls.total_courses,
        }

    def add_course(self, course):
        if course.course_code in self.courses:
            raise ValueError(f"Course '{course.course_code}' already exists.")
        self.courses[course.course_code] = course
        SchoolService.total_courses += 1
        self.save_data()

    def find_course(self, course_code):
        return self.courses.get(course_code.upper())
 
    def display_all_courses(self):
        if not self.courses:
            print("  No courses added yet.")
            return
        for i, course in enumerate(self.courses.values(), start=1):
            print(f"  {i}. {course}")

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError(f"Student ID '{student.student_id}' is already registered.")
        self.students[student.student_id] = student
        SchoolService.total_students += 1
        self.save_data()

    def find_student(self, student_id):
        return self.students.get(student_id.strip())
 
    def display_all_students(self):
        if not self.students:
            print("  No students registered yet.")
            return
        for i, student in enumerate(self.students.values(), start=1):
            print(f"  {i}. {student}")

    def assign_grade(self, student_id, course_code, score):
        if not Student.validate_score(score):
            raise ValueError("Score must be a number between 0 and 100.")
        student = self._get_student(student_id)
        self._get_course(course_code)
        student.add_grade(course_code.upper(), score)
        self.save_data()

    def mark_attendance(self, student_id, course_code, present):
        student = self._get_student(student_id)
        self._get_course(course_code)
        student.mark_attendance(course_code.upper(), present)
        self.save_data()

    def search_students(self, query):
        query = query.lower()
        results = []
        for student in self.students.values():
            if query in student.name.lower() or query in student.student_id.lower():
                results.append(student)
        return results

    def filter_by_min_average(self, min_avg):
        results = []
        for student in self.students.values():
            if student.calculate_average() >= min_avg:
                results.append(student)
        return results

    def get_top_students(self, n=3):
        all_students = list(self.students.values())
        all_students.sort(key=lambda s: s.calculate_average(), reverse=True)
        return all_students[:n]

    def get_school_average(self):
        averages = []
        for student in self.students.values():
            if student.grades:
                averages.append(student.calculate_average())
        if not averages:
            return 0.0
        return round(sum(averages) / len(averages), 2)

    def show_statistics(self):
        school_avg = self.get_school_average()
        top = self.get_top_students(3)
        stats = SchoolService.get_class_stats()
        print(f"\n  --- School Statistics ---")
        for label, value in stats.items():
            print(f"  {label}: {value}")
        print(f"  Active students:           {len(self.students)}")
        print(f"  Active courses:            {len(self.courses)}")
        print(f"  School-wide average score: {school_avg:.1f}")
        print(f"\n  Top 3 Students:")
        if not top:
            print("  No grades recorded yet.")
        else:
            for i, student in enumerate(top, start=1):
                avg = student.calculate_average()
                gpa = student.calculate_gpa(self.courses)
                print(f"  {i}. {student.name} | Avg: {avg:.1f} | GPA: {gpa:.2f}")
 
    def generate_report_card(self, student_id):
        student = self._get_student(student_id)
        gpa = student.calculate_gpa(self.courses)
        avg = student.calculate_average()

        lines = []
        lines.append("=" * 52)
        lines.append(f"  REPORT CARD — {SchoolService.school_name}")
        lines.append(f"  Date: {date.today()}")
        lines.append("=" * 52)
        lines.append(f"  Name:       {student.name}")
        lines.append(f"  Student ID: {student.student_id}")
        lines.append(f"  Type:       {type(student).__name__}")
        if isinstance(student, UndergraduateStudent):
            lines.append(f"  Year:       {student.year}")
            on_prob = student.is_on_probation(self.courses)
            status = "ACADEMIC PROBATION" if on_prob else "Good Standing"
            lines.append(f"  Status:     {status}")
        elif isinstance(student, GraduateStudent):
            lines.append(f"  Supervisor: {student.supervisor}")
        lines.append("-" * 52)
        lines.append(f"  {'Course':<28} {'Score':>6} {'Grade':>6}")
        lines.append("-" * 52)
        if not student.grades:
            lines.append("  No grades recorded yet.")
        else:
            for grade in student.grades:
                course = self.courses.get(grade.course_code)
                course_name = course.name if course else grade.course_code
                name_display = course_name[:27]
                att = student.get_attendance_rate(grade.course_code)
                att_str = f"  (Att: {att}%)" if att is not None else ""
                lines.append(
                    f"  {name_display:<28} {grade.score:>6.1f} {grade.get_letter():>6}{att_str}"
                )
        lines.append("-" * 52)
        lines.append(f"  Average Score : {avg:.1f} / 100")
        lines.append(f"  GPA           : {gpa:.2f} / 4.00")
        lines.append("=" * 52)
        return "\n".join(lines)

    def export_report_card(self, student_id):
        report = self.generate_report_card(student_id)
        filename = f"report_{student_id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  Report saved to '{filename}'.")

    def _get_student(self, student_id):
        student = self.find_student(student_id)
        if student is None:
            raise ValueError(f"No student found with ID '{student_id}'.")
        return student

    def _get_course(self, course_code):
        course = self.find_course(course_code)
        if course is None:
            raise ValueError(f"No course found with code '{course_code}'.")
        return course

    def save_data(self):
        data = {
            "school_name": SchoolService.school_name,
            "total_students": SchoolService.total_students,
            "total_courses": SchoolService.total_courses,
            "courses": [],
            "students": [],
        }
        for course in self.courses.values():
            data["courses"].append({
                "course_code": course.course_code,
                "name": course.name,
                "credits": course.credits,
            })
        for student in self.students.values():
            data["students"].append(student.to_dict())

        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            SchoolService.school_name = data.get("school_name", SchoolService.school_name)
            SchoolService.total_students = data.get("total_students", 0)
            SchoolService.total_courses = data.get("total_courses", 0)
            for entry in data.get("courses", []):
                course = Course(entry["course_code"], entry["name"], entry["credits"])
                self.courses[course.course_code] = course
            for entry in data.get("students", []):
                student_type = entry.get("type", "Student")
                if student_type == "UndergraduateStudent":
                    student = UndergraduateStudent.from_dict(entry)
                elif student_type == "GraduateStudent":
                    student = GraduateStudent.from_dict(entry)
                else:
                    student = Student.from_dict(entry)
                self.students[student.student_id] = student
            print(f"  Data loaded. {len(self.students)} student(s), {len(self.courses)} course(s).")
        except FileNotFoundError:
            return
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  Could not load data: {e}. Starting fresh.")

    def __str__(self):
        return (
            f"{SchoolService.school_name} | "
            f"Students: {len(self.students)} | "
            f"Courses: {len(self.courses)}"
        )

    def __repr__(self):
        return f"SchoolService(name={SchoolService.school_name!r})"