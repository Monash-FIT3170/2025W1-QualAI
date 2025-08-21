import subprocess
import os
from upload.video_to_audio import convert_media

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
        self.diarize_path = "./upload/whisper-diarization/diarize.py"

    def transcribe(self, audio_filepath: str):
        """
        Transcribes the audio located at the provided filepath into text using the OpenAI-whisper model.

            :param audio_filepath: the filepath of the audio file to be transcribed

            :return str: the transcribed text
        """

        # Ensure file is converted to mp3
        filepath_mp3 = convert_media(audio_filepath)

        # Run diarize process as subprocess
        subprocess.run(
            ['/opt/venv/bin/python', 
             self.diarize_path, 
             '-a', audio_filepath,
             "--batch-size", '1']) # Reduces load on docker to avoid crashing 
        
        # Retrieve text file transcription
        filepath_txt = filepath_mp3.with_suffix(".txt")
        filepath_srt = filepath_mp3.with_suffic(".srt")
        transcript = open(filepath_txt)

        # TODO: Delete created transcripts (.txt and .srt file)
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
    