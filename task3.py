#!/usr/bin/python3

import json

def add_student(students):
    name = input("Enter student name: ")
    for student in students:
        if student["name"] == name:
            print("Student already exists.")
            return
    students.append({"name": name, "grades": {}})
    print("Student added successfully.")

def add_update_grade(students):
    name = input("Enter student name: ")
    subject = input("Enter subject name: ")
    for student in students:
        if student["name"] == name:
            try:
                score = float(input("Enter grade: "))
                if score < 0 or score > 100:
                    print("Grade must be between 0 and 100.")
                    return
            except ValueError:
                print("Invalid grade. Please enter a number.")
                return
            student["grades"][subject] = score
            print("Grade added/updated successfully.")
            return
    print("Student not found.")


def view_student_details(students):
    name = input("Enter student name: ")
    for student in students:
        if student["name"] == name:
            print(f"Student: {student['name']}")
            print("Grades:")
            for subject, score in student["grades"].items():
                print(f"  {subject}: {score}")
            return
    print("Student not found.")

def view_class_average(students):
    total = 0
    count = 0
    for student in students:
        for subject, score in student["grades"].items():
            total += score
            count += 1
    if count > 0:
        print(f"Class Average: {total / count:.2f}")
    else:
        print("No grades available.")

def save_to_file(students):
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)

def load_from_file():
    try:
        with open("students.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def main():
    students = load_from_file()
    while True:
        print("\n1. Add Student")
        print("2. Add/Update Grade")
        print("3. View Student Details")
        print("4. View Class Average")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_student(students)
        elif choice == "2":
            add_update_grade(students)
        elif choice == "3":
            view_student_details(students)
        elif choice == "4":
            view_class_average(students)
        elif choice == "5":
            save_to_file(students)
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()