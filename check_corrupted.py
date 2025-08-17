import os
import argparse
from mutagen.mp3 import MP3, HeaderNotFoundError

def is_mp3_corrupted(file_path):
    """
    Checks if an MP3 file is corrupted by attempting to read its header.

    Args:
        file_path (str): The full path to the MP3 file.

    Returns:
        tuple: A tuple containing (bool, str) where the boolean indicates
               if the file is valid, and the string contains an error message
               if it's not.
    """
    try:
        # Attempt to initialize an MP3 object. This will parse the file's header.
        MP3(file_path)
        return True, None
    except HeaderNotFoundError:
        # This is a common error for a corrupted or non-MP3 file.
        return False, "Corrupted or not a valid MP3 file."
    except Exception as e:
        # Catches other potential errors, like permission issues or generic read errors.
        return False, f"An unexpected error occurred: {e}"

def bulk_check_mp3_files(directory_path):
    """
    Scans a directory for MP3 files and checks if they are corrupted.

    Args:
        directory_path (str): The path to the directory to scan.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return

    print(f"Scanning directory: {directory_path}\n")

    checked_count = 0
    corrupted_count = 0

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory_path):
        for filename in files:
            # Check for files with the .mp3 extension
            if filename.lower().endswith('.mp3'):
                checked_count += 1
                file_path = os.path.join(root, filename)
                
                # Check for corruption
                is_valid, error_message = is_mp3_corrupted(file_path)
                
                if is_valid:
                    print(f"✅ VALID: {file_path}")
                else:
                    corrupted_count += 1
                    print(f"❌ CORRUPTED: {file_path} -> {error_message}")

    print("\n" + "="*50)
    print(f"Scan complete. Found {checked_count} MP3 files.")
    print(f"🟢 Valid files: {checked_count - corrupted_count}")
    print(f"🔴 Corrupted files: {corrupted_count}")
    print("="*50)

if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Bulk check MP3 files for corruption.")
    parser.add_argument("directory", help="The path to the directory containing MP3 files.")

    # Parse the argument from the command line
    args = parser.parse_args()

    # Run the bulk check
    bulk_check_mp3_files(args.directory)
