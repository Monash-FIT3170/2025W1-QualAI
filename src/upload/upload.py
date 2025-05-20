from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from transcription import AudioTranscriber

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Is called when "upload file" button is clicked. Prompts the user to browse for an audio file.
    The file path will then be passed into the Transcriber to be eventually added to the database.

    :return: Whether was a success or if there was an error.
    """
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        # Make sure the uploads directory exists
        os.makedirs('uploads', exist_ok=True)

        filepath = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(filepath)

        process_file(filepath)

        #delete the file after

    except Exception as e:
        print("Error during file upload:", e)

def process_file(path: str) -> str:
    """
    Accepts a file path as an input to be sent to the transcriber.

    :return: TEMPORARY, outputs the file length, the mp3 won't need to be saved in the future.
    """
    audio_transcriber = AudioTranscriber()
    transcribed_text = audio_transcriber.transcribe(path)
    

app.run()