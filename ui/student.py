import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Student Dashboard")
root.geometry("1000x600")
root.configure(bg="white")

# ---------------- Sidebar (Left Panel) ---------------- #
sidebar = tk.Frame(root, bg="#4C6EF5", width=200, height=600)
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

# ---------------- Top Bar ---------------- #
top_bar = tk.Frame(root, bg="white", height=50)
top_bar.place(x=200, y=0, width=800)

# Search Bar
search_entry = tk.Entry(top_bar, font=("Arial", 10), fg="gray", bd=1, relief="solid")
search_entry.insert(0, " Search...")
search_entry.place(x=10, y=10, width=200, height=30)

# Notification Icon
notif_icon = tk.Label(top_bar, text="🔔", font=("Arial", 12), bg="white")
notif_icon.place(x=230, y=10)

# Profile Icon
profile_icon = tk.Label(top_bar, text="⚪", font=("Arial", 12), bg="white")
profile_icon.place(x=270, y=10)

# ---------------- Dashboard Cards ---------------- #
card_frame = tk.Frame(root, bg="white")
card_frame.place(x=220, y=80)

# Dashboard Cards Data
cards = [
    ("Current GPA", "3.85"),
    ("Upcoming Deadlines", "3"),
    ("Course Registration Status", "Open"),
    ("Fee Dues", "$1500")
]

x_offset = 0
for title, value in cards:
    card = tk.Frame(card_frame, bg="white", width=180, height=100, bd=1, relief="solid")
    card.place(x=x_offset, y=0)
    
    title_label = tk.Label(card, text=title, font=("Arial", 10, "bold"), bg="white")
    title_label.place(x=10, y=10)
    
    value_label = tk.Label(card, text=value, font=("Arial", 14), fg="blue", bg="white")
    value_label.place(x=10, y=40)
    
    x_offset += 190  # Space between cards

# Run Tkinter main loop
root.mainloop()
