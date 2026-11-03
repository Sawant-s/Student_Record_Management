import database




# Function to take student details
def get_student_details():

    name = input("Enter Student Name: ").strip()

    while True:
        try:
            age = int(input("Enter Age: "))
            if age <= 0:
                print("Age must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid age.")

    course = input("Enter Course: ").strip()

    while True:
        try:
            semester = int(input("Enter Semester: "))
            if semester <= 0:
                print("Semester must be greater than zero.")
                continue
            break
        except ValueError:
            print("Please enter a valid semester.")

    phone = input("Enter Phone Number: ").strip()

    if not name or not course or not phone:
        print("Name, course and phone cannot be empty.")
        return None

    return name, age, course, semester, phone


# Function to display one student
def display_student(student):

    print("\n------ STUDENT DETAILS ------")
    print("Student ID :", student[0])
    print("Name       :", student[1])
    print("Age        :", student[2])
    print("Course     :", student[3])
    print("Semester   :", student[4])
    print("Phone      :", student[5])
    print("-----------------------------")


# Add student
def add_student():

    print("\n--- ADD STUDENT ---")

    student_id = input("Enter Student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    details = get_student_details()

    if details is None:
        return

    success = database.add_student(student_id, *details)

    if success:
        print("\nStudent added successfully!")
    else:
        print("\nStudent ID already exists!")


# Display all students
def view_students():

    print("\n--- ALL STUDENTS ---")

    students = database.get_all_students()

    if not students:
        print("No student records found.")
        return

    for student in students:
        display_student(student)


# Search student
def search_student():

    print("\n--- SEARCH STUDENT ---")

    student_id = input("Enter Student ID: ").strip()

    student = database.search_student(student_id)

    if student:
        display_student(student)
    else:
        print("Student not found!")


# Update student
def update_student():

    print("\n--- UPDATE STUDENT ---")

    student_id = input("Enter Student ID: ").strip()

    existing = database.search_student(student_id)

    if not existing:
        print("Student not found!")
        return

    print("Enter updated details:")
    details = get_student_details()

    if details is None:
        return

    success = database.update_student(student_id, *details)

    if success:
        print("\nStudent updated successfully!")


# Delete student
def delete_student():

    print("\n--- DELETE STUDENT ---")

    student_id = input("Enter Student ID: ").strip()

    student = database.search_student(student_id)

    if not student:
        print("Student not found!")
        return

    display_student(student)

    confirm = input("Are you sure you want to delete? (yes/no): ")

    if confirm.lower() == "yes":

        success = database.delete_student(student_id)

        if success:
            print("Student deleted successfully!")

    else:
        print("Delete operation cancelled.")


# Main menu
def main():

    database.create_table()

    while True:

        print("\n================================")
        print(" STUDENT RECORD MANAGEMENT SYSTEM")
        print("================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("================================")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Thank you for using Student Record Management System!")
            break

        else:
            print("Invalid choice! Please select 1 to 6.")


if __name__ == "__main__":
    main()