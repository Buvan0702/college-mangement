import customtkinter as ctk
from tkinter import ttk

# Initialize CustomTkinter
ctk.set_appearance_mode("light")  # Change to "dark" for dark mode
ctk.set_default_color_theme("blue")

# Initialize main window
root = ctk.CTk()
root.title("Student Course Registration")
root.geometry("1100x600")

# ---------------- Left Sidebar ---------------- #
sidebar = ctk.CTkFrame(root, width=250, height=600, fg_color="#5A67D8")
sidebar.place(x=0, y=0)

ctk.CTkLabel(sidebar, text="👤 Student", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Available Courses", "Registered Courses", "Previous Semesters",
                "Drop Courses", "Course Management", "Attendance Tracking", "Exams and Grade", "Fee Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_color = "#D9DBFF" if option == "Course Registration" else "#5A67D8"
    btn_text_color = "black" if option == "Course Registration" else "white"
    ctk.CTkButton(sidebar, text=option, font=("Arial", 12), fg_color=btn_color, text_color=btn_text_color,
                  width=220, height=30, corner_radius=5, hover_color="#4251CC").place(x=10, y=y_position)
    y_position += 40

# ---------------- Dropdown for Selecting Semester ---------------- #
sort_var = ctk.StringVar(value="Select Semester")
sort_dropdown = ctk.CTkComboBox(root, variable=sort_var, values=["Select Semester", "Fall 2023", "Spring 2023", "Fall 2022"],
                                width=180, height=35, fg_color="white", text_color="black", dropdown_hover_color="#3B82F6")
sort_dropdown.place(x=280, y=20)

# ---------------- Search Bar ---------------- #
search_entry = ctk.CTkEntry(root, placeholder_text="Search Courses", width=250, height=35, fg_color="white", text_color="black")
search_entry.place(x=500, y=20)

search_button = ctk.CTkButton(root, text="Filter", font=("Arial", 12), fg_color="#3B82F6", text_color="white", width=80, height=35)
search_button.place(x=770, y=20)

# ---------------- Course Table ---------------- #
table_frame = ctk.CTkFrame(root, width=780, height=300, fg_color="white", border_width=1)
table_frame.place(x=280, y=60)

columns = ("Course Code", "Course Name", "Instructor", "Credits")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
tree.place(x=10, y=10, width=750, height=250)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=180, anchor="center")

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

# ---------------- Register Buttons ---------------- #
y_offset = 90
for _ in courses:
    register_button = ctk.CTkButton(root, text="Register", font=("Arial", 12), fg_color="#3B82F6",
                                    text_color="white", width=100, height=30, corner_radius=5)
    register_button.place(x=930, y=y_offset)
    y_offset += 30

# Run the CustomTkinter main loop
root.mainloop()
