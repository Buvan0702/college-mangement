import tkinter as tk
from tkinter import Frame, Label, Button

# Initialize main window
root = tk.Tk()
root.title("Reports & Analytics Dashboard")
root.geometry("1500x700")
root.configure(bg="#0F111A")  # Dark background

# ---------------- Left Sidebar ---------------- #
sidebar = Frame(root, bg="#4A5FC1", width=250, height=600)
sidebar.place(x=0, y=0)

Label(sidebar, text="Reports & Analytics", font=("Arial", 14, "bold"), fg="white", bg="#4A5FC1").place(x=20, y=20)

# Sidebar Options
menu_options = ["Student Reports", "Attendance Analytics", "Financial Reports", "Performance Tracking"]
y_position = 60

for option in menu_options:
    Label(sidebar, text=option, font=("Arial", 12), fg="#C0C0C0", bg="#4A5FC1").place(x=20, y=y_position)
    y_position += 30

# ---------------- Top Menu ---------------- #
Label(root, text="Export Report", font=("Arial", 12), fg="white", bg="#0F111A").place(x=300, y=20)
Label(root, text="Print Report", font=("Arial", 12), fg="white", bg="#0F111A").place(x=450, y=20)

# ---------------- Report Cards ---------------- #
card_bg = "#1A1D2A"
card_width = 300
card_height = 200
x_positions = [270, 600, 930]
titles = ["Semester-wise Student Report", "Attendance Trends", "Fee Collection Statistics"]

for i in range(3):
    card = Frame(root, bg=card_bg, width=card_width, height=card_height)
    card.place(x=x_positions[i], y=80)

    Label(card, text=titles[i], font=("Arial", 12, "bold"), fg="white", bg=card_bg).place(x=10, y=10)
    Label(card, text="(Report Data Placeholder)", font=("Arial", 10), fg="grey", bg=card_bg).place(x=60, y=90)

# Run the Tkinter main loop
root.mainloop()
