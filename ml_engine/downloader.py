import yt_dlp
import os
import uuid

class VideoDownloader:
    def __init__(self, download_folder="temp_data"):
        self.download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    def download_from_url(self, url):
        """
        Downloads video or audio from a URL.
        Returns: (file_path, is_audio_only)
        """
        print(f"⬇️ Downloading content from {url}...")
        
        # Unique ID to prevent filename conflicts
        file_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(self.download_folder, f"{file_id}.%(ext)s")
        
        # Configuration for yt-dlp
        ydl_opts = {
            'format': 'best[ext=mp4]/best', # Try to get MP4 video
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Check metadata to see if it's audio only
                is_audio = False
                if info.get('vcodec') == 'none' or 'audio' in info.get('format_note', '').lower():
                    is_audio = True
                
                return filename, is_audio
        except Exception as e:
            print(f" Download failed: {e}")
            return None, False