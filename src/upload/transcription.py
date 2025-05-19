import whisper
import videoToAudio
import subprocess

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
        self.model = whisper.load_model("base")
        self.diarize_path = "./whisper-diarization/diarize.py"

    def transcribe(self, audio_filepath: str):
        """
        Transcribes the audio located at the provided filepath into text using the OpenAI-whisper model.

            :param audio_filepath: the filepath of the audio file to be transcribed

            :return str: the transcribed text
        """
        audio = whisper.load_audio(audio_filepath)
        audio = whisper.pad_or_trim(audio)

        result = whisper.transcribe(model=self.model, audio=audio)
        return result["text"]
    
    def transcribe_with_speakers(self, filepath: str):
        """
        Transcribes the audio contained at the file path using an open sourced
        local application of whisper that is able to assign speakers to the transcribed
        text.

            :param filepath: the filepath of either a video or mp3 file to be transcribed.

            :return str: transcribed text from file and speakers assigned to respective transcription
        """

        # Ensure file is converted into mp3 format prior to transcription
        filepath_mp3 = videoToAudio.convert_media(filepath)

        # Run diarize process as subprocess
        subprocess.run(['python', self.diarize_path, '-a', filepath_mp3])

        # Retrieve text file transcription
        filepath_txt = filepath_mp3.with_suffix(".txt")
        transcript = open(filepath_txt)

        

        return transcript.read()
       
    

if __name__ == "__main__":
    transcriber = AudioTranscriber()
    transcriber.transcribe_with_speakers("./sample-audio/podcast_sample.mp3")