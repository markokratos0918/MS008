# College Database Management System (SQLite + Python)

## Overview
This project is a **command-line database management system** built with **Python** and **SQLite**.  
It simulates a **college database** containing records for Students, Lecturers, Courses, Subjects, Admin staff, Enrollments, and Fees.  

The system provides two main modes:
1. **Main Menu** – For general users to view records and enrollment counts.  
2. **Admin Menu** – For administrators to manage records (add, update, delete, view).  

---

## Technical Features

### Database
- Uses **SQLite3** as the backend (file: `college_database.db`).  
- Tables included:
  - **Student** – student details and program info  
  - **Lecturer** – lecturer information and departments  
  - **Admin** – administrative staff with roles  
  - **Course** – courses offered, linked to lecturers  
  - **Subject** – subjects belonging to courses  
  - **Enrollment** – student-course enrollments with semester and status  
  - **Fees** – tuition and payment tracking  

Each table is created with **foreign key relationships** where applicable (e.g., Student ↔ Enrollment, Course ↔ Subject).

---

### Menus
#### Main Menu
```
1. View Yoobee College Records
2. View Enrollment Counts
3. Admin Options
0. Exit
```

#### Admin Management Menu
```
1. View Tables
2. Add Record
3. Update Record
4. Delete Record
0. Back to Main Menu
```

---

### Core Functions
- **create_connection()** → Connects to the SQLite database.  
- **create_tables()** → Ensures all required tables are created if they don’t exist.  
- **view_table()** → Displays all records from a user-selected table.  
- **show_enrollment_counts()** → Aggregates number of students enrolled per course.  
- **add_record()** → Allows admin to insert new data into a table.  
- **update_record()** → Allows admin to modify existing records.  
- **delete_record()** → Removes records matching a condition.  
- **show_all_tables()** → Lists all tables currently stored in the database.  

---

## Running the Program
1. Ensure Python 3 is installed.  
2. Save the script as `college_database.py`.  
3. Run from terminal:
   ```
   python college_database.py
   ```
4. Follow on-screen menu options to interact with the database.  


