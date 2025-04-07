import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import hashlib
from PIL import Image, ImageTk
import os
import tkinter as tk
import sys

# ------------------- Gradient Background Frame -------------------
class GradientFrame(tk.Frame):
    def __init__(self, master, start_color, end_color, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.start_color = start_color
        self.end_color = end_color
        self.bind("<Configure>", self._on_configure)
        
    def _on_configure(self, event):
        # Recreate the gradient background
        self.delete_gradient()
        self.create_gradient(event.width, event.height)
        
    def delete_gradient(self):
        # Delete existing gradient canvas if it exists
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()
                
    def create_gradient(self, width, height):
        # Create a canvas for gradient
        canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create gradient
        for i in range(height):
            # Interpolate between start and end colors
            r1, g1, b1 = self.hex_to_rgb(self.start_color)
            r2, g2, b2 = self.hex_to_rgb(self.end_color)
            
            # Calculate interpolated color
            r = int(r1 + (r2 - r1) * i / height)
            g = int(g1 + (g2 - g1) * i / height)
            b = int(b1 + (b2 - b1) * i / height)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            canvas.create_line(0, i, width, i, fill=color)
        
    def hex_to_rgb(self, hex_color):
        # Convert hex color to RGB
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# ------------------- Login Page Class -------------------
class LoginPage:
    def __init__(self, root, callback=None):
        self.root = root
        self.login_callback = callback
        
        # Configure window
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.title("Student Management System - Login")
        self.root.geometry("1200x700")
        
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create a custom frame with gradient background
        self.gradient_frame = GradientFrame(self.root, start_color="#3B82F6", end_color="#8B5CF6")
        self.gradient_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main Content Frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Left Side - Illustration
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", width=500, height=500)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Load the image
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "image.png")
        
        try:
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((500, 400), Image.LANCZOS)
            image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(500, 400))
            image_label = ctk.CTkLabel(self.left_frame, image=image, text="")
            image_label.pack(expand=True, fill="both")
        except Exception as e:
            error_label = ctk.CTkLabel(self.left_frame, text="Student Management System", font=("Arial", 24, "bold"), text_color="white")
            error_label.pack(expand=True, fill="both")
            print(f"Image not found. Using text instead: {e}")
        
        # Right Side - Login Form
        self.form_frame = ctk.CTkFrame(self.main_frame, fg_color="white", width=400, height=500, corner_radius=20)
        self.form_frame.grid(row=0, column=1, padx=20, pady=20)
        
        # Profile Icon
        profile_icon = ctk.CTkLabel(self.form_frame, text="👤", font=("Arial", 36), text_color="black")
        profile_icon.pack(pady=(30, 10))
        
        # Login Title
        title_label = ctk.CTkLabel(self.form_frame, text="Login to Your Account", font=("Arial", 18, "bold"), text_color="black")
        title_label.pack(pady=10)
        
        # Email Entry
        email_label = ctk.CTkLabel(self.form_frame, text="Email", font=("Arial", 12), text_color="black", anchor="w")
        email_label.pack(pady=(10, 0), padx=40, anchor="w")
        self.email_entry = ctk.CTkEntry(self.form_frame, font=("Arial", 14), width=320, height=40, corner_radius=10)
        self.email_entry.pack(pady=5, padx=40)
        
        # Password Entry
        password_label = ctk.CTkLabel(self.form_frame, text="Password", font=("Arial", 12), text_color="black")
        password_label.pack(pady=(10, 0), padx=40, anchor="w")
        
        # Password Entry with Toggle
        password_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        password_frame.pack(pady=5, padx=40, fill="x")
        
        self.password_entry = ctk.CTkEntry(password_frame, font=("Arial", 14), width=290, height=40, corner_radius=10, show="*")
        self.password_entry.pack(side="left", expand=True, fill="x")
        
        toggle_btn = ctk.CTkButton(password_frame, text="👁", width=40, height=40, fg_color="transparent", text_color="black", 
                                  font=("Arial", 16), command=self.toggle_password)
        toggle_btn.pack(side="right")
        
        # Remember Me Checkbox
        remember_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        remember_frame.pack(pady=10, padx=40, fill="x")
        
        remember_me = ctk.CTkCheckBox(remember_frame, text="Remember Me", font=("Arial", 12), text_color="black", fg_color="#3B82F6")
        remember_me.pack(side="left")
        
        # Forgot Password
        forgot_pass = ctk.CTkLabel(remember_frame, text="Forgot Password?", font=("Arial", 12), text_color="#3B82F6", cursor="hand2")
        forgot_pass.pack(side="right")
        forgot_pass.bind("<Button-1>", lambda e: self.forgot_password())
        
        # Login Button
        login_btn = ctk.CTkButton(self.form_frame, text="Login", font=("Arial", 14), fg_color="#3B82F6", text_color="white", 
                                width=320, height=40, corner_radius=10, command=self.login_user)
        login_btn.pack(pady=20, padx=40)
        
        # Sign Up Link
        signup_link = ctk.CTkLabel(self.form_frame, text="Don't have an account? Sign Up", 
                                  font=("Arial", 12, "underline"), text_color="#3B82F6", cursor="hand2")
        signup_link.pack(pady=(0, 20))
        signup_link.bind("<Button-1>", lambda e: self.sign_up())
    
    def toggle_password(self):
        current_show = self.password_entry.cget("show")
        self.password_entry.configure(show="" if current_show == "*" else "*")
    
    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Please contact your administrator to reset your password.")
    
    def sign_up(self):
        messagebox.showinfo("Sign Up", "Please contact your administrator to create a new account.")
    
    def login_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
            return
        
        # Debug output: Show the raw password for debugging
        print(f"Attempting login with email: {email}")
        print(f"Password: {password}")
        
        # Skip database check for testing - Direct login
        if email == "john.doe@example.com" and password == "password123":
            messagebox.showinfo("Debug Login", "Bypassing database check for testing.")
            if self.login_callback:
                self.login_callback(1)  # Hard-coded student_id=1
            return
            
        # Normal login flow with database check
        hashed_password = self.hash_password(password)
        print(f"Hashed password: {hashed_password}")
        
        try:
            connection = self.connect_db()
            
            if not connection:
                messagebox.showerror("Database Error", "Could not connect to database. Using direct login.")
                # Fallback direct login
                if email == "john.doe@example.com" and password == "password123":
                    if self.login_callback:
                        self.login_callback(1)
                return
                
            cursor = connection.cursor()
            
            # Debug: First check if the user exists at all
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_exists = cursor.fetchone()
            
            if not user_exists:
                print("User does not exist in database")
                messagebox.showerror("Login Failed", "User not found. Try john.doe@example.com/password123.")
                return
                
            # Get the stored password hash for comparison
            cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            stored_password_record = cursor.fetchone()
            
            if stored_password_record:
                stored_password = stored_password_record[0]
                print(f"Stored password hash: {stored_password}")
                print(f"Matching? {stored_password == hashed_password}")
            
            # Continue with normal login check
            cursor.execute(
                "SELECT user_id, user_type FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
            
            if user:
                user_id, user_type = user
                
                # For debugging, we'll accept any password for the sample user
                if email == "john.doe@example.com":
                    cursor.execute(
                        "SELECT student_id FROM students WHERE user_id = %s",
                        (user_id,)
                    )
                    student_result = cursor.fetchone()
                    
                    if student_result:
                        student_id = student_result[0]
                        messagebox.showinfo("Login Successful", "Welcome to the Student Management System!")
                        
                        # Call the callback function with student_id
                        if self.login_callback:
                            self.login_callback(student_id)
                        return
                
                # Try full credential check
                cursor.execute(
                    "SELECT user_id, user_type FROM users WHERE email = %s AND password = %s",
                    (email, hashed_password)
                )
                user_with_password = cursor.fetchone()
                
                if user_with_password:
                    user_id, user_type = user_with_password
                    
                    # If user is a student, get the student_id
                    if user_type == 'student':
                        cursor.execute(
                            "SELECT student_id FROM students WHERE user_id = %s",
                            (user_id,)
                        )
                        student_result = cursor.fetchone()
                        
                        if student_result:
                            student_id = student_result[0]
                            messagebox.showinfo("Login Successful", "Welcome to the Student Management System!")
                            
                            # Call the callback function with student_id
                            if self.login_callback:
                                self.login_callback(student_id)
                        else:
                            messagebox.showerror("Login Error", "Student record not found.")
                    else:
                        messagebox.showinfo("Login Successful", f"Welcome {user_type}!")
                else:
                    messagebox.showerror("Login Failed", "Invalid Password. Try 'password123'.")
            else:
                messagebox.showerror("Login Failed", "Invalid Email or Password.")
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            # Fallback: Use test login (for development/testing)
            if email == "john.doe@example.com" and password == "password123":
                messagebox.showinfo("Dev Login", "Welcome to the Student Management System (Dev Mode)!")
                if self.login_callback:
                    self.login_callback(1)  # Use student_id=1 for development
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
    
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="new_password",
            database="college_system"
        )
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()