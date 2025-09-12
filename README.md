
# 🎬 YouTube Media Downloader Suite

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)  
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-orange.svg)](https://github.com/yt-dlp/yt-dlp)  
[![FFmpeg](https://img.shields.io/badge/ffmpeg-required-lightgrey.svg)](https://ffmpeg.org/)  

A collection of Python scripts to **download, convert, and manage YouTube media files** (MP3 and MP4).  

---

## ✨ Features

- **`download.py`** – Download YouTube videos and convert them to **MP3 audio files**.  
- **`downloadmp4.py`** – Download YouTube videos in **MP4 format**.  
- **`auto_clipboard.py`** – Monitor your clipboard for YouTube URLs and log them to a CSV file automatically.  
- **`check_corrupted.py`** – Scan a directory for **corrupted MP3 files** and remove them.  
- **`download_old.py`** – Legacy downloader (uses the yt-dlp **Python package** instead of the standalone binary).  

---

## 🗂 Project Structure



YouTube-Media-Downloader-Suite/
│
├── download.py             # Download YouTube videos as MP3
├── downloadmp4.py          # Download YouTube videos as MP4
├── auto\_clipboard.py       # Monitor clipboard for YouTube links
├── check\_corrupted.py      # Remove corrupted MP3 files
├── download\_old.py         # Legacy script (Python yt-dlp package)
├── urls.csv                # Example CSV file (timestamp, url)
├── README.md               # Project documentation



---

## 📦 Requirements

Make sure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)  
- [FFmpeg](https://ffmpeg.org/download.html) – For audio/video conversion  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) – For downloading media  
- [pyperclip](https://pypi.org/project/pyperclip/) – For clipboard monitoring (`auto_clipboard.py`)  
- [mutagen](https://pypi.org/project/mutagen/) – For corrupted file detection (`check_corrupted.py`)  

---

## ⚙️ Setup Instructions (Windows)

### 1. Install FFmpeg and yt-dlp

Install **FFmpeg** using a package manager:

```sh
# Using Chocolatey
choco install ffmpeg

# Using Winget
winget install "FFmpeg (Essentials Build)"
````

Then download **yt-dlp.exe** from the [official releases page](https://github.com/yt-dlp/yt-dlp/releases) and place it in a folder accessible to your scripts.

---

### 2. Install Python Packages

Install required dependencies with pip:

```sh
pip install pyperclip mutagen
```

---

## 🚀 Usage

### Download Audio and Video

Both `download.py` and `downloadmp4.py` read URLs from a **CSV file**.
The file must have a **header row** with a `timestamp` column and a `url` column.

```sh
# Download MP3 files
python download.py <path_to_urls_file.csv>

# Download MP4 files
python downloadmp4.py <path_to_urls_file.csv>
```

> ✅ The script will **update the CSV file** as each download completes, ensuring the same video won’t be downloaded twice.

---

### Monitor Clipboard

Automatically log copied YouTube URLs to a CSV file:

```sh
python auto_clipboard.py
```

---

### Check for Corrupted Files

Scan a directory for corrupted MP3s and remove them:

```sh
python check_corrupted.py <path_to_directory>
```

---

## 🗂 Legacy Script

The **`download_old.py`** script belongs to an earlier version of this project.
It uses the **yt-dlp Python library**, but the standalone `yt-dlp.exe` approach is **recommended** for simplicity.

---

## 📜 License

This project is licensed under the **MIT License**.
Please review YouTube’s [Terms of Service](https://www.youtube.com/t/terms) before downloading content.

---


