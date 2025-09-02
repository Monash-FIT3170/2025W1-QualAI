import os
from typing import Any

from flask import Flask, request, jsonify

from upload.AudioTranscriber import AudioTranscriber
from chat.text_transformer.neo4j_interactor import Neo4JInteractor
from chat.text_transformer.text_vectoriser import TextVectoriser
from mongodb.DocumentStore import DocumentStore

from chat.database_client.vector_database import VectorDatabase


class DocumentUploader:
  
    def __init__(
        self, collection: DocumentStore.Collection, vector_database: Neo4JInteractor, vectoriser: TextVectoriser
    ) -> None:
        self.__collection = collection
        self.__database = VectorDatabase()

    def register_routes(self, app: Flask) -> None:
        @app.route('/upload', methods=['POST'])
        def upload_file() -> tuple[Any, int]:
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

                filename = uploaded_file.filename

                filepath = os.path.join('uploads', filename)
                uploaded_file.save(filepath)

                return self.__process_file(filepath, filename)

                # TODO: delete the file after

            except Exception as e:
                print("Error during file upload:", e)
                return jsonify({"error": str(e)}), 500

    def __process_file(self, path: str, name: str) -> tuple[Any, int]:
        """
        Accepts a file path as an input to be sent to the transcriber.

        :return: TEMPORARY, outputs the file length, the mp3 won't need to be saved in the future.
        """
        audio_transcriber = AudioTranscriber()
        transcribed_text = audio_transcriber.transcribe(path)
        self.__collection.add_document(name, transcribed_text)
        self.__database.store_entries(transcribed_text, name)
        return jsonify({"status": "ok"}), 200
