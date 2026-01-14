import csv
import os
from datetime import datetime
from collections import defaultdict
from student_manager import get_students
STUDENTS_FILE = "data/students.csv"
ATTENDANCE_FILE = "data/attendance.csv"


ATTENDANCE_FILE = "data/attendance.csv"
os.makedirs("data", exist_ok=True)

def mark_attendance(student_id, status):
    # Record attendance for a student
    date = datetime.today().date().isoformat()
    file_exists = os.path.exists(ATTENDANCE_FILE)
    with open(ATTENDANCE_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Student ID", "Status"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({"Date": date, "Student ID": student_id, "Status": status})

def view_attendance():
    students = get_students()
    if not students:
        print("No students found.")
        return

    if not os.path.exists("data/attendance.csv"):
        print("No attendance records found.")
        return

    # Read all attendance records
    attendance_data = {}  # {date: {student_id: status}}
    dates = set()
    with open("data/attendance.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = row["Date"]
            student_id = row["Student ID"]
            status = row["Status"]

            if date not in attendance_data:
                attendance_data[date] = {}
            attendance_data[date][student_id] = status
            dates.add(date)

    if not dates:
        print("No attendance records found.")
        return

    # Sort dates
    sorted_dates = sorted(dates)

    # Print table header
    print("\n--- Full Attendance Table ---")
    header = ["Student ID", "Name"] + sorted_dates
    print(" | ".join(f"{h:<12}" for h in header))
    print("-" * (15 * len(header)))

    # Print each student’s attendance
    for student in students:
        sid = student["Student ID"]
        name = student["Name"]
        row = [sid, name]
        for date in sorted_dates:
            status = attendance_data.get(date, {}).get(sid, "N/A")
            row.append(status)
        print(" | ".join(f"{c:<12}" for c in row))

def attendance_report_by_date():
    students = get_students()
    if not students:
        print("No students found.")
        return

    # Ask for date
    date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date_input:
        report_date = datetime.today().date().isoformat()
    else:
        try:
            report_date = datetime.strptime(date_input, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

    # Read attendance records for that date
    attendance_records = {}
    if os.path.exists("data/attendance.csv"):
        with open("data/attendance.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Date"] == report_date:
                    attendance_records[row["Student ID"]] = row["Status"]

    print(f"\n--- Attendance Report for {report_date} ---")
    print(f"{'Student ID':<12} {'Name':<20} {'Status':<10}")
    print("-" * 45)
    for student in students:
        sid = student["Student ID"]
        name = student["Name"]
        status = attendance_records.get(sid, "Not Marked")
        print(f"{sid:<12} {name:<20} {status:<10}")


def calculate_attendance_percentage():
    students = get_students()
    if not students:
        print("No students found.")
        return

    attendance_data = defaultdict(list)  # {student_id: [P/A, P/A, ...]}
    try:
        with open("data/attendance.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                attendance_data[row["Student ID"]].append(row["Status"])
    except FileNotFoundError:
        print("No attendance records found.")
        return

    print("\n--- Attendance Percentage ---")
    for student in students:
        sid = student["Student ID"]
        name = student["Name"]
        records = attendance_data.get(sid, [])
        if not records:
            percentage = 0
        else:
            total = len(records)
            present_count = records.count("P")
            percentage = (present_count / total) * 100

        print(f"{name} ({sid}): {percentage:.2f}%")
def reset_system():
    os.makedirs("data", exist_ok=True)
    
    # Clear students file
    with open(STUDENTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Student ID", "Name"])
        writer.writeheader()
    
    # Clear attendance file
    with open(ATTENDANCE_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Student ID", "Status"])
        writer.writeheader()
    
    print("System has been reset: all students and attendance records cleared!")
