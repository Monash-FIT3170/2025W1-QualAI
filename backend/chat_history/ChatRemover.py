import re
from flask import Flask, jsonify

from mongodb.ChatStore import ChatStore


class ChatRemover:
    """
    This class represents a way to provide delete functionality 
    for uploaded files in the system.

    Removed files are removed by their file_key from both the mongodb
    collection and neo4j vector databasee

    :author: Kade Lucy
    """
  
    def __init__(
        self, collection: ChatStore.Collection
    ) -> None:
        """
        Is defined using the chat mongodb database types for the system
        
        :param collection: Mongodb database collection
        """
        self.__collection = collection

    def register_routes(self, app: Flask) -> None:
        """
        Provides the route path to connect the frontend
        to the backend functionality to process deletion

        :params app: Flask application running the system
        """
        @app.route('/chatdelete/<path:file_key>', methods=['DELETE'])
        def delete_chat_file(file_key: str):
            """
            Attempts to remove the file with associated file_key 
            in both the collection and vector database

            :param file_key: file_key associated with a document in each database
            """
            try:
                print(self.__collection.get_all_documents())
                print(self.__collection.find_document(file_key))
                file_key = float(file_key)
                self.__collection.remove_document(file_key)

            
                return jsonify({"message": f"{file_key} successfully removed"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500


            