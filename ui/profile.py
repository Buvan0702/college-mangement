import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Student Profile")
root.geometry("900x500")
root.configure(bg="white")

# ---------------- Sidebar (Left Panel) ---------------- #
sidebar = tk.Frame(root, bg="#4C6EF5", width=200, height=500)
sidebar.place(x=0, y=0)

# Sidebar Title
title_label = tk.Label(sidebar, text="📚 Student", font=("Arial", 14, "bold"), fg="white", bg="#4C6EF5", anchor="w")
title_label.place(x=20, y=20)

# Sidebar Buttons
menu_items = [
    "Course Registration", "Course Management", "Attendance Tracking",
    "Exams and Grade", "Fee Payment", "Profile"
]
y_pos = 60
for item in menu_items:
    button = tk.Button(sidebar, text=item, font=("Arial", 10), fg="white", bg="#4C6EF5", bd=0, anchor="w")
    button.place(x=20, y=y_pos, width=160)
    y_pos += 30

# Highlighted Active Section
profile_button = tk.Button(sidebar, text="Profile", font=("Arial", 10, "bold"), fg="black", bg="white", bd=0, anchor="w")
profile_button.place(x=20, y=240, width=160)

# ---------------- Profile Section (Right Panel) ---------------- #
profile_frame = tk.Frame(root, bg="white", width=700, height=500)
profile_frame.place(x=200, y=0)

# Profile Picture Placeholder
profile_pic = tk.Canvas(profile_frame, width=80, height=80, bg="#E5E7EB", highlightthickness=0)
profile_pic.create_text(40, 40, text="Profile Picture", font=("Arial", 8), fill="gray")
profile_pic.place(x=20, y=20)

# Student Name & Details
student_name = tk.Label(profile_frame, text="Student Name", font=("Arial", 14, "bold"), bg="white")
student_name.place(x=120, y=20)

student_details = tk.Label(profile_frame, text="Masters in Computer Science\nCurrent Semester: Fall 2023",
                           font=("Arial", 10), fg="gray", bg="white", justify="left")
student_details.place(x=120, y=50)

# Enrolled Courses
courses_label = tk.Label(profile_frame, text="Enrolled Courses", font=("Arial", 12, "bold"), bg="white")
courses_label.place(x=20, y=100)

courses_text = "CS101 - Introduction to Computer Science\nMATH201 - Calculus II\nENG202 - Advanced English"
enrolled_courses = tk.Label(profile_frame, text=courses_text, font=("Arial", 10), bg="white", justify="left")
enrolled_courses.place(x=20, y=130)

# GPA Trend Placeholder
gpa_label = tk.Label(profile_frame, text="GPA Trend", font=("Arial", 12, "bold"), bg="white")
gpa_label.place(x=20, y=180)

gpa_placeholder = tk.Canvas(profile_frame, width=500, height=80, bg="#E5E7EB", highlightthickness=0)
gpa_placeholder.create_text(250, 40, text="GPA Trend Graph Placeholder", font=("Arial", 10), fill="gray")
gpa_placeholder.place(x=20, y=210)

# Personal Information
personal_info_label = tk.Label(profile_frame, text="Personal Information", font=("Arial", 12, "bold"), bg="white")
personal_info_label.place(x=20, y=310)

email_label = tk.Label(profile_frame, text="Email: john.doe@example.com", font=("Arial", 10), bg="white", fg="gray")
email_label.place(x=20, y=340)

phone_label = tk.Label(profile_frame, text="Phone: (123) 456-7890", font=("Arial", 10), bg="white", fg="gray")
phone_label.place(x=20, y=360)

# Edit Profile Button
edit_profile_btn = tk.Button(profile_frame, text="Edit Profile", font=("Arial", 10), bg="#3B82F6", fg="white", relief="flat")
edit_profile_btn.place(x=20, y=400)

# Logout Button
logout_btn = tk.Button(profile_frame, text="Logout", font=("Arial", 10), bg="#3B82F6", fg="white", relief="flat")
logout_btn.place(x=620, y=20)

# Run the Tkinter main loop
root.mainloop()
