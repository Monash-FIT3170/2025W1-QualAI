from chat.database_client.database_client import DatabaseClient
from mongodb.DocumentStore import DocumentStore
from flask import Flask, jsonify

class DocumentRemover:
    """
    This class represents a way to provide delete functionality 
    for uploaded files in the system.

    Removed files are removed by their file_key from both the mongodb
    collection and neo4j vector databasee

    :author: Kade Lucy
    """
  
    def __init__(
        self, collection: DocumentStore.Collection, database: DatabaseClient
    ) -> None:
        """
        Is defined using the two used database types for the system
        
        :param collection: Mongodb database collection
        :param vector_database: Neo4J vector database
        """
        self.__collection = collection
        self.__database = database

    def register_routes(self, app: Flask) -> None:
        """
        Provides the route path to connect the frontend
        to the backend functionality to process deletion

        :params app: Flask application running the system
        """
        @app.route('/delete/<string:file_key>', methods=['DELETE'])
        def delete_file(file_key: str):
            """
            Attempts to remove the file with associated file_key 
            in both the collection and vector database

            :param file_key: file_key associated with a document in each database
            """
            try:
                self.__collection.remove_document(file_key)
                self.__database.remove_node_by_file_id(file_key)
            
                return jsonify({"message": f"{file_key} successfully removed"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            