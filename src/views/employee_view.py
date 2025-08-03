"""
Employee view for the Employee Assignment Management System.
This module provides the employee management interface.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

from ..models.employee import Employee
from ..models.location import Location
from .base_view import BaseView

class EmployeeView(BaseView):
    """View for managing employee records."""
    
    def _create_widgets(self) -> None:
        """Create and arrange the widgets for the employee view."""
        # Configure grid and create main frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create header with title and search
        self._create_header()
        
        # Create main content area with list and details
        self._create_main_content()
        
        # Load employee data
        self.load_employees()
    
    def _create_header(self) -> None:
        """Create the header with title and search bar."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        
        # Title
        ctk.CTkLabel(
            header,
            text="Employee Management",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        # Search bar
        search_frame = ctk.CTkFrame(header, fg_color="transparent")
        search_frame.grid(row=0, column=1, sticky="e")
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *a: self._filter_employees())
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search employees...",
            textvariable=self.search_var,
            width=300
        ).pack(side="left", padx=(0, 10))
    
    def _create_main_content(self) -> None:
        """Create the main content area with employee list and details."""
        # Main container
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        content.grid_columnconfigure(0, weight=2)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        
        # Employee list container
        list_container = ctk.CTkFrame(content)
        list_container.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        list_container.grid_rowconfigure(1, weight=1)
        list_container.grid_columnconfigure(0, weight=1)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(list_container, fg_color="transparent")
        btn_frame.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        
        ctk.CTkButton(
            btn_frame, 
            text="Add Employee",
            command=self._show_add_dialog,
            width=120
        ).pack(side="left", padx=(0, 10))
        
        self.edit_btn = ctk.CTkButton(
            btn_frame,
            text="Edit",
            command=self._show_edit_dialog,
            width=80,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=(0, 10))
        
        self.delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            command=self._delete_employee,
            width=80,
            fg_color="#d9534f",
            hover_color="#c9302c",
            state="disabled"
        )
        self.delete_btn.pack(side="left")
        
        # Employee list
        self._create_employee_list(list_container)
        
        # Employee details (initially hidden)
        self.details_frame = ctk.CTkFrame(content)
        self.details_frame.grid(row=0, column=1, sticky="nsew")
        self.details_frame.grid_remove()
    
    def _create_employee_list(self, parent) -> None:
        """Create the employee list treeview."""
        # Create treeview with scrollbars
        tree_frame = ctk.CTkFrame(parent)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Define columns
        columns = ["id", "name", "email", "position", "location"]
        
        # Create treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("position", text="Position")
        self.tree.heading("location", text="Location")
        
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("email", width=200, anchor="w")
        self.tree.column("position", width=150, anchor="w")
        self.tree.column("location", width=200, anchor="w")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", lambda e: self._show_edit_dialog())
    
    def load_employees(self, search: str = "") -> None:
        """Load employees into the list."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Get employees from controller
            employees = self.controller.employee_controller.search_employees(search)
            
            # Add to treeview
            for emp in employees:
                self.tree.insert("", "end",
                    values=(
                        emp.numEmp,
                        f"{emp.nom}, {emp.prenom}",
                        emp.mail,
                        emp.poste,
                        f"{emp.lieu_design} ({emp.province})" if emp.lieu_design else "Unassigned"
                    ),
                    tags=("unassigned" if not emp.idlieu else "")
                )
            
            # Configure tag for unassigned employees
            self.tree.tag_configure("unassigned", foreground="gray")
            
        except Exception as e:
            self.controller.update_status(f"Error loading employees: {str(e)}", True)
    
    def _on_select(self, event=None) -> None:
        """Handle employee selection."""
        selected = self.tree.selection()
        
        if selected:
            self.edit_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
            self._show_employee_details(selected[0])
        else:
            self.edit_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
            self.details_frame.grid_remove()
    
    def _show_employee_details(self, item_id: str) -> None:
        """Show details for the selected employee."""
        # Get employee ID from selection
        values = self.tree.item(item_id, "values")
        if not values:
            return
            
        try:
            # Get employee data
            employee = self.controller.employee_controller.get_by_id(values[0])
            if not employee:
                return
            
            # Clear existing details
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            
            # Show details frame
            self.details_frame.grid()
            
            # Create details UI
            ctk.CTkLabel(
                self.details_frame,
                text=f"{employee.prenom} {employee.nom}",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=10)
            
            ctk.CTkLabel(
                self.details_frame,
                text=employee.poste,
                text_color=("gray50", "gray70")
            ).pack(pady=(0, 20))
            
            # Contact info
            info_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text="Email:",
                font=ctk.CTkFont(weight="bold")
            ).grid(row=0, column=0, sticky="w", pady=2)
            
            ctk.CTkLabel(
                info_frame,
                text=employee.mail
            ).grid(row=0, column=1, sticky="w", padx=10, pady=2)
            
            # Location info
            ctk.CTkLabel(
                info_frame,
                text="Location:",
                font=ctk.CTkFont(weight="bold")
            ).grid(row=1, column=0, sticky="w", pady=2)
            
            location_text = (
                f"{employee.lieu_design} ({employee.province})" 
                if employee.lieu_design 
                else "Unassigned"
            )
            
            ctk.CTkLabel(
                info_frame,
                text=location_text
            ).grid(row=1, column=1, sticky="w", padx=10, pady=2)
            
            # Action buttons
            btn_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
            btn_frame.pack(pady=20)
            
            ctk.CTkButton(
                btn_frame,
                text="Assign Location",
                command=lambda: self._assign_location(employee)
            ).pack(pady=5)
            
        except Exception as e:
            self.controller.update_status(f"Error loading details: {str(e)}", True)
    
    def _show_add_dialog(self) -> None:
        """Show the add employee dialog."""
        dialog = EmployeeDialog(self, self.controller, "Add Employee")
        self.wait_window(dialog)
        if dialog.result:
            self.load_employees()
    
    def _show_edit_dialog(self, event=None) -> None:
        """Show the edit employee dialog."""
        selected = self.tree.selection()
        if not selected:
            return
            
        try:
            employee_id = self.tree.item(selected[0], "values")[0]
            employee = self.controller.employee_controller.get_by_id(employee_id)
            
            if employee:
                dialog = EmployeeDialog(
                    self, 
                    self.controller, 
                    "Edit Employee",
                    employee=employee
                )
                self.wait_window(dialog)
                
                if dialog.result:
                    self.load_employees()
                    
        except Exception as e:
            self.controller.update_status(f"Error: {str(e)}", True)
    
    def _delete_employee(self) -> None:
        """Delete the selected employee."""
        selected = self.tree.selection()
        if not selected:
            return
            
        try:
            employee_id = self.tree.item(selected[0], "values")[0]
            employee_name = self.tree.item(selected[0], "values")[1]
            
            if messagebox.askyesno(
                "Confirm Delete",
                f"Delete {employee_name}? This cannot be undone."
            ):
                success, message = self.controller.employee_controller.delete(employee_id)
                
                if success:
                    self.controller.update_status(message)
                    self.load_employees()
                    self.details_frame.grid_remove()
                else:
                    self.controller.update_status(message, True)
                    
        except Exception as e:
            self.controller.update_status(f"Error deleting employee: {str(e)}", True)
    
    def _assign_location(self, employee: Employee) -> None:
        """Show dialog to assign a location to the employee."""
        dialog = AssignLocationDialog(self, self.controller, employee)
        self.wait_window(dialog)
        
        if dialog.result:
            self.load_employees()
            self._on_select()
    
    def _filter_employees(self) -> None:
        """Filter employees based on search term."""
        self.load_employees(self.search_var.get().strip())
    
    def on_show(self) -> None:
        """Handle view being shown."""
        self.load_employees()
        self.controller.update_status("Employee management loaded.")


class EmployeeDialog(ctk.CTkToplevel):
    """Dialog for adding/editing employees."""
    
    def __init__(self, parent, controller, title: str, employee: Employee = None):
        super().__init__(parent)
        self.controller = controller
        self.employee = employee
        self.result = False
        
        self.title(title)
        self.geometry("500x500")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        
        if employee:
            self._load_employee_data()
    
    def _create_widgets(self) -> None:
        """Create the dialog widgets."""
        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        ctk.CTkLabel(container, text="First Name:").pack(pady=(10, 0))
        self.first_name = ctk.CTkEntry(container)
        self.first_name.pack(fill="x", pady=5)
        
        ctk.CTkLabel(container, text="Last Name:").pack(pady=(10, 0))
        self.last_name = ctk.CTkEntry(container)
        self.last_name.pack(fill="x", pady=5)
        
        ctk.CTkLabel(container, text="Email:").pack(pady=(10, 0))
        self.email = ctk.CTkEntry(container)
        self.email.pack(fill="x", pady=5)
        
        ctk.CTkLabel(container, text="Position:").pack(pady=(10, 0))
        self.position = ctk.CTkEntry(container)
        self.position.pack(fill="x", pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Save",
            command=self._save,
            width=100
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="gray",
            hover_color="darkgray",
            width=100
        ).pack(side="right", padx=5)
    
    def _load_employee_data(self) -> None:
        """Load employee data into the form."""
        if not self.employee:
            return
            
        self.first_name.insert(0, self.employee.prenom)
        self.last_name.insert(0, self.employee.nom)
        self.email.insert(0, self.employee.mail)
        self.position.insert(0, self.employee.poste)
    
    def _save(self) -> None:
        """Save the employee data."""
        data = {
            "prenom": self.first_name.get().strip(),
            "nom": self.last_name.get().strip(),
            "mail": self.email.get().strip().lower(),
            "poste": self.position.get().strip()
        }
        
        try:
            if self.employee:
                # Update existing employee
                success, message = self.controller.employee_controller.update(
                    self.employee.numEmp,
                    data
                )
            else:
                # Create new employee
                success, message, _ = self.controller.employee_controller.create(data)
            
            if success:
                self.result = True
                self.destroy()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save employee: {str(e)}")


class AssignLocationDialog(ctk.CTkToplevel):
    """Dialog for assigning a location to an employee."""
    
    def __init__(self, parent, controller, employee: Employee):
        super().__init__(parent)
        self.controller = controller
        self.employee = employee
        self.result = False
        
        self.title(f"Assign Location to {employee.prenom} {employee.nom}")
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.transient(parent)
        self.grab_set()
        
        self._create_widgets()
        self._load_locations()
    
    def _create_widgets(self) -> None:
        """Create the dialog widgets."""
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            container,
            text=f"Current Location: {self.employee.lieu_design or 'Unassigned'}"
        ).pack(pady=10)
        
        ctk.CTkLabel(container, text="New Location:").pack(pady=(20, 5))
        
        self.location_var = ctk.StringVar()
        self.location_menu = ctk.CTkOptionMenu(
            container,
            variable=self.location_var,
            values=["Loading..."]
        )
        self.location_menu.pack(fill="x", pady=5)
        
        ctk.CTkLabel(container, text="Assignment Date:").pack(pady=(20, 5))
        
        self.date_entry = ctk.CTkEntry(container)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(fill="x", pady=5)
        
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Assign",
            command=self._assign_location,
            width=100
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="gray",
            hover_color="darkgray",
            width=100
        ).pack(side="right", padx=5)
    
    def _load_locations(self) -> None:
        """Load available locations."""
        try:
            locations = self.controller.location_controller.get_all()
            location_names = [f"{loc.design} ({loc.province})" for loc in locations]
            location_ids = [loc.idlieu for loc in locations]
            
            self.location_menu.configure(values=location_names)
            self.locations = dict(zip(location_names, location_ids))
            
            if location_names:
                self.location_menu.set(location_names[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load locations: {str(e)}")
            self.destroy()
    
    def _assign_location(self) -> None:
        """Assign the selected location to the employee."""
        location_name = self.location_var.get()
        if not location_name or location_name == "Loading...":
            messagebox.showerror("Error", "Please select a location")
            return
            
        location_id = self.locations.get(location_name)
        if not location_id:
            messagebox.showerror("Error", "Invalid location selected")
            return
            
        assignment_date = self.date_entry.get().strip()
        
        try:
            # Create assignment
            success, message = self.controller.assignment_controller.create({
                "numEmp": self.employee.numEmp,
                "AncienLieu": self.employee.idlieu or "",
                "NouveauLieu": location_id,
                "dateAffect": assignment_date,
                "datePriseService": assignment_date
            })
            
            if success:
                self.result = True
                self.destroy()
            else:
                messagebox.showerror("Error", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign location: {str(e)}")
