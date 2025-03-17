import tkinter as tk
from tkinter import ttk

# Initialize main window
root = tk.Tk()
root.title("Login Page")
root.geometry("1000x550")
root.configure(bg="#4C00FF")  # Set background to match the blue-purple gradient

# ---------------- Left Side (Illustration Placeholder) ---------------- #
canvas = tk.Canvas(root, bg="#4C00FF", width=500, height=550, highlightthickness=0)
canvas.place(x=0, y=0)

# Illustration Placeholder
canvas.create_rectangle(50, 150, 450, 450, fill="#3A0CA3", outline="white")  # Placeholder for the image
canvas.create_text(250, 300, text="Illustration Here", font=("Arial", 16, "bold"), fill="white")

# ---------------- Right Side (Login Form) ---------------- #
form_frame = tk.Frame(root, bg="white", width=400, height=400, relief="solid", bd=1)
form_frame.place(x=550, y=75)

# Profile Icon
profile_icon = tk.Label(form_frame, text="👤", font=("Arial", 24), bg="white")
profile_icon.place(x=180, y=20)

# Login Title
title_label = tk.Label(form_frame, text="Login to Your Account", font=("Arial", 14, "bold"), bg="white")
title_label.place(x=100, y=60)

# Email Label & Entry
email_label = tk.Label(form_frame, text="Email", font=("Arial", 10), bg="white")
email_label.place(x=50, y=100)
email_entry = ttk.Entry(form_frame, width=40)
email_entry.place(x=50, y=120)

# Password Label & Entry
password_label = tk.Label(form_frame, text="Password", font=("Arial", 10), bg="white")
password_label.place(x=50, y=160)
password_entry = ttk.Entry(form_frame, width=40, show="*")
password_entry.place(x=50, y=180)

# Remember Me Checkbox
remember_me = tk.Checkbutton(form_frame, text="Remember Me", bg="white", font=("Arial", 9))
remember_me.place(x=50, y=210)

# Login Button
login_btn = tk.Button(form_frame, text="Login", font=("Arial", 11), bg="#3B82F6", fg="white", width=30, relief="flat")
login_btn.place(x=50, y=250)

# Forgot Password & Sign Up Links
forgot_pass = tk.Label(form_frame, text="Forgot Password?", font=("Arial", 9, "underline"), fg="#3B82F6", bg="white", cursor="hand2")
forgot_pass.place(x=50, y=290)

signup_link = tk.Label(form_frame, text="Sign Up", font=("Arial", 9, "underline"), fg="#3B82F6", bg="white", cursor="hand2")
signup_link.place(x=280, y=290)

# Run the Tkinter main loop
root.mainloop()
