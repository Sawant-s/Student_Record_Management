
import tkinter as tk
from tkinter import ttk, messagebox
import database
import csv
import os
from datetime import datetime


# ==============================
# COLORS AND THEME
# ==============================

NAVY = "#172B4D"
SIDEBAR = "#14243D"
BLUE = "#2563EB"
LIGHT_BG = "#F3F6FB"
WHITE = "#FFFFFF"
TEXT = "#263445"
MUTED = "#64748B"
GREEN = "#16A34A"
RED = "#DC2626"
PURPLE = "#7C3AED"


class StudentManagementApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1250x750")
        self.root.minsize(1050, 650)
        self.root.configure(bg=LIGHT_BG)

        self.selected_id = None
        self.search_var = tk.StringVar()
        self.page_title = None
        self.content = None
        self.table = None
        self.total_value = None
        self.course_value = None
        self.semester_value = None
        self.status_label = None

        database.create_table()

        self.setup_styles()
        self.create_layout()
        self.show_dashboard()

    # ==============================
    # STYLES
    # ==============================

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=38,
            fieldbackground=WHITE,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#E8EEF7",
            foreground=NAVY,
            font=("Segoe UI", 10, "bold"),
            padding=12,
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", NAVY)]
        )

        style.configure(
            "Vertical.TScrollbar",
            background="#CBD5E1",
            troughcolor=LIGHT_BG,
            borderwidth=0
        )

    # ==============================
    # MAIN LAYOUT
    # ==============================

    def create_layout(self):

        # Left sidebar
        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=240
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main area
        self.main_area = tk.Frame(
            self.root,
            bg=LIGHT_BG
        )
        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.create_topbar()

        self.content = tk.Frame(
            self.main_area,
            bg=LIGHT_BG
        )
        self.content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=22
        )

        # Footer
        footer = tk.Frame(
            self.main_area,
            bg=LIGHT_BG
        )
        footer.pack(fill="x", padx=28, pady=(0, 10))

        tk.Label(
            footer,
            text="Student Record Management System",
            font=("Segoe UI", 9),
            bg=LIGHT_BG,
            fg=MUTED
        ).pack(side="left")

        self.status_label = tk.Label(
            footer,
            text="Ready",
            font=("Segoe UI", 9),
            bg=LIGHT_BG,
            fg=GREEN
        )
        self.status_label.pack(side="right")

    # ==============================
    # SIDEBAR
    # ==============================

    def create_sidebar(self):

        tk.Label(
            self.sidebar,
            text="SRMS",
            font=("Segoe UI", 25, "bold"),
            bg=SIDEBAR,
            fg=WHITE
        ).pack(anchor="w", padx=25, pady=(28, 2))

        tk.Label(
            self.sidebar,
            text="STUDENT MANAGEMENT",
            font=("Segoe UI", 8, "bold"),
            bg=SIDEBAR,
            fg="#94A3B8"
        ).pack(anchor="w", padx=27, pady=(0, 35))

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 9, "bold"),
            bg=SIDEBAR,
            fg="#94A3B8"
        ).pack(anchor="w", padx=22, pady=(0, 12))

        self.nav_button(
            "▦   Dashboard",
            self.show_dashboard
        )

        self.nav_button(
            "▤   Student Records",
            self.show_students
        )

        self.nav_button(
            "⇩   Export Records",
            self.export_csv
        )

        # Bottom information
        bottom = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )
        bottom.pack(side="bottom", fill="x", pady=25)

        tk.Label(
            bottom,
            text="PROJECT VERSION 1.0",
            font=("Segoe UI", 8, "bold"),
            bg=SIDEBAR,
            fg="#94A3B8"
        ).pack(pady=5)

        tk.Label(
            bottom,
            text="Developed with Python + SQLite",
            font=("Segoe UI", 8),
            bg=SIDEBAR,
            fg="#94A3B8"
        ).pack()

        self.nav_button(
            "⏻   Exit Application",
            self.exit_app
        )

    def nav_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=SIDEBAR,
            fg="#E2E8F0",
            activebackground="#29446B",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            pady=14,
            cursor="hand2"
        )

        button.pack(fill="x", padx=10, pady=3)

    # ==============================
    # TOP BAR
    # ==============================

    def create_topbar(self):

        topbar = tk.Frame(
            self.main_area,
            bg=WHITE,
            height=75
        )
        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        self.page_title = tk.Label(
            topbar,
            text="Dashboard",
            font=("Segoe UI", 19, "bold"),
            bg=WHITE,
            fg=NAVY
        )
        self.page_title.pack(side="left", padx=28)

        tk.Label(
            topbar,
            text="ADMIN PANEL",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=BLUE
        ).pack(side="right", padx=28)

    # ==============================
    # COMMON FUNCTIONS
    # ==============================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def set_status(self, text, color=GREEN):

        self.status_label.config(
            text=text,
            fg=color
        )

    def get_students(self):

        return database.get_all_students()

    # ==============================
    # DASHBOARD
    # ==============================

    def show_dashboard(self):

        self.clear_content()
        self.page_title.config(text="Dashboard")

        students = self.get_students()

        total = len(students)

        courses = set(
            student[3] for student in students
        )

        semesters = set(
            student[4] for student in students
        )

        tk.Label(
            self.content,
            text="Welcome to Student Management",
            font=("Segoe UI", 19, "bold"),
            bg=LIGHT_BG,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            self.content,
            text="Manage student information from one place.",
            font=("Segoe UI", 10),
            bg=LIGHT_BG,
            fg=MUTED
        ).pack(anchor="w", pady=(5, 22))

        # Statistics cards
        cards = tk.Frame(
            self.content,
            bg=LIGHT_BG
        )
        cards.pack(fill="x")

        self.create_card(
            cards, "TOTAL STUDENTS",
            str(total), BLUE
        )

        self.create_card(
            cards, "TOTAL COURSES",
            str(len(courses)), PURPLE
        )

        self.create_card(
            cards, "ACTIVE SEMESTERS",
            str(len(semesters)), GREEN
        )

        # Quick actions
        tk.Label(
            self.content,
            text="Quick Actions",
            font=("Segoe UI", 15, "bold"),
            bg=LIGHT_BG,
            fg=NAVY
        ).pack(anchor="w", pady=(30, 15))

        actions = tk.Frame(
            self.content,
            bg=LIGHT_BG
        )
        actions.pack(anchor="w")

        self.action_button(
            actions, "+ Add Student",
            self.add_student, GREEN
        )

        self.action_button(
            actions, "View Students",
            self.show_students, BLUE
        )

        self.action_button(
            actions, "Export CSV",
            self.export_csv, PURPLE
        )

        # Recent student records
        tk.Label(
            self.content,
            text="Recent Student Records",
            font=("Segoe UI", 15, "bold"),
            bg=LIGHT_BG,
            fg=NAVY
        ).pack(anchor="w", pady=(30, 12))

        self.create_student_table(
            self.content,
            students[-5:][::-1],
            height=5
        )

        self.set_status("Dashboard loaded")

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15),
            ipady=12
        )

        tk.Frame(
            card,
            bg=color,
            height=4
        ).pack(fill="x")

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", padx=18, pady=(15, 5))

        tk.Label(
            card,
            text=value,
            font=("Segoe UI", 26, "bold"),
            bg=WHITE,
            fg=color
        ).pack(anchor="w", padx=18, pady=(0, 12))

    def action_button(self, parent, text, command, color):

        tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=11,
            cursor="hand2"
        ).pack(side="left", padx=(0, 12))

    # ==============================
    # STUDENT TABLE
    # ==============================

    def create_student_table(
        self, parent, students, height=12
    ):

        table_frame = tk.Frame(
            parent,
            bg=WHITE
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "ID", "Name", "Age",
            "Course", "Semester", "Phone"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=height
        )

        widths = [90, 180, 60, 180, 90, 140]

        for column, width in zip(columns, widths):

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=width,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for student in students:

            self.table.insert(
                "",
                "end",
                values=student
            )

    # ==============================
    # STUDENT RECORDS PAGE
    # ==============================

    def show_students(self):

        self.clear_content()
        self.page_title.config(text="Student Records")

        heading = tk.Frame(
            self.content,
            bg=LIGHT_BG
        )
        heading.pack(fill="x")

        tk.Label(
            heading,
            text="All Student Records",
            font=("Segoe UI", 18, "bold"),
            bg=LIGHT_BG,
            fg=NAVY
        ).pack(side="left")

        tk.Button(
            heading,
            text="+ Add Student",
            command=self.add_student,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

        tk.Label(
            self.content,
            text="Search by student ID or student name",
            font=("Segoe UI", 10),
            bg=LIGHT_BG,
            fg=MUTED
        ).pack(anchor="w", pady=(8, 10))

        search_frame = tk.Frame(
            self.content,
            bg=LIGHT_BG
        )
        search_frame.pack(fill="x", pady=(0, 15))

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1
        )

        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=9
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.filter_students()
        )

        tk.Button(
            search_frame,
            text="Clear Search",
            command=self.clear_search,
            bg="#64748B",
            fg=WHITE,
            relief="flat",
            padx=14,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=10)

        self.records_count = tk.Label(
            self.content,
            text="",
            font=("Segoe UI", 9),
            bg=LIGHT_BG,
            fg=MUTED
        )
        self.records_count.pack(anchor="w", pady=(0, 8))

        # Action buttons are placed ABOVE the table so they remain visible.
        buttons = tk.Frame(
            self.content,
            bg=LIGHT_BG
        )
        buttons.pack(fill="x", pady=(0, 12))

        self.action_button(
            buttons, "Update Selected",
            self.update_student, BLUE
        )

        self.action_button(
            buttons, "Delete Selected",
            self.delete_student, RED
        )

        self.action_button(
            buttons, "Refresh",
            self.refresh_students, "#64748B"
        )

        # The table uses the remaining available space.
        self.create_student_table(
            self.content,
            self.get_students()
        )

        self.update_records_count()
        self.set_status("Student records loaded")

    def update_records_count(self):

        if self.records_count and self.records_count.winfo_exists():

            count = len(self.table.get_children())

            self.records_count.config(
                text=f"Showing {count} student record(s)"
            )

    def filter_students(self):

        search_text = self.search_var.get().strip().lower()

        for item in self.table.get_children():
            self.table.delete(item)

        students = self.get_students()

        for student in students:

            if (
                search_text in str(student[0]).lower()
                or search_text in str(student[1]).lower()
            ):

                self.table.insert(
                    "",
                    "end",
                    values=student
                )

        self.update_records_count()

    def clear_search(self):

        self.search_var.set("")
        self.filter_students()

    def refresh_students(self):

        self.show_students()
        self.set_status("Records refreshed")

    # ==============================
    # FORM VALIDATION
    # ==============================

    def validate_details(self, entries, window):

        name = entries["name"].get().strip()
        age_text = entries["age"].get().strip()
        course = entries["course"].get().strip()
        semester_text = entries["semester"].get().strip()
        phone = entries["phone"].get().strip()

        if not all([
            name, age_text, course,
            semester_text, phone
        ]):

            messagebox.showerror(
                "Validation Error",
                "Please fill all the fields.",
                parent=window
            )

            return None

        if not any(char.isalpha() for char in name) or not all(
            char.isalpha() or char.isspace() or char in ".-'"
            for char in name
        ):

            messagebox.showerror(
                "Invalid Name",
                "Please enter a valid student name.",
                parent=window
            )

            return None

        try:
            age = int(age_text)
            semester = int(semester_text)

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Age and semester must be whole numbers.",
                parent=window
            )

            return None

        if not 1 <= age <= 120:

            messagebox.showerror(
                "Invalid Age",
                "Age must be between 1 and 120.",
                parent=window
            )

            return None

        if not 1 <= semester <= 12:

            messagebox.showerror(
                "Invalid Semester",
                "Semester must be between 1 and 12.",
                parent=window
            )

            return None

        if not phone.isdigit() or len(phone) != 10:

            messagebox.showerror(
                "Invalid Phone",
                "Enter a valid 10-digit phone number.",
                parent=window
            )

            return None

        return name, age, course, semester, phone

    # ==============================
    # ADD / UPDATE FORM
    # ==============================

    def open_student_form(self, title, student=None):

        window = tk.Toplevel(self.root)
        window.title(title)

        # Keep the form within the available screen height.
        screen_height = window.winfo_screenheight()
        form_height = min(680, screen_height - 80)
        window.geometry(f"520x{form_height}")
        window.minsize(480, min(600, form_height))
        window.resizable(True, True)
        window.configure(bg=WHITE)
        window.transient(self.root)
        window.grab_set()

        # Heading
        tk.Label(
            window,
            text=title,
            font=("Segoe UI", 20, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(pady=(16, 3))

        tk.Label(
            window,
            text="Enter the student information below",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=MUTED
        ).pack(pady=(0, 8))

        # Keep action buttons fixed at the bottom so they remain visible.
        button_frame = tk.Frame(window, bg=WHITE)
        button_frame.pack(side="bottom", fill="x", padx=28, pady=14)

        entries_frame = tk.Frame(window, bg=WHITE)
        entries_frame.pack(fill="both", expand=True, padx=35, pady=(0, 5))

        fields = [
            ("Student ID", "id"),
            ("Full Name", "name"),
            ("Age", "age"),
            ("Course", "course"),
            ("Semester", "semester"),
            ("Phone Number", "phone")
        ]

        entries = {}

        for label, key in fields:
            tk.Label(
                entries_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(anchor="w", pady=(4, 2))

            entry = tk.Entry(
                entries_frame,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )
            entry.pack(fill="x", ipady=5)

            if key == "id" and student:
                entry.insert(0, student[0])
                entry.config(state="readonly")
            elif student:
                index = {
                    "name": 1,
                    "age": 2,
                    "course": 3,
                    "semester": 4,
                    "phone": 5
                }.get(key)

                if index is not None:
                    entry.insert(0, student[index])

            entries[key] = entry

        def save_student():
            student_id = entries["id"].get().strip()

            if not student_id:
                messagebox.showerror(
                    "Validation Error",
                    "Student ID is required.",
                    parent=window
                )
                return

            details = self.validate_details(entries, window)
            if details is None:
                return

            if student:
                success = database.update_student(student_id, *details)
                if success:
                    messagebox.showinfo(
                        "Success",
                        "Student updated successfully!",
                        parent=window
                    )
                else:
                    messagebox.showerror(
                        "Error",
                        "Unable to update student.",
                        parent=window
                    )
                    return
            else:
                success = database.add_student(student_id, *details)
                if success:
                    messagebox.showinfo(
                        "Success",
                        "Student added successfully!",
                        parent=window
                    )
                else:
                    messagebox.showerror(
                        "Duplicate ID",
                        "This Student ID already exists.",
                        parent=window
                    )
                    return

            window.destroy()
            self.show_students()
            self.set_status("Student record saved")

        tk.Button(
            button_frame,
            text="Save Student",
            command=save_student,
            bg=BLUE,
            fg=WHITE,
            activebackground="#1D4ED8",
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        tk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy,
            bg="#E2E8F0",
            fg=NAVY,
            activebackground="#CBD5E1",
            activeforeground=NAVY,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(side="left", fill="x", expand=True, padx=(8, 0))

    def add_student(self):

        self.open_student_form(
            "Add New Student"
        )

    # ==============================
    # UPDATE STUDENT
    # ==============================

    def get_selected_student(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a student record first."
            )

            return None

        values = self.table.item(
            selected[0], "values"
        )

        return database.search_student(values[0])

    def update_student(self):

        student = self.get_selected_student()

        if student:

            self.open_student_form(
                "Update Student Details",
                student
            )

    # ==============================
    # DELETE STUDENT
    # ==============================

    def delete_student(self):

        student = self.get_selected_student()

        if not student:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete "
            f"{student[1]} (ID: {student[0]})?"
        )

        if confirm:

            if database.delete_student(student[0]):

                messagebox.showinfo(
                    "Deleted",
                    "Student record deleted successfully!"
                )

                self.show_students()
                self.set_status("Student deleted")

    # ==============================
    # CSV EXPORT
    # ==============================

    def export_csv(self):

        students = self.get_students()

        if not students:

            messagebox.showwarning(
                "No Records",
                "There are no student records to export."
            )

            return

        export_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "exports"
        )

        os.makedirs(
            export_folder,
            exist_ok=True
        )

        filename = (
            "students_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".csv"
        )

        file_path = os.path.join(
            export_folder,
            filename
        )

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Student ID",
                    "Name",
                    "Age",
                    "Course",
                    "Semester",
                    "Phone"
                ])

                writer.writerows(students)

            messagebox.showinfo(
                "Export Successful",
                f"Records exported successfully!\n\n"
                f"Saved in:\n{file_path}"
            )

            self.set_status("CSV exported successfully")

        except OSError as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # ==============================
    # EXIT
    # ==============================

    def exit_app(self):

        confirm = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit?"
        )

        if confirm:
            self.root.destroy()


# ==============================
# START APPLICATION
# ==============================

def run_app():

    root = tk.Tk()

    app = StudentManagementApp(root)

    root.mainloop()


if __name__ == "__main__":
    run_app()
