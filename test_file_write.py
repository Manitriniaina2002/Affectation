import os

def main():
    # Get the current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # List files in the current directory
    print("\nFiles in current directory:")
    for f in os.listdir('.'):
        print(f"- {f}")
    
    # Write to a test file
    test_file = "test_output.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file.\n")
        f.write(f"Created at: {cwd}\\{test_file}\n")
    
    print(f"\nTest file created at: {os.path.abspath(test_file)}")
    
    # Read and display the test file
    print("\nTest file contents:")
    with open(test_file, 'r') as f:
        print(f.read())

if __name__ == "__main__":
    print("Starting file I/O test...")
    main()
    print("\nTest completed successfully!")
