import customtkinter as ctk

# Initialize CustomTkinter
ctk.set_appearance_mode("light")  # Change to "dark" for dark mode
ctk.set_default_color_theme("blue")

# Initialize main window
root = ctk.CTk()
root.title("Student Course Management")
root.geometry("1100x600")

# ---------------- Left Sidebar ---------------- #
sidebar = ctk.CTkFrame(root, width=250, height=600, fg_color="#5A67D8")
sidebar.place(x=0, y=0)

ctk.CTkLabel(sidebar, text="👤 Student", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Course Management", "Current Semester", "Previous Semesters",
                "Course Materials", "Assignments", "Attendance Tracking", "Exams and Grade", "Fee Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_color = "#D9DBFF" if option == "Course Management" else "#5A67D8"
    btn_text_color = "black" if option == "Course Management" else "white"
    ctk.CTkButton(sidebar, text=option, font=("Arial", 12), fg_color=btn_color, text_color=btn_text_color,
                  width=220, height=30, corner_radius=5, hover_color="#4251CC").place(x=10, y=y_position)
    y_position += 40

# ---------------- Dropdown for Selecting Semester ---------------- #
sort_var = ctk.StringVar(value="Select Semester")
sort_dropdown = ctk.CTkComboBox(root, variable=sort_var, values=["Select Semester", "Fall 2023", "Spring 2023", "Fall 2022"],
                                width=180, height=35, fg_color="white", text_color="black", dropdown_hover_color="#3B82F6")
sort_dropdown.place(x=280, y=20)

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
    frame = ctk.CTkFrame(root, width=200, height=140, fg_color="white", border_width=1, border_color="#D9DBFF")
    frame.place(x=x_position, y=y_position)
    
    ctk.CTkLabel(frame, text=course[0], font=("Arial", 12, "bold"), text_color="black").place(x=10, y=5)
    
    details = f"Instructor: {course[1]}\nCredits: {course[2]}\nAttendance: {course[3]}\nAssignments Due: {course[4]}\nGrade Status: {course[5]}"
    ctk.CTkLabel(frame, text=details, font=("Arial", 10), text_color="black", justify="left").place(x=10, y=30)

    view_button = ctk.CTkButton(frame, text="View Details", font=("Arial", 10), fg_color="#3B82F6", text_color="white",
                                width=120, height=30, corner_radius=5)
    view_button.place(x=40, y=100)

    x_position += 220
    if x_position > 800:
        x_position = 280
        y_position += 160

# Run the CustomTkinter main loop
root.mainloop()
