import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Student Course Management")
root.geometry("1100x600")
root.configure(bg="#F5F5F5")  # Light Gray Background

# ---------------- Left Sidebar ---------------- #
sidebar = tk.Frame(root, bg="#5A67D8", width=250, height=600)
sidebar.place(x=0, y=0)

tk.Label(sidebar, text="👤 Student", font=("Arial", 16, "bold"), fg="white", bg="#5A67D8").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Course Management", "Current Semester", "Previous Semesters",
                "Course Materials", "Assignments", "Attendance Tracking", "Exams and Grade", "Fee Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_bg = "#D9DBFF" if option == "Course Management" else "#5A67D8"
    btn_fg = "black" if option == "Course Management" else "white"
    tk.Button(sidebar, text=option, font=("Arial", 11), fg=btn_fg, bg=btn_bg, bd=0, anchor="w", width=28, 
              relief="flat").place(x=10, y=y_position)
    y_position += 35

# ---------------- Dropdown for Selecting Semester ---------------- #
sort_var = tk.StringVar()
sort_options = ["Select Semester", "Fall 2023", "Spring 2023", "Fall 2022"]
sort_dropdown = ttk.Combobox(root, textvariable=sort_var, values=sort_options, state="readonly", width=20)
sort_dropdown.place(x=280, y=20)
sort_dropdown.set("Select Semester")  # Default selection

# ---------------- Course Cards ---------------- #
courses = [
    ("Data Structures", "Dr. Smith", "3", "85%", "2", "A"),
    ("Operating Systems", "Prof. Johnson", "4", "90%", "1", "B+"),
    ("Database Management", "Ms. Davis", "3", "80%", "3", "A-"),
    ("Software Engineering", "Dr. Green", "4", "95%", "2", "B"),
    ("Web Development", "Dr. White", "3", "88%", "4", "A+")
]

x_position = 280
y_position = 60

for course in courses:
    frame = tk.Frame(root, bg="white", width=200, height=140, highlightbackground="#D9DBFF", highlightthickness=1)
    frame.place(x=x_position, y=y_position)
    
    title = tk.Label(frame, text=course[0], font=("Arial", 10, "bold"), bg="white")
    title.place(x=10, y=5)
    
    details = f"Instructor: {course[1]}\nCredits: {course[2]}\nAttendance: {course[3]}\nAssignments Due: {course[4]}\nGrade Status: {course[5]}"
    label = tk.Label(frame, text=details, font=("Arial", 9), bg="white", justify="left")
    label.place(x=10, y=25)

    view_button = tk.Button(frame, text="View Details", font=("Arial", 9), fg="white", bg="#3B82F6", relief="flat")
    view_button.place(x=40, y=100, width=120, height=25)

    x_position += 220
    if x_position > 800:
        x_position = 280
        y_position += 160

# Run the Tkinter main loop
root.mainloop()
