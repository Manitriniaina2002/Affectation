import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def test_tkinter():
    """Test basic Tkinter functionality."""
    print("Starting Tkinter test...")
    
    # Create main window
    root = tk.Tk()
    root.title("Tkinter Test")
    root.geometry("400x300")
    
    # Add a label
    label = ttk.Label(root, text="Tkinter is working!", font=('Arial', 14))
    label.pack(pady=20)
    
    # Add a button
    def on_click():
        messagebox.showinfo("Test", "Button clicked!")
    
    button = ttk.Button(root, text="Click Me!", command=on_click)
    button.pack(pady=10)
    
    # Add a treeview
    tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    
    # Add sample data
    for i in range(5):
        tree.insert("", "end", values=(i, f"Item {i}"))
    
    tree.pack(pady=20, padx=10, fill="both", expand=True)
    
    print("Tkinter window should be visible now.")
    print("If you can see the window, Tkinter is working correctly.")
    
    root.mainloop()

if __name__ == "__main__":
    test_tkinter()
    print("Test completed.")
