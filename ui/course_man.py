import customtkinter as ctk
import mysql.connector
from tkinter import messagebox, simpledialog
from sidebar import Sidebar  # Import the shared sidebar component

class CourseManagementSystem:
    def __init__(self, parent_frame, student_id, nav_callbacks=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.nav_callbacks = nav_callbacks
        
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create sidebar with navigation
        self.sidebar = Sidebar(self.parent_frame, active_item="course_management", nav_callbacks=self.nav_callbacks)
        
        # Create content area
        self.create_content_area()
    
    def create_content_area(self):
        # Title
        ctk.CTkLabel(
            self.parent_frame, 
            text="Course Management", 
            font=("Arial", 24, "bold"), 
            text_color="#3B82F6"
        ).place(x=280, y=20)
        
        # Create top bar with semester selector
        self.create_top_bar()
        
        # Create course cards
        self.create_course_cards()
    
    def create_top_bar(self):
        # Semester Dropdown
        self.semester_var = ctk.StringVar(value="Current Semester")
        self.semester_dropdown = ctk.CTkComboBox(
            self.parent_frame, 
            variable=self.semester_var, 
            values=["Current Semester", "Fall 2023", "Spring 2023", "Fall 2022"],
            width=180, 
            height=35, 
            fg_color="white", 
            text_color="black", 
            dropdown_hover_color="#3B82F6",
            command=self.filter_courses
        )
        self.semester_dropdown.place(x=280, y=60)

    def create_course_cards(self):
        # Fetch and display course cards
        self.course_frame = ctk.CTkFrame(
            self.parent_frame, 
            fg_color="white"
        )
        self.course_frame.place(x=280, y=120, width=900, height=550)

        # Fetch courses from database
        self.fetch_courses()

    def fetch_courses(self):
        """Fetch student's courses from database"""
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor(dictionary=True)

            # Check if necessary tables exist
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'college_system' AND table_name = 'student_courses'
            """)
            if cursor.fetchone()['COUNT(*)'] == 0:
                # Create student_courses table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student_courses (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        course_code VARCHAR(10),
                        semester VARCHAR(50) DEFAULT 'Fall 2023',
                        attendance_percentage DECIMAL(5,2) DEFAULT 85.0,
                        attendance_status VARCHAR(20) DEFAULT 'Present',
                        last_attended_date DATE DEFAULT CURRENT_DATE,
                        assignments_due INT DEFAULT 0,
                        grade_status VARCHAR(5) DEFAULT 'B+',
                        FOREIGN KEY (student_id) REFERENCES students(student_id)
                    )
                """)
                
                # Check if courses table exists
                cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_schema = 'college_system' AND table_name = 'courses'
                """)
                
                if cursor.fetchone()['COUNT(*)'] == 0:
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
                
                # Insert sample student_courses
                student_courses_data = [
                    (self.student_id, 'CS101', 'Fall 2023', 92.5, 'Present', '2023-10-10', 2, 'A'),
                    (self.student_id, 'MATH201', 'Fall 2023', 85.0, 'Late', '2023-10-09', 1, 'B+'),
                    (self.student_id, 'ENG202', 'Fall 2023', 78.5, 'Absent', '2023-10-08', 3, 'A-'),
                    (self.student_id, 'BIO301', 'Spring 2023', 90.0, 'Present', '2023-10-07', 0, 'B'),
                    (self.student_id, 'PHYS101', 'Spring 2023', 88.5, 'Present', '2023-10-06', 1, 'A+')
                ]
                
                cursor.executemany("""
                    INSERT INTO student_courses 
                    (student_id, course_code, semester, attendance_percentage, 
                     attendance_status, last_attended_date, assignments_due, grade_status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, student_courses_data)
                
                connection.commit()

            # Construct query based on selected semester
            semester = self.semester_var.get()
            query = """
                SELECT 
                    c.course_code, 
                    c.course_name, 
                    c.instructor, 
                    c.credits,
                    sc.attendance_percentage,
                    sc.assignments_due,
                    sc.grade_status,
                    sc.semester
                FROM courses c
                JOIN student_courses sc ON c.course_code = sc.course_code
                WHERE sc.student_id = %s
            """
            params = [self.student_id]

            if semester and semester != "Current Semester":
                query += " AND sc.semester = %s"
                params.append(semester)

            cursor.execute(query, params)
            courses = cursor.fetchall()

            # Clear existing course cards
            for widget in self.course_frame.winfo_children():
                widget.destroy()

            # Create course cards
            if not courses:
                no_courses_label = ctk.CTkLabel(
                    self.course_frame,
                    text="No courses found for the selected semester",
                    font=("Arial", 14),
                    text_color="gray"
                )
                no_courses_label.place(relx=0.5, rely=0.5, anchor="center")
                return

            # Create course cards
            x_position = 10
            y_position = 10
            for course in courses:
                card = ctk.CTkFrame(
                    self.course_frame, 
                    width=260, 
                    height=180, 
                    fg_color="white", 
                    border_width=1, 
                    border_color="#D9DBFF",
                    corner_radius=10
                )
                card.place(x=x_position, y=y_position)
               
                # Course name with color bar at top
                color_bar = ctk.CTkFrame(
                    card,
                    width=260,
                    height=6,
                    fg_color="#3B82F6",
                    corner_radius=0
                )
                color_bar.place(x=0, y=0)
               
                # Course name (truncate if too long)
                course_name = course['course_name']
                if len(course_name) > 25:
                    course_name = course_name[:22] + "..."
                
                ctk.CTkLabel(
                    card, 
                    text=course_name, 
                    font=("Arial", 14, "bold"), 
                    text_color="black"
                ).place(x=15, y=15)
                
                # Course code
                ctk.CTkLabel(
                    card,
                    text=course['course_code'],
                    font=("Arial", 12),
                    text_color="#666666"
                ).place(x=15, y=40)
               
                # Course details
                details = (
                    f"Instructor: {course['instructor']}\n"
                    f"Credits: {course['credits']}\n"
                    f"Attendance: {course['attendance_percentage']}%\n"
                    f"Assignments Due: {course['assignments_due']}\n"
                    f"Grade: {course['grade_status']}"
                )
                ctk.CTkLabel(
                    card, 
                    text=details, 
                    font=("Arial", 12), 
                    text_color="black", 
                    justify="left"
                ).place(x=15, y=65)

                # View Details Button
                view_button = ctk.CTkButton(
                    card, 
                    text="View Details", 
                    font=("Arial", 12), 
                    fg_color="#3B82F6", 
                    text_color="white",
                    width=120, 
                    height=30, 
                    corner_radius=5,
                    command=lambda c=course: self.show_course_details(c)
                )
                view_button.place(x=70, y=140)
                
                # Update positions
                x_position += 280
                if x_position > 800:
                    x_position = 10
                    y_position += 200

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def filter_courses(self, *args):
        """Filter courses based on selected semester"""
        self.fetch_courses()

    def show_course_details(self, course):
        """Display detailed course information"""
        # Create a popup window with course details
        details_window = ctk.CTkToplevel(self.parent_frame)
        details_window.title(f"Course Details: {course['course_code']}")
        details_window.geometry("500x400")
        details_window.resizable(False, False)
        
        # Course name header
        ctk.CTkLabel(
            details_window,
            text=course['course_name'],
            font=("Arial", 18, "bold"),
            text_color="#3B82F6"
        ).pack(pady=(20, 5))
        
        # Course code
        ctk.CTkLabel(
            details_window,
            text=course['course_code'],
            font=("Arial", 14),
            text_color="#666666"
        ).pack(pady=(0, 10))
        
        # Details frame
        details_frame = ctk.CTkFrame(
            details_window,
            fg_color="white",
            border_width=1,
            border_color="#D9DBFF",
            corner_radius=10,
            width=400,
            height=250
        )
        details_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Course details
        info = [
            ("Instructor", course['instructor']),
            ("Department", course.get('department', "Not specified")),
            ("Credits", str(course['credits'])),
            ("Semester", course['semester']),
            ("Attendance", f"{course['attendance_percentage']}%"),
            ("Assignments Due", str(course['assignments_due'])),
            ("Grade Status", course['grade_status'])
        ]
        
        y_pos = 20
        for label, value in info:
            # Label
            ctk.CTkLabel(
                details_frame,
                text=f"{label}:",
                font=("Arial", 14, "bold"),
                text_color="black",
                anchor="w"
            ).place(x=30, y=y_pos)
            
            # Value
            ctk.CTkLabel(
                details_frame,
                text=value,
                font=("Arial", 14),
                text_color="#333333",
                anchor="w"
            ).place(x=180, y=y_pos)
            
            y_pos += 30
        
        # Close button
        ctk.CTkButton(
            details_window,
            text="Close",
            font=("Arial", 14),
            fg_color="#3B82F6",
            text_color="white",
            width=120,
            height=35,
            corner_radius=5,
            command=details_window.destroy
        ).pack(pady=(10, 20))

# This allows the module to be run directly for testing
def main():
    root = ctk.CTk()
    root.title("Course Management")
    root.geometry("1200x700")
    
    main_frame = ctk.CTkFrame(root, fg_color="white")
    main_frame.pack(fill='both', expand=True)
    
    app = CourseManagementSystem(main_frame, student_id=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()