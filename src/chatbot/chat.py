import requests 
import re
from src.config.config import JWS_KEY, API_URL

class Chatbot: 
    """
    A class for interacting with the deepseek-r1 model via API
    Supports basic chat functionality and context injection

    :author: Felix Chung
    """

    def __init__(self):
        """
        Initializes the Chatbot class with API URL and JWS key
        """
        self.api_url = API_URL
        self.jws_key = JWS_KEY
        self.headers = {
            'Authorization': f'Bearer {JWS_KEY}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def remove_think_blocks(self, text: str) -> str:
        """
        Removes all text enclosed in deepseek-r1 model's think blocks 

        :param text: the text to clean 

        :return: the cleaned text with think block removed
        """
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    def chat_with_model(self, message):
        """
        Sends a basic message to the model and returns the response.

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """
        headers = {
            'Authorization': f'Bearer {JWS_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        response = requests.post(API_URL, headers=self.headers, json=data)
        return response.json()["choices"][0]["message"]["content"]

    def chat_with_model_context_injection(self, context_text, message):
        """
        Sends a message to the model with additional context injected as a system message.

        :param context_text: The external context (e.g., from a document).
        :param message: The user’s question.
        :return: The JSON response from the API.
        """
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are a helpful research assistant that provides short, to the point answers. Answer questions using the following context: \n\n{context_text} \n\n The context ends here. \n\n Now, please answer the following question: "
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
        response = requests.post(API_URL, headers=self.headers, json=data)
        return response.json()["choices"][0]["message"]["content"]