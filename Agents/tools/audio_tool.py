from gtts import gTTS
from pydub import AudioSegment

class TextToSpeechTool:
    def generate_audio(self, text: str) -> str:
        """Converts the given text to speech and saves it as an audio file."""
        try:
            tts = gTTS(text=text)
            audio_file = "generated_audio.mp3"
            tts.save(audio_file)
            return f"Audio generated and saved as '{audio_file}'"
        except Exception as e:
            return f"Failed to generate audio: {str(e)}"