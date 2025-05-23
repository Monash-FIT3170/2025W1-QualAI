from flask import Flask
from flask import request, jsonify 
from chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from chatbot.text_transformer.text_vectoriser import TextVectoriser
from chatbot.chat import Chatbot


class ChatService:
    """
        A class to handle chat messages and provide responses from the chatbot as API endpoint via flask 
        
        author: Felix Chung
    """
    def __init__(
            self, vector_database: Neo4JInteractor, vectoriser: TextVectoriser, deepseek_client: Chatbot        
        ) -> None:
        self.__chatbot = Chatbot(deepseek_client=deepseek_client, vector_database=vector_database, vectoriser=vectoriser)
        
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
                response = self.__chatbot.chat(message)
                return jsonify({'response': response}), 200
            
            except Exception as e:
                return jsonify({'error': str(e)}), 500