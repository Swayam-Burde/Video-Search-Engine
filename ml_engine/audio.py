import whisper
import warnings

warnings.filterwarnings("ignore")

class AudioTranscriber:
    def __init__(self, model_size="base"):
        print(f"Loading Whisper model ({model_size})...")
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_path):
        print(f"Transcribing {audio_path}...")
        result = self.model.transcribe(audio_path)
        return result["segments"] # Returns text with timestamps

if __name__ == "__main__":
    print("Audio module is ready.")