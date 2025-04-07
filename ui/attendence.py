import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
from sidebar import Sidebar  # Import the shared sidebar component

class AttendanceTracking:
    def __init__(self, parent_frame, student_id, nav_callbacks=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.nav_callbacks = nav_callbacks
        
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create sidebar with navigation
        self.sidebar = Sidebar(self.parent_frame, active_item="attendance_tracking", nav_callbacks=self.nav_callbacks)
        
        # Create content area
        self.create_content_area()
    
    def create_content_area(self):
        # Title and top bar
        self.create_top_bar()
        
        # Attendance table
        self.create_attendance_table()
    
    def create_top_bar(self):
        # Title
        ctk.CTkLabel(
            self.parent_frame, 
            text="Attendance Tracking", 
            font=("Arial", 24, "bold"), 
            text_color="#3B82F6"
        ).place(x=280, y=20)
        
        # Sorting Dropdown
        self.sort_var = ctk.StringVar(value="Sort by Attendance")
        self.sort_dropdown = ctk.CTkComboBox(
            self.parent_frame, 
            variable=self.sort_var, 
            values=[
                "Sort by Attendance", 
                "Sort by Name", 
                "Sort by Date"
            ],
            width=180, 
            height=35, 
            fg_color="white", 
            text_color="black", 
            dropdown_hover_color="#3B82F6",
            command=self.sort_attendance
        )
        self.sort_dropdown.place(x=280, y=60)

    def create_attendance_table(self):
        # Table Frame
        self.table_frame = ctk.CTkFrame(
            self.parent_frame, 
            width=900, 
            height=550, 
            fg_color="white",
            border_width=1,
            border_color="#DDDDDD"
        )
        self.table_frame.place(x=280, y=120)

        # Create Treeview
        columns = ("Course Name", "Attendance Percentage", "Last Attended Date", "Attendance Status")
        self.tree = ttk.Treeview(
            self.table_frame, 
            columns=columns, 
            show="headings", 
            height=15
        )
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=200, anchor="center")

        # Define tag colors
        self.tree.tag_configure("green", foreground="green")
        self.tree.tag_configure("orange", foreground="orange")
        self.tree.tag_configure("red", foreground="red")

        # Fetch and display attendance data
        self.fetch_attendance_data()

    def fetch_attendance_data(self):
        """Fetch attendance data from database"""
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
                        semester VARCHAR(50),
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
                    (self.student_id, 'BIO301', 'Fall 2023', 90.0, 'Present', '2023-10-07', 0, 'B'),
                    (self.student_id, 'PHYS101', 'Fall 2023', 88.5, 'Present', '2023-10-06', 1, 'A+')
                ]
                
                cursor.executemany("""
                    INSERT INTO student_courses 
                    (student_id, course_code, semester, attendance_percentage, 
                     attendance_status, last_attended_date, assignments_due, grade_status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, student_courses_data)
                
                connection.commit()

            # Fetch attendance data
            query = """
                SELECT 
                    c.course_name, 
                    sc.attendance_percentage, 
                    sc.last_attended_date,
                    sc.attendance_status
                FROM student_courses sc
                JOIN courses c ON sc.course_code = c.course_code
                WHERE sc.student_id = %s
            """
            cursor.execute(query, (self.student_id,))
            attendance_data = cursor.fetchall()

            # Clear existing items
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Insert data into the table
            for item in attendance_data:
                # Determine tag based on attendance status
                tag = (
                    "green" if item['attendance_status'] == "Present" 
                    else "orange" if item['attendance_status'] == "Late" 
                    else "red"
                )
                
                # Format percentage and date
                percentage = f"{item['attendance_percentage']}%"
                last_date = item['last_attended_date'].strftime("%Y-%m-%d") if item['last_attended_date'] else "N/A"
                
                self.tree.insert("", "end", values=(
                    item['course_name'], 
                    percentage, 
                    last_date, 
                    item['attendance_status']
                ), tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def sort_attendance(self, *args):
        """Sort attendance based on selected criteria"""
        sort_type = self.sort_var.get()
        
        # Fetch new data with sorting
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor(dictionary=True)

            # Construct query based on sort type
            query = """
                SELECT 
                    c.course_name, 
                    sc.attendance_percentage, 
                    sc.last_attended_date,
                    sc.attendance_status
                FROM student_courses sc
                JOIN courses c ON sc.course_code = c.course_code
                WHERE sc.student_id = %s
            """
            
            # Add ORDER BY clause based on sort type
            if sort_type == "Sort by Name":
                query += " ORDER BY c.course_name"
            elif sort_type == "Sort by Attendance":
                query += " ORDER BY sc.attendance_percentage DESC"
            elif sort_type == "Sort by Date":
                query += " ORDER BY sc.last_attended_date DESC"

            cursor.execute(query, (self.student_id,))
            attendance_data = cursor.fetchall()

            # Clear existing items
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Insert sorted data
            for item in attendance_data:
                # Determine tag based on attendance status
                tag = (
                    "green" if item['attendance_status'] == "Present" 
                    else "orange" if item['attendance_status'] == "Late" 
                    else "red"
                )
                
                # Format percentage and date
                percentage = f"{item['attendance_percentage']}%"
                last_date = item['last_attended_date'].strftime("%Y-%m-%d") if item['last_attended_date'] else "N/A"
                
                self.tree.insert("", "end", values=(
                    item['course_name'], 
                    percentage, 
                    last_date, 
                    item['attendance_status']
                ), tags=(tag,))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def sort_column(self, col, reverse):
        """Sort table by clicking column headers"""
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        try:
            # For numeric sorting of percentage
            if col == "Attendance Percentage":
                l.sort(key=lambda t: float(t[0].rstrip('%')), reverse=reverse)
            else:
                l.sort(reverse=reverse)
        except ValueError:
            # Fallback for non-numeric sorting
            l.sort(reverse=reverse)

        # Rearrange items
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        
        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

# This allows the module to be run directly for testing
def main():
    root = ctk.CTk()
    root.title("Attendance Tracking")
    root.geometry("1200x700")
    
    main_frame = ctk.CTkFrame(root, fg_color="white")
    main_frame.pack(fill='both', expand=True)
    
    app = AttendanceTracking(main_frame, student_id=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()