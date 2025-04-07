import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import hashlib
import traceback
import sys

# Import the login page and sidebar
from login import LoginPage
from sidebar import Sidebar

class DatabaseSetup:
    @staticmethod
    def create_database():
        """Create the database and all necessary tables"""
        try:
            # Establish connection to MySQL server
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password"
            )
            cursor = connection.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS college_system")
            cursor.execute("USE college_system")

            # Create tables
            # Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                user_type ENUM('student', 'admin', 'faculty') DEFAULT 'student',
                is_active BOOLEAN DEFAULT TRUE
            )
            """)

            # Students table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20),
                program VARCHAR(100),
                semester VARCHAR(50),
                gpa DECIMAL(3,2),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """)

            # Sample data tables
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_code VARCHAR(10) PRIMARY KEY,
                course_name VARCHAR(100) NOT NULL,
                department VARCHAR(50),
                credits INT,
                instructor VARCHAR(100)
            )
            """)

            # Insert sample data
            def hash_password(password):
                return hashlib.sha256(password.encode()).hexdigest()

            # Insert sample users
            cursor.execute("""
            INSERT IGNORE INTO users (user_id, email, password, user_type) VALUES
            (1, 'john.doe@example.com', %s, 'student')
            """, (hash_password('password123'),))

            # Insert sample students
            cursor.execute("""
            INSERT IGNORE INTO students 
            (student_id, user_id, name, email, phone, program, semester, gpa) VALUES
            (1, 1, 'John Doe', 'john.doe@example.com', '(123) 456-7890', 
             'Masters in Computer Science', 'Fall 2023', 3.85)
            """)

            # Commit changes
            connection.commit()
            print("Database setup completed successfully!")

        except mysql.connector.Error as err:
            print(f"Error in database setup: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class StudentManagementSystem:
    def __init__(self):
        # Initialize the main application
        self.root = ctk.CTk()
        self.root.title("Student Management System")
        self.root.geometry("1200x700")
        
        # Current active screen
        self.current_screen = None
        self.student_id = None

        # Setup database
        DatabaseSetup.create_database()

        # Define navigation callbacks
        self.nav_callbacks = {
            'dashboard': self.show_dashboard,
            'course_registration': self.show_course_registration,
            'course_management': self.show_course_management,
            'attendance_tracking': self.show_attendance_tracking,
            'exams_grades': self.show_exams_grades,
            'fee_payment': self.show_fee_payment,
            'profile': self.show_profile,
            'logout': self.logout
        }

        # Start with login screen
        self.show_login_screen()

    def clear_screen(self):
        """Clear the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Display the login screen."""
        print("Showing login screen...")
        self.clear_screen()
        
        # Initialize the login page
        self.current_screen = LoginPage(self.root, self.handle_login)

    def handle_login(self, student_id):
        """Handle successful login and open dashboard."""
        try:
            print(f"Login successful! Received student_id: {student_id}")
            self.student_id = student_id
            
            # Show the dashboard
            self.show_dashboard()
            
        except Exception as e:
            print(f"Error in handle_login: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Error", f"Failed to load dashboard: {str(e)}")
            # Restart login screen as fallback
            self.show_login_screen()

    def show_dashboard(self):
        """Display the student dashboard."""
        try:
            print("Loading dashboard...")
            self.clear_screen()
            
            # Create main frame
            main_frame = ctk.CTkFrame(self.root, fg_color="white")
            main_frame.pack(fill='both', expand=True)
            
            # Create sidebar with navigation
            sidebar = Sidebar(main_frame, active_item="dashboard", nav_callbacks=self.nav_callbacks)
            
            # Dashboard content area
            content_frame = ctk.CTkFrame(main_frame, fg_color="white")
            content_frame.place(x=250, y=0, relwidth=0.8, relheight=1)
            
            # Welcome header
            ctk.CTkLabel(
                content_frame,
                text="Welcome to Student Dashboard",
                font=("Arial", 24, "bold"),
                text_color="#3B82F6"
            ).place(x=20, y=20)
            
            # Fetch student name from database
            student_name = self.get_student_name(self.student_id)
            ctk.CTkLabel(
                content_frame,
                text=f"Hello, {student_name}!",
                font=("Arial", 16),
                text_color="#333333"
            ).place(x=20, y=60)
            
            # Quick stats
            self.create_stat_cards(content_frame)
            
            print("Dashboard loaded successfully")
            
        except Exception as e:
            print(f"Error loading dashboard: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Navigation Error", f"Failed to load dashboard: {str(e)}")
    
    def create_stat_cards(self, parent_frame):
        """Create dashboard stat cards."""
        cards_data = [
            ("Current GPA", "3.85", "#4CAF50"),
            ("Courses Enrolled", "5", "#2196F3"),
            ("Pending Assignments", "3", "#FF9800"),
            ("Fee Due", "$1,800", "#F44336")
        ]
        
        # Place cards
        for i, (title, value, color) in enumerate(cards_data):
            x_pos = 20 + (i % 2) * 250
            y_pos = 120 + (i // 2) * 140
            
            card = ctk.CTkFrame(
                parent_frame,
                width=220,
                height=120,
                corner_radius=10,
                fg_color="white",
                border_width=1,
                border_color="#DDDDDD"
            )
            card.place(x=x_pos, y=y_pos)
            
            ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 14),
                text_color="#666666"
            ).place(x=15, y=15)
            
            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 28, "bold"),
                text_color=color
            ).place(x=15, y=50)
    
    def get_student_name(self, student_id):
        """Fetch student name from database."""
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor()
            cursor.execute(
                "SELECT name FROM students WHERE student_id = %s",
                (student_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else "Student"
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return "Student"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def show_module(self, module_name, class_name, active_item):
        """Generic method to show any module with proper navigation."""
        try:
            print(f"Loading {module_name} module...")
            self.clear_screen()
            
            # Create main frame
            main_frame = ctk.CTkFrame(self.root, fg_color="white")
            main_frame.pack(fill='both', expand=True)
            
            # Create sidebar with navigation
            sidebar = Sidebar(main_frame, active_item=active_item, nav_callbacks=self.nav_callbacks)
            
            # Load the actual module - dynamic import
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            
            # Initialize with main_frame and student_id
            # We'll modify each module to accept these parameters
            module_instance = class_(main_frame, self.student_id)
            
            print(f"{module_name} loaded successfully")
            
        except Exception as e:
            print(f"Error loading {module_name}: {e}")
            print(traceback.format_exc())
            messagebox.showerror("Navigation Error", f"Failed to load {module_name}: {str(e)}")
            # Return to dashboard as fallback
            self.show_dashboard()
    
    def show_course_registration(self):
        """Show course registration screen."""
        self.show_module("course_reg", "CourseRegistrationSystem", "course_registration")
    
    def show_course_management(self):
        """Show course management screen."""
        self.show_module("course_man", "CourseManagementSystem", "course_management")
    
    def show_attendance_tracking(self):
        """Show attendance tracking screen."""
        self.show_module("attendence", "AttendanceTracking", "attendance_tracking")
    
    def show_exams_grades(self):
        """Show exams and grades screen."""
        messagebox.showinfo("Coming Soon", "Exams & Grades module is under development.")
        self.show_dashboard()
    
    def show_fee_payment(self):
        """Show fee payment screen."""
        self.show_module("fee", "FeePaymentSystem", "fee_payment")
    
    def show_profile(self):
        """Show profile screen."""
        self.show_module("profile", "StudentProfile", "profile")
    
    def logout(self):
        """Handle logout."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.student_id = None
            self.show_login_screen()

    def run(self):
        """Run the main application."""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error in mainloop: {e}")
            print(traceback.format_exc())

def main():
    """Main entry point for the application."""
    app = StudentManagementSystem()
    app.run()

if __name__ == "__main__":
    main()