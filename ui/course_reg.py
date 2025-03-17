import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Student Course Registration")
root.geometry("1100x600")
root.configure(bg="#F5F5F5")  # Light Gray Background

# ---------------- Left Sidebar ---------------- #
sidebar = tk.Frame(root, bg="#5A67D8", width=250, height=600)
sidebar.place(x=0, y=0)

tk.Label(sidebar, text="👤 Student", font=("Arial", 16, "bold"), fg="white", bg="#5A67D8").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Available Courses", "Registered Courses", "Previous Semesters",
                "Drop Courses", "Course Management", "Attendance Tracking", "Exams and Grade", "Fee Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_bg = "#D9DBFF" if option == "Course Registration" else "#5A67D8"
    btn_fg = "black" if option == "Course Registration" else "white"
    tk.Button(sidebar, text=option, font=("Arial", 11), fg=btn_fg, bg=btn_bg, bd=0, anchor="w", width=28, 
              relief="flat").place(x=10, y=y_position)
    y_position += 35

# ---------------- Dropdown for Selecting Semester ---------------- #
sort_var = tk.StringVar()
sort_options = ["Select Semester", "Fall 2023", "Spring 2023", "Fall 2022"]
sort_dropdown = ttk.Combobox(root, textvariable=sort_var, values=sort_options, state="readonly", width=20)
sort_dropdown.place(x=280, y=20)
sort_dropdown.set("Select Semester")  # Default selection

# ---------------- Search Bar ---------------- #
search_entry = tk.Entry(root, font=("Arial", 11), width=30, relief="solid", bd=1)
search_entry.place(x=580, y=20)
search_entry.insert(0, "Search Courses")

search_button = tk.Button(root, text="Filter", font=("Arial", 10), fg="white", bg="#3B82F6", relief="flat", width=8)
search_button.place(x=850, y=18)

# ---------------- Course Table ---------------- #
columns = ("Course Code", "Course Name", "Instructor", "Credits", "Register")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
tree.place(x=280, y=60, width=780, height=300)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")

# Sample course data
courses = [
    ("CS101", "Introduction to Computer Science", "Dr. Smith", "3"),
    ("MATH201", "Calculus II", "Prof. Johnson", "4"),
    ("ENG202", "Advanced English", "Ms. Davis", "3"),
    ("BIO301", "Biology of Organisms", "Dr. Green", "4"),
    ("CHEM101", "General Chemistry", "Dr. White", "3"),
]

# Insert data into the table
for course in courses:
    tree.insert("", "end", values=course)

# Register Button for Each Course
for i in range(len(courses)):
    register_button = tk.Button(root, text="Register", font=("Arial", 10), fg="white", bg="#3B82F6", relief="flat")
    register_button.place(x=930, y=88 + (i * 30), width=80, height=25)

# Run the Tkinter main loop
root.mainloop()
