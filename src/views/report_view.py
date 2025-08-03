"""
Report view for the Employee Assignment Management System.
This module provides reporting functionality for the application.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Callable
import csv
import os

from .base_view import BaseView

class ReportView(BaseView):
    """View for generating and viewing reports."""
    
    def _create_widgets(self) -> None:
        """Create and arrange the widgets for the reports view."""
        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text="Reports", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        # Report type selection frame
        report_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        report_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Report type selection
        ctk.CTkLabel(
            report_frame,
            text="Report Type:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.report_type = tk.StringVar(value="assignments")
        
        # Report type options
        report_types = [
            ("Assignments by Date Range", "assignments"),
            ("Current Assignments", "current_assignments"),
            ("Unassigned Employees", "unassigned"),
            ("Location Utilization", "utilization")
        ]
        
        for i, (text, value) in enumerate(report_types, 1):
            rb = ctk.CTkRadioButton(
                report_frame,
                text=text,
                variable=self.report_type,
                value=value,
                command=self._on_report_type_changed
            )
            rb.grid(row=i, column=0, sticky="w", pady=2, padx=20)
        
        # Date range frame (initially hidden)
        self.date_frame = ctk.CTkFrame(report_frame, corner_radius=0)
        
        ctk.CTkLabel(
            self.date_frame,
            text="Date Range:"
        ).grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        # Start date
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        self.start_date_entry = ctk.CTkEntry(
            self.date_frame,
            textvariable=self.start_date_var,
            width=120
        )
        self.start_date_entry.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(
            self.date_frame,
            text="to"
        ).grid(row=0, column=2, padx=5)
        
        # End date
        self.end_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.end_date_entry = ctk.CTkEntry(
            self.date_frame,
            textvariable=self.end_date_var,
            width=120
        )
        self.end_date_entry.grid(row=0, column=3, padx=5)
        
        # Location selection (for utilization report)
        self.location_frame = ctk.CTkFrame(report_frame, corner_radius=0)
        
        ctk.CTkLabel(
            self.location_frame,
            text="Location:"
        ).pack(side="left", padx=(0, 10))
        
        self.location_var = tk.StringVar()
        self.location_dropdown = ctk.CTkComboBox(
            self.location_frame,
            variable=self.location_var,
            width=300,
            state="readonly"
        )
        self.location_dropdown.pack(side="left")
        
        # Button frame
        button_frame = ctk.CTkFrame(report_frame, corner_radius=0)
        button_frame.grid(row=10, column=0, sticky="e", pady=20)
        
        # Generate report button
        generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate Report",
            command=self._generate_report,
            width=150
        )
        generate_btn.pack(side="left", padx=5)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            button_frame,
            text="Export to CSV",
            command=self._export_to_csv,
            width=120,
            state="disabled"
        )
        self.export_btn.pack(side="left", padx=5)
        
        # Results frame
        results_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        results_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview for results
        self.tree = ttk.Treeview(
            results_frame,
            columns=(),
            show="headings",
            selectmode="browse"
        )
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(results_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        # Store the main frame as the content
        self.content = self.main_frame
        
        # Store report data
        self.report_data = []
        
        # Initialize UI
        self._on_report_type_changed()
    
    def _on_report_type_changed(self) -> None:
        """Handle report type selection change."""
        report_type = self.report_type.get()
        
        # Show/hide date frame
        if report_type == "assignments":
            self.date_frame.grid(row=6, column=0, sticky="w", pady=10, padx=20)
            self.location_frame.grid_remove()
        elif report_type == "utilization":
            self.date_frame.grid_remove()
            self.location_frame.grid(row=6, column=0, sticky="w", pady=10, padx=20)
            self._load_locations()
        else:
            self.date_frame.grid_remove()
            self.location_frame.grid_remove()
    
    def _load_locations(self) -> None:
        """Load locations into the dropdown."""
        locations = self.master.master.location_controller.get_all()
        location_options = [f"{loc['id']} - {loc['nom']}" for loc in locations]
        self.location_dropdown.configure(values=location_options)
        if location_options:
            self.location_var.set(location_options[0])
    
    def _generate_report(self) -> None:
        """Generate the selected report."""
        report_type = self.report_type.get()
        
        try:
            if report_type == "assignments":
                self._generate_assignments_report()
            elif report_type == "current_assignments":
                self._generate_current_assignments_report()
            elif report_type == "unassigned":
                self._generate_unassigned_report()
            elif report_type == "utilization":
                self._generate_utilization_report()
                
            self.export_btn.configure(state="normal")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def _generate_assignments_report(self) -> None:
        """Generate assignments report for the selected date range."""
        try:
            start_date = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date_var.get(), "%Y-%m-%d")
            
            if start_date > end_date:
                messagebox.showerror("Error", "Start date cannot be after end date.")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        
        # Get assignments in date range
        assignments = self.master.master.assignment_controller.get_by_date_range(start_date, end_date)
        
        # Configure treeview columns
        self._clear_tree()
        self.tree["columns"] = ("id", "employee", "location", "start_date", "end_date", "status")
        
        # Configure column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("employee", text="Employee")
        self.tree.heading("location", text="Location")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("end_date", text="End Date")
        self.tree.heading("status", text="Status")
        
        # Configure column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("employee", width=200)
        self.tree.column("location", width=200)
        self.tree.column("start_date", width=100, anchor="center")
        self.tree.column("end_date", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        
        # Add data to treeview
        self.report_data = []
        for assignment in assignments:
            status = "Active" if not assignment["date_fin"] else "Completed"
            
            # Format dates
            start_date = assignment["date_debut"].strftime("%Y-%m-%d")
            end_date = assignment["date_fin"].strftime("%Y-%m-%d") if assignment["date_fin"] else "-"
            
            # Add to treeview
            self.tree.insert(
                "", "end",
                values=(
                    assignment["id"],
                    f"{assignment['employee_nom']} {assignment['employee_prenom']}",
                    assignment["lieu_nom"],
                    start_date,
                    end_date,
                    status
                )
            )
            
            # Store data for export
            self.report_data.append({
                "ID": assignment["id"],
                "Employee": f"{assignment['employee_nom']} {assignment['employee_prenorn']}",
                "Location": assignment["lieu_nom"],
                "Start Date": start_date,
                "End Date": end_date,
                "Status": status
            })
    
    def _generate_current_assignments_report(self) -> None:
        """Generate report of current assignments."""
        # Get current date
        current_date = datetime.now().date()
        
        # Get all assignments
        assignments = self.master.master.assignment_controller.get_all()
        
        # Filter current assignments (start date <= today and (no end date or end date >= today))
        current_assignments = [
            a for a in assignments 
            if a["date_debut"].date() <= current_date and 
               (a["date_fin"] is None or a["date_fin"].date() >= current_date)
        ]
        
        # Configure treeview columns
        self._clear_tree()
        self.tree["columns"] = ("id", "employee", "location", "start_date", "days_assigned")
        
        # Configure column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("employee", text="Employee")
        self.tree.heading("location", text="Location")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("days_assigned", text="Days Assigned")
        
        # Configure column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("employee", width=200)
        self.tree.column("location", width=200)
        self.tree.column("start_date", width=100, anchor="center")
        self.tree.column("days_assigned", width=100, anchor="center")
        
        # Add data to treeview
        self.report_data = []
        for assignment in current_assignments:
            # Calculate days assigned
            days_assigned = (current_date - assignment["date_debut"].date()).days
            
            # Add to treeview
            self.tree.insert(
                "", "end",
                values=(
                    assignment["id"],
                    f"{assignment['employee_nom']} {assignment['employee_prenom']}",
                    assignment["lieu_nom"],
                    assignment["date_debut"].strftime("%Y-%m-%d"),
                    f"{days_assigned} days"
                )
            )
            
            # Store data for export
            self.report_data.append({
                "ID": assignment["id"],
                "Employee": f"{assignment['employee_nom']} {assignment['employee_prenorn']}",
                "Location": assignment["lieu_nom"],
                "Start Date": assignment["date_debut"].strftime("%Y-%m-%d"),
                "Days Assigned": days_assigned
            })
    
    def _generate_unassigned_report(self) -> None:
        """Generate report of unassigned employees."""
        # Get all employees
        employees = self.master.master.employee_controller.get_all()
        
        # Get current assignments
        assignments = self.master.master.assignment_controller.get_all()
        
        # Get set of assigned employee IDs
        assigned_employee_ids = {a["employe_id"] for a in assignments if not a["date_fin"]}
        
        # Find unassigned employees
        unassigned_employees = [e for e in employees if e["id"] not in assigned_employee_ids]
        
        # Configure treeview columns
        self._clear_tree()
        self.tree["columns"] = ("id", "name", "email", "position", "hire_date")
        
        # Configure column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("position", text="Position")
        self.tree.heading("hire_date", text="Hire Date")
        
        # Configure column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("email", width=200)
        self.tree.column("position", width=150)
        self.tree.column("hire_date", width=100, anchor="center")
        
        # Add data to treeview
        self.report_data = []
        for emp in unassigned_employees:
            # Add to treeview
            self.tree.insert(
                "", "end",
                values=(
                    emp["id"],
                    f"{emp['nom']} {emp['prenom']}",
                    emp["email"],
                    emp.get("poste", ""),
                    emp.get("date_embauche", "").strftime("%Y-%m-%d") if emp.get("date_embauche") else ""
                )
            )
            
            # Store data for export
            self.report_data.append({
                "ID": emp["id"],
                "Name": f"{emp['nom']} {emp['prenom']}",
                "Email": emp["email"],
                "Position": emp.get("poste", ""),
                "Hire Date": emp.get("date_embauche", "").strftime("%Y-%m-%d") if emp.get("date_embauche") else ""
            })
    
    def _generate_utilization_report(self) -> None:
        """Generate location utilization report."""
        # Get selected location
        location_str = self.location_var.get()
        if not location_str:
            messagebox.showerror("Error", "Please select a location.")
            return
            
        try:
            location_id = int(location_str.split(" - ")[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid location selected.")
            return
        
        # Get location details
        location = self.master.master.location_controller.get_by_id(location_id)
        if not location:
            messagebox.showerror("Error", "Selected location not found.")
            return
        
        # Get current assignments at this location
        current_assignments = self.master.master.assignment_controller.get_current_assignments(location_id=location_id)
        
        # Calculate utilization
        total_capacity = location["capacite"]
        current_usage = len(current_assignments)
        utilization_pct = (current_usage / total_capacity * 100) if total_capacity > 0 else 0
        
        # Configure treeview columns
        self._clear_tree()
        self.tree["columns"] = ("metric", "value")
        
        # Configure column headings
        self.tree.heading("metric", text="Metric")
        self.tree.heading("value", text="Value")
        
        # Configure column widths
        self.tree.column("metric", width=200, anchor="w")
        self.tree.column("value", width=400, anchor="w")
        
        # Add summary data
        self.tree.insert("", "end", values=("Location", f"{location['nom']} (ID: {location['id']})"))
        self.tree.insert("", "end", values=("Address", f"{location['adresse']}, {location['ville']}"))
        self.tree.insert("", "end", values=("Total Capacity", total_capacity))
        self.tree.insert("", "end", values=("Current Assignments", current_usage))
        self.tree.insert("", "end", values=("Utilization", f"{utilization_pct:.1f}%"))
        
        # Add separator
        self.tree.insert("", "end", values=("-" * 50, "-" * 50))
        
        # Add current assignments
        self.tree.insert("", "end", values=("Current Assignments:", ""))
        
        for i, assignment in enumerate(current_assignments, 1):
            self.tree.insert(
                "", "end",
                values=(
                    f"  {i}. {assignment['employee_nom']} {assignment['employee_prenom']}",
                    f"Since: {assignment['date_debut'].strftime('%Y-%m-%d')}"
                )
            )
        
        # Store data for export
        self.report_data = [
            {"Metric": "Location", "Value": f"{location['nom']} (ID: {location['id']})"},
            {"Metric": "Address", "Value": f"{location['adresse']}, {location['ville']}"},
            {"Metric": "Total Capacity", "Value": total_capacity},
            {"Metric": "Current Assignments", "Value": current_usage},
            {"Metric": "Utilization", "Value": f"{utilization_pct:.1f}%"},
            {"Metric": "-", "Value": "-"},
            {"Metric": "Current Assignments:", "Value": ""}
        ]
        
        for i, assignment in enumerate(current_assignments, 1):
            self.report_data.append({
                "Metric": f"  {i}. {assignment['employee_nom']} {assignment['employee_prenom']}",
                "Value": f"Since: {assignment['date_debut'].strftime('%Y-%m-%d')}"
            })
    
    def _export_to_csv(self) -> None:
        """Export the current report to a CSV file."""
        if not self.report_data:
            messagebox.showinfo("Info", "No data to export.")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Report As"
        )
        
        if not file_path:
            return  # User cancelled
        
        try:
            # Get fieldnames from the first data row
            fieldnames = list(self.report_data[0].keys())
            
            # Write to CSV
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.report_data)
            
            messagebox.showinfo("Success", f"Report exported successfully to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def _clear_tree(self) -> None:
        """Clear the treeview and reset columns."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Clear existing columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text="")
            self.tree.column(col, width=0, minwidth=0, stretch=tk.NO)
        
        # Reset columns
        self.tree["columns"] = ()
    
    def on_show(self) -> None:
        """Called when the view is shown."""
        # Reset the view
        self.report_type.set("assignments")
        self._on_report_type_changed()
        self._clear_tree()
        self.export_btn.configure(state="disabled")
        self.report_data = []
