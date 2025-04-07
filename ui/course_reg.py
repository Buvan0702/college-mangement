import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from sidebar import Sidebar  # Import the shared sidebar component

class CourseRegistrationSystem:
    def __init__(self, parent_frame, student_id, nav_callbacks=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.nav_callbacks = nav_callbacks
        
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create sidebar with navigation
        self.sidebar = Sidebar(self.parent_frame, active_item="course_registration", nav_callbacks=self.nav_callbacks)
        
        # Create content area
        self.create_content_area()
    
    def create_content_area(self):
        # Title and top bar
        self.create_top_bar()
        
        # Course table
        self.create_course_table()
    
    def create_top_bar(self):
        # Title
        ctk.CTkLabel(
            self.parent_frame, 
            text="Course Registration", 
            font=("Arial", 24, "bold"), 
            text_color="#3B82F6"
        ).place(x=280, y=20)
        
        # Semester Dropdown
        self.semester_var = ctk.StringVar(value="Select Semester")
        self.semester_dropdown = ctk.CTkComboBox(
            self.parent_frame, 
            variable=self.semester_var, 
            values=["Select Semester", "Fall 2023", "Spring 2023", "Fall 2022"],
            width=180, 
            height=35, 
            fg_color="white", 
            text_color="black", 
            dropdown_hover_color="#3B82F6"
        )
        self.semester_dropdown.place(x=280, y=60)

        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self.parent_frame, 
            placeholder_text="Search Courses", 
            width=250, 
            height=35, 
            fg_color="white", 
            text_color="black"
        )
        self.search_entry.place(x=500, y=60)

        # Filter Button
        self.filter_button = ctk.CTkButton(
            self.parent_frame, 
            text="Filter", 
            font=("Arial", 12), 
            fg_color="#3B82F6", 
            text_color="white", 
            width=80, 
            height=35,
            command=self.filter_courses
        )
        self.filter_button.place(x=770, y=60)

    def create_course_table(self):
        # Table Frame
        self.table_frame = ctk.CTkFrame(
            self.parent_frame, 
            width=780, 
            height=550, 
            fg_color="white", 
            border_width=1,
            border_color="#DDDDDD"
        )
        self.table_frame.place(x=280, y=120)

        # Create Treeview
        columns = ("Course Code", "Course Name", "Instructor", "Credits", "Register")
        self.tree = ttk.Treeview(
            self.table_frame, 
            columns=columns, 
            show="headings", 
            height=15
        )
        self.tree.place(x=10, y=10, width=760, height=530)

        # Configure columns
        self.tree.heading("Course Code", text="Course Code")
        self.tree.heading("Course Name", text="Course Name")
        self.tree.heading("Instructor", text="Instructor")
        self.tree.heading("Credits", text="Credits")
        self.tree.heading("Register", text="Register")

        self.tree.column("Course Code", width=100, anchor="center")
        self.tree.column("Course Name", width=300, anchor="center")
        self.tree.column("Instructor", width=150, anchor="center")
        self.tree.column("Credits", width=100, anchor="center")
        self.tree.column("Register", width=100, anchor="center")

        # Fetch and populate courses
        self.fetch_courses()

    def fetch_courses(self):
        """Fetch available courses from database"""
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor()

            # Check if courses table exists
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'college_system' AND table_name = 'courses'
            """)
            if cursor.fetchone()[0] == 0:
                # Create courses table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS courses (
                        course_code VARCHAR(10) PRIMARY KEY,
                        course_name VARCHAR(100) NOT NULL,
                        department VARCHAR(50),
                        credits INT,
                        instructor VARCHAR(100)
                    )
                """)
                
                # Insert sample courses
                sample_courses = [
                    ('CS101', 'Introduction to Computer Science', 'Computer Science', 3, 'Dr. Smith'),
                    ('MATH201', 'Calculus II', 'Mathematics', 4, 'Prof. Johnson'),
                    ('ENG202', 'Advanced English', 'Humanities', 3, 'Ms. Davis'),
                    ('BIO301', 'Biology', 'Biology', 4, 'Dr. Green'),
                    ('PHYS101', 'Physics I', 'Physics', 4, 'Dr. Brown')
                ]
                
                cursor.executemany("""
                    INSERT INTO courses (course_code, course_name, department, credits, instructor)
                    VALUES (%s, %s, %s, %s, %s)
                """, sample_courses)
                
                connection.commit()

            # Check if student_courses table exists
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'college_system' AND table_name = 'student_courses'
            """)
            if cursor.fetchone()[0] == 0:
                # Create student_courses table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student_courses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        course_code VARCHAR(10),
                        semester VARCHAR(50),
                        FOREIGN KEY (student_id) REFERENCES students(student_id),
                        FOREIGN KEY (course_code) REFERENCES courses(course_code)
                    )
                """)
                connection.commit()

            # Execute query to fetch courses
            cursor.execute("""
                SELECT course_code, course_name, instructor, credits 
                FROM courses 
                WHERE course_code NOT IN (
                    SELECT course_code 
                    FROM student_courses 
                    WHERE student_id = %s
                )
            """, (self.student_id,))

            courses = cursor.fetchall()

            # Clear existing items
            for i in self.tree.get_children():
                self.tree.delete(i)

            # If no courses found, show message
            if not courses:
                messagebox.showinfo("No Courses", "No available courses found. You may have registered for all available courses.")
                return

            # Populate table
            for course in courses:
                item = self.tree.insert("", "end", values=course + ("",))
                
                # Create register button
                register_btn = ctk.CTkButton(
                    self.tree, 
                    text="Register", 
                    font=("Arial", 10), 
                    fg_color="#3B82F6",
                    text_color="white", 
                    width=80, 
                    height=25,
                    command=lambda c=course[0]: self.register_course(c)
                )
                
                # Position the button in the Register column
                self.tree.item(item, tags=(item,))
                self.tree.tag_configure(item, background="white")
                
                # Add "Register" text in the register column
                self.tree.set(item, "Register", "Register")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def filter_courses(self):
        """Filter courses based on search term"""
        search_term = self.search_entry.get().lower()
        semester = self.semester_var.get()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor()

            # Construct query with search and semester filters
            query = """
                SELECT course_code, course_name, instructor, credits 
                FROM courses 
                WHERE (LOWER(course_name) LIKE %s OR LOWER(course_code) LIKE %s)
            """
            params = [f"%{search_term}%", f"%{search_term}%"]

            if semester and semester != "Select Semester":
                query += " AND semester = %s"
                params.append(semester)

            cursor.execute(query, params)
            courses = cursor.fetchall()

            # Clear existing items
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Populate filtered table
            for course in courses:
                item = self.tree.insert("", "end", values=course + ("",))
                self.tree.set(item, "Register", "Register")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def register_course(self, course_code):
        """Register student for a course"""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor()

            # Insert course registration
            cursor.execute("""
                INSERT INTO student_courses (student_id, course_code, semester) 
                VALUES (%s, %s, %s)
            """, (self.student_id, course_code, self.semester_var.get() or "Fall 2023"))

            connection.commit()
            messagebox.showinfo("Success", f"Registered for course {course_code}")

            # Refresh course list
            self.fetch_courses()

        except mysql.connector.Error as err:
            messagebox.showerror("Registration Error", str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# This allows the module to be run directly for testing
def main():
    root = ctk.CTk()
    root.title("Course Registration")
    root.geometry("1200x700")
    
    main_frame = ctk.CTkFrame(root, fg_color="white")
    main_frame.pack(fill='both', expand=True)
    
    app = CourseRegistrationSystem(main_frame, student_id=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()