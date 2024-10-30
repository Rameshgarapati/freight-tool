import subprocess
import datetime

def log_terminal_activities(log_filename):
    """
    Logs terminal activities to a specified log file.

    Args:
        log_filename (str): Path to the log file.
    """
    try:
        with open(log_filename, "a") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] Terminal activity:\n")
            while True:
                command = input("Enter a command (or 'exit' to stop logging): ")
                if command.lower() == "exit":
                    break
                result = subprocess.getoutput(command)
                log_file.write(f"Command: {command}\n")
                log_file.write(f"Result:\n{result}\n\n")
            print(f"Terminal activities logged in '{log_filename}'.")
    except Exception as e:
        print(f"Error while logging activities: {e}")


