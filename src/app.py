"""
Main application module for the Employee Assignment Management System.
This module initializes the application and sets up the main window.
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime

from .models.database import Database
from .controllers.location_controller import LocationController
from .controllers.employee_controller import EmployeeController
from .controllers.assignment_controller import AssignmentController
from .views.base_view import BaseView

class EmployeeAssignmentApp(ctk.CTk):
    """Main application class for the Employee Assignment Management System."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        # Configure the main window
        self.title("Employee Assignment Management System")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Set appearance mode and color theme
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # Initialize database and controllers
        self._init_database()
        self._init_controllers()
        
        # Setup the UI
        self._setup_ui()
        
        # Load initial data
        self._load_initial_data()
    
    def _init_database(self):
        """Initialize the database connection."""
        from .models.database import Database
        import os
        import sys
        
        # Use the test database we created
        db_name = 'test_employee_assignments.db'
        db_path = os.path.abspath(db_name)
        
        # Print debug information
        print("\n" + "="*50, file=sys.stderr)
        print(f"DEBUG: Initializing database...", file=sys.stderr)
        print(f"DEBUG: Current working directory: {os.getcwd()}", file=sys.stderr)
        print(f"DEBUG: Database path: {db_path}", file=sys.stderr)
        print(f"DEBUG: Database exists: {os.path.exists(db_path)}", file=sys.stderr)
        
        try:
            # Initialize database with the test database
            print(f"DEBUG: Creating Database instance...", file=sys.stderr)
            self.db = Database(db_path)
            print(f"DEBUG: Database instance created successfully", file=sys.stderr)
            
            # Verify tables and data
            cursor = self.db.conn.cursor()
            
            # List all tables
            print("\nDEBUG: Checking database tables...", file=sys.stderr)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"DEBUG: Tables in database: {[t[0] for t in tables]}", file=sys.stderr)
            
            # Check LIEU table specifically
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='LIEU'")
            table_exists = cursor.fetchone() is not None
            print(f"\nDEBUG: LIEU table exists: {table_exists}", file=sys.stderr)
            
            if table_exists:
                # Get table structure
                print("\nDEBUG: LIEU table structure:", file=sys.stderr)
                cursor.execute("PRAGMA table_info(LIEU)")
                columns = cursor.fetchall()
                print("DEBUG: Columns in LIEU table:", file=sys.stderr)
                for col in columns:
                    print(f"  {col[1]} ({col[2]}) - PK: {bool(col[5])}", file=sys.stderr)
                
                # Count locations
                cursor.execute("SELECT COUNT(*) FROM LIEU")
                count = cursor.fetchone()[0]
                print(f"\nDEBUG: Number of locations in LIEU table: {count}", file=sys.stderr)
                
                # Print first few locations
                if count > 0:
                    print("\nDEBUG: Sample locations (first 5):", file=sys.stderr)
                    cursor.execute("SELECT * FROM LIEU LIMIT 5")
                    for row in cursor.fetchall():
                        print(f"  - {row}", file=sys.stderr)
                else:
                    print("\nDEBUG: No locations found in LIEU table", file=sys.stderr)
                    
                    # If no locations, try to seed the database
                    print("\nDEBUG: Attempting to seed the database...", file=sys.stderr)
                    try:
                        self.db.seed_initial_data()
                        print("DEBUG: Database seeded successfully", file=sys.stderr)
                        
                        # Verify seeding
                        cursor.execute("SELECT COUNT(*) FROM LIEU")
                        new_count = cursor.fetchone()[0]
                        print(f"DEBUG: Locations after seeding: {new_count}", file=sys.stderr)
                        
                    except Exception as seed_error:
                        print(f"ERROR: Failed to seed database: {str(seed_error)}", file=sys.stderr)
            else:
                print("\nDEBUG: LIEU table does not exist. Creating tables...", file=sys.stderr)
                try:
                    self.db.create_tables()
                    print("DEBUG: Tables created successfully", file=sys.stderr)
                    
                    # Seed initial data
                    print("DEBUG: Seeding initial data...", file=sys.stderr)
                    self.db.seed_initial_data()
                    print("DEBUG: Initial data seeded successfully", file=sys.stderr)
                    
                except Exception as create_error:
                    print(f"ERROR: Failed to create tables: {str(create_error)}", file=sys.stderr)
                    raise
            
            print("\n" + "="*50 + "\n", file=sys.stderr)
            
        except Exception as e:
            error_msg = f"ERROR: Database initialization failed: {str(e)}"
            print(error_msg, file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            
            messagebox.showerror(
                "Database Error",
                f"Failed to initialize the database: {str(e)}\n\nCheck the console for more details."
            )
            raise
            sys.exit(1)
    
    def _init_controllers(self) -> None:
        """Initialize the application controllers."""
        self.location_controller = LocationController(self.db)
        self.employee_controller = EmployeeController(self.db)
        self.assignment_controller = AssignmentController(self.db)
    
    def _setup_ui(self) -> None:
        """Set up the main user interface.
        
        This includes:
        1. The main container
        2. The sidebar with navigation buttons
        3. The main content area where views will be displayed
        4. The status bar
        """
        # Configure grid layout (1x2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        # Add logo and title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Employee\nAssignment\nSystem",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation buttons
        self.dashboard_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Dashboard",
            command=self.show_dashboard,
            font=ctk.CTkFont(weight="bold")
        )
        self.dashboard_btn.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.employees_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Employees",
            command=self.show_employees,
            font=ctk.CTkFont(weight="bold")
        )
        self.employees_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.locations_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Locations",
            command=self.show_locations,
            font=ctk.CTkFont(weight="bold")
        )
        self.locations_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.assignments_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Assignments",
            command=self.show_assignments,
            font=ctk.CTkFont(weight="bold")
        )
        self.assignments_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.reports_btn = ctk.CTkButton(
            self.sidebar_frame, 
            text="Reports",
            command=self.show_reports,
            font=ctk.CTkFont(weight="bold")
        )
        self.reports_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        # Appearance mode menu
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Appearance Mode:", 
            anchor="w"
        )
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=10, sticky="s")
        
        # Create main container for views
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.grid(row=0, column=1, rowspan=3, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Create status bar
        self.status_bar = ctk.CTkLabel(
            self, 
            text="Ready", 
            anchor="w",
            padx=10,
            height=25,
            fg_color=("gray85", "gray16"),
            corner_radius=0
        )
        self.status_bar.grid(row=3, column=1, sticky="ew")
        
        # Store the current view
        self.current_view = None
    
    def _load_initial_data(self) -> None:
        """Load initial data and show the dashboard."""
        self.show_dashboard()
    
    def show_view(self, view_class, *args, **kwargs) -> None:
        """Show a view in the main container.
        
        Args:
            view_class: The view class to instantiate
            *args: Positional arguments to pass to the view
            **kwargs: Keyword arguments to pass to the view
        """
        print(f"DEBUG: Showing view: {view_class.__name__}")
        
        # Hide the current view if it exists
        if self.current_view:
            print("DEBUG: Hiding current view")
            try:
                self.current_view.on_hide()
            except Exception as e:
                print(f"WARNING: Error in on_hide(): {e}")
            self.current_view.destroy()
        
        try:
            # Create the new view
            print("DEBUG: Creating new view instance")
            self.current_view = view_class(self.main_container, self, *args, **kwargs)
            
            # Configure the view to expand
            self.current_view.grid(row=0, column=0, sticky="nsew")
            self.current_view.grid_rowconfigure(0, weight=1)
            self.current_view.grid_columnconfigure(0, weight=1)
            
            # Force update the display
            self.current_view.update_idletasks()
            
            # Call on_show after the view is visible
            print("DEBUG: Calling on_show()")
            self.current_view.on_show()
            
            # Force another update
            self.current_view.update_idletasks()
            
            print(f"DEBUG: View {view_class.__name__} displayed successfully")
            
        except Exception as e:
            error_msg = f"ERROR: Failed to show view {view_class.__name__}: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.update_status(error_msg, is_error=True)
    
    def show_dashboard(self) -> None:
        """Show the dashboard view."""
        from .views.dashboard_view import DashboardView
        self.show_view(DashboardView)
        self._update_nav_buttons_style("dashboard")
    
    def show_employees(self) -> None:
        """Show the employees view."""
        from .views.employee_view import EmployeeView
        self.show_view(EmployeeView)
        self._update_nav_buttons_style("employees")
    
    def show_locations(self) -> None:
        """Show the locations view."""
        from .views.location_view import LocationView
        self.show_view(LocationView)
        self._update_nav_buttons_style("locations")
    
    def show_assignments(self) -> None:
        """Show the assignments view."""
        from .views.assignment_view import AssignmentView
        self.show_view(AssignmentView)
        self._update_nav_buttons_style("assignments")
    
    def show_reports(self) -> None:
        """Show the reports view."""
        from .views.report_view import ReportView
        self.show_view(ReportView)
        self._update_nav_buttons_style("reports")
    
    def _update_nav_buttons_style(self, active_button: str) -> None:
        """Update the style of the navigation buttons.
        
        Args:
            active_button: The name of the currently active button
        """
        buttons = {
            "dashboard": self.dashboard_btn,
            "employees": self.employees_btn,
            "locations": self.locations_btn,
            "assignments": self.assignments_btn,
            "reports": self.reports_btn
        }
        
        # Reset all buttons to default style
        for btn in buttons.values():
            btn.configure(fg_color=("gray75", "gray25"))  # Default color
        
        # Highlight the active button
        if active_button in buttons:
            buttons[active_button].configure(fg_color=("gray50", "gray50"))  # Active color
    
    def update_status(self, message: str, is_error: bool = False) -> None:
        """Update the status bar with a message.
        
        Args:
            message: The message to display
            is_error: Whether this is an error message (will be shown in red)
        """
        self.status_bar.configure(text=message)
        
        if is_error:
            self.status_bar.configure(text_color="red")
            # Reset to default color after 5 seconds
            self.after(5000, lambda: self.status_bar.configure(text_color=("gray10", "gray90")))
        else:
            self.status_bar.configure(text_color=("gray10", "gray90"))
    
    def change_appearance_mode(self, new_appearance_mode: str) -> None:
        """Change the appearance mode of the application.
        
        Args:
            new_appearance_mode: The new appearance mode ("Light", "Dark", or "System")
        """
        ctk.set_appearance_mode(new_appearance_mode.lower())
    
    def on_closing(self) -> None:
        """Handle application closing."""
        # Close the database connection
        if hasattr(self, 'db'):
            self.db.close()
        

def main():
    """Main entry point for the application."""
    print("DEBUG: Starting application...")
    
    try:
        print("DEBUG: Creating application instance...")
        app = EmployeeAssignmentApp()
        print("DEBUG: Application instance created successfully")
        
        # Handle window closing
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        print("DEBUG: Centering window on screen...")
        app.update_idletasks()
        width = app.winfo_width()
        height = app.winfo_height()
        x = (app.winfo_screenwidth() // 2) - (width // 2)
        y = (app.winfo_screenheight() // 2) - (height // 2)
        app.geometry(f'{width}x{height}+{x}+{y}')
        
        print("DEBUG: Starting main loop...")
        app.mainloop()
        print("DEBUG: Main loop ended")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Try to show error in a message box if possible
        try:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Critical Error", f"The application encountered a critical error and will now exit.\n\nError: {str(e)}")
        except:
            pass
            
        # Exit with error code
        import sys
        sys.exit(1)
    
    # Start the main loop
    app.mainloop()

if __name__ == "__main__":
    main()
