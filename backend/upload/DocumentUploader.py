import os
from dataclasses import dataclass
from flask import Flask, request, jsonify, current_app
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
        self, mongo_database: DocumentStore.Database, database: DatabaseClient
    ) -> None:
        self.__mongo_database = mongo_database
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

            collection_name = request.form.get("project")
            collection = self.__mongo_database.get_collection(collection_name)

            if not uploaded_files:
                return jsonify({"error": "No file uploaded"}), 400

            folder_mapping = {}
            for file in uploaded_files:
                fpi, err = self.__filepath_and_filename(collection, file, folder_mapping)
                if not fpi:
                    print("Error during file upload:", err)
                    return jsonify({"error": str(err)}), 500

                result, err = self.__save_file(collection, file, fpi)
                if not result:
                    print("Error during file upload:", err)
                    return jsonify({"error": str(err)}), 500
            return jsonify({"status": "ok"}), 200
        
        @app.route('/toggle_state', methods=['POST'])
        def toggle_state() -> tuple[Any, int]:
            """
            Called when the React 'Assign Speakers' toggle is clicked.
            Updates the internal toggle state.
            """
            try:
                data = request.get_json()
                active = data.get('active', False)
                app.config["UPLOAD_TOGGLE_ACTIVE"] = active 
                return jsonify({"status": "success", "active": active}), 200

            except Exception as e:
                print("Error processing toggle:", e)
                return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def __filepath_and_filename(collection: DocumentStore.Collection, file, folder_mapping) -> tuple[Optional[FilePathInfo], Optional[Exception]]:
        try:
            filename = file.filename
            parts = filename.split("/")
            root, rest = parts[0], parts[1:]

            is_dir = len(rest) > 0
            if is_dir:
                if root not in folder_mapping:
                    folder_mapping[root] = collection.update_dir_name(root)
                root = folder_mapping[root]

                joined_rest = "/".join(rest)
                filepath = os.path.join('uploads', root, joined_rest)
                filename = root + "/" + joined_rest
            else:
                filepath = os.path.join('uploads', filename)
            return FilePathInfo(filepath, filename), None

        except Exception as e:
            return None, e

    def __save_file(self, collection: DocumentStore.Collection, file, fpi: FilePathInfo):
        try:
            os.makedirs(os.path.dirname(fpi.filepath), exist_ok=True)
            file.save(fpi.filepath)

            self.__process_file(collection, fpi.filepath, fpi.filename)

            return True, None

        except Exception as e:
            # print("Error during file upload:", e)
            # return jsonify({"error": str(e)}), 500
            return False, e

    def __process_file(self, collection: DocumentStore.Collection, path: str, name: str):
        """
        Accepts a file path as an input to be sent to the transcriber.

        :return: TEMPORARY, outputs the file length, the mp3 won't need to be saved in the future.
        """
        audio_transcriber = AudioTranscriber()
        audio_transcriber.set_assign_speakers(current_app.config.get("UPLOAD_TOGGLE_ACTIVE", False))
        transcribed_text = audio_transcriber.transcribe(path)
        name = collection.update_document_name(name)
        collection.add_document(name, transcribed_text)
        self.__database.store_entries(transcribed_text, name)
        return jsonify({"status": "ok"}), 200
