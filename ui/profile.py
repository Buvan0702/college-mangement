import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sidebar import Sidebar  # Import the shared sidebar component

class StudentProfile:
    def __init__(self, parent_frame, student_id, nav_callbacks=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.nav_callbacks = nav_callbacks
        
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create sidebar with navigation
        self.sidebar = Sidebar(self.parent_frame, active_item="profile", nav_callbacks=self.nav_callbacks)
        
        # Create content area
        self.create_profile_content()
    
    def create_profile_content(self):
        # Title
        ctk.CTkLabel(
            self.parent_frame, 
            text="Student Profile", 
            font=("Arial", 24, "bold"), 
            text_color="#3B82F6"
        ).place(x=280, y=20)
        
        # Fetch student profile data
        student_data = self.fetch_student_data()
        
        # Create profile sections
        self.create_profile_header(student_data)
        self.create_course_section(student_data)
        self.create_gpa_trend_graph(student_data)
        self.create_personal_info_section(student_data)
    
    def create_profile_header(self, student_data):
        # Profile picture and basic info
        profile_frame = ctk.CTkFrame(
            self.parent_frame,
            width=900,
            height=150,
            fg_color="white",
            border_width=1,
            border_color="#D9DBFF",
            corner_radius=10
        )
        profile_frame.place(x=280, y=60)
        
        # Profile Picture (placeholder)
        profile_pic = ctk.CTkLabel(
            profile_frame, 
            text="👤", 
            font=("Arial", 60), 
            text_color="#3B82F6"
        )
        profile_pic.place(x=30, y=30)

        # Student Name
        ctk.CTkLabel(
            profile_frame, 
            text=student_data.get('name', 'Student Name'), 
            font=("Arial", 20, "bold"),
            text_color="black"
        ).place(x=150, y=40)

        # Student Details
        ctk.CTkLabel(
            profile_frame, 
            text=f"{student_data.get('program', 'Masters in Computer Science')}\n"
                 f"Current Semester: {student_data.get('semester', 'Fall 2023')}", 
            font=("Arial", 14), 
            text_color="#666666"
        ).place(x=150, y=80)
        
        # Edit Profile Button
        edit_profile_btn = ctk.CTkButton(
            profile_frame, 
            text="Edit Profile", 
            font=("Arial", 14), 
            fg_color="#3B82F6",
            text_color="white", 
            width=120, 
            height=35, 
            corner_radius=5,
            command=self.edit_profile
        )
        edit_profile_btn.place(x=700, y=60)
    
    def create_course_section(self, student_data):
        # Enrolled Courses Section
        courses_frame = ctk.CTkFrame(
            self.parent_frame,
            width=420,
            height=250,
            fg_color="white",
            border_width=1,
            border_color="#D9DBFF",
            corner_radius=10
        )
        courses_frame.place(x=280, y=230)
        
        # Section Title
        ctk.CTkLabel(
            courses_frame, 
            text="Enrolled Courses", 
            font=("Arial", 16, "bold"),
            text_color="black"
        ).place(x=20, y=20)

        # Course list
        courses = student_data.get('courses', [
            "CS101 - Introduction to Computer Science",
            "MATH201 - Calculus II", 
            "ENG202 - Advanced English",
            "BIO301 - Biology",
            "PHYS101 - Physics I"
        ])

        # Create scrollable frame for courses
        course_list_frame = ctk.CTkScrollableFrame(
            courses_frame,
            width=380,
            height=180,
            fg_color="white"
        )
        course_list_frame.place(x=20, y=50)
        
        # Add courses to the list
        for i, course in enumerate(courses):
            course_frame = ctk.CTkFrame(
                course_list_frame,
                fg_color="#F5F7FF" if i % 2 == 0 else "white",
                corner_radius=5,
                height=40
            )
            course_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(
                course_frame,
                text=course,
                font=("Arial", 12),
                text_color="black",
                anchor="w"
            ).pack(side="left", padx=10, pady=8)

    def create_gpa_trend_graph(self, student_data):
        # GPA Trend Section
        gpa_frame = ctk.CTkFrame(
            self.parent_frame,
            width=420,
            height=250,
            fg_color="white",
            border_width=1,
            border_color="#D9DBFF",
            corner_radius=10
        )
        gpa_frame.place(x=720, y=230)
        
        # Section Title
        ctk.CTkLabel(
            gpa_frame, 
            text="GPA Trend", 
            font=("Arial", 16, "bold"),
            text_color="black"
        ).place(x=20, y=20)

        # Create a graph using matplotlib
        try:
            # Sample GPA trend data (replace with actual data)
            gpa_history = student_data.get('gpa_history', [
                ('Fall 2022', 3.5),
                ('Spring 2023', 3.7),
                ('Fall 2023', 3.85)
            ])
            
            semesters = [semester for semester, _ in gpa_history]
            gpa_values = [gpa for _, gpa in gpa_history]
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(4, 2.5), dpi=80)
            
            # Plot the GPA trend
            ax.plot(semesters, gpa_values, marker='o', linestyle='-', color='#3B82F6', linewidth=2, markersize=8)
            
            # Set y-axis range (common for GPA visualization)
            ax.set_ylim([2.0, 4.0])
            
            # Add labels and title
            ax.set_xlabel('Semester')
            ax.set_ylabel('GPA')
            
            # Customize grid and appearance
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Embed the plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=gpa_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.place(x=10, y=50, width=400, height=180)
            
        except Exception as e:
            print(f"Error creating GPA graph: {e}")
            # Display error message in place of graph
            ctk.CTkLabel(
                gpa_frame,
                text="Unable to display GPA trend graph",
                font=("Arial", 12),
                text_color="red"
            ).place(x=20, y=100)

    def create_personal_info_section(self, student_data):
        # Personal Information Section
        info_frame = ctk.CTkFrame(
            self.parent_frame,
            width=860,
            height=120,
            fg_color="white",
            border_width=1,
            border_color="#D9DBFF",
            corner_radius=10
        )
        info_frame.place(x=280, y=500)
        
        # Section Title
        ctk.CTkLabel(
            info_frame, 
            text="Personal Information", 
            font=("Arial", 16, "bold"),
            text_color="black"
        ).place(x=20, y=20)

        # Personal details
        details_text = (
            f"Email: {student_data.get('email', 'john.doe@example.com')}\n"
            f"Phone: {student_data.get('phone', '(123) 456-7890')}\n"
            f"Student ID: {self.student_id}"
        )
        
        ctk.CTkLabel(
            info_frame, 
            text=details_text, 
            font=("Arial", 14),
            text_color="#333333",
            justify="left"
        ).place(x=20, y=50)
        
        # Change Password Button
        change_pwd_btn = ctk.CTkButton(
            info_frame, 
            text="Change Password", 
            font=("Arial", 14), 
            fg_color="#3B82F6",
            text_color="white", 
            width=150, 
            height=35, 
            corner_radius=5,
            command=self.change_password
        )
        change_pwd_btn.place(x=680, y=40)

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
            
            # Check if student_gpa_history table exists
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'college_system' AND table_name = 'student_gpa_history'
            """)
            
            if cursor.fetchone()['COUNT(*)'] == 0:
                # Create student_gpa_history table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student_gpa_history (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        semester VARCHAR(50),
                        gpa DECIMAL(3,2),
                        FOREIGN KEY (student_id) REFERENCES students(student_id)
                    )
                """)
                
                # Insert sample GPA history
                gpa_history_data = [
                    (self.student_id, 'Fall 2022', 3.50),
                    (self.student_id, 'Spring 2023', 3.70),
                    (self.student_id, 'Fall 2023', 3.85)
                ]
                
                cursor.executemany("""
                    INSERT INTO student_gpa_history 
                    (student_id, semester, gpa) 
                    VALUES (%s, %s, %s)
                """, gpa_history_data)
                
                connection.commit()

            # Fetch GPA history
            cursor.execute("""
                SELECT semester, gpa
                FROM student_gpa_history
                WHERE student_id = %s
                ORDER BY id
            """, (self.student_id,))
            gpa_history = [(row['semester'], row['gpa']) for row in cursor.fetchall()]
            student['gpa_history'] = gpa_history

            # Fetch enrolled courses
            cursor.execute("""
                SELECT 
                    CONCAT(c.course_code, ' - ', c.course_name) as course
                FROM student_courses sc
                JOIN courses c ON sc.course_code = c.course_code
                WHERE sc.student_id = %s
            """, (self.student_id,))
            courses = [row['course'] for row in cursor.fetchall()]
            student['courses'] = courses
            
            return student

        except mysql.connector.Error as err:
            print(f"Database error in profile: {err}")
            messagebox.showerror("Database Error", str(err))
            # Return default data if database error
            return {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '(123) 456-7890',
                'program': 'Masters in Computer Science',
                'semester': 'Fall 2023',
                'gpa': 3.85,
                'courses': [
                    "CS101 - Introduction to Computer Science",
                    "MATH201 - Calculus II", 
                    "ENG202 - Advanced English",
                    "BIO301 - Biology",
                    "PHYS101 - Physics I"
                ],
                'gpa_history': [
                    ('Fall 2022', 3.5),
                    ('Spring 2023', 3.7),
                    ('Fall 2023', 3.85)
                ]
            }