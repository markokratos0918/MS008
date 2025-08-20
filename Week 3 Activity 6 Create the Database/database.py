
import sqlite3

# Connect to SQLite database

def create_connection():
    return sqlite3.connect("college_database.db") 


# Create tables

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Student (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    program TEXT,
    year_level INTEGER
    );
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lecturer (
        lecturer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Admin (
        admin_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Course (
        course_id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        description TEXT,
        credits INTEGER,
        lecturer_id INTEGER,
        FOREIGN KEY (lecturer_id) REFERENCES Lecturer(lecturer_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subject (
        subject_id INTEGER PRIMARY KEY,
        subject_name TEXT NOT NULL,
        course_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES Course(course_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Enrollment (
        enrollment_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        course_id INTEGER,
        semester TEXT,
        status TEXT,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (course_id) REFERENCES Course(course_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fees (
        fee_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        amount REAL,
        due_date TEXT,
        status TEXT,
        FOREIGN KEY (student_id) REFERENCES Student(student_id)
    );
    """)

    conn.commit()
    conn.close()

# Inserting Sample Data - Optional
conn = create_connection()
cursor = conn.cursor()

cursor.execute("INSERT OR IGNORE INTO Student VALUES (1, 'Alice Smith', 'alice@example.com', 'Computer Science', 1);")
cursor.execute("INSERT OR IGNORE INTO Student VALUES (2, 'Bob Johnson', 'bob@example.com', 'Information Systems', 2);")

cursor.execute("INSERT OR IGNORE INTO Lecturer VALUES (1, 'Dr. Jane Doe', 'jane.doe@example.com', 'Computer Science');")

cursor.execute("INSERT OR IGNORE INTO Course VALUES (1, 'Intro to Programming', 'Learn programming basics', 3, 1);")
cursor.execute("INSERT OR IGNORE INTO Course VALUES (2, 'Database Systems', 'Relational databases and SQL', 3, 1);")

cursor.execute("INSERT OR IGNORE INTO Subject VALUES (1, 'Python Basics', 1);")
cursor.execute("INSERT OR IGNORE INTO Subject VALUES (2, 'SQL Fundamentals', 2);")

cursor.execute("INSERT OR IGNORE INTO Enrollment VALUES (1, 1, 1, 'Fall 2023', 'enrolled');")
cursor.execute("INSERT OR IGNORE INTO Enrollment VALUES (2, 2, 2, 'Fall 2023', 'enrolled');")
cursor.execute("INSERT OR IGNORE INTO Enrollment VALUES (3, 1, 2, 'Fall 2023', 'enrolled');")

cursor.execute("INSERT OR IGNORE INTO Fees VALUES (1, 1, 1500.00, '2023-09-01', 'paid');")
cursor.execute("INSERT OR IGNORE INTO Fees VALUES (2, 2, 1500.00, '2023-09-01', 'unpaid');")

conn.commit()
conn.close()