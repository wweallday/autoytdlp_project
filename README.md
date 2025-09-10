YouTube Media Downloader SuiteThis project is a collection of Python scripts designed to automate the process of downloading and managing YouTube audio and video files.Featuresdownload.py: Downloads YouTube videos and converts them to MP3 audio files.downloadmp4.py: Downloads YouTube videos in MP4 format.auto_clipboard.py: Monitors your clipboard for YouTube URLs and automatically logs them to a CSV file.check_corrupted.py: Scans a directory for MP3 files and removes any that are corrupted.RequirementsTo run these scripts, you will need the following installed on your system:Python: The core language for the scripts.FFmpeg: An essential tool for handling the audio/video conversion and recoding.yt-dlp: A powerful command-line program for downloading media from YouTube and many other sites.pyperclip: Required for the clipboard monitoring script (auto_clipboard.py).mutagen: Required for the corrupted file checker (check_corrupted.py).Setup Instructions (Windows)Follow these steps to set up the required tools and Python packages on your Windows machine.1. Install FFmpeg and yt-dlpYou can install ffmpeg and download yt-dlp using the following methods:FFmpeg: Use a package manager like choco (Chocolatey) or winget.# Using Chocolatey
choco install ffmpeg

# Using winget
winget install "FFmpeg (Essentials Build)"
yt-dlp: Download the latest yt-dlp.exe from the official yt-dlp GitHub releases page and place it in a location where your scripts can easily access it.2. Install Python PackagesInstall the necessary Python libraries using pip:pip install pyperclip
pip install mutagen
UsageEach script is designed for a specific task. Here is how to use them.Download Audio and VideoThe download.py and downloadmp4.py scripts read URLs from a CSV file. The file should have a header row and columns for a timestamp and the URL.# To download MP3s
python download.py <path_to_urls_file.csv>

# To download MP4s
python downloadmp4.py <path_to_urls_file.csv>
Note: The scripts will update the CSV file as each download is completed, marking it so it won't be downloaded again on subsequent runs.Monitor ClipboardThe auto_clipboard.py script runs in the background and automatically logs any valid YouTube URLs you copy.python auto_clipboard.py
Check for Corrupted FilesThe check_corrupted.py script scans a specified directory for MP3 files and removes any that are damaged.python check_corrupted.py <path_to_directory>
Legacy ProjectThe download_old.py file was part of a previous version of this project that used the yt-dlp Python package. The current approach using the standalone yt-dlp executable is generally recommended for simplicity and ease of use.
