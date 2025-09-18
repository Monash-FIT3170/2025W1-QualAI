from flask import Flask, jsonify

from mongodb.DocumentStore import DocumentStore


class DocumentRetriever:
  
    def __init__(
        self, database: DocumentStore.Database
    ) -> None:
        self.__database = database

    def register_routes(self, app: Flask) -> None:
        @app.route('/<project>/documents', methods=['GET'])
        def get_all_documents(project):
            try:
                collection = self.__database.get_collection(project)
                documents_cursor = collection.get_all_documents()
                documents = list(documents_cursor)
                # Extract key for each document
                result = [{"key": doc.get("key"), "content": doc.get("content")} for doc in documents]
                return jsonify(result), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
        @app.route('/<project>/documents/<path:file_key>', methods=['GET'])
        def get_document(project, file_key):
            try:
                collection = self.__database.get_collection(project)
                doc = collection.find_document(file_key)
                if not doc:
                    return jsonify({"error": "Document not found"}), 404
                return jsonify({"content": doc.get("content", "")}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
