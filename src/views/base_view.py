"""
Base view class for the Employee Assignment Management System.
This module provides a base class for all views in the application.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

class BaseView(ctk.CTkFrame):
    """Base view class that provides common functionality for all views."""
    
    def __init__(self, parent: Any, controller: Any = None, **kwargs):
        """Initialize the base view.
        
        Args:
            parent: Parent widget
            controller: Controller that manages this view
            **kwargs: Additional arguments to pass to the parent class
        """
        super().__init__(parent, **kwargs)
        self.controller = controller
        self._setup_style()
        self._create_widgets()
        
    def _setup_style(self) -> None:
        """Set up the style for this view."""
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Set default font
        self.default_font = ctk.CTkFont(family="Segoe UI", size=12)
        self.title_font = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        
    def _create_widgets(self) -> None:
        """Create the widgets for this view. Should be implemented by subclasses."""
        pass
        
    def show_info(self, title: str, message: str) -> None:
        """Show an information message.
        
        Args:
            title: Dialog title
            message: Message to display
        """
        ctk.CTkMessagebox(
            title=title,
            message=message,
            icon="info"
        )
        
    def show_error(self, title: str, message: str) -> None:
        """Show an error message.
        
        Args:
            title: Dialog title
            message: Error message to display
        """
        ctk.CTkMessagebox(
            title=title,
            message=message,
            icon="cancel"
        )
        
    def ask_yesno(self, title: str, message: str) -> bool:
        """Ask a yes/no question.
        
        Args:
            title: Dialog title
            message: Question to ask
            
        Returns:
            bool: True if user clicked Yes, False otherwise
        """
        result = ctk.CTkMessagebox(
            title=title,
            message=message,
            icon="question",
            option_1="No",
            option_2="Yes"
        )
        return result.get() == "Yes"
    
    def create_form_field(
        self, 
        parent: Any, 
        label: str, 
        row: int, 
        widget_class: Type[tk.Widget] = ctk.CTkEntry,
        **kwargs
    ) -> Any:
        """Create a form field with a label.
        
        Args:
            parent: Parent widget
            label: Field label
            row: Grid row
            widget_class: Widget class to create
            **kwargs: Additional arguments to pass to the widget
            
        Returns:
            The created widget
        """
        # Create label
        label_widget = ctk.CTkLabel(parent, text=label, font=self.default_font)
        label_widget.grid(row=row, column=0, padx=5, pady=5, sticky="e")
        
        # Create widget
        widget = widget_class(parent, **kwargs)
        widget.grid(row=row, column=1, padx=5, pady=5, sticky="ew")
        
        return widget
    
    def create_button(
        self, 
        parent: Any, 
        text: str, 
        command: Callable,
        row: int, 
        column: int = 0,
        columnspan: int = 1,
        **kwargs
    ) -> ctk.CTkButton:
        """Create a styled button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Command to execute when clicked
            row: Grid row
            column: Grid column
            columnspan: Number of columns to span
            **kwargs: Additional arguments to pass to the button
            
        Returns:
            The created button
        """
        button = ctk.CTkButton(
            parent, 
            text=text, 
            command=command,
            font=self.default_font,
            **kwargs
        )
        button.grid(
            row=row, 
            column=column, 
            columnspan=columnspan,
            padx=5, 
            pady=5, 
            sticky="ew"
        )
        return button
    
    def create_treeview(
        self,
        parent: Any,
        columns: List[Dict[str, Any]],
        show_headings: bool = True,
        select_mode: str = "browse",
        **kwargs
    ) -> ttk.Treeview:
        """Create a Treeview widget with the specified columns.
        
        Args:
            parent: Parent widget
            columns: List of column definitions. Each definition is a dict with:
                - id: Column ID
                - text: Column header text
                - width: Column width in pixels
                - anchor: Text alignment (e.g., 'w' for left, 'e' for right, 'center')
                - stretch: Whether the column should stretch with the widget
            show_headings: Whether to show column headings
            select_mode: Selection mode ('browse', 'extended', 'none')
            **kwargs: Additional arguments to pass to the Treeview
            
        Returns:
            The created Treeview widget
        """
        # Create the Treeview
        style = ttk.Style()
        style.theme_use("default")
        
        # Configure the style to match the app theme
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#1f6aa5",
            foreground="white",
            relief="flat"
        )
        style.map(
            "Treeview",
            background=[('selected', '#1f6aa5')],
            foreground=[('selected', 'white')]
        )
        
        # Create the Treeview
        tree = ttk.Treeview(
            parent,
            columns=[col['id'] for col in columns if col['id'] != '#0'],
            show='headings' if show_headings else '',
            selectmode=select_mode,
            **kwargs
        )
        
        # Configure columns
        for col in columns:
            col_id = col['id']
            
            if col_id == '#0':
                # Tree column
                tree.column(
                    col_id,
                    width=col.get('width', 100),
                    anchor=col.get('anchor', 'w'),
                    stretch=col.get('stretch', True)
                )
                tree.heading(col_id, text=col['text'])
            else:
                # Regular column
                tree.column(
                    col_id,
                    width=col.get('width', 100),
                    anchor=col.get('anchor', 'w'),
                    stretch=col.get('stretch', True)
                )
                tree.heading(col_id, text=col['text'])
        
        # Add scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid the tree and scrollbars
        tree.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(0, 5))
        vsb.grid(row=0, column=1, sticky="ns", pady=(0, 5))
        hsb.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        
        # Configure grid weights
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        return tree
    
    def clear_widgets(self) -> None:
        """Clear all widgets from this view."""
        for widget in self.winfo_children():
            widget.destroy()
            
    def update_status(self, message: str, is_error: bool = False) -> None:
        """Update the status bar if available.
        
        Args:
            message: Status message to display
            is_error: Whether this is an error message
        """
        if hasattr(self.controller, 'update_status'):
            self.controller.update_status(message, is_error)
    
    def on_show(self) -> None:
        """Called when the view is shown. Can be overridden by subclasses."""
        pass
    
    def on_hide(self) -> None:
        """Called when the view is hidden. Can be overridden by subclasses."""
        pass
