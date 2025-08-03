import os
import sys

# Test file writing
with open('test_output.txt', 'w') as f:
    f.write("This is a test file.\n")
    f.write(f"Current directory: {os.getcwd()}\n")
    f.write(f"Python version: {sys.version}\n")

# Print to console
print("This is a test print statement.")
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")

# Create a simple window
import tkinter as tk
root = tk.Tk()
root.title("Test Window")
label = tk.Label(root, text="If you can see this, Tkinter is working!")
label.pack(padx=20, pady=20)
root.after(3000, root.destroy)  # Close after 3 seconds
root.mainloop()

# Indicate completion
with open('test_output.txt', 'a') as f:
    f.write("Test completed successfully!\n")
