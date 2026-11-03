import sqlite3

# Connect to SQLite database
def connect_db():
    return sqlite3.connect("student.db")


# Create student table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL,
            semester INTEGER NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Add student
def add_student(student_id, name, age, course, semester, phone):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students
            (student_id, name, age, course, semester, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, name, age, course, semester, phone))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# Display all students
def get_all_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    conn.close()
    return records


# Search student by ID
def search_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    record = cursor.fetchone()

    conn.close()
    return record


# Update student
def update_student(student_id, name, age, course, semester, phone):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, course = ?, semester = ?, phone = ?
        WHERE student_id = ?
    """, (name, age, course, semester, phone, student_id))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()
    return updated


# Delete student
def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()
    return deleted