import os
import re

def clean_filenames(target_dir="."):
    """
    Cleans filenames in the target directory by removing content in square 
    brackets from MP3 files. It resolves naming conflicts by appending a 
    numbered suffix (e.g., (1), (2)).
    """
    
    print(f"Scanning directory: {os.path.abspath(target_dir)}")

    # 1. Loop through files in the directory
    for filename in os.listdir(target_dir):
        if filename.lower().endswith(".mp3"):
            
            # Remove [ ... ] before .mp3 (e.g., "Song [192kbps].mp3" -> "Song.mp3")
            # The regex ensures we only target content right before the extension.
            cleaned_base_name = re.sub(r"\s*\[.*?\](?=\.mp3$)", "", filename)
            
            # Only proceed if a change was actually made
            if cleaned_base_name != filename:
                old_path = os.path.join(target_dir, filename)
                
                # Use os.path.splitext to safely separate base and extension
                base, ext = os.path.splitext(cleaned_base_name)
                
                # Start with the cleaned name as the initial new name candidate
                final_new_name = cleaned_base_name
                new_path = os.path.join(target_dir, final_new_name)
                
                # 2. Conflict Resolution Logic
                if os.path.exists(new_path):
                    # File conflict detected, find a unique numbered name
                    counter = 1
                    
                    # Loop until a non-existent path is found
                    while os.path.exists(new_path):
                        # Generate candidate name: "base (1).ext", "base (2).ext", etc.
                        final_new_name = f"{base} ({counter}){ext}"
                        new_path = os.path.join(target_dir, final_new_name)
                        counter += 1
                    
                    print(f"Conflict detected. Resolved to: {final_new_name}")

                # 3. Rename the file
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: '{filename}' -> '{final_new_name}'")
                except OSError as e:
                    # Catch OS errors (like permission denied or file locked)
                    print(f"Error renaming '{filename}': {e}")
            else:
                # File was an MP3, but no bracket content was found to clean.
                pass 

if __name__ == "__main__":
    # Get user input for the target directory
    folder = input("Enter directory to clean (leave empty for current directory): ").strip()
    
    if not folder:
        # Default to current directory
        folder = "."
        
    if os.path.isdir(folder):
        clean_filenames(folder)
    else:
        print(f"Error: Directory '{folder}' does not exist.")
