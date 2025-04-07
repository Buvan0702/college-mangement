import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import hashlib
import os

class DatabaseManager:
    """Manages database connections and operations"""
    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"  # Changed to match main.py database name
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            return None

class StudentDashboard:
    def __init__(self, root, student_id, navigation_callbacks=None):
        self.root = root
        self.student_id = student_id
        self.navigation_callbacks = navigation_callbacks or {}
        self.student_data = self.fetch_student_data()

        # Configure main window
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.title("Student Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg='white')

        # Create main frame
        self.main_frame = ctk.CTkFrame(root, fg_color="white")
        self.main_frame.pack(fill='both', expand=True)

        # Sidebar
        self.create_sidebar()

        # Top bar
        self.create_topbar()

        # Dashboard cards
        self.create_dashboard_cards()

        # Profile section
        self.create_profile_section()

    def create_sidebar(self):
        # Sidebar with gradient background
        self.sidebar = ctk.CTkFrame(
            self.main_frame, 
            fg_color="#5A67D8", 
            width=250, 
            corner_radius=0
        )
        self.sidebar.place(x=0, y=0, relheight=1)

        # Sidebar title
        title_label = ctk.CTkLabel(
            self.sidebar, 
            text="📚 Student", 
            font=("Arial", 18, "bold"), 
            text_color="white"
        )
        title_label.place(x=20, y=20)

        # Menu items with navigation callbacks
        menu_items = [
            ("📜 Course Registration", "course_registration"),
            ("📖 Course Management", "course_management"),
            ("📅 Attendance Tracking", "attendance_tracking"),
            ("📝 Exams & Grades", "exams_grades"),
            ("💰 Fee Payment", "fee_payment"),
            ("👤 Profile", "profile")
        ]

        y_pos = 60
        for label, callback_key in menu_items:
            btn = ctk.CTkButton(
                self.sidebar, 
                text=label, 
                font=("Arial", 14), 
                fg_color="transparent", 
                text_color="white",
                hover_color="#4251CC", 
                corner_radius=10, 
                width=220, 
                height=40,
                command=lambda key=callback_key: self.navigate(key)
            )
            btn.place(x=10, y=y_pos)
            y_pos += 50

    def navigate(self, key):
        """Navigate to different screens based on sidebar selection"""
        navigation_map = {
            "course_registration": self.go_to_course_registration,
            "course_management": self.go_to_course_management,
            "attendance_tracking": self.go_to_attendance_tracking,
            "exams_grades": self.go_to_exams_grades,
            "fee_payment": self.go_to_fee_payment,
            "profile": self.go_to_profile
        }
        
        if key in navigation_map:
            navigation_map[key]()
    
    def go_to_course_registration(self):
        """Navigate to course registration screen"""
        if 'course_registration' in self.navigation_callbacks:
            self.navigation_callbacks['course_registration']()
        else:
            self.open_module('course_reg')
    
    def go_to_course_management(self):
        """Navigate to course management screen"""
        if 'course_management' in self.navigation_callbacks:
            self.navigation_callbacks['course_management']()
        else:
            self.open_module('course_man')
    
    def go_to_attendance_tracking(self):
        """Navigate to attendance tracking screen"""
        if 'attendance_tracking' in self.navigation_callbacks:
            self.navigation_callbacks['attendance_tracking']()
        else:
            self.open_module('attendence')
    
    def go_to_exams_grades(self):
        """Navigate to exams and grades screen"""
        if 'exams_grades' in self.navigation_callbacks:
            self.navigation_callbacks['exams_grades']()
        else:
            messagebox.showinfo("Coming Soon", "Exams & Grades module is under development.")
    
    def go_to_fee_payment(self):
        """Navigate to fee payment screen"""
        if 'fee_payment' in self.navigation_callbacks:
            self.navigation_callbacks['fee_payment']()
        else:
            self.open_module('fee')
    
    def go_to_profile(self):
        """Navigate to profile screen"""
        if 'profile' in self.navigation_callbacks:
            self.navigation_callbacks['profile']()
        else:
            self.open_module('profile')
    
    def open_module(self, module_name):
        """Helper method to open a module directly"""
        try:
            # Clear current window
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Import and initialize the module
            if module_name == 'course_reg':
                from course_reg import CourseRegistrationSystem
                CourseRegistrationSystem(self.root, self.student_id)
            elif module_name == 'course_man':
                from course_man import CourseManagementSystem
                CourseManagementSystem(self.root, self.student_id)
            elif module_name == 'attendence':
                from attendence import AttendanceTracking
                AttendanceTracking(self.root, self.student_id)
            elif module_name == 'fee':
                from fee import FeePaymentSystem
                FeePaymentSystem(self.root, self.student_id)
            elif module_name == 'profile':
                from profile import StudentProfile
                StudentProfile(self.root, self.student_id)
        except Exception as e:
            messagebox.showerror("Navigation Error", f"Could not navigate to {module_name}: {str(e)}")
            # Recreate dashboard as fallback
            StudentDashboard(self.root, self.student_id, self.navigation_callbacks)

    def create_topbar(self):
        # Top bar
        top_bar = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            height=70, 
            corner_radius=0
        )
        top_bar.place(x=250, y=0)

        # Search bar
        search_entry = ctk.CTkEntry(
            top_bar, 
            placeholder_text="🔍 Search...", 
            width=300, 
            height=40, 
            corner_radius=20
        )
        search_entry.place(x=20, y=15)

        # Notification and profile icons
        icon_frame = ctk.CTkFrame(top_bar, fg_color="white")
        icon_frame.place(x=700, y=15)

        notification_icon = ctk.CTkLabel(
            icon_frame, 
            text="🔔", 
            font=("Arial", 20), 
            text_color="gray"
        )
        notification_icon.pack(side="left", padx=10)

        profile_icon = ctk.CTkLabel(
            icon_frame, 
            text="👤", 
            font=("Arial", 20), 
            text_color="gray"
        )
        profile_icon.pack(side="left", padx=10)
        
        # Logout button
        logout_btn = ctk.CTkButton(
            icon_frame,
            text="Logout",
            font=("Arial", 12),
            fg_color="#FF5757",
            text_color="white",
            width=80,
            height=30,
            corner_radius=5,
            command=self.logout
        )
        logout_btn.pack(side="left", padx=10)

    def logout(self):
        """Handle logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if 'logout' in self.navigation_callbacks:
                self.navigation_callbacks['logout']()
            else:
                # Clear current window
                for widget in self.root.winfo_children():
                    widget.destroy()
                
                # Redirect to login
                from login import LoginPage
                LoginPage(self.root, lambda student_id: StudentDashboard(self.root, student_id))

    def create_dashboard_cards(self):
        # Cards frame
        cards_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white"
        )
        cards_frame.place(x=280, y=80)

        # Card details
        cards_data = [
            ("Current GPA", str(self.student_data.get('gpa', '3.85'))),
            ("Upcoming Deadlines", "3"),
            ("Course Registration", "Open"),
            ("Fee Dues", f"${self.student_data.get('fee_dues', '1500')}")
        ]

        # Create cards
        for i, (title, value) in enumerate(cards_data):
            card = ctk.CTkFrame(
                cards_frame, 
                fg_color="white", 
                border_width=1, 
                border_color="lightgray", 
                corner_radius=10
            )
            card.place(x=20 + i*220, y=0, width=200, height=120)

            ctk.CTkLabel(
                card, 
                text=title, 
                font=("Arial", 12), 
                text_color="gray"
            ).place(x=15, y=15)

            ctk.CTkLabel(
                card, 
                text=value, 
                font=("Arial", 18, "bold"), 
                text_color="#3B82F6"
            ).place(x=15, y=45)

    def create_profile_section(self):
        # Profile section
        profile_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color="white", 
            border_width=1, 
            border_color="lightgray", 
            corner_radius=10
        )
        profile_frame.place(x=280, y=250, width=880, height=400)

        # Profile details
        ctk.CTkLabel(
            profile_frame, 
            text="👤", 
            font=("Arial", 50)
        ).place(x=30, y=30)

        # Student name and details
        ctk.CTkLabel(
            profile_frame, 
            text=self.student_data.get('name', 'John Doe'), 
            font=("Arial", 18, "bold")
        ).place(x=150, y=40)

        ctk.CTkLabel(
            profile_frame, 
            text=f"{self.student_data.get('program', 'Masters in Computer Science')}\n"
                 f"Current Semester: {self.student_data.get('semester', 'Fall 2023')}", 
            font=("Arial", 12), 
            text_color="gray"
        ).place(x=150, y=80)

        # Enrolled courses
        ctk.CTkLabel(
            profile_frame, 
            text="📚 Enrolled Courses", 
            font=("Arial", 14, "bold")
        ).place(x=30, y=150)

        courses = self.student_data.get('courses', [
            "CS101 - Introduction to Computer Science",
            "MATH201 - Calculus II", 
            "ENG202 - Advanced English"
        ])
        
        y_pos = 190
        for course in courses:
            ctk.CTkLabel(
                profile_frame, 
                text=course, 
                font=("Arial", 12), 
                text_color="gray",
                anchor="w"
            ).place(x=30, y=y_pos)
            y_pos += 30

        # Buttons
        ctk.CTkButton(
            profile_frame, 
            text="Edit Profile", 
            font=("Arial", 12),

            fg_color="#3B82F6",
            command=self.go_to_profile
        ).place(x=30, y=330, width=150)

    def fetch_student_data(self):
        """Fetch student data from database"""
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor(dictionary=True)

            # Fetch student basic information
            cursor.execute("""
                SELECT name, email, phone, program, semester, gpa
                FROM students
                WHERE student_id = %s
            """, (self.student_id,))
            student = cursor.fetchone() or {}

            # Get total fee dues
            cursor.execute("""
                SELECT SUM(amount) as fee_dues
                FROM student_fees
                WHERE student_id = %s AND payment_status = 'Unpaid'
            """, (self.student_id,))
            fees = cursor.fetchone()
            if fees and fees['fee_dues']:
                student['fee_dues'] = fees['fee_dues']
            else:
                student['fee_dues'] = 0

            # Fetch enrolled courses
            cursor.execute("""
                SELECT CONCAT(c.course_code, ' - ', c.course_name) as course
                FROM student_courses sc
                JOIN courses c ON sc.course_code = c.course_code
                WHERE sc.student_id = %s
            """, (self.student_id,))
            courses = [course['course'] for course in cursor.fetchall()]
            
            # Combine student data
            student['courses'] = courses
            return student

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
            return {
                'name': 'John Doe',
                'program': 'Masters in Computer Science',
                'semester': 'Fall 2023',
                'gpa': 3.85,
                'fee_dues': 1800,
                'courses': [
                    "CS101 - Introduction to Computer Science",
                    "MATH201 - Calculus II", 
                    "ENG202 - Advanced English"
                ]
            }
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

def main():
    root = ctk.CTk()
    app = StudentDashboard(root, student_id=1)  # Replace with actual student ID
    root.mainloop()

if __name__ == "__main__":
    main()