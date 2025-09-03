from flask import Flask,  jsonify, request

from mongodb.DocumentStore import DocumentStore
from chat.database_client.database_client import DatabaseClient

class DocumentEditor:
  
    def __init__(
        self, collection: DocumentStore.Collection,
        database: DatabaseClient,
    ) -> None:
        self.__collection = collection
        self.__database = database

    def register_routes(self, app: Flask) -> None:
        @app.route('/edit/<string:file_key>', methods=['PATCH'])
        def update_document(file_key):
            try:
                new_content = request.json.get('content')
                if new_content is None:
                    return jsonify({"error": "No content provided"}), 400

                doc = self.__collection.find_document(file_key)
                if not doc:
                    return jsonify({"error": "Document not found"}), 404
                self.__collection.update_document(file_key, new_content)

                self.__database.remove_node_by_file_id(file_key)

                self.__database.store_entries(new_content, file_key)

                return jsonify({"message": "Document updated successfully"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
