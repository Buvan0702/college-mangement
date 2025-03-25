import customtkinter as ctk

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")  # Change to "light" for light mode
ctk.set_default_color_theme("blue")

# Initialize main window
root = ctk.CTk()
root.title("Reports & Analytics Dashboard")
root.geometry("1500x700")

# ---------------- Left Sidebar ---------------- #
sidebar = ctk.CTkFrame(root, width=250, height=700, fg_color="#4A5FC1")
sidebar.place(x=0, y=0)

ctk.CTkLabel(sidebar, text="📊 Reports & Analytics", font=("Arial", 16, "bold"), text_color="white").place(x=20, y=20)

# Sidebar Options
menu_options = ["Student Reports", "Attendance Analytics", "Financial Reports", "Performance Tracking"]
y_position = 60

for option in menu_options:
    ctk.CTkButton(sidebar, text=option, font=("Arial", 13), fg_color="transparent", text_color="white",
                  width=220, height=35, corner_radius=5, hover_color="#3747A5").place(x=10, y=y_position)
    y_position += 50

# ---------------- Top Menu ---------------- #
ctk.CTkButton(root, text="📤 Export Report", font=("Arial", 12), fg_color="#1F2336", text_color="white",
              width=150, height=35, corner_radius=5, hover_color="#3B82F6").place(x=300, y=20)

ctk.CTkButton(root, text="🖨 Print Report", font=("Arial", 12), fg_color="#1F2336", text_color="white",
              width=150, height=35, corner_radius=5, hover_color="#3B82F6").place(x=470, y=20)

# ---------------- Report Cards ---------------- #
card_bg = "#1A1D2A"
card_width = 300
card_height = 180
x_positions = [270, 600, 930]
titles = ["📑 Semester-wise Student Report", "📈 Attendance Trends", "💰 Fee Collection Statistics"]

for i in range(3):
    card = ctk.CTkFrame(root, fg_color=card_bg, width=card_width, height=card_height, corner_radius=10)
    card.place(x=x_positions[i], y=80)

    ctk.CTkLabel(card, text=titles[i], font=("Arial", 13, "bold"), text_color="white").place(x=20, y=20)
    ctk.CTkLabel(card, text="(Report Data Placeholder)", font=("Arial", 10), text_color="grey").place(x=80, y=80)

# Run the CustomTkinter main loop
root.mainloop()
