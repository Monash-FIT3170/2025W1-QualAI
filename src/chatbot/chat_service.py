from flask import Flask
from flask import request, jsonify 
from src.chatbot.chat import Chatbot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
chatbot = Chatbot()

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
        response = chatbot.chat(message)
        return jsonify({'response': response}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500