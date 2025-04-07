import customtkinter as ctk

class Sidebar:
    """
    Reusable sidebar component for all screens in the Student Management System.
    Creates a consistent navigation interface with proper callbacks.
    """
    def __init__(self, parent_frame, active_item=None, nav_callbacks=None):
        """
        Initialize the sidebar.
        
        Args:
            parent_frame: The parent frame to place the sidebar in
            active_item: String name of the currently active item (to highlight it)
            nav_callbacks: Dictionary of navigation callbacks for each menu item
        """
        self.parent_frame = parent_frame
        self.active_item = active_item
        self.nav_callbacks = nav_callbacks or {}
        
        # Create the sidebar frame
        self.sidebar = ctk.CTkFrame(
            parent_frame, 
            fg_color="#5A67D8", 
            width=250, 
            corner_radius=0
        )
        self.sidebar.place(x=0, y=0, relheight=1)

        # Sidebar title
        ctk.CTkLabel(
            self.sidebar, 
            text="👤 Student", 
            font=("Arial", 18, "bold"), 
            text_color="white"
        ).place(x=20, y=20)
        
        # Create menu items
        self.create_menu_items()
    
    def create_menu_items(self):
        """Create the menu items in the sidebar."""
        # Define all menu items and their corresponding callback keys
        menu_items = [
            ("Course Registration", "course_registration"),
            ("Course Management", "course_management"),
            ("Attendance Tracking", "attendance_tracking"),
            ("Exams and Grades", "exams_grades"),
            ("Fee Payment", "fee_payment"),
            ("Profile", "profile"),
            ("Dashboard", "dashboard")
        ]
        
        # Place menu items in the sidebar
        y_position = 60
        for item_text, callback_key in menu_items:
            # Determine if this item is active
            is_active = callback_key == self.active_item
            
            # Set colors based on active state
            btn_color = "#D9DBFF" if is_active else "#5A67D8"
            btn_text_color = "black" if is_active else "white"
            
            # Create the button
            btn = ctk.CTkButton(
                self.sidebar, 
                text=item_text, 
                font=("Arial", 12), 
                fg_color=btn_color, 
                text_color=btn_text_color,
                width=220, 
                height=30, 
                corner_radius=5, 
                hover_color="#4251CC",
                command=lambda key=callback_key: self.handle_navigation(key)
            )
            btn.place(x=10, y=y_position)
            y_position += 40
        
        # Add logout button at the bottom
        logout_btn = ctk.CTkButton(
            self.sidebar, 
            text="Logout", 
            font=("Arial", 12, "bold"), 
            fg_color="#FF5757",
            text_color="white",
            width=220, 
            height=30, 
            corner_radius=5,
            hover_color="#FF3131",
            command=lambda: self.handle_navigation("logout")
        )
        logout_btn.place(x=10, y=600)  # Fixed position at bottom
    
    def handle_navigation(self, callback_key):
        """Handle navigation based on the callback key."""
        if callback_key in self.nav_callbacks and callable(self.nav_callbacks[callback_key]):
            self.nav_callbacks[callback_key]()
        else:
            print(f"Warning: No callback found for '{callback_key}'")