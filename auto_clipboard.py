import pyperclip
import time
import re
import csv
import os

# Define the name of the CSV log file
LOG_FILE_NAME = "url_log.csv"

def is_valid_url(text):
    """
    Checks if a given string is a valid URL using a regular expression.
    
    Args:
        text (str): The string to check.

    Returns:
        bool: True if the string is a valid URL, False otherwise.
    """
    # A robust regex for matching URLs, including http, https, ftp, etc.
    url_regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)
    return re.match(url_regex, text) is not None

def log_url_to_csv(url):
    """
    Appends a URL and an empty title to a CSV file. It creates the file 
    and writes headers if it doesn't exist.

    Args:
        url (str): The URL to log.
    """
    file_exists = os.path.isfile(LOG_FILE_NAME)
    with open(LOG_FILE_NAME, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write new headers if the file is new
            writer.writerow(['Timestamp', 'URL', 'Title'])
        # Write the new row with an empty string for the title
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), url, ''])

def monitor_clipboard(history_size=5):
    """
    Monitors the clipboard for URLs, logs them to a CSV, and keeps a
    history of the last 'history_size' unique URLs.

    Args:
        history_size (int): The number of URLs to keep in the history.
    """
    clipboard_history = []
    last_known_content = ""

    print(f"Monitoring clipboard for URLs. Will log to '{LOG_FILE_NAME}'.")
    print("Copy the text '$EXIT' to quit the program.")
    print("Press Ctrl+C to exit.\n")
    print("Script started. Copy a URL to see the history update...")
    print("-" * 20)

    try:
        # The main loop to continuously check the clipboard
        while True:
            current_content = pyperclip.paste()
            
            # Exit condition check
            if current_content == "$EXIT":
                print("\nReceived exit command. Exiting clipboard monitor.")
                break

            # Check if the content has changed and is a valid URL
            if current_content and current_content != last_known_content and is_valid_url(current_content):
                # Log the URL to the CSV file
                log_url_to_csv(current_content)
                
                # Add the new content to the front of the history list
                clipboard_history.insert(0, current_content)

                # Keep the history list at the desired size
                if len(clipboard_history) > history_size:
                    clipboard_history.pop()

                print("\n" + "-" * 20)
                print("Logged URL History (Oldest to Newest):")
                # Iterate through the list with an index for cleaner output
                for i, item in enumerate(reversed(clipboard_history)):
                    print(f"{i + 1}. {item}")
                print("-" * 20 + "\n")

                # Update the last known content
                last_known_content = current_content

            # Pause the script for a second to avoid using too much CPU
            time.sleep(1)

    except pyperclip.PyperclipException as e:
        print(f"Error: {e}")
        print("Could not access clipboard. Please ensure you have a clipboard utility installed.")
    except KeyboardInterrupt:
        print("\nExiting clipboard monitor.")

if __name__ == "__main__":
    monitor_clipboard()
