import traceback

from flask import Flask

from flask import request, jsonify

from chat.deepseek_client import DeepSeekClient
from chat.context_retriever.context_retriever import ContextRetriever


class Chatbot:
    """
    A class to process chat messages and get responses from the deepseek-r1 model via client

    :author: Felix Chung
    """

    def __init__(self, context_retriever: ContextRetriever):
        """
        Initializes the Chatbot class by with instances of the DeepSeekClient, TextVectoriser, and Neo4JInteractor classes.
        """
        self.deepseek_client = DeepSeekClient()
        self.context_retriever = context_retriever

    def chat_with_model(self, query: str) -> str:
        """
        Processes a chat message and returns the model's response.
        Chunks, vectorises the query then searches in Neo4JInteractor for context.  

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """

        context = self.context_retriever.get_context(query)
        response = self.deepseek_client.chat_with_model_triples(context, query)
        
        return response

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
                return jsonify({'response': response}), 200

            except Exception as e:
                traceback.print_exc()
                return jsonify({'error': str(e)}), 500
    
    def close_connections(self) -> None:
        """
        Closes the connections to the Neo4j database.
        """
        self.neoInteractor.close_driver()