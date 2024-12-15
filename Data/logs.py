import datetime
import os

def log_action(action, username):
    # Get the current timestamp in a human-readable format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the log message
    log_message = f"[{timestamp}] Action: {action}, Performed by: {username}\n"
    
    # Write the log message to the log file (logs.txt) in append mode
    with open("logs.txt", "a") as log_file:
        log_file.write(log_message)

def rotate_logs():
    log_file = "logs.txt"
    max_size = 5 * 1024 * 1024  # 5 MB (adjust as needed)
    
    if os.path.exists(log_file) and os.path.getsize(log_file) > max_size:
        # Rotate the log file by renaming it with a timestamp and creating a new one
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.rename(log_file, f"logs_{timestamp}.txt")
        print(f"Log file rotated. Old log saved as logs_{timestamp}.txt.")
