from flask import Flask,  jsonify, request

from mongodb.DocumentStore import DocumentStore
from chat.text_transformer.neo4j_interactor import Neo4JInteractor
from chat.text_transformer.text_vectoriser import TextVectoriser
from typing import Any, Callable


class DocumentEditor:
  
    def __init__(
        self, collection: DocumentStore.Collection,
        vector_database: Neo4JInteractor,
        vectoriser: TextVectoriser
    ) -> None:
        self.__collection = collection
        self.__vector_database = vector_database
        self.__vectoriser = vectoriser

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

        self.__vector_database.remove_node_by_file_id(key)

        self.__vector_database.store_multiple_vectors(
            self.__vectoriser.chunk_and_embed_text(content), key
        )

        return jsonify({"message": "Document updated successfully"}), 200

    def __edit_request(self, key: str, content: str) -> tuple[Any, int]:
        if not self.__collection.rename_document(key, content):
            return jsonify({"error": "Document not found"}), 404

        self.__vector_database.rekey_node(key, content)

        return jsonify({"message": "Document updated successfully"}), 200

    def register_routes(self, app: Flask) -> None:
        @app.route('/edit/<string:file_key>', methods=['PATCH'])
        def update_document(file_key):
            return DocumentEditor.__request_content(file_key, self.__update_request)

        @app.route("/rename/<string:file_key>", methods=['PATCH'])
        def rename_document(file_key: str) -> tuple[Any, int]:
            return DocumentEditor.__request_content(file_key, self.__edit_request)

