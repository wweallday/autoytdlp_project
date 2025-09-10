import csv
import yt_dlp
import re

def sanitize_filename(filename):
    """Sanitize the filename to remove invalid characters"""
    sanitized = re.sub(r'[\\/*?:"<>|]', '_', filename)
    sanitized = sanitized.strip()
    sanitized = re.sub(r'\s+', ' ', sanitized)
    return sanitized

def download_mp3(youtube_url, song_name, artist):
    """Downloads YouTube audio and converts to MP3 using yt-dlp"""
    filename = f"{song_name} {artist}"
    sanitized = sanitize_filename(filename)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': f'{sanitized}.%(ext)s',
        'noplaylist': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"✅ Downloaded: {sanitized}.mp3")
    except Exception as e:
        print(f"⚠️ Error downloading {song_name}: {e}")

def process_csv(file_path):
    """Reads CSV and triggers downloads"""
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = row['link'].strip()
            song_name = row['nhac'].strip()
            artist = row['casi'].strip()
            
            print(f"\n🎵 Processing: {song_name} by {artist}")
            download_mp3(link, song_name, artist)

if __name__ == "__main__":
    process_csv("chien.csv")
