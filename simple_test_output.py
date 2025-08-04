# Simple test script to verify Python execution and file output
import os
import sys

def main():
    # Print to console
    print("This is a test message to console")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Write to a file
    with open("test_output.txt", "w") as f:
        f.write("This is a test message to file\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Current directory: {os.getcwd()}\n")
    
    print("Test completed. Check test_output.txt for output.")

if __name__ == "__main__":
    main()
