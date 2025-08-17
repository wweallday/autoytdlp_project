import subprocess
import sys
import os
import csv

# --- Configuration ---
YT_DLP_PATH = r"E:\3uToolsV3\Programdate\yt-dlp.exe"

# --- Main Script ---
def download_mp3_from_urls():
    """
    Reads a list of URLs from a CSV file, downloads audio as MP3s,
    and updates the CSV to mark completed downloads.
    """
    if len(sys.argv) < 2:
        print("Error: No input file specified.")
        print(f"Usage: python {os.path.basename(sys.argv[0])} <path_to_urls_file>")
        return

    urls_file = sys.argv[1]

    if not os.path.exists(YT_DLP_PATH):
        print(f"Error: yt-dlp executable not found at '{YT_DLP_PATH}'.")
        print("Please check the path and try again.")
        return

    if not os.path.exists(urls_file):
        print(f"Error: URLs file '{urls_file}' not found.")
        print("Please ensure the file exists at the specified path.")
        return

    # Read all rows from the CSV file
    data = []
    try:
        with open(urls_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            data = [row for row in reader]
    except csv.Error as e:
        print(f"Error reading CSV file {urls_file}: {e}")
        return
    except FileNotFoundError:
        print(f"Error: The file '{urls_file}' was not found.")
        return

    if not data:
        print(f"The '{urls_file}' file is empty or contains no URLs. Please add some URLs to it.")
        return

    print("Starting bulk download of YouTube audio as MP3...")
    print("-" * 40)

    base_command = [
        YT_DLP_PATH,
        "-x",
        "--audio-format", "mp3"
    ]

    for i, row in enumerate(data):
        timestamp, url = row[0], row[1]
        
        # Check if the download has already been completed
        if timestamp == '1':
            print(f"[{i + 1}/{len(data)}] Skipping: {url} (already downloaded)")
            continue

        print(f"[{i + 1}/{len(data)}] Downloading: {url}")
        
        full_command = base_command + [url]
        download_successful = False

        try:
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='latin-1'
            )

            for line in process.stdout:
                print(line, end='')

            return_code = process.wait()
            if return_code == 0:
                print(f"Successfully downloaded audio from {url}.")
                download_successful = True
            else:
                download_successful = True
                print(f"An error occurred while downloading {url}.")
                print(f"yt-dlp exited with code {return_code}.")
        
        except FileNotFoundError:
            print(f"Error: The yt-dlp executable was not found at '{YT_DLP_PATH}'.")
            break
        except Exception as e:
            download_successful = True
            print(f"An unexpected error occurred: {e}")
            break

        # If the download was successful, update the timestamp in the data list
        if download_successful:
            data[i][0] = '1'
            
            # Write the updated data back to the CSV file
            try:
                with open(urls_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(data)
                print("CSV file updated successfully.")
            except IOError as e:
                print(f"Error: Could not write to the CSV file '{urls_file}': {e}")
                
        print("-" * 40)

    print("All downloads completed.")

if __name__ == "__main__":
    download_mp3_from_urls()