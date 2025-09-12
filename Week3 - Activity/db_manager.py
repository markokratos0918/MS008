from database import create_connection
import sqlite3

# ---------- USER FUNCTIONS ----------
def add_user(name, email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))  # FIXED
    conn.commit()
    conn.close()
    

def search_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------- STUDENT FUNCTION ----------
def add_student(name, address):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, address) VALUES (?, ?)", (name, address))
    conn.commit()
    conn.close()

# ---------View all---------    

def view_all_info():
    conn = create_connection()
    cursor = conn.cursor()

    # Get all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Get all students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    print("\n=== USERS TABLE ===")
    if users:
        for u in users:
            print(f"User ID: {u[0]} | Name: {u[1]} | Email: {u[2]}")
    else:
        print("No users found.")

    print("\n=== STUDENTS TABLE ===")
    if students:
        for s in students:
            print(f"Student ID: {s[0]} | Name: {s[1]} | Address: {s[2]}")
    else:
        print("No students found.")


