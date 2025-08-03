import os
import sys
from pathlib import Path

def test_file_operations():
    """Test basic file operations in the project directory."""
    print("Testing file operations...\n")
    
    # Get current working directory
    cwd = Path.cwd()
    print(f"Current working directory: {cwd}")
    
    # Try to create a test file
    test_file = cwd / "test_file.txt"
    print(f"\nCreating test file: {test_file}")
    
    try:
        # Try to write to the file
        with open(test_file, 'w') as f:
            f.write("This is a test file.\n")
        print("Successfully wrote to test file.")
        
        # Verify the file was created
        print(f"\nFile exists: {test_file.exists()}")
        print(f"File size: {test_file.stat().st_size} bytes")
        
    except Exception as e:
        print(f"\nError writing to file: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # Try to list directory contents
    try:
        print("\nListing directory contents:")
        for item in cwd.iterdir():
            print(f"- {item.name}")
    except Exception as e:
        print(f"\nError listing directory: {str(e)}")
    
    # Clean up
    try:
        if test_file.exists():
            test_file.unlink()
            print("\nCleaned up test file.")
    except Exception as e:
        print(f"\nError cleaning up: {str(e)}")
    
    print("\nTest completed.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    test_file_operations()
