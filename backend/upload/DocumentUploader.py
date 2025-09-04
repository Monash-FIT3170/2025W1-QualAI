import os
from dataclasses import dataclass
from flask import Flask, request, jsonify
from typing import Any, Optional

from chat.database_client.database_client import DatabaseClient
from mongodb.DocumentStore import DocumentStore
from upload.AudioTranscriber import AudioTranscriber


@dataclass
class FilePathInfo:
    filepath: str
    filename: str


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

            folder_mapping = {}
            for file in uploaded_files:
                fpi, err = self.__filepath_and_filename(file, folder_mapping)
                if not fpi:
                    print("Error during file upload:", err)
                    return jsonify({"error": str(err)}), 500

                result, err = self.__save_file(file, fpi)
                if not result:
                    print("Error during file upload:", err)
                    return jsonify({"error": str(err)}), 500
            return jsonify({"status": "ok"}), 200

    def __filepath_and_filename(self, file, folder_mapping) -> tuple[Optional[FilePathInfo], Optional[Exception]]:
        try:
            filename = file.filename
            parts = filename.split("/")
            root, rest = parts[0], parts[1:]

            is_dir = len(rest) > 0
            if is_dir:
                if root not in folder_mapping:
                    folder_mapping[root] = self.__collection.update_dir_name(root)
                root = folder_mapping[root]

                joined_rest = "/".join(rest)
                filepath = os.path.join('uploads', root, joined_rest)
                filename = root + "/" + joined_rest
            else:
                filepath = os.path.join('uploads', filename)
            return FilePathInfo(filepath, filename), None

        except Exception as e:
            return None, e

    def __save_file(self, file, fpi: FilePathInfo):
        try:
            os.makedirs(os.path.dirname(fpi.filepath), exist_ok=True)
            file.save(fpi.filepath)

            self.__process_file(fpi.filepath, fpi.filename)

            return True, None

        except Exception as e:
            # print("Error during file upload:", e)
            # return jsonify({"error": str(e)}), 500
            return False, e

    def __process_file(self, path: str, name: str):
        """
        Accepts a file path as an input to be sent to the transcriber.

        :return: TEMPORARY, outputs the file length, the mp3 won't need to be saved in the future.
        """
        audio_transcriber = AudioTranscriber()
        transcribed_text = audio_transcriber.transcribe(path)
        name = self.__collection.update_document_name(name)
        self.__collection.add_document(name, transcribed_text)
        self.__database.store_entries(transcribed_text, name)
        return jsonify({"status": "ok"}), 200
