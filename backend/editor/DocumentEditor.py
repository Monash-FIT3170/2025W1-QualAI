import re
from flask import Flask, jsonify, request
from typing import Any, Callable

from chat.database_client.database_client import DatabaseClient
from mongodb.DocumentStore import DocumentStore


class DocumentEditor:
  
    def __init__(
        self, mongo_database: DocumentStore.Database,
        database: DatabaseClient,
    ) -> None:
        self.__mongo_database = mongo_database
        self.__database = database

    def __request_content(self, key: str, do_request: Callable[[DocumentStore.Collection, str, str], tuple[Any, int]]):
        try:
            project = request.get_json().get("project")
            collection = self.__mongo_database.get_collection(project)
            content = request.json.get("content")
            if content is None:
                return jsonify({ "error": "No content provided" }), 400
            return do_request(collection, key, content)
        except Exception as e:
            return jsonify({ "error": str(e) }), 500

    def __update_request(self, collection: DocumentStore.Collection, key: str, content: str) -> tuple[Any, int]:
        if not collection.update_document(key, content):
            return jsonify({"error": "Document not found"}), 404

        self.__database.remove_node_by_file_id(key)

        self.__database.store_entries(
            content, key
        )

        return jsonify({"message": "Document updated successfully"}), 200

    def __edit_request(self, collection: DocumentStore.Collection, key: str, content: str) -> tuple[Any, int]:
        content = collection.update_document_name(content)
        if not collection.rename_document(key, content):
            return jsonify({"error": "Document not found"}), 404

        self.__database.rekey_node(key, content)

        return jsonify({"message": "Document updated successfully"}), 200

    def __edit_dir_request(self, collection: DocumentStore.Collection, dir: str, content: str) -> tuple[Any, int]:
        content = collection.update_dir_name(content)
        if not dir.endswith("/"):
            dir = dir + "/"

        docs = collection.matching_documents(f"^{re.escape(dir)}")

        for doc in docs:
            current_key = str(doc.get("key"))
            # Replace the matching directory prefix with the new content
            if current_key.startswith(dir):
                new_key = content + "/" + current_key[len(dir):]
                collection.rename_document(current_key, new_key)
                self.__database.rekey_node(current_key, new_key)

        return jsonify({"message": "Document/s updated successfully"}), 200

    def register_routes(self, app: Flask) -> None:
        @app.route('/edit/<path:file_key>', methods=['PATCH'])
        def update_document(file_key):
            return self.__request_content(file_key, self.__update_request)

        @app.route("/rename/<path:file_key>", methods=['PATCH'])
        def rename_document(file_key: str) -> tuple[Any, int]:
            return self.__request_content(file_key, self.__edit_request)

        @app.route("/rename-dir/<path:dir>", methods=['PATCH'])
        def rename_dir(dir: str) -> tuple[Any, int]:
            return self.__request_content(dir, self.__edit_dir_request)

