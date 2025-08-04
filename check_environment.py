"""
Environment and dependency check script for the Employee Assignment Management System.
"""
import sys
import os
import platform
import subprocess
from importlib import metadata

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"{title:^50}")
    print("=" * 50)

def check_python_version():
    """Check Python version and related information."""
    print_header("PYTHON ENVIRONMENT")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"PYTHONPATH: {sys.path}")

def check_dependencies():
    """Check if required packages are installed."""
    print_header("REQUIRED PACKAGES")
    required = [
        'customtkinter',
        'Pillow',
        'reportlab',
        'pytz',
        'python-dotenv'
    ]
    
    for package in required:
        try:
            version = metadata.version(package)
            print(f"✓ {package}: {version}")
        except metadata.PackageNotFoundError:
            print(f"✗ {package}: Not installed")

def check_tkinter():
    """Check if Tkinter is working."""
    print_header("TKINTER TEST")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Don't show the window
        print("✓ Tkinter is working")
        return True
    except Exception as e:
        print(f"✗ Tkinter error: {e}")
        return False

def check_customtkinter():
    """Check if customtkinter is working."""
    print_header("CUSTOMTKINTER TEST")
    try:
        import customtkinter as ctk
        print(f"✓ CustomTkinter is working (v{ctk.__version__})")
        return True
    except Exception as e:
        print(f"✗ CustomTkinter error: {e}")
        return False

def check_database_connection():
    """Check if database connection works."""
    print_header("DATABASE CONNECTION")
    try:
        import sqlite3
        from src.models.database import Database
        
        db_path = os.path.join(os.getcwd(), 'test_employee_assignments.db')
        print(f"Database path: {db_path}")
        
        if not os.path.exists(db_path):
            print("✗ Database file not found")
            return False
            
        db = Database(db_path)
        cursor = db.conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("✗ No tables found in the database")
            return False
            
        print("✓ Database connection successful")
        print(f"Tables found: {[t[0] for t in tables]}")
        return True
        
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def main():
    """Run all checks."""
    check_python_version()
    check_dependencies()
    tk_ok = check_tkinter()
    ctk_ok = check_customtkinter()
    db_ok = check_database_connection()
    
    print_header("SUMMARY")
    print(f"Tkinter: {'✓' if tk_ok else '✗'}")
    print(f"CustomTkinter: {'✓' if ctk_ok else '✗'}")
    print(f"Database: {'✓' if db_ok else '✗'}")
    
    if tk_ok and ctk_ok and db_ok:
        print("\n✓ All checks passed!")
    else:
        print("\n✗ Some checks failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
