import os
import sys
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Integration Test")
        self.root.geometry("800x600")
        
        # Database connection
        self.db_path = os.path.abspath('test_employee_assignments.db')
        self.conn = None
        
        # Create UI
        self.create_widgets()
        
        # Test database connection
        self.test_connection()
    
    def create_widgets(self):
        """Create the UI elements."""
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Database info
        info_frame = ttk.LabelFrame(main_frame, text="Database Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Database: {os.path.basename(self.db_path)}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Path: {self.db_path}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Exists: {'Yes' if os.path.exists(self.db_path) else 'No'}").pack(anchor=tk.W)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Test Connection", command=self.test_connection).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load Locations", command=self.load_locations).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Test Data", command=self.add_test_data).pack(side=tk.LEFT, padx=5)
        
        # Treeview for locations
        tree_frame = ttk.LabelFrame(main_frame, text="Locations", padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbars
        self.tree = ttk.Treeview(tree_frame, columns=('idlieu', 'design', 'province'), show='headings')
        
        # Define headings
        self.tree.heading('idlieu', text='ID')
        self.tree.heading('design', text='Designation')
        self.tree.heading('province', text='Province')
        
        # Set column widths
        self.tree.column('idlieu', width=100, anchor=tk.CENTER)
        self.tree.column('design', width=200, anchor=tk.W)
        self.tree.column('province', width=150, anchor=tk.W)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def test_connection(self):
        """Test database connection and update status."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = ', '.join([t[0] for t in tables]) if tables else 'No tables found'
            self.status_var.set(f"Connected to database. Tables: {table_names}")
            return True
        except Exception as e:
            self.status_var.set(f"Connection failed: {str(e)}")
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def load_locations(self):
        """Load locations from the database into the treeview."""
        if not self.test_connection():
            return
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Fetch locations
            cursor.execute("SELECT idlieu, design, province FROM LIEU")
            locations = cursor.fetchall()
            
            if not locations:
                self.status_var.set("No locations found in the database.")
                return
            
            # Add locations to treeview
            for loc in locations:
                self.tree.insert('', tk.END, values=loc)
            
            self.status_var.set(f"Loaded {len(locations)} locations from the database.")
            
        except Exception as e:
            self.status_var.set(f"Error loading locations: {str(e)}")
        finally:
            if self.conn:
                self.conn.close()
    
    def add_test_data(self):
        """Add test data to the database."""
        if not self.test_connection():
            return
        
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS LIEU (
                idlieu TEXT PRIMARY KEY,
                design TEXT NOT NULL,
                province TEXT NOT NULL
            )
            ''')
            
            # Add test data
            test_data = [
                ('L1', 'Antananarivo', 'Antananarivo'),
                ('L2', 'Toamasina', 'Toamasina'),
                ('L3', 'Antsirabe', 'Antananarivo'),
                ('L4', 'Fianarantsoa', 'Fianarantsoa'),
                ('L5', 'Mahajanga', 'Mahajanga')
            ]
            
            cursor.executemany("""
                INSERT OR REPLACE INTO LIEU (idlieu, design, province) 
                VALUES (?, ?, ?)
            """, test_data)
            
            self.conn.commit()
            self.status_var.set(f"Added {len(test_data)} test locations to the database.")
            
            # Refresh the view
            self.load_locations()
            
        except Exception as e:
            self.status_var.set(f"Error adding test data: {str(e)}")
        finally:
            if self.conn:
                self.conn.close()

def main():
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
