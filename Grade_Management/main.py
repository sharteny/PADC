import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models.student import Student, UndergraduateStudent, GraduateStudent
from models.course import Course
from services.school_service import SchoolService
from utils.validators import get_nonempty_input, get_float_input, get_int_input
 
def action_add_student(school):
    print("\n-- Add Student --")
    print("  1. Standard")
    print("  2. Undergraduate")
    print("  3. Graduate")
    choice = get_int_input("  Choose type (1-3): ", 1, 3)
    student_id = get_nonempty_input("  Student ID: ")
    name = get_nonempty_input("  Full name: ")

    if not Student.validate_name(name):
        print("  Error: Name must contain only letters and spaces.")
        return
    try:
        if choice == 1:
            student = Student(student_id, name)
        elif choice == 2:
            year = get_int_input("  Year (1-4): ", 1, 4)
            student = UndergraduateStudent(student_id, name, year)
        else:
            supervisor = get_nonempty_input("  Supervisor name: ")
            student = GraduateStudent(student_id, name, supervisor)
        school.add_student(student)
        print(f"  Student registered: {student}")
    except ValueError as e:
        print(f"  Error: {e}")

def action_add_student_from_string(school):
    print("\n-- Add Student from String --")
    print("  Standard format:       student_id,name")
    print("  Undergraduate format:  student_id,name,year")
    print("  Graduate format:       student_id,name,supervisor")
    print("  1. Standard")
    print("  2. Undergraduate")
    print("  3. Graduate")
    choice = get_int_input("  Choose type (1-3): ", 1, 3)
    text = get_nonempty_input("  Enter string: ")
    try:
        if choice == 1:
            student = Student.from_string(text)
        elif choice == 2:
            student = UndergraduateStudent.from_string(text)
        else:
            student = GraduateStudent.from_string(text)
        school.add_student(student)
        print(f"  Student registered: {student}")
    except ValueError as e:
        print(f"  Error: {e}")

def action_add_course(school):
    print("\n-- Add Course --")
    code = get_nonempty_input("  Course code (e.g. CS101): ")
    if not Course.validate_code(code):
        print("  Error: Course code must be alphanumeric.")
        return
    name = get_nonempty_input("  Course name: ")
    credits = get_int_input("  Credits (1-6): ", 1, 6)
    if not Course.validate_credits(credits):
        print("  Error: Credits must be a positive integer.")
        return
    try:
        course = Course(code, name, credits)
        school.add_course(course)
        print(f"  Course added: {course}")
    except ValueError as e:
        print(f"  Error: {e}")

def action_assign_grade(school):
    print("\n-- Assign Grade --")
    student_id = get_nonempty_input("  Student ID: ")
    course_code = get_nonempty_input("  Course code: ")
    score = get_float_input("  Score (0-100): ", 0, 100)
    try:
        school.assign_grade(student_id, course_code, score)
        print(f"  Grade assigned: {student_id} | {course_code.upper()} | {score}")
    except ValueError as e:
        print(f"  Error: {e}")


def action_mark_attendance(school):
    print("\n-- Mark Attendance --")
    student_id = get_nonempty_input("  Student ID: ")
    course_code = get_nonempty_input("  Course code: ")
    raw = input("  Present? (y/n): ").strip().lower()
    if raw not in ("y", "n"):
        print("  Please enter 'y' or 'n'.")
        return
    try:
        school.mark_attendance(student_id, course_code, raw == "y")
        status = "Present" if raw == "y" else "Absent"
        print(f"  Marked {status} for {student_id} in {course_code.upper()}.")
    except ValueError as e:
        print(f"  Error: {e}")

def action_report_card(school):
    print("\n-- Report Card --")
    student_id = get_nonempty_input("  Student ID: ")
    try:
        report = school.generate_report_card(student_id)
        print("\n" + report)
        export = input("\n  Export to file? (y/n): ").strip().lower()
        if export == "y":
            school.export_report_card(student_id)
    except ValueError as e:
        print(f"  Error: {e}")

def action_search(school):
    print("\n-- Search Students --")
    query = get_nonempty_input("  Search by name or ID: ")
    results = school.search_students(query)
    if not results:
        print("  No students found.")
    else:
        print(f"  Found {len(results)} result(s):")
        for student in results:
            print(f"  - {student}")

def action_filter_by_grade(school):
    print("\n-- Filter by Minimum Average --")
    min_avg = get_float_input("  Minimum average (0-100): ", 0, 100)
    results = school.filter_by_min_average(min_avg)
    if not results:
        print(f"  No students with an average >= {min_avg}.")
    else:
        print(f"  Students with average >= {min_avg}:")
        for student in results:
            print(f"  - {student}")

def action_top_students(school):
    print("\n-- Top 3 Students --")
    top = school.get_top_students(3)
    if not top:
        print("  No grades recorded yet.")
        return
    for i, student in enumerate(top, start=1):
        avg = student.calculate_average()
        gpa = student.calculate_gpa(school.courses)
        print(f"  {i}. {student.name} | Avg: {avg:.1f} | GPA: {gpa:.2f}")

def action_display_all(school):
    print("\n-- All Students --")
    school.display_all_students()
    print("\n-- All Courses --")
    school.display_all_courses()

def action_statistics(school):
    school.show_statistics()

def print_menu(school):
    print(f"\n{'='*45}")
    print(f"  {SchoolService.school_name} — Main Menu")
    print(f"{'='*45}")
    print("  1.  Add student")
    print("  2.  Add student from string")
    print("  3.  Add course")
    print("  4.  Assign grade")
    print("  5.  Mark attendance")
    print("  6.  Generate report card")
    print("  7.  Search students")
    print("  8.  Filter by minimum average")
    print("  9.  Top 3 students")
    print("  10. Display all students & courses")
    print("  11. School statistics")
    print("  0.  Quit")
    print(f"{'='*45}")

def main():
    name = input("Enter school name (or press Enter for default): ").strip()
    if not name:
        name = "Python Academy"
    school = SchoolService(name)
    print(f"\nWelcome to {SchoolService.school_name}!")

    while True:
        print_menu(school)
        choice = input("  Your choice: ").strip()

        if choice == "1":
            action_add_student(school)
        elif choice == "2":
            action_add_student_from_string(school)
        elif choice == "3":
            action_add_course(school)
        elif choice == "4":
            action_assign_grade(school)
        elif choice == "5":
            action_mark_attendance(school)
        elif choice == "6":
            action_report_card(school)
        elif choice == "7":
            action_search(school)
        elif choice == "8":
            action_filter_by_grade(school)
        elif choice == "9":
            action_top_students(school)
        elif choice == "10":
            action_display_all(school)
        elif choice == "11":
            action_statistics(school)
        elif choice == "0":
            school.save_data()
            print("  Goodbye!")
            break
        else:
            print("  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()