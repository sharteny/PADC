#!/usr/bin/python3

import argparse
import os
import shutil
from pathlib import Path

CATEGORIES = {
    "documents": [".doc", ".docx", ".txt", ".xls", ".xlsx"],
    "pdfs": [".pdf"],
    "images": [".jpg", ".jpeg", ".png", ".gif"],
    "archives": [".zip", ".rar", ".tar"]
}


def get_category(extension):
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "others"

def creat_folder(path):
    folders = ["documents", "pdfs", "images", "archives", "others"]
    for f in folders:
        f_path = os.path.join(path, f)
        if not os.path.exists(f_path):
            os.mkdir(f_path)

def organize_files(path):
    report ={
        "documents": 0,
        "pdfs": 0,
        "images": 0,
        "archives": 0,
        "others": 0
    }
    creat_folder(path)
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(file)
            category = get_category(extension)
            dest_folder = os.path.join(path, category)
            dest_path = os.path.join(dest_folder, file)
            shutil.move(file_path, dest_path)
            report[category] +=1
    return report


def main():
    parser = argparse.ArgumentParser(description="Source directory path")
    parser.add_argument('path', help="Source directory path")

    args = parser.parse_args()
    source_path = Path(args.path)
    if not source_path.exists():
        print("folder is empty")
        return
    report = organize_files(source_path)
    for category, count in report.items():
        print(f"- {count} {category}")

if __name__ == "__main__":
    main()