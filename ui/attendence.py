import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Student Attendance Tracking")
root.geometry("1500x550")
root.configure(bg="#F5F5F5")  # Light Gray Background

# ---------------- Left Sidebar ---------------- #
sidebar = tk.Frame(root, bg="#5A67D8", width=250, height=550)
sidebar.place(x=0, y=0)

tk.Label(sidebar, text="👤 Student", font=("Arial", 16, "bold"), fg="white", bg="#5A67D8").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Course Management", "Attendance Tracking", "My Attendance", 
                "Course-Wise Attendance", "Semester Reports", "Exams and Grade", "Fee Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_bg = "#D9DBFF" if option == "Attendance Tracking" else "#5A67D8"
    btn_fg = "black" if option == "Attendance Tracking" else "white"
    tk.Button(sidebar, text=option, font=("Arial", 11), fg=btn_fg, bg=btn_bg, bd=0, anchor="w", width=28, 
              relief="flat").place(x=10, y=y_position)
    y_position += 35

# ---------------- Dropdown for Sorting ---------------- #
sort_var = tk.StringVar()
sort_options = ["Sort by Attendance", "Sort by Name", "Sort by Date"]
sort_dropdown = ttk.Combobox(root, textvariable=sort_var, values=sort_options, state="readonly", width=20)
sort_dropdown.place(x=280, y=20)
sort_dropdown.set("Sort by Attendance")  # Default selection

# ---------------- Attendance Table ---------------- #
columns = ("Course Name", "Attendance Percentage", "Last Attended Date", "Attendance Status")

tree = ttk.Treeview(root, columns=columns, show="headings", height=6)
tree.place(x=280, y=80)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

# Sample data (with colors for different attendance status)
attendance_data = [
    ("Introduction to Computer Science", "92%", "2023-10-10", "Present"),
    ("Calculus II", "85%", "2023-10-09", "Late"),
    ("Advanced English", "78%", "2023-10-08", "Absent"),
    ("Biology of Organisms", "90%", "2023-10-07", "Present"),
    ("General Chemistry", "88%", "2023-10-06", "Present"),
]

# Insert data into the table
for item in attendance_data:
    tag = "green" if item[3] == "Present" else "orange" if item[3] == "Late" else "red"
    tree.insert("", "end", values=item, tags=(tag,))

# Define tag colors
tree.tag_configure("green", foreground="green")
tree.tag_configure("orange", foreground="orange")
tree.tag_configure("red", foreground="red")

# Run the Tkinter main loop
root.mainloop()
