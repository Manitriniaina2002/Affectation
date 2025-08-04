import sys
import os

def main():
    # Print to stdout and stderr
    print("This is a test message to stdout")
    print("This is a test message to stderr", file=sys.stderr)
    
    # Write to a file
    with open("python_test_output.txt", "w") as f:
        f.write("Python test output file\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Current directory: {os.getcwd()}\n")
        f.write(f"Files in directory: {os.listdir('.')}\n")

if __name__ == "__main__":
    main()
