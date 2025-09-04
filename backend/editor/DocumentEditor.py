import re
from flask import Flask,  jsonify, request

from mongodb.DocumentStore import DocumentStore
from chat.database_client.database_client import DatabaseClient
from typing import Any, Callable


class DocumentEditor:
  
    def __init__(
        self, collection: DocumentStore.Collection,
        database: DatabaseClient,
    ) -> None:
        self.__collection = collection
        self.__database = database

    @staticmethod
    def __request_content(key: str, do_request: Callable[[str, str], tuple[Any, int]]):
        try:
            content = request.json.get("content")
            if content is None:
                return jsonify({ "error": "No content provided" }), 400
            return do_request(key, content)
        except Exception as e:
            return jsonify({ "error": str(e) }), 500

    def __update_request(self, key: str, content: str) -> tuple[Any, int]:
        if not self.__collection.update_document(key, content):
            return jsonify({"error": "Document not found"}), 404

        self.__database.remove_node_by_file_id(key)

        self.__vector_database.store_entries(
            content, key
        )

        return jsonify({"message": "Document updated successfully"}), 200

    def __edit_request(self, key: str, content: str) -> tuple[Any, int]:
        if not self.__collection.rename_document(key, content):
            return jsonify({"error": "Document not found"}), 404

        self.__database.rekey_node(key, content)

        return jsonify({"message": "Document updated successfully"}), 200

    def __edit_dir_request(self, dir: str, content: str) -> tuple[Any, int]:
        if not dir.endswith("/"):
            dir = dir + "/"

        docs = self.__collection.matching_documents(f"^{re.escape(dir)}")

        for doc in docs:
            current_key = str(doc.get("key"))
            # Replace the matching directory prefix with the new content
            if current_key.startswith(dir):
                new_key = content + "/" + current_key[len(dir):]
                self.__collection.rename_document(current_key, new_key)
                self.__database.rekey_node(current_key, new_key)

        return jsonify({"message": "Document/s updated successfully"}), 200

    def register_routes(self, app: Flask) -> None:
        @app.route('/edit/<path:file_key>', methods=['PATCH'])
        def update_document(file_key):
            return DocumentEditor.__request_content(file_key, self.__update_request)

        @app.route("/rename/<path:file_key>", methods=['PATCH'])
        def rename_document(file_key: str) -> tuple[Any, int]:
            return DocumentEditor.__request_content(file_key, self.__edit_request)

        @app.route("/rename-dir/<path:dir>", methods=['PATCH'])
        def rename_dir(dir: str) -> tuple[Any, int]:
            return DocumentEditor.__request_content(dir, self.__edit_dir_request)

