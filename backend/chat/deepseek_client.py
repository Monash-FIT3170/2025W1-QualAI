import json
import re

import requests

from config.config import JWS_KEY, API_URL
from mongodb.DocumentStore import DocumentStore
from .text_transformer.neo4j_interactor import Neo4JInteractor
# main testing imports
from .text_transformer.text_pipeline import TextPipeline
from .text_transformer.text_vectoriser import TextVectoriser


class DeepSeekClient: 
    """
    A class for interacting with the deepseek-r1 model via API
    Supports basic chat functionality and context injection

    :author: Felix Chung
    """

    def __init__(self):
        """
        Initializes the Chatbot class with API URL and JWS key
        """
        self.api_url = "http://ollama:11434/api/chat"
        self.jws_key = JWS_KEY
        self.headers = {
            'Authorization': f'Bearer {JWS_KEY}',
            'Content-Type': 'application/json'
        }

    @staticmethod
    def remove_think_blocks(text: str) -> str:
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
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)

        # NDJSON: split by lines and parse each one
        messages = []
        for line in response.text.strip().splitlines():
            try:
                obj = json.loads(line)
                msg = obj.get("message", {}).get("content")
                if msg:
                    messages.append(msg)
            except json.JSONDecodeError as e:
                print("Skipping malformed JSON line:", line, e)

        # Join all message content
        full_reply = "".join(messages)

        # Strip internal <think>...</think> tags or anything custom
        reply = self.remove_think_blocks(full_reply)

        return reply

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
                    "content": (
                        "You are a helpful, highly concise assistant. Answer the user's question using only the provided context below."
                        "Return a short and factual answer. Use as few words as possible. Use lists or bullet points if needed. Avoid explanation unless asked for more detail. Do not speculate. If the answer is not in the context, respond with: "
                        "'I don't have enough information to answer that.'\n\n"
                        f"Context:\n{context_text}"
            )},
                {
                    "role": "user",
                    "content": message
                }
            ],
            "options": {
                "temperature": 0.2,
                "max_tokens": 50
            }
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)

        # NDJSON: split by lines and parse each one
        messages = []
        for line in response.text.strip().splitlines():
            try:
                obj = json.loads(line)
                msg = obj.get("message", {}).get("content")
                if msg:
                    messages.append(msg)
            except json.JSONDecodeError as e:
                print("Skipping malformed JSON line:", line, e)

        # Join all message content
        full_reply = "".join(messages)

        # Strip internal <think>...</think> tags or anything custom
        reply = self.remove_think_blocks(full_reply)

        return reply