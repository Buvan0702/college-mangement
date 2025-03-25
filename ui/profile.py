import customtkinter as ctk

# Initialize main window
ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Student Profile")
root.geometry("1000x550")

# ---------------- Sidebar (Left Panel) ---------------- #
sidebar = ctk.CTkFrame(root, fg_color="#4C6EF5", width=200, height=500, corner_radius=0)
sidebar.place(x=0, y=0)

# Sidebar Title
title_label = ctk.CTkLabel(sidebar, text="📚 Student", font=("Arial", 14, "bold"), text_color="white")
title_label.place(x=20, y=20)

# Sidebar Buttons with Hover Effects
menu_items = [
    "Course Registration", "Course Management", "Attendance Tracking",
    "Exams and Grades", "Fee Payment", "Profile"
]

y_pos = 60
for item in menu_items:
    button = ctk.CTkButton(sidebar, text=item, font=("Arial", 10), fg_color="transparent", text_color="white",
                           hover_color="#354DBC", corner_radius=5, width=160, height=30)
    button.place(x=20, y=y_pos)
    y_pos += 40

# Highlighted Active Section
profile_button = ctk.CTkButton(sidebar, text="Profile", font=("Arial", 10, "bold"), fg_color="white", 
                               text_color="black", hover_color="white", corner_radius=5, width=160, height=30)
profile_button.place(x=20, y=260)

# ---------------- Profile Section (Right Panel) ---------------- #
profile_frame = ctk.CTkFrame(root, fg_color="white", width=700, height=500)
profile_frame.place(x=200, y=0)

# Profile Picture Placeholder (Rounded Look)
profile_pic = ctk.CTkLabel(profile_frame, text="👤", font=("Arial", 40), fg_color="#E5E7EB", width=80, height=80, corner_radius=40)
profile_pic.place(x=20, y=20)

# Student Name & Details
student_name = ctk.CTkLabel(profile_frame, text="John Doe", font=("Arial", 14, "bold"), text_color="black")
student_name.place(x=180, y=20)

student_details = ctk.CTkLabel(profile_frame, text="Masters in Computer Science\nCurrent Semester: Fall 2023",
                               font=("Arial", 10), text_color="gray", justify="left")
student_details.place(x=180, y=50)

# Enrolled Courses
courses_label = ctk.CTkLabel(profile_frame, text="Enrolled Courses", font=("Arial", 12, "bold"), text_color="black")
courses_label.place(x=20, y=100)

courses_text = "CS101 - Introduction to Computer Science\nMATH201 - Calculus II\nENG202 - Advanced English"
enrolled_courses = ctk.CTkLabel(profile_frame, text=courses_text, font=("Arial", 10), text_color="black", justify="left")
enrolled_courses.place(x=20, y=130)

# GPA Trend Placeholder
gpa_label = ctk.CTkLabel(profile_frame, text="GPA Trend", font=("Arial", 12, "bold"), text_color="black")
gpa_label.place(x=20, y=180)

gpa_placeholder = ctk.CTkLabel(profile_frame, text="📊 GPA Trend Graph Placeholder", font=("Arial", 10),
                               fg_color="#E5E7EB", width=500, height=80, corner_radius=10)
gpa_placeholder.place(x=20, y=210)

# Personal Information
personal_info_label = ctk.CTkLabel(profile_frame, text="Personal Information", font=("Arial", 12, "bold"), text_color="black")
personal_info_label.place(x=20, y=310)

email_label = ctk.CTkLabel(profile_frame, text="📧 Email: john.doe@example.com", font=("Arial", 10), text_color="gray")
email_label.place(x=20, y=340)

phone_label = ctk.CTkLabel(profile_frame, text="📞 Phone: (123) 456-7890", font=("Arial", 10), text_color="gray")
phone_label.place(x=20, y=360)

# Edit Profile Button
edit_profile_btn = ctk.CTkButton(profile_frame, text="Edit Profile", font=("Arial", 10), fg_color="#3B82F6", 
                                 text_color="white", corner_radius=10, width=120)
edit_profile_btn.place(x=20, y=400)

# Logout Button
logout_btn = ctk.CTkButton(profile_frame, text="Logout", font=("Arial", 10), fg_color="#FF5733", 
                            text_color="white", corner_radius=10, width=120)
logout_btn.place(x=550, y=20)

# Run the Tkinter main loop
root.mainloop()
