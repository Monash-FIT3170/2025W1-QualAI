import whisper


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

    def transcribe(self, audio_filepath: str):
        """
        Transcribes the audio located at the provided filepath into text using the OpenAI-whisper model.

            :param audio_filepath: the filepath of the audio file to be transcribed

            :return str: the transcribed text
        """
        audio = whisper.load_audio(audio_filepath)
        result = whisper.transcribe(model=self.model, audio=audio)
        
        # audio = whisper.pad_or_trim(audio)
        # result = whisper.transcribe(model=self.model, audio=audio)
        return result["text"]
 
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    