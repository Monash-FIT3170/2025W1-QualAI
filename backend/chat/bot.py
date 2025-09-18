import traceback

from chat.database_client.database_client import DatabaseClient
from mongodb.ChatStore import ChatStore
from chat.text_transformer.text_vectoriser import TextVectoriser
import time

from flask import Flask

from flask import request, jsonify

from chat.deepseek_client import DeepSeekClient


class Chatbot:
    """
    A class to process chat messages and get responses from the deepseek-r1 model via client

    :author: Felix Chung
    """

    def __init__(self, db: DatabaseClient, collection: ChatStore.Collection):
        """
        Initializes the Chatbot class by with instances of the DeepSeekClient, TextVectoriser, and Neo4JInteractor classes.
        """
        self.deepseek_client = DeepSeekClient()
        self.collection = collection
        self.db = db

    def chat_with_model(self, query: str) -> str:
        """
        Processes a chat message and returns the model's response.
        Chunks, vectorises the query then searches in Neo4JInteractor for context.  

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """

        context = self.db.search(query)
        if len(context) > 0:
            response = self.deepseek_client.chat_with_model_context_injection(context, query)
        else:
            response = self.deepseek_client.chat_with_model(query)
        
        return response
        
    def chat_with_model_triples(self, query: str) -> str: 
        """
        Process a chat message return the model's reponse. 
        Extracts triples form the query then searchs in Knowledge Graph database for context. 

        :param str message: The message to send to the model. 
        :return: The JSON response from the API 
        """ 
        triples = self.deepseek_client.chat_extract_triples(query)
        
        context_triples = ""

        for triple in triples: 
            subject = triple[0]
            object = triple[1]
            result = self.db.search(subject)

            for row in result:
                context_triples += f"{row['subject']} {row['predicate']} {row['object']}, "
            
            result = self.db.search(object)

            for row in result:
                context_triples += f"{row['subject']} {row['predicate']} {row['object']}, "

        return self.deepseek_client.chat_with_model_triples(context_triples, query)

    def register_routes(self, app: Flask) -> None:
        @app.route('/chat', methods=['POST'])
        def chat():
            """
            API endpoint for handling chat messages.
            Expects a JSON payload with a 'message' key.

            :return: A JSON response containing either the model's reply or an error message.
            """
            data = request.get_json()
            message = data.get('message')

            if not message:
                return jsonify({'error': 'No message provided'}), 400

            try:
                response = self.chat_with_model(message)

                curTime = time.time()
                content = {
                    "question" : message,
                    "response" : response
                }

                self.collection.add_document(curTime, content)
                return jsonify({'response': response}), 200

            except Exception as e:
                traceback.print_exc()
                return jsonify({'error': str(e)}), 500
            
            

    
    def close_connections(self) -> None:
        """
        Closes the connections to the Neo4j database.
        """
        self.db.close_driver()