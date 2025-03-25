import customtkinter as ctk
from tkinter import ttk

# Initialize CustomTkinter
ctk.set_appearance_mode("light")  # Change to "dark" for dark mode
ctk.set_default_color_theme("blue")

# Initialize main window
root = ctk.CTk()
root.title("Student Attendance Tracking")
root.geometry("1500x550")

# ---------------- Left Sidebar ---------------- #
sidebar = ctk.CTkFrame(root, width=250, height=550, fg_color="#5A67D8")
sidebar.place(x=0, y=0)

ctk.CTkLabel(sidebar, text="👤 Student", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Course Management", "Attendance Tracking", "My Attendance", 
                "Course-Wise Attendance", "Semester Reports", "Exams and Grade", "Fee Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_color = "#D9DBFF" if option == "Attendance Tracking" else "#5A67D8"
    btn_text_color = "black" if option == "Attendance Tracking" else "white"
    ctk.CTkButton(sidebar, text=option, font=("Arial", 12), fg_color=btn_color, text_color=btn_text_color,
                  width=220, height=30, corner_radius=5, hover_color="#4251CC").place(x=10, y=y_position)
    y_position += 40

# ---------------- Dropdown for Sorting ---------------- #
sort_var = ctk.StringVar(value="Sort by Attendance")
sort_dropdown = ctk.CTkComboBox(root, variable=sort_var, values=["Sort by Attendance", "Sort by Name", "Sort by Date"],
                                width=180, height=35, fg_color="white", text_color="black", dropdown_hover_color="#3B82F6")
sort_dropdown.place(x=280, y=20)

# ---------------- Attendance Table ---------------- #
columns = ("Course Name", "Attendance Percentage", "Last Attended Date", "Attendance Status")

# Create a Treeview inside a CTkFrame
table_frame = ctk.CTkFrame(root, width=1200, height=300, fg_color="white")
table_frame.place(x=280, y=80)

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
tree.pack(expand=True, fill="both", padx=10, pady=10)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=250)

# Sample attendance data
attendance_data = [
    ("Introduction to Computer Science", "92%", "2023-10-10", "Present"),
    ("Calculus II", "85%", "2023-10-09", "Late"),
    ("Advanced English", "78%", "2023-10-08", "Absent"),
    ("Biology of Organisms", "90%", "2023-10-07", "Present"),
    ("General Chemistry", "88%", "2023-10-06", "Present"),
]

# Insert data into the table with color-coded status
for item in attendance_data:
    tag = "green" if item[3] == "Present" else "orange" if item[3] == "Late" else "red"
    tree.insert("", "end", values=item, tags=(tag,))

# Define tag colors
tree.tag_configure("green", foreground="green")
tree.tag_configure("orange", foreground="orange")
tree.tag_configure("red", foreground="red")

# Run the CustomTkinter main loop
root.mainloop()
