from student_manager import add_student, get_students
from attendance_manager import mark_attendance, view_attendance, attendance_report_by_date,calculate_attendance_percentage, reset_system

def menu():
    print("\n--- Attendance Management System ---")
    print("1. Add Student")
    print("2. Mark Attendance")
    print("3. View Attendance")
    print("4. Attendance report by Date")
    print("5. Attendance percentage Calculation")
    print("6. Reset System")
    print("7. Exit")

while True:
    menu()
    choice = input("Enter choice: ")

    if choice == "1":
        sid = input("Student ID: ")
        name = input("Student Name: ")
        add_student(sid, name)
        print("Student added successfully.")
    elif choice == "2":
        students = get_students()
        if not students:
            print("No students found.")
            continue

        for student in students:
            status = input(f"{student['Name']} (P/A): ").upper()
            mark_attendance(student["Student ID"], status)

        print("Attendance marked.")
    elif choice == "3":
        view_attendance()
    elif choice == "4":
        attendance_report_by_date()
    elif choice =="5":
        calculate_attendance_percentage()
    elif choice=="6":
        confirm = input("Are you sure you want to reset the system? This will delete all students and attendance records (y/n): ").lower()
        if confirm == "y":
            reset_system()
        else:
            print("Reset canceled.")
    elif choice == "7":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
