from database import create_connection
import sqlite3
# --- Menus ---
def show_main_menu():
    print("\nMain Menu")
    print("1. View Yoobee College Records")
    print("2. View Enrollment Counts")
    print("3. Admin Options")
    print("4. Exit")

def show_admin_menu():
    print("\nAdmin Management Menu")
    print("1. View Tables")
    print("2. Add Record")
    print("3. Update Record")
    print("4. Delete Record")
    print("0. Back to Main Menu")

# --- Database operations (self-contained) ---
def view_table():
    table = input("Enter list of records to view (Student, Lecturer, Admin, Course, Subject, Enrollment, Fees): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Error: {e}")
    conn.close()

    
def show_enrollment_counts():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Course.course_name, COUNT(Enrollment.student_id) AS num_enrolled
    FROM Course
    LEFT JOIN Enrollment ON Course.course_id = Enrollment.course_id
    GROUP BY Course.course_id;
    """)
    results = cursor.fetchall()
    for course_name, count in results:
        print(f"{course_name}: {count} students enrolled")
    conn.close()

# --- Admin Menu Loop ---
