import customtkinter as ctk

# Initialize main window
ctk.set_appearance_mode("light")  # Choose "dark", "light", or "system"
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Login Page")
root.geometry("1000x550")

# ---------------- Left Side (Illustration Placeholder) ---------------- #
left_frame = ctk.CTkFrame(root, fg_color="#4C00FF", width=500, height=550)
left_frame.place(x=0, y=0)

canvas = ctk.CTkCanvas(left_frame, bg="#4C00FF", width=500, height=550, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_rectangle(50, 150, 450, 450, fill="#3A0CA3", outline="white")
canvas.create_text(250, 300, text="Illustration Here", font=("Arial", 16, "bold"), fill="white")

# ---------------- Right Side (Login Form) ---------------- #
form_frame = ctk.CTkFrame(root, fg_color="white", width=400, height=400, corner_radius=15)
form_frame.place(x=550, y=75)

# Profile Icon
profile_icon = ctk.CTkLabel(form_frame, text="👤", font=("Arial", 24), text_color="black")
profile_icon.place(x=180, y=20)

# Login Title
title_label = ctk.CTkLabel(form_frame, text="Login to Your Account", font=("Arial", 14, "bold"), text_color="black")
title_label.place(x=100, y=60)

# Email Label & Entry
email_label = ctk.CTkLabel(form_frame, text="Email", font=("Arial", 10), text_color="black")
email_label.place(x=50, y=100)
email_entry = ctk.CTkEntry(form_frame, width=280, height=35, corner_radius=10)
email_entry.place(x=50, y=120)

# Password Label & Entry (with toggle button)
password_label = ctk.CTkLabel(form_frame, text="Password", font=("Arial", 10), text_color="black")
password_label.place(x=50, y=160)

password_entry = ctk.CTkEntry(form_frame, width=240, height=35, corner_radius=10, show="*")
password_entry.place(x=50, y=180)

# Toggle Password Visibility
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

toggle_btn = ctk.CTkButton(form_frame, text="👁", width=20, height=20, fg_color="transparent", text_color="black", 
                           font=("Arial", 12), command=toggle_password)
toggle_btn.place(x=300, y=185)

# Remember Me Checkbox
remember_me = ctk.CTkCheckBox(form_frame, text="Remember Me", font=("Arial", 9), text_color="black", fg_color="#3B82F6")
remember_me.place(x=50, y=220)

# Login Button
login_btn = ctk.CTkButton(form_frame, text="Login", font=("Arial", 11), fg_color="#3B82F6", text_color="white", width=280, height=35, corner_radius=10)
login_btn.place(x=50, y=260)

# Forgot Password & Sign Up Links (Clickable)
def on_forgot_password():
    print("Redirect to Forgot Password Page")

def on_signup():
    print("Redirect to Sign Up Page")

forgot_pass = ctk.CTkLabel(form_frame, text="Forgot Password?", font=("Arial", 9, "underline"), text_color="#3B82F6", cursor="hand2")
forgot_pass.place(x=50, y=300)
forgot_pass.bind("<Button-1>", lambda e: on_forgot_password())

signup_link = ctk.CTkLabel(form_frame, text="Sign Up", font=("Arial", 9, "underline"), text_color="#3B82F6", cursor="hand2")
signup_link.place(x=280, y=300)
signup_link.bind("<Button-1>", lambda e: on_signup())

# Run the Tkinter main loop
root.mainloop()
