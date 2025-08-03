"""
Location view for the Employee Assignment Management System.
This module provides the UI for managing locations.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from typing import Any, Dict, List, Optional, Tuple, Callable

from .base_view import BaseView

class LocationView(BaseView):
    """View for managing locations."""
    
    def _create_widgets(self) -> None:
        """Create and arrange the widgets for the location management."""
        # Create main container
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Changed from 1 to 2 to match the treeview row
        
        # Header
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(
            header_frame, 
            text="Locations", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        # Add location button
        add_btn = ctk.CTkButton(
            header_frame, 
            text="+ Add Location",
            command=self._show_add_location_dialog
        )
        add_btn.pack(side="right", padx=10)
        
        # Search frame
        search_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        search_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            search_frame, 
            text="Search:"
        ).pack(side="left", padx=(10, 5), pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._on_search_changed)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search locations...",
            width=300
        )
        search_entry.pack(side="left", padx=(0, 10), pady=10)
        
        # Locations treeview
        tree_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("idlieu", "design", "province"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.tree.heading("idlieu", text="ID")
        self.tree.heading("design", text="Designation")
        self.tree.heading("province", text="Province")
        
        self.tree.column("idlieu", width=100, anchor="center")
        self.tree.column("design", width=250)
        self.tree.column("province", width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview
        self.tree.pack(fill="both", expand=True)
        
        # Bind double click event
        self.tree.bind("<Double-1>", self._on_location_selected)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        button_frame.grid(row=3, column=0, sticky="e", padx=10, pady=(0, 10))
        
        # Action buttons
        self.edit_btn = ctk.CTkButton(
            button_frame,
            text="Edit",
            command=self._edit_location,
            state="disabled"
        )
        self.edit_btn.pack(side="left", padx=5)
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self._delete_location,
            fg_color="#d9534f",
            hover_color="#c9302c",
            state="disabled"
        )
        self.delete_btn.pack(side="left", padx=5)
        
        # Store the main frame as the content
        self.content = self.main_frame
        
        # Load locations
        self._load_locations()
    
    def _load_locations(self, search_query: str = "") -> None:
        """Load locations into the treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get locations from controller
        locations = self.master.master.location_controller.get_all()
        
        # Debug: Print the number of locations retrieved
        print(f"DEBUG: Retrieved {len(locations)} locations from controller")
        
        # Filter locations if search query is provided
        if search_query:
            search_lower = search_query.lower()
            locations = [
                loc for loc in locations 
                if (search_lower in loc.design.lower() or 
                     search_lower in loc.province.lower())
            ]
            print(f"DEBUG: Filtered to {len(locations)} locations after search")
        
        # Debug: Print the first few locations
        for i, loc in enumerate(locations[:3]):
            print(f"DEBUG: Location {i+1}: id={loc.idlieu}, design={loc.design}, province={loc.province}")
        
        # Add locations to treeview
        for loc in locations:
            self.tree.insert(
                "", "end",
                values=(
                    loc.idlieu,
                    loc.design,
                    loc.province
                )
            )
        
        # Debug: Print treeview items count
        print(f"DEBUG: Treeview now has {len(self.tree.get_children())} items")
    
    def _on_search_changed(self, *args) -> None:
        """Handle search query changes."""
        search_query = self.search_var.get()
        self._load_locations(search_query)
    
    def _on_location_selected(self, event) -> None:
        """Handle location selection in the treeview."""
        selected_items = self.tree.selection()
        if selected_items:
            self.edit_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
    
    def _show_add_location_dialog(self) -> None:
        """Show the add location dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Location")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        # Make dialog modal
        dialog.transient(self)
        dialog.focus_set()
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog, corner_radius=0)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=(10, 5))
        name_entry = ctk.CTkEntry(form_frame, width=300)
        name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(form_frame, text="Address:").grid(row=1, column=0, sticky="w", pady=5)
        address_entry = ctk.CTkEntry(form_frame, width=300)
        address_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="City:").grid(row=2, column=0, sticky="w", pady=5)
        city_entry = ctk.CTkEntry(form_frame, width=300)
        city_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Capacity:").grid(row=3, column=0, sticky="w", pady=5)
        capacity_entry = ctk.CTkEntry(form_frame, width=100)
        capacity_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def save_location():
            """Save the new location."""
            data = {
                "nom": name_entry.get().strip(),
                "adresse": address_entry.get().strip(),
                "ville": city_entry.get().strip(),
                "capacite": capacity_entry.get().strip()
            }
            
            # Validate data
            if not all(data.values()):
                messagebox.showerror("Error", "All fields are required.")
                return
                
            try:
                data["capacite"] = int(data["capacite"])
                if data["capacite"] <= 0:
                    raise ValueError("Capacity must be a positive number")
            except ValueError:
                messagebox.showerror("Error", "Capacity must be a positive integer.")
                return
            
            # Save location
            success, result = self.master.master.location_controller.create(data)
            
            if success:
                messagebox.showinfo("Success", "Location added successfully!")
                self._load_locations()
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"Failed to add location: {result}")
        
        ctk.CTkButton(
            button_frame,
            text="Save",
            command=save_location
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=10)
    
    def _edit_location(self) -> None:
        """Edit the selected location."""
        selected_items = self.tree.selection()
        if not selected_items:
            return
            
        location_id = self.tree.item(selected_items[0], "values")[0]
        location = self.master.master.location_controller.get_by_id(location_id)
        
        if not location:
            messagebox.showerror("Error", "Selected location not found.")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Location")
        dialog.geometry("500x400")
        dialog.grab_set()
        
        # Make dialog modal
        dialog.transient(self)
        dialog.focus_set()
        
        # Form frame
        form_frame = ctk.CTkFrame(dialog, corner_radius=0)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        ctk.CTkLabel(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=(10, 5))
        name_entry = ctk.CTkEntry(form_frame, width=300)
        name_entry.insert(0, location.nom)
        name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(form_frame, text="Address:").grid(row=1, column=0, sticky="w", pady=5)
        address_entry = ctk.CTkEntry(form_frame, width=300)
        address_entry.insert(0, location.adresse)
        address_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="City:").grid(row=2, column=0, sticky="w", pady=5)
        city_entry = ctk.CTkEntry(form_frame, width=300)
        city_entry.insert(0, location.ville)
        city_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Capacity:").grid(row=3, column=0, sticky="w", pady=5)
        capacity_entry = ctk.CTkEntry(form_frame, width=100)
        capacity_entry.insert(0, str(location.capacite))
        capacity_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def update_location():
            """Update the location."""
            data = {
                "nom": name_entry.get().strip(),
                "adresse": address_entry.get().strip(),
                "ville": city_entry.get().strip(),
                "capacite": capacity_entry.get().strip()
            }
            
            # Validate data
            if not all(data.values()):
                messagebox.showerror("Error", "All fields are required.")
                return
                
            try:
                data["capacite"] = int(data["capacite"])
                if data["capacite"] <= 0:
                    raise ValueError("Capacity must be a positive number")
            except ValueError:
                messagebox.showerror("Error", "Capacity must be a positive integer.")
                return
            
            # Update location
            success, result = self.master.master.location_controller.update(location_id, data)
            
            if success:
                messagebox.showinfo("Success", "Location updated successfully!")
                self._load_locations()
                dialog.destroy()
            else:
                messagebox.showerror("Error", f"Failed to update location: {result}")
        
        ctk.CTkButton(
            button_frame,
            text="Update",
            command=update_location
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=dialog.destroy
        ).pack(side="left", padx=10)
    
    def _delete_location(self):
        """Delete the selected location."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a location to delete.")
            return
            
        location_id = self.tree.item(selected_items[0], "values")[0]
        location_design = self.tree.item(selected_items[0], "values")[1]
        
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the location '{location_design}'?\nThis action cannot be undone."
        ):
            success, result = self.master.master.location_controller.delete(location_id)
            
            if success:
                messagebox.showinfo("Success", f"Location '{location_design}' has been deleted.")
                self._load_locations()  # Refresh the list
            else:
                messagebox.showerror("Error", f"Failed to delete location: {result}")
    
    def on_show(self):
        """Called when the view is shown."""
        # Load locations when the view is shown
        self._load_locations()
        
        # Enable/disable buttons based on selection
        selected = bool(self.tree.selection())
        self.edit_btn.configure(state="normal" if selected else "disabled")
        self.delete_btn.configure(state="normal" if selected else "disabled")
        
        # Clear selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
