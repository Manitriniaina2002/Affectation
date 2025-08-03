with open('test_output.txt', 'w') as f:
    f.write("This is a test file.\n")
    f.write("If you can see this, the script ran successfully.\n")
    f.write(f"Current directory: {__import__('os').getcwd()}\n")
    f.write(f"Python version: {__import__('sys').version}\n")
    
print("Script completed. Check test_output.txt for results.")
