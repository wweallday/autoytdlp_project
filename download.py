import subprocess
import sys
import os
import csv

# --- Configuration ---
YT_DLP_PATH = r"E:\3uToolsV3\Programdate\yt-dlp.exe"

# --- Main Script ---
def download_mp3_from_urls():
    """
    Reads URLs from a CSV, downloads audio as MP3s, gets the video title,
    and updates the CSV to mark completed downloads and add the title.
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

    # Read all rows and header from the CSV file
    data = []
    header = []
    try:
        with open(urls_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            # Make script backward-compatible with old 2-column CSV
            if 'Title' not in header:
                header.append('Title')
            
            data = [row for row in reader]
            # Pad rows that have fewer than 3 columns
            for row in data:
                while len(row) < 3:
                    row.append('')
    except (StopIteration, FileNotFoundError): # Handles empty or non-existent file
        print(f"The file '{urls_file}' is empty or not found. Please check it.")
        return
    except csv.Error as e:
        print(f"Error reading CSV file {urls_file}: {e}")
        return

    if not data:
        print(f"The '{urls_file}' file contains no URLs. Please add some URLs to it.")
        return

    print("Starting bulk download of YouTube audio as MP3...")
    print("-" * 40)

    base_download_command = [
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

        print(f"[{i + 1}/{len(data)}] Processing: {url}")
        
        # 1. Get the video title first
        video_title = "Title not found"
        try:
            get_title_command = [YT_DLP_PATH, "--print", "%(title)s", url]
            title_process = subprocess.run(
                get_title_command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            video_title = title_process.stdout.strip()
            print(f"Found Title: {video_title}")
        except subprocess.CalledProcessError:
            print(f"Warning: Could not fetch title for {url}. It may be private or deleted.")
        except Exception as e:
            print(f"An unexpected error occurred while fetching title: {e}")

        # 2. Download the audio
        print(f"Now Downloading: {url}")
        full_command = base_download_command + [url]
        download_successful = False
        try:
            # Using subprocess.run for simpler execution and error handling
            result = subprocess.run(full_command, check=True, capture_output=True, text=True, encoding='latin-1')
            print(result.stdout) # Print yt-dlp output
            print(f"Successfully downloaded audio from {url}.")
            download_successful = True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while downloading {url}.")
            print(f"yt-dlp exited with code {e.returncode}.")
            print(f"Output:\n{e.stdout}\n{e.stderr}")
        except FileNotFoundError:
            print(f"Error: The yt-dlp executable was not found at '{YT_DLP_PATH}'.")
            break
        except Exception as e:
            print(f"An unexpected error occurred during download: {e}")

        # 3. If successful, update the data in memory and write back to the CSV
        if download_successful:
            data[i][0] = '1'  # Mark as downloaded
            data[i][2] = video_title  # Add the title
            
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
