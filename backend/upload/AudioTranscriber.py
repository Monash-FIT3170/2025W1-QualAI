import whisper
import subprocess
import os
import whisper
import sys
from upload.video_to_audio import convert_media
from moviepy import AudioFileClip

# whisper-diarization
class AudioTranscriber:
    """
    A class for taking in an audio file and converting
    the contents into a text chunk that can be uploaded
    to mongoBD

    :author: Kade Lucy
    """

    def __init__(self):
        """
        Initialises the transcriber by loading in the 
        OpenAI whisper model to base configuration and
        """
        # Path to whisper-diarization model
        self.model = whisper.load_model("base")
        self.diarize_path = "./upload/whisper-diarization/diarize.py"
        self.model = whisper.load_model("base")

    def transcribe(self, audio_filepath: str):
        """
        Transcribes the audio located at the provided filepath into text using the OpenAI-whisper model.

            :param audio_filepath: the filepath of the audio file to be transcribed

            :return str: the transcribed text
        """

        # Validate file types (.txt or audio/video formats only)
        if audio_filepath.endswith(".txt"):
            # Return contents of text file
            transcript = open(audio_filepath)
            return transcript.read()
        # Convert audio file to mp3
        filepath_mp3 = convert_media(audio_filepath)

        # Use default whisper for short clips (Less than 50 seconds)
        if (AudioFileClip(filepath_mp3).duration < 50):
            audio = whisper.load_audio(filepath_mp3)
            result = whisper.transcribe(model = self.model, audio = audio)

            return result["text"]
        
        # Run diarize process as subprocess
        subprocess.run(
            ['/opt/venv/bin/python', 
             self.diarize_path, 
             '-a', audio_filepath,
             "--batch-size", '2',
             "--no-stem"]) # Reduces load on docker to avoid crashing 
        
        # Retrieve text file transcription
        filepath_txt = filepath_mp3.with_suffix(".txt")
        filepath_srt = filepath_mp3.with_suffix(".srt")
        transcript = open(filepath_txt)

        # Delete created transcripts (.txt and .srt file)
        if os.path.exists(filepath_txt):
            try:
                os.remove(filepath_txt)
            except OSError as e:
                print(f'Error: {filepath_txt}: {e.strerror}')
        
        if os.path.exists(filepath_srt):
            try:
                os.remove(filepath_srt)
            except OSError as e:
                print(f'Error: {filepath_srt}: {e.strerror}')

        return transcript.read()
 
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    