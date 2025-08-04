import os
import datetime

def main():
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a test file with timestamp
    test_file = "test_creation.txt"
    with open(test_file, "w") as f:
        f.write(f"Test file created at: {timestamp}\n")
        f.write(f"Current working directory: {os.getcwd()}\n")
    
    print(f"Test file created at: {os.path.abspath(test_file)}")

if __name__ == "__main__":
    main()
