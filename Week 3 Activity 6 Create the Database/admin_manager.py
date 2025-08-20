from database import create_connection
from db_manager import show_admin_menu, view_table
import sqlite3

#---Admin Menu loop----#
def admin_interface():
    while True:
        show_admin_menu()
        choice = input("Select an admin option: ")
        if choice == "1":
            view_table()
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