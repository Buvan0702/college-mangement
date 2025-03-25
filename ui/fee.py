import customtkinter as ctk
from tkinter import ttk

# Initialize CustomTkinter
ctk.set_appearance_mode("light")  # Change to "dark" for dark mode
ctk.set_default_color_theme("blue")

# Initialize main window
root = ctk.CTk()
root.title("Student Fee Payment")
root.geometry("1100x600")

# ---------------- Left Sidebar ---------------- #
sidebar = ctk.CTkFrame(root, width=250, height=600, fg_color="#5A67D8")
sidebar.place(x=0, y=0)

ctk.CTkLabel(sidebar, text="👤 Student", font=("Arial", 18, "bold"), text_color="white").place(x=20, y=20)

# Sidebar Options
menu_options = ["Course Registration", "Course Management", "Attendance Tracking", "Exams and Grade",
                "Fee Payment", "Fee Breakdown", "Pending Payments", "Transaction History", "Make Payment", "Profile"]

y_position = 60
for option in menu_options:
    btn_color = "#D9DBFF" if option == "Fee Payment" else "#5A67D8"
    btn_text_color = "black" if option == "Fee Payment" else "white"
    ctk.CTkButton(sidebar, text=option, font=("Arial", 12), fg_color=btn_color, text_color=btn_text_color,
                  width=220, height=30, corner_radius=5, hover_color="#4251CC").place(x=10, y=y_position)
    y_position += 40

# ---------------- Download Invoice Button ---------------- #
download_btn = ctk.CTkButton(root, text="Download Invoice", font=("Arial", 12, "bold"), fg_color="#3B82F6",
                             text_color="white", width=150, height=35, corner_radius=5)
download_btn.place(x=280, y=20)

# ---------------- Fee Breakdown Section ---------------- #
fee_breakdown_frame = ctk.CTkFrame(root, width=400, height=150, fg_color="white", border_width=1)
fee_breakdown_frame.place(x=280, y=80)

ctk.CTkLabel(fee_breakdown_frame, text="Fee Breakdown", font=("Arial", 14, "bold"), text_color="black").place(x=10, y=10)

# ---------------- Due Payments Table ---------------- #
due_payments_frame = ctk.CTkFrame(root, width=300, height=150, fg_color="white", border_width=1)
due_payments_frame.place(x=750, y=80)

ctk.CTkLabel(due_payments_frame, text="Due Payments", font=("Arial", 14, "bold"), text_color="black").place(x=10, y=10)

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
pay_now_btn = ctk.CTkButton(root, text="Pay Now", font=("Arial", 14, "bold"), fg_color="#3B82F6",
                            text_color="white", width=120, height=40, corner_radius=5, hover_color="#2A62D6")
pay_now_btn.place(x=600, y=300)

# Run the CustomTkinter main loop
root.mainloop()
