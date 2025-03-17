import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Student Fee Payment")
root.geometry("1100x600")
root.configure(bg="#F5F5F5")  # Light Gray Background

# ---------------- Left Sidebar ---------------- #
sidebar = tk.Frame(root, bg="#5A67D8", width=250, height=600)
sidebar.place(x=0, y=0)

tk.Label(sidebar, text="👤 Student", font=("Arial", 16, "bold"), fg="white", bg="#5A67D8").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Course Management", "Attendance Tracking", "Exams and Grade",
                "Fee Payment", "Fee Breakdown", "Pending Payments", "Transaction History", "Make Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_bg = "#D9DBFF" if option == "Fee Payment" else "#5A67D8"
    btn_fg = "black" if option == "Fee Payment" else "white"
    tk.Button(sidebar, text=option, font=("Arial", 11), fg=btn_fg, bg=btn_bg, bd=0, anchor="w", width=28,
              relief="flat").place(x=10, y=y_position)
    y_position += 35

# ---------------- Download Invoice Button ---------------- #
download_btn = tk.Button(root, text="Download Invoice", font=("Arial", 11), fg="white", bg="#3B82F6",
                         relief="flat", width=18)
download_btn.place(x=280, y=20)

# ---------------- Fee Breakdown Section ---------------- #
fee_breakdown_frame = tk.Frame(root, bg="white", width=400, height=150, relief="solid", bd=1)
fee_breakdown_frame.place(x=280, y=80)

tk.Label(fee_breakdown_frame, text="Fee Breakdown", font=("Arial", 12, "bold"), fg="black", bg="white").place(x=10, y=10)

# ---------------- Due Payments Table ---------------- #
due_payments_frame = tk.Frame(root, bg="white", width=300, height=150, relief="solid", bd=1)
due_payments_frame.place(x=750, y=80)

tk.Label(due_payments_frame, text="Due Payments", font=("Arial", 12, "bold"), fg="black", bg="white").place(x=10, y=10)

# Table Structure
columns = ("Description", "Amount")
tree = ttk.Treeview(due_payments_frame, columns=columns, show="headings", height=3)
tree.place(x=10, y=40, width=280, height=100)

# Define column headings
tree.heading("Description", text="Description")
tree.heading("Amount", text="Amount")

# Sample Fee Data
fees = [
    ("Tuition Fee", "$1500"),
    ("Library Fee", "$100"),
    ("Lab Fee", "$200")
]

# Insert data into table
for fee in fees:
    tree.insert("", "end", values=fee)

# ---------------- Pay Now Button ---------------- #
pay_now_btn = tk.Button(root, text="Pay Now", font=("Arial", 12), fg="white", bg="#3B82F6",
                        relief="flat", width=12)
pay_now_btn.place(x=600, y=300)

# Run the Tkinter main loop
root.mainloop()
