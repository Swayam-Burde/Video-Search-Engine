# File: ml_engine/processing.py
import cv2
import os
import subprocess
import sys

class VideoProcessor:
    def __init__(self, temp_folder="temp_data"):
        self.temp_folder = temp_folder
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

    def _get_ffmpeg_path(self):
        """
        Tries to find the absolute path to ffmpeg.exe in the current environment.
        """
        # 1. Look in the environment's Scripts folder (Where you pasted it)
        env_ffmpeg = os.path.join(sys.prefix, "Scripts", "ffmpeg.exe")
        if os.path.exists(env_ffmpeg):
            return env_ffmpeg
        
        # 2. Fallback to just "ffmpeg" (Assumes it's in System PATH)
        return "ffmpeg"

    def extract_audio(self, input_path):
        """
        Converts video/audio input to a standard WAV format for Whisper.
        """
        print(f"🔊 Processing audio track from: {input_path}")
        audio_path = os.path.join(self.temp_folder, "processed_audio.wav")
        
        # Get the correct path to the tool
        ffmpeg_exe = self._get_ffmpeg_path()
        
        # Command: Overwrite (-y), Mono (-ac 1), 16kHz (-ar 16000)
        command = [
            ffmpeg_exe, "-i", input_path, "-vn", "-ac", "1", "-ar", "16000", 
            audio_path, "-y"
        ]
        
        try:
            # Run FFmpeg (hide ugly logs unless error)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode != 0:
                print(f"⚠️ FFmpeg failed. Error logs:\n{result.stderr.decode()}")
                return None

            # CRITICAL CHECK: Did it actually create a file?
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                return audio_path
            else:
                print("❌ FFmpeg ran, but created an empty file.")
                return None

        except Exception as e:
            print(f"⚠️ FFmpeg System Error: {e}")
            return None

    def extract_keyframes(self, video_path, interval=2):
        """
        Extracts images. Returns empty list [] if file is audio-only.
        """
        print(f"🖼️ Attempting to extract frames from {video_path}...")
        
        if not os.path.exists(video_path):
            print("❌ Video file not found.")
            return []

        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("ℹ️ CV2 could not open file (Likely Audio-Only).")
            return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            cap.release()
            return []

        frame_paths = []
        count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if int(count % (fps * interval)) == 0:
                frame_filename = os.path.join(self.temp_folder, f"frame_{len(frame_paths)}.jpg")
                cv2.imwrite(frame_filename, frame)
                frame_paths.append(frame_filename)
            count += 1
            
        cap.release()
        print(f"✅ Extracted {len(frame_paths)} visual frames.")
        return frame_paths