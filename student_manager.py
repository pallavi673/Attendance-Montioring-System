import csv
import os

STUDENTS_FILE = "data/students.csv"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

def add_student(student_id, name):
    # Add a student to the CSV file
    file_exists = os.path.exists(STUDENTS_FILE)
    with open(STUDENTS_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Student ID", "Name"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"Student ID": student_id, "Name": name})

def get_students():
    # Return list of students as dictionaries
    if not os.path.exists(STUDENTS_FILE):
        return []
    with open(STUDENTS_FILE, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
