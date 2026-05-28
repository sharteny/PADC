#!/usr/bin/python3
import argparse
import os
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

def read_data(filename):
    students = []
    try:
        with open(filename)as f:
            line = f.readlines()
            header = line[0].strip().split(',')
            for l in line[1:]:
                values = l.strip().split(',')
                student = {}
                for i in range(len(header)):
                    student[header[i]] = values[i]
                students.append(student)

        return header, students
    except FileNotFoundError:
        print("File Not Found")
        return None, None
            
def excel_write(file, students, header):
    wb = Workbook()
    ws1 = wb.active
    ws1.append(header)
    for student in students:
        ws1.append([student[h] for h in header])
    for cell in ws1[1]:
        cell.font = Font(bold=True, color="00AA00")
        cell.alignment = Alignment(horizontal="center")
    wb.save(file)

def filter_students(students, args):
    result = students

    if args.faculty:
        result = [s for s in result if s["faculty"] == args.faculty]
    if args.age:
        result = [s for s in result if s["age"] == args.age]
    if args.gender:
        result = [s for s in result if s["gender"] == args.gender]
    return result



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument("--faculty")
    parser.add_argument("--age")
    parser.add_argument("--gender")
    args = parser.parse_args()
    _, ex = os.path.splitext(args.input)
    __, ex2 = os.path.splitext(args.output)
    if ex != ".txt":
        print("Only .txt files are allowed")
        return
    if ex2 != ".xlsx":
        print("Only .xlsx files are allowed")
        return
    header, students = read_data(args.input)
    if not students:
        return
    students = filter_students(students, args)
    excel_write(args.output, students, header)
   
if __name__ == "__main__":
    main()
    