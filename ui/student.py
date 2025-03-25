import customtkinter as ctk

# Initialize main window
ctk.set_appearance_mode("light")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Student Dashboard")
root.geometry("1000x600")

# ---------------- Sidebar (Left Panel) ---------------- #
sidebar = ctk.CTkFrame(root, fg_color="#4C6EF5", width=200, height=600, corner_radius=0)
sidebar.place(x=0, y=0)

# Sidebar Title
title_label = ctk.CTkLabel(sidebar, text="📚 Student", font=("Arial", 16, "bold"), text_color="white")
title_label.place(x=20, y=20)

# Sidebar Buttons with Hover Effects
menu_items = [
    "📜 Course Registration", "📖 Course Management", "📅 Attendance Tracking",
    "📝 Exams & Grades", "💰 Fee Payment", "👤 Profile"
]

y_pos = 60
for item in menu_items:
    button = ctk.CTkButton(sidebar, text=item, font=("Arial", 12), fg_color="transparent", text_color="white",
                           hover_color="#354DBC", corner_radius=5, width=180, height=35)
    button.place(x=10, y=y_pos)
    y_pos += 50

# ---------------- Top Bar ---------------- #
top_bar = ctk.CTkFrame(root, fg_color="white", height=50)
top_bar.place(x=200, y=0)

# Search Bar
search_entry = ctk.CTkEntry(top_bar, placeholder_text="🔍 Search...", width=250, height=30)
search_entry.place(x=10, y=10)

# Notification Icon
notif_icon = ctk.CTkLabel(top_bar, text="🔔", font=("Arial", 14))
notif_icon.place(x=280, y=10)

# Profile Icon
profile_icon = ctk.CTkLabel(top_bar, text="👤", font=("Arial", 14))
profile_icon.place(x=320, y=10)

# ---------------- Dashboard Cards ---------------- #
card_frame = ctk.CTkFrame(root, fg_color="white")
card_frame.place(x=220, y=80)

# Dashboard Cards Data
cards = [
    ("📊 Current GPA", "3.85"),
    ("⏳ Upcoming Deadlines", "3"),
    ("📖 Course Registration", "Open"),
    ("💰 Fee Dues", "$1500")
]

x_offset = 0
for title, value in cards:
    card = ctk.CTkFrame(card_frame, fg_color="white", width=220, height=100, border_width=1, corner_radius=10)
    card.place(x=x_offset, y=0)
    
    title_label = ctk.CTkLabel(card, text=title, font=("Arial", 12, "bold"), text_color="black")
    title_label.place(x=10, y=10)
    
    value_label = ctk.CTkLabel(card, text=value, font=("Arial", 16), text_color="blue")
    value_label.place(x=10, y=40)
    
    x_offset += 230  # Space between cards

# ---------------- Profile Section ---------------- #
profile_frame = ctk.CTkFrame(root, fg_color="white", width=780, height=300, corner_radius=10, border_width=1)
profile_frame.place(x=220, y=200)

# Profile Picture
profile_pic = ctk.CTkLabel(profile_frame, text="🧑‍🎓", font=("Arial", 40))
profile_pic.place(x=20, y=20)

# Student Details
student_name = ctk.CTkLabel(profile_frame, text="John Doe", font=("Arial", 16, "bold"))
student_name.place(x=100, y=20)

student_details = ctk.CTkLabel(profile_frame, text="Masters in Computer Science\nCurrent Semester: Fall 2023",
                               font=("Arial", 12), text_color="gray", justify="left")
student_details.place(x=100, y=60)

# Enrolled Courses
courses_label = ctk.CTkLabel(profile_frame, text="📚 Enrolled Courses", font=("Arial", 14, "bold"))
courses_label.place(x=20, y=120)

courses_text = "CS101 - Introduction to Computer Science\nMATH201 - Calculus II\nENG202 - Advanced English"
enrolled_courses = ctk.CTkLabel(profile_frame, text=courses_text, font=("Arial", 12), justify="left")
enrolled_courses.place(x=20, y=150)

# Edit Profile Button
edit_profile_btn = ctk.CTkButton(profile_frame, text="✏ Edit Profile", font=("Arial", 12), fg_color="#3B82F6", text_color="white")
edit_profile_btn.place(x=20, y=220)

# Logout Button
logout_btn = ctk.CTkButton(profile_frame, text="🚪 Logout", font=("Arial", 12), fg_color="red", text_color="white")
logout_btn.place(x=660, y=20)

# ---------------- Light/Dark Mode Toggle ---------------- #
def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    new_mode = "dark" if current_mode == "light" else "light"
    ctk.set_appearance_mode(new_mode)

theme_toggle_btn = ctk.CTkButton(root, text="🌗 Toggle Theme", font=("Arial", 12), fg_color="#4C6EF5", text_color="white",
                                 command=toggle_theme)
theme_toggle_btn.place(x=850, y=560)

# Run Tkinter main loop
root.mainloop()
