import os
import sys
import datetime

def main():
    # Create a log file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "execution_verification.log"
    
    with open(log_file, 'w') as f:
        f.write(f"Execution Verification Log\n")
        f.write(f"=========================\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        # System information
        f.write("System Information:\n")
        f.write(f"- Python Version: {sys.version}\n")
        f.write(f"- Executable: {sys.executable}\n")
        f.write(f"- Platform: {sys.platform}\n")
        f.write(f"- Current Working Directory: {os.getcwd()}\n\n")
        
        # Environment variables
        f.write("Environment Variables:\n")
        for key, value in os.environ.items():
            if 'PATH' in key or 'PYTHON' in key.upper():
                f.write(f"- {key} = {value}\n")
        f.write("\n")
        
        # Directory contents
        f.write("Directory Contents:\n")
        for item in os.listdir('.'):
            f.write(f"- {item}\n")
    
    print(f"Verification log created at: {os.path.abspath(log_file)}")

if __name__ == "__main__":
    main()
