"""
Assignment view for the Employee Assignment Management System.
This module provides the UI for managing employee assignments.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Callable

from .base_view import BaseView

class AssignmentView(BaseView):
    """View for managing employee assignments."""
    
    def _create_widgets(self) -> None:
        """Create and arrange the widgets for assignment management."""
        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text="Assignments", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        # Add assignment button
        add_btn = ctk.CTkButton(
            header_frame, 
            text="+ New Assignment",
            command=self._show_add_assignment_dialog
        )
        add_btn.pack(side="right", padx=10)
        
        # Filter frame
        filter_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        filter_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Date range filter
        ctk.CTkLabel(
            filter_frame, 
            text="Date Range:"
        ).grid(row=0, column=0, sticky="w", padx=(10, 5), pady=10)
        
        # Start date
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        start_date_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.start_date_var,
            width=120
        )
        start_date_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        ctk.CTkLabel(
            filter_frame, 
            text="to"
        ).grid(row=0, column=2, padx=5, pady=10)
        
        # End date
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        end_date_entry = ctk.CTkEntry(
            filter_frame,
            textvariable=self.end_date_var,
            width=120
        )
        end_date_entry.grid(row=0, column=3, padx=5, pady=10, sticky="w")
        
        # Apply filter button
        apply_btn = ctk.CTkButton(
            filter_frame,
            text="Apply Filter",
            command=self._load_assignments,
            width=100
        )
        apply_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        search_frame.grid(row=0, column=5, sticky="e", padx=10, pady=10)
        
        ctk.CTkLabel(
            search_frame, 
            text="Search:"
        ).pack(side="left", padx=(10, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_changed)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search assignments...",
            width=200
        )
        search_entry.pack(side="left")
        
        # Assignments treeview
        tree_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "employee", "location", "start_date", "end_date", "status"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.tree.heading("id", text="ID")
        self.tree.heading("employee", text="Employee")
        self.tree.heading("location", text="Location")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("end_date", text="End Date")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("employee", width=200)
        self.tree.column("location", width=200)
        self.tree.column("start_date", width=120, anchor="center")
        self.tree.column("end_date", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview
        self.tree.pack(fill="both", expand=True)
        
        # Bind double click event
        self.tree.bind("<Double-1>", self._on_assignment_selected)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        button_frame.grid(row=3, column=0, sticky="e", padx=10, pady=(0, 10))
        
        # Action buttons
        self.edit_btn = ctk.CTkButton(
            button_frame,
            text="Edit",
            command=self._edit_assignment,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=5)
        
        self.end_btn = ctk.CTkButton(
            button_frame,
            text="End Assignment",
            command=self._end_assignment,
            fg_color="#f0ad4e",
            hover_color="#ec971f",
            state="disabled"
        )
        self.end_btn.pack(side="left", padx=5)
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self._delete_assignment,
            fg_color="#d9534f",
            hover_color="#c9302c",
            state="disabled"
        )
        self.delete_btn.pack(side="left", padx=5)
        
        # Store the main frame as the content
        self.content = self.main_frame
        
        # Load assignments
        self._load_assignments()
    
    def _load_assignments(self) -> None:
        """Load assignments into the treeview based on filters."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get date range
        try:
            start_date = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date_var.get(), "%Y-%m-%d")
            
            if start_date > end_date:
                messagebox.showerror("Error", "Start date cannot be after end date.")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        
        # Get assignments from controller
        assignments = self.master.master.assignment_controller.get_by_date_range(
            start_date=start_date,
            end_date=end_date
        )
        
        # Add assignments to treeview
        for assignment in assignments:
            status = "Active" if not assignment["date_fin"] else "Completed"
            self.tree.insert(
                "", "end",
                values=(
                    assignment["id"],
                    f"{assignment['employee_nom']} {assignment['employee_prenom']}",
                    assignment["lieu_nom"],
                    assignment["date_debut"].strftime("%Y-%m-%d"),
                    assignment["date_fin"].strftime("%Y-%m-%d") if assignment["date_fin"] else "-",
                    status
                )
            )
    
    def _on_search_changed(self, *args) -> None:
        """Handle search query changes."""
        search_query = self.search_var.get().lower()
        
        # If search is empty, show all items
        if not search_query:
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
            return
        
        # Show only items matching search
        for item in self.tree.get_children():
            values = [str(v).lower() for v in self.tree.item(item, 'values')]
            if any(search_query in value for value in values):
                self.tree.item(item, tags=('match',))
            else:
                self.tree.item(item, tags=())
    
    def _on_assignment_selected(self, event) -> None:
        """Handle assignment selection in the treeview."""
        selected_items = self.tree.selection()
        if selected_items:
            self.edit_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
            
            # Enable/disable end button based on status
            status = self.tree.item(selected_items[0], "values")[5]
            self.end_btn.configure(state="normal" if status == "Active" else "disabled")
    
    def _show_add_assignment_dialog(self) -> None:
        """Show the add assignment dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("New Assignment")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        # Make dialog modal
        dialog.transient(self)
        dialog.focus_set()
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog, corner_radius=0)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get employees and locations for dropdowns
        employees = self.master.master.employee_controller.get_all()
        locations = self.master.master.location_controller.get_all()
        
        # Employee selection
        ctk.CTkLabel(form_frame, text="Employee:").grid(row=0, column=0, sticky="w", pady=(10, 5))
        employee_var = tk.StringVar()
        employee_dropdown = ctk.CTkComboBox(
            form_frame,
            variable=employee_var,
            values=[f"{emp['id']} - {emp['nom']} {emp['prenom']}" for emp in employees],
            width=400
        )
        employee_dropdown.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 5))
        
        # Location selection
        ctk.CTkLabel(form_frame, text="Location:").grid(row=1, column=0, sticky="w", pady=5)
        location_var = tk.StringVar()
        location_dropdown = ctk.CTkComboBox(
            form_frame,
            variable=location_var,
            values=[f"{loc['id']} - {loc['nom']}" for loc in locations],
            width=400
        )
        location_dropdown.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Start date
        ctk.CTkLabel(form_frame, text="Start Date:").grid(row=2, column=0, sticky="w", pady=5)
        start_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        start_date_entry = ctk.CTkEntry(
            form_frame,
            textvariable=start_date_var,
            width=150
        )
        start_date_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # End date (optional)
        ctk.CTkLabel(form_frame, text="End Date (optional):").grid(row=3, column=0, sticky="w", pady=5)
        end_date_var = tk.StringVar()
        end_date_entry = ctk.CTkEntry(
            form_frame,
            textvariable=end_date_var,
            placeholder_text="Leave empty for open-ended assignment",
            width=200
        )
        end_date_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Notes
        ctk.CTkLabel(form_frame, text="Notes:").grid(row=4, column=0, sticky="nw", pady=5)
        notes_text = ctk.CTkTextbox(form_frame, width=400, height=100)
        notes_text.grid(row=4, column=1, sticky="nsew", padx=10, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_assignment():
            """Save the new assignment."""
            # Validate employee
            if not employee_var.get():
                messagebox.showerror("Error", "Please select an employee.")
                return
                
            # Validate location
            if not location_var.get():
                messagebox.showerror("Error", "Please select a location.")
                return
                
            # Parse employee and location IDs
            try:
                employee_id = int(employee_var.get().split(" - ")[0])
                location_id = int(location_var.get().split(" - ")[0])
            except (ValueError, IndexError):
                messagebox.showerror("Error", "Invalid selection.")
                return
                
            # Parse dates
            try:
                start_date = datetime.strptime(start_date_var.get(), "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_var.get(), "%Y-%m-%d").date() if end_date_var.get() else None
                
                if end_date and end_date < start_date:
                    messagebox.showerror("Error", "End date cannot be before start date.")
                    return
                    
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return
            
            # Prepare data
            data = {
                "employe_id": employee_id,
                "lieu_id": location_id,
                "date_debut": start_date,
                "date_fin": end_date,
                "notes": notes_text.get("1.0", "end-1c").strip()
            }
            
            # Save assignment
            success, result = self.master.master.assignment_controller.create(data)
            
            if success:
                messagebox.showinfo("Success", "Assignment created successfully!")
                self._load_assignments()
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"Failed to create assignment: {result}")
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=save_assignment
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=10)
    
    def _edit_assignment(self) -> None:
        """Edit the selected assignment."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        assignment_id = self.tree.item(selected_items[0], "values")[0]
        assignment = self.master.master.assignment_controller.get_by_id(assignment_id)
        
        if not assignment:
            messagebox.showerror("Error", "Selected assignment not found.")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Assignment")
        dialog.geometry("600x500")
        dialog.grab_set()
        
        # Make dialog modal
        dialog.transient(self)
        dialog.focus_set()
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog, corner_radius=0)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Get employees and locations for dropdowns
        employees = self.master.master.employee_controller.get_all()
        locations = self.master.master.location_controller.get_all()
        
        # Employee selection
        ctk.CTkLabel(form_frame, text="Employee:").grid(row=0, column=0, sticky="w", pady=(10, 5))
        employee_var = tk.StringVar(value=f"{assignment['employe_id']} - {assignment['employee_nom']} {assignment['employee_prenom']}")
        employee_dropdown = ctk.CTkComboBox(
            form_frame,
            variable=employee_var,
            values=[f"{emp['id']} - {emp['nom']} {emp['prenom']}" for emp in employees],
            width=400,
            state="readonly"
        )
        employee_dropdown.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 5))
        
        # Location selection
        ctk.CTkLabel(form_frame, text="Location:").grid(row=1, column=0, sticky="w", pady=5)
        location_var = tk.StringVar(value=f"{assignment['lieu_id']} - {assignment['lieu_nom']}")
        location_dropdown = ctk.CTkComboBox(
            form_frame,
            variable=location_var,
            values=[f"{loc['id']} - {loc['nom']}" for loc in locations],
            width=400,
            state="readonly"
        )
        location_dropdown.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Start date
        ctk.CTkLabel(form_frame, text="Start Date:").grid(row=2, column=0, sticky="w", pady=5)
        start_date_var = tk.StringVar(value=assignment["date_debut"].strftime("%Y-%m-%d"))
        start_date_entry = ctk.CTkEntry(
            form_frame,
            textvariable=start_date_var,
            width=150
        )
        start_date_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # End date
        ctk.CTkLabel(form_frame, text="End Date:").grid(row=3, column=0, sticky="w", pady=5)
        end_date_var = tk.StringVar()
        if assignment["date_fin"]:
            end_date_var.set(assignment["date_fin"].strftime("%Y-%m-%d"))
        end_date_entry = ctk.CTkEntry(
            form_frame,
            textvariable=end_date_var,
            placeholder_text="Leave empty for open-ended assignment",
            width=200
        )
        end_date_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Notes
        ctk.CTkLabel(form_frame, text="Notes:").grid(row=4, column=0, sticky="nw", pady=5)
        notes_text = ctk.CTkTextbox(form_frame, width=400, height=100)
        notes_text.insert("1.0", assignment.get("notes", ""))
        notes_text.grid(row=4, column=1, sticky="nsew", padx=10, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def update_assignment():
            """Update the assignment."""
            # Parse dates
            try:
                start_date = datetime.strptime(start_date_var.get(), "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_var.get(), "%Y-%m-%d").date() if end_date_var.get() else None
                
                if end_date and end_date < start_date:
                    messagebox.showerror("Error", "End date cannot be before start date.")
                    return
                    
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                return
            
            # Prepare data
            data = {
                "date_debut": start_date,
                "date_fin": end_date,
                "notes": notes_text.get("1.0", "end-1c").strip()
            }
            
            # Update assignment
            success, result = self.master.master.assignment_controller.update(assignment_id, data)
            
            if success:
                messagebox.showinfo("Success", "Assignment updated successfully!")
                self._load_assignments()
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"Failed to update assignment: {result}")
        
        ctk.CTkButton(
            button_frame,
            text="Update",
            command=update_assignment
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=10)
    
    def _end_assignment(self) -> None:
        """End the selected assignment."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        assignment_id = self.tree.item(selected_items[0], "values")[0]
        assignment = self.master.master.assignment_controller.get_by_id(assignment_id)
        
        if not assignment:
            messagebox.showerror("Error", "Selected assignment not found.")
            return
            
        if assignment["date_fin"]:
            messagebox.showinfo("Info", "This assignment is already ended.")
            return
            
        if messagebox.askyesno(
            "Confirm End Assignment",
            f"Are you sure you want to end this assignment?\n"
            f"Employee: {assignment['employee_nom']} {assignment['employee_prenom']}\n"
            f"Location: {assignment['lieu_nom']}"
        ):
            # Set end date to today
            data = {
                "date_fin": datetime.now().date()
            }
            
            success, result = self.master.master.assignment_controller.update(assignment_id, data)
            
            if success:
                messagebox.showinfo("Success", "Assignment ended successfully!")
                self._load_assignments()
                self.end_btn.configure(state="disabled")
            else:
                messagebox.showerror("Error", f"Failed to end assignment: {result}")
    
    def _delete_assignment(self) -> None:
        """Delete the selected assignment."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        assignment_id = self.tree.item(selected_items[0], "values")[0]
        employee_name = self.tree.item(selected_items[0], "values")[1]
        location_name = self.tree.item(selected_items[0], "values")[2]
        
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this assignment?\n\n"
            f"Employee: {employee_name}\n"
            f"Location: {location_name}\n\n"
            "This action cannot be undone."
        ):
            success, result = self.master.master.assignment_controller.delete(assignment_id)
            
            if success:
                messagebox.showinfo("Success", "Assignment deleted successfully!")
                self._load_assignments()
                self.edit_btn.configure(state="disabled")
                self.end_btn.configure(state="disabled")
                self.delete_btn.configure(state="disabled")
            else:
                messagebox.showerror("Error", f"Failed to delete assignment: {result}")
    
    def on_show(self) -> None:
        """Called when the view is shown."""
        self._load_assignments()
        self.edit_btn.configure(state="disabled")
        self.end_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        
        # Clear selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
