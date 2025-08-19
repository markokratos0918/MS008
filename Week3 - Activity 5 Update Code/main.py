from database import create_tables
from db_manager import add_user, view_all_info, search_user, delete_user, add_student


# ---------- MENU ----------
def menu():
    create_tables()

    while True:
        print("\n===== MENU =====")
        print("1. Add User")
        print("2. Add Student")
        print("3. View Users/Students")
        print("4. Search User by Name")
        print("5. Delete User by ID")
        print("6. Exit")
        

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            add_user(name, email)
            print("User added.")

        elif choice == "2":
            name = input("Enter Student Name: ")
            address = input("Enter Student Address: ")
            add_student(name, address)
            print("Student added.")
            
        elif choice == "3":
            view_all_info()

        elif choice == "4":
            name = input("Enter name to search: ")
            users = search_user(name)
            for user in users:
                print(user)

        elif choice == "5":
            user_id = int(input("Enter user ID to delete: "))
            delete_user(user_id)
            print("🗑️ User deleted.")
 
        elif choice == "6":
            print("Exiting...GoodBye!")
            break

        else:
            print("Invalid choice, try again.")


# ---------- MAIN ----------
if __name__ == "__main__":
    menu()