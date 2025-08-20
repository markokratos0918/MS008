from database import create_tables
from db_manager import view_table, show_enrollment_counts, admin_interface, show_main_menu
def main():
    create_tables()  # ensure schema exists

    while True:
        show_main_menu()
        choice = input("Select an option: ")
        if choice == "1":
            view_table()
        elif choice == "2":
            show_enrollment_counts()
        elif choice == "3":
            admin_interface()
        elif choice == "0":
            print("\nHave a Nice Day! Goodbye!")
            break
            
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()