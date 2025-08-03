"""
Dashboard view for the Employee Assignment Management System.
This module provides the dashboard view that shows key metrics and recent activities.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import datetime, timedelta

from .base_view import BaseView

class DashboardView(BaseView):
    """Dashboard view showing key metrics and recent activities."""
    
    def _create_widgets(self) -> None:
        """Create and arrange the widgets for the dashboard."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(
            row=0, column=0, 
            padx=20, pady=(20, 10), 
            sticky="w"
        )
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(
            row=1, column=0, 
            padx=20, pady=10, 
            sticky="nsew"
        )
        self.content_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Stats cards
        self._create_stats_cards()
        
        # Recent activities frame
        self.activities_frame = ctk.CTkFrame(self.content_frame)
        self.activities_frame.grid(
            row=1, column=0, 
            columnspan=3, 
            padx=5, pady=(20, 10), 
            sticky="nsew"
        )
        self.activities_frame.grid_columnconfigure(0, weight=1)
        self.activities_frame.grid_rowconfigure(1, weight=1)
        
        # Activities title
        activities_title = ctk.CTkLabel(
            self.activities_frame,
            text="Recent Activities",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        activities_title.grid(
            row=0, column=0, 
            padx=10, pady=(10, 5), 
            sticky="w"
        )
        
        # Activities treeview
        self.activities_tree = self._create_activities_tree()
        
        # Load data
        self.load_data()
    
    def _create_stats_cards(self) -> None:
        """Create the statistics cards for the dashboard."""
        # Total Employees Card
        self.employees_card = self._create_stat_card(
            parent=self.content_frame,
            title="Total Employees",
            value="0",
            icon="👥",
            row=0,
            column=0
        )
        
        # Total Locations Card
        self.locations_card = self._create_stat_card(
            parent=self.content_frame,
            title="Total Locations",
            value="0",
            icon="📍",
            row=0,
            column=1
        )
        
        # Recent Assignments Card
        self.assignments_card = self._create_stat_card(
            parent=self.content_frame,
            title="This Month's Assignments",
            value="0",
            icon="📅",
            row=0,
            column=2
        )
    
    def _create_stat_card(self, parent, title: str, value: str, icon: str, row: int, column: int) -> ctk.CTkFrame:
        """Create a statistics card.
        
        Args:
            parent: Parent widget
            title: Card title
            value: Initial value to display
            icon: Icon to display
            row: Grid row
            column: Grid column
            
        Returns:
            The created card frame
        """
        # Card frame
        card = ctk.CTkFrame(
            parent,
            corner_radius=10
        )
        card.grid(
            row=row, column=column, 
            padx=10, pady=10, 
            sticky="nsew"
        )
        card.grid_columnconfigure(0, weight=1)
        
        # Icon and title
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        
        # Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(weight="bold")
        )
        title_label.pack(side="left")
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        value_label.grid(row=1, column=0, padx=10, pady=(0, 10))
        
        # Store the value label for later updates
        card.value_label = value_label
        
        return card
    
    def _create_activities_tree(self) -> ttk.Treeview:
        """Create the activities treeview.
        
        Returns:
            The created treeview widget
        """
        # Create a frame to hold the treeview and scrollbars
        tree_frame = ctk.CTkFrame(self.activities_frame)
        tree_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create the treeview
        columns = ["date", "employee", "from_location", "to_location", "status"]
        column_headings = {
            "date": "Date",
            "employee": "Employee",
            "from_location": "From",
            "to_location": "To",
            "status": "Status"
        }
        
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        for col in columns:
            tree.heading(col, text=column_headings[col])
            
            # Set column widths
            if col == "date":
                tree.column(col, width=120, anchor="center")
            elif col == "employee":
                tree.column(col, width=200, anchor="w")
            elif col in ["from_location", "to_location"]:
                tree.column(col, width=150, anchor="center")
            elif col == "status":
                tree.column(col, width=100, anchor="center")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid the tree and scrollbars
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configure tag colors
        tree.tag_configure("completed", foreground="green")
        tree.tag_configure("pending", foreground="orange")
        tree.tag_configure("upcoming", foreground="blue")
        
        return tree
    
    def load_data(self) -> None:
        """Load data into the dashboard."""
        try:
            # Get employee count
            cursor = self.controller.db.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM EMPLOYE")
            employee_count = cursor.fetchone()[0]
            self.employees_card.value_label.configure(text=str(employee_count))
            
            # Get location count
            cursor.execute("SELECT COUNT(*) FROM LIEU")
            location_count = cursor.fetchone()[0]
            self.locations_card.value_label.configure(text=str(location_count))
            
            # Get this month's assignments count
            first_day = datetime.now().replace(day=1).strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT COUNT(*) 
                FROM AFFECTER 
                WHERE dateAffect >= ?
            """, (first_day,))
            assignments_count = cursor.fetchone()[0]
            self.assignments_card.value_label.configure(text=str(assignments_count))
            
            # Load recent activities
            self._load_recent_activities()
            
        except Exception as e:
            self.controller.update_status(f"Error loading dashboard data: {str(e)}", is_error=True)
    
    def _load_recent_activities(self) -> None:
        """Load recent activities into the treeview."""
        # Clear existing items
        for item in self.activities_tree.get_children():
            self.activities_tree.delete(item)
        
        try:
            # Get recent assignments
            cursor = self.controller.db.conn.cursor()
            cursor.execute("""
                SELECT 
                    a.numAffect,
                    a.dateAffect,
                    e.numEmp,
                    e.nom,
                    e.prenom,
                    al.design as ancien_lieu,
                    al.province as ancien_province,
                    nl.design as nouveau_lieu,
                    nl.province as nouveau_province,
                    a.datePriseService
                FROM AFFECTER a
                JOIN EMPLOYE e ON a.numEmp = e.numEmp
                JOIN LIEU al ON a.AncienLieu = al.idlieu
                JOIN LIEU nl ON a.NouveauLieu = nl.idlieu
                ORDER BY a.dateAffect DESC, a.datePriseService DESC
                LIMIT 50
            """)
            
            # Add assignments to treeview
            for row in cursor.fetchall():
                assign_date = datetime.strptime(row[1], "%Y-%m-%d").strftime("%Y-%m-%d")
                employee_name = f"{row[3]} {row[4]}"
                from_location = f"{row[5]} ({row[6]})" if row[5] else "N/A"
                to_location = f"{row[7]} ({row[8]})" if row[7] else "N/A"
                
                # Determine status
                today = datetime.now().date()
                service_date = datetime.strptime(row[9], "%Y-%m-%d").date()
                
                if service_date < today:
                    status = "Completed"
                    tag = "completed"
                elif service_date == today:
                    status = "Today"
                    tag = "pending"
                else:
                    status = "Upcoming"
                    tag = "upcoming"
                
                self.activities_tree.insert(
                    "", "end",
                    values=(
                        assign_date,
                        employee_name,
                        from_location,
                        to_location,
                        status
                    ),
                    tags=(tag,)
                )
                
        except Exception as e:
            self.controller.update_status(f"Error loading activities: {str(e)}", is_error=True)
    
    def on_show(self) -> None:
        """Handle view being shown."""
        # Refresh data when the view is shown
        self.load_data()
        self.controller.update_status("Dashboard loaded.")
