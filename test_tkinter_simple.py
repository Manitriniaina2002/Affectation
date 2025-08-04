import tkinter as tk
import sys

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Tkinter Test")
    
    # Add a label
    label = tk.Label(root, text="Tkinter is working!")
    label.pack(padx=20, pady=20)
    
    # Add a quit button
    button = tk.Button(root, text="Quit", command=root.quit)
    button.pack(pady=10)
    
    # Log to a file
    with open("tkinter_test.log", "w") as f:
        f.write("Tkinter test started\n")
        f.write(f"Python version: {sys.version}\n")
    
    # Start the main loop
    root.mainloop()
    
    # Log when the window is closed
    with open("tkinter_test.log", "a") as f:
        f.write("Tkinter test completed\n")

if __name__ == "__main__":
    main()
