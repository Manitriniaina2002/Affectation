import sys
import os
import platform
import sqlite3
import tkinter as tk
from tkinter import ttk

def check_environment():
    """Check Python environment and basic functionality."""
    print("=" * 50)
    print("Python Environment Check")
    print("=" * 50)
    
    # Basic Python info
    print("\nPython Version:")
    print(f"Python {sys.version}")
    print(f"Executable: {sys.executable}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Platform: {platform.platform()}")
    
    # Check file system access
    print("\nFile System Access:")
    test_file = "test_env_check.txt"
    try:
        with open(test_file, 'w') as f:
            f.write("Test file created successfully.\n")
        print(f"✓ Successfully wrote to {test_file}")
        os.remove(test_file)
        print(f"✓ Successfully deleted {test_file}")
    except Exception as e:
        print(f"✗ File system access error: {str(e)}")
    
    # Check SQLite
    print("\nSQLite Check:")
    try:
        print(f"SQLite Version: {sqlite3.sqlite_version}")
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO test (name) VALUES ('test')")
        cursor.execute("SELECT * FROM test")
        result = cursor.fetchone()
        print(f"✓ SQLite test query: {result}")
        conn.close()
    except Exception as e:
        print(f"✗ SQLite error: {str(e)}")
    
    # Check Tkinter
    print("\nTkinter Check:")
    try:
        root = tk.Tk()
        root.withdraw()  # Don't show the window
        print(f"✓ Tkinter version: {root.tk.call('info', 'patchlevel')}")
        root.destroy()
    except Exception as e:
        print(f"✗ Tkinter error: {str(e)}")
    
    # Check environment variables
    print("\nEnvironment Variables:")
    for var in ['PYTHONPATH', 'PYTHONHOME', 'PATH']:
        print(f"{var}: {os.environ.get(var, 'Not set')}")
    
    print("\n" + "=" * 50)
    print("Environment check completed.")
    print("If you see any '✗' marks above, those checks failed.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    check_environment()
