import os
from typing import Any

from flask import Flask, request, jsonify

from upload.AudioTranscriber import AudioTranscriber
from chat.database_client.database_client import DatabaseClient
from mongodb.DocumentStore import DocumentStore


class DocumentUploader:
  
    def __init__(
        self, collection: DocumentStore.Collection, database: DatabaseClient
    ) -> None:
        self.__collection = collection
        self.__database = database

    def register_routes(self, app: Flask) -> None:
        @app.route('/upload', methods=['POST'])
        def upload_file() -> tuple[Any, int]:
            """
            Is called when "upload file" button is clicked. Prompts the user to browse for an audio file.
            The file path will then be passed into the Transcriber to be eventually added to the database.

            :return: Whether was a success or if there was an error.
            """
            uploaded_files = request.files.getlist("files[]")
            if not uploaded_files:
                return jsonify({"error": "No file uploaded"}), 400

            for file in uploaded_files:
                result = self.__save_file(file)
                if not result[0]:
                    err = result[1]
                    print("Error during file upload:", err)
                    return jsonify({ "error": str(err) }), 500
            return jsonify({"status": "ok"}), 200

    def __save_file(self, file):
        try:
            filename = file.filename
            filepath = os.path.join('uploads', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)

            self.__process_file(filepath, filename)

            # TODO: delete the file after
            return True, None

        except Exception as e:
            # print("Error during file upload:", e)
            # return jsonify({"error": str(e)}), 500
            return False, e

    def __process_file(self, path: str, name: str) -> None:
        """
        Accepts a file path as an input to be sent to the transcriber.

        :return: TEMPORARY, outputs the file length, the mp3 won't need to be saved in the future.
        """
        audio_transcriber = AudioTranscriber()
        transcribed_text = audio_transcriber.transcribe(path)
        self.__collection.add_document(name, transcribed_text)
        self.__database.store_entries(transcribed_text, name)
        return jsonify({"status": "ok"}), 200