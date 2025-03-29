#
# openai_whisper.py
#
# A spike for testing the usage of the OpenAI-whisper model for transcribing speech into text.
#
# Author: Kays Beslen
# Last modified: 29/03/25
#

import whisper


def transcribe(audio_filepath: str) -> str:
    """
        Transcribes the audio located at the provided filepath into text using the OpenAI-whisper model.

            :param audio_filepath: the filepath of the audio file to be transcribed

            :return str: the transcribed text
    """
    # Load the base OpenAI-whisper model.
    model = whisper.load_model("base")

    # Initial pre-processing of the audio.
    audio = whisper.load_audio(audio_filepath)
    audio = whisper.pad_or_trim(audio)

    # Transcribe the audio into text.
    result = whisper.transcribe(model=model, audio=audio)
    return result["text"]


if __name__ == '__main__':
    print(transcribe("../resources/hello.mp3"))
