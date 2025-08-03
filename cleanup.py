"""
Cleanup script for the Employee Assignment Management System.
Removes unnecessary files and directories.
"""
import os
import shutil
from pathlib import Path

def clean_project():
    """Remove unnecessary files and directories."""
    project_root = Path(__file__).parent
    
    # Files to remove
    files_to_remove = [
        project_root / 'database.py',
        project_root / 'main.py',
    ]
    
    # Directories to remove
    dirs_to_remove = [
        project_root / '__pycache__',
        project_root / 'src' / '__pycache__',
        project_root / 'src' / 'models' / '__pycache__',
        project_root / 'src' / 'views' / '__pycache__',
        project_root / 'src' / 'controllers' / '__pycache__',
    ]
    
    # Remove files
    for file_path in files_to_remove:
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
    
    # Remove directories
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"Removed directory: {dir_path}")
            except Exception as e:
                print(f"Error removing {dir_path}: {e}")
    
    print("\nCleanup complete!")
    print("The following files/directories were kept:")
    print("- src/ (source code)")
    print("- requirements.txt (dependencies)")
    print("- employee_assignments.db (database)")
    print("- venv/ (virtual environment)")

if __name__ == "__main__":
    print("Starting cleanup...")
    clean_project()
