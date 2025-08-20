from database import create_connection
import sqlite3
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
def admin_interface():
    while True:
        show_admin_menu()
        choice = input("Select an admin option: ")
        if choice == "1":
            show_all_tables()
        elif choice == "2":
            add_record()
        elif choice == "3":
            update_record()
        elif choice == "4":
            delete_record()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
            
def show_all_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    if tables:
        print("\nTables in the database:")
        for (table_name,) in tables:
            print(f"- {table_name}")
    else:
        print("No tables found in the database.")
    conn.close()

def add_record():
    table = input("Enter table name to add record to: ")
    columns = input("Enter column names (comma-separated): ")
    values = input("Enter values (comma-separated, use quotes for text): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({values})")
        conn.commit()
        print("Record added successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    conn.close()

def update_record():
    table = input("Enter table name to update: ")
    set_clause = input("Enter SET clause (e.g., name='John'): ")
    condition = input("Enter WHERE condition (e.g., student_id=1): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {condition}")
        conn.commit()
        print("Record updated successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    conn.close()

def delete_record():
    table = input("Enter table name to delete from: ")
    condition = input("Enter WHERE condition (e.g., student_id=1): ")
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM {table} WHERE {condition}")
        conn.commit()
        print("Record deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    conn.close()