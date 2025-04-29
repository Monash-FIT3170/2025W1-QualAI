import whisper
from pyannote.audio import Pipeline
from pydub import AudioSegment
import os


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

        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1")

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
    
    def transcribe_with_speakers(self, audio_filepath: str):
        """
        Transcribes the audio located at the provided filepath into text and assigns
        speakers using the pyannote module to segment the text based on speakers 
        and OpenAI-whisper model to transcribe the segmented text.

            :param audiofilepath: the filepath of the audio file to be transcribed

            :return str: concatenated string of the transcribed segments 
        """
        audio = AudioSegment.from_file(audio_filepath)

        diarization = self.pipeline(audio_filepath)

        for turn, _, speaker in diarization.itertracks(yield_label = True):
            audio_segment = audio[turn.start* 1000: turn.end * 1000]
            path_segment = f"{speaker}_segment_{turn.start:.2f}_{turn.end:.2f}.wav"
            audio_segment.export(path_segment, format="wav")
            

            result = self.model.transcribe(path_segment)
            os.remove(path_segment)

            print(f"Speaker {speaker}: {result["text"]}")
        
        
 
if __name__ == "__main__":
    transcriber = AudioTranscriber()
    print(transcriber.transcribe("sample_audio/greetings.mp3"))
    transcriber.transcribe_with_speakers("sample_audio/greetings.mp3")