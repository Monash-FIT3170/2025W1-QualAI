from flask import Flask,  jsonify

from mongodb.DocumentStore import DocumentStore


class DocumentRetriever:
  
    def __init__(
        self, collection: DocumentStore.Collection
    ) -> None:
        self.__collection = collection

    def register_routes(self, app: Flask) -> None:
        @app.route('/documents', methods=['GET'])
        def get_all_documents():
            try:
                documents_cursor = self.__collection.get_all_documents()
                documents = list(documents_cursor)
                # Extract key for each document
                result = [{"key": doc.get("key")} for doc in documents]
                return jsonify(result), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
        @app.route('/documents/<string:file_key>', methods=['GET'])
        def get_document(file_key):
            try:
                doc = self.__collection.find_document(file_key)  
                if not doc:
                    return jsonify({"error": "Document not found"}), 404
                return jsonify({"content": doc.get("content", "")}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
