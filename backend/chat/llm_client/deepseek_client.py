import json
import re

import requests

from chat.llm_client.llm_client import LLMClient

import requests
import os

class DeepSeekClient(LLMClient): 
    """
    A class for interacting with the deepseek-r1 model via API
    Supports basic chat functionality and context injection

    :author: Felix Chung
    """
    def __init__(self):
        """
        Initializes the Chatbot class with API URL and JWS key
        """
        self.init_client()

    def init_client(self):
        self.api_url = "http://ollama:11434/api/chat"      

        self.headers = {
            'Content-Type': 'application/json'
        }

    def extract_triples(self, text: str) -> list[tuple[str, str, str]]:
        """
        Uses the LLM to extract triples from a message in the output format:

        (Subject, Predicate, Object)

        :param text: The text we are to extract triple from 
        :return: A list of triples 
        """
        data = {
            "model": "deepseek-r1:1.5b",
            "prompt": (
                "You are an AI helping humans extract knowledge triples about all relevant people, things, concepts, etc. "
                "Extract ALL of the knowledge triples from the text provided to you. "
                "Ensure that you consider the context of the ENTIRE statement. "
                "DO NOT output explanations, reasoning, or anything else. "
                "Your output MUST ONLY be:\n"
                "- One or more triples in the format (SUBJECT, PREDICATE, OBJECT), separated by '|'\n"
                "- Or exactly 'NONE'\n\n"

                "EXAMPLE\n"
                "Barack Obama was born in Honolulu, a city of the US.\n"
                "Output: (Barack Obama, was born in, Honolulu)|(Honolulu, is in, US)|(Honolulu, is a, city)\n"
                "END OF EXAMPLE\n\n"

                "EXAMPLE\n"
                "I'm going to the store.\n"
                "Output: NONE\n"
                "END OF EXAMPLE\n\n"

                "EXAMPLE\n"
                "Hi Jae! Did you know that Jae likes to cook steak whilst listening to music. "
                "Also, he recently got a new job which his teacher Rio, introduced him to.\n"
                "Output: (Jae, likes to cook, steak)|(Jae, listens to, music)|(Jae, has a, job)|"
                "(Jae, is taught by, Rio)|(Rio, has a student called, Jae)\n"
                "END OF EXAMPLE\n\n"

                "YOUR TURN\n"
                f"{text}\n"
                "Output:"
            )
        }

        response = requests.post(self.api_url, headers = self.headers, json = data)

        # NDJSON: split by lines and parse each one
        messages = []
        for line in response.text.strip().splitlines():
            try:
                obj = json.loads(line)
                if "response" in obj:
                    messages.append(obj["response"])
            except json.JSONDecodeError as e:
                print("Skipping malformed JSON line:", line, e)

        # Join all message content
        full_reply = "".join(messages)

        # Strip internal <think>...</think> tags or anything custom
        reply = self.remove_think_blocks(full_reply)

        if reply == "NONE":
            return []

        matches = re.findall(r"\(([^)]*)\)", reply)
        tuples = [tuple(part.strip() for part in m.split(',', 2)) for m in matches]

        return tuples

    def chat_with_model(self, message: str):
        """
        Sends a basic message to the model and returns the response.

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """
        data = {
            "model": "deepseek-r1:1.5b",
            "messages": [
                { "role": "system", "content": "You are a helpful, highly concise assistant. " },
                { "role": "user", "content": f"{message}"}
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
                        "Return a short and factual answer, sticking to the question's scope. Use as few words as possible. Avoid explanation unless asked for more detail. Do not speculate. If the answer is not in the context, respond with: "
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
                "top_p": 0.9,
                "top_k": 50,
                "repeat_penalty": 1.2,
                "presence_penalty": 0.5,
                "num_predict": 2048
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
    
    def chat_with_model_triples(self, triples, message):
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
                        "You must answer questions using only the provided triples and examples"
                        "Think step by step"

                        f"Knowledge Triples from query: {triples}"

                        "Rules: 1. Use ONLY the facts from the triples. 2. If the answer is not directly supported, say 'The answer is not avaliable from the provided transcripts'" 

                        "Return a short and factual answer, sticking to the question's scope. Get straight to the facts, concisely" 

                        "Task: Now, use triples to answer the following query"
            )
             
             },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "top_k": 50,
                "repeat_penalty": 1.2,
                "presence_penalty": 0.5,
                "num_predict": 2048
            }
        }
        response = requests.post(self.api_url, headers=self.headers, json=data)
        print(response.text)

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
    
    @staticmethod
    def remove_think_blocks(text: str) -> str:
        """
        Removes all text enclosed in deepseek-r1 model's think blocks 

        :param text: the text to clean 

        :return: the cleaned text with think block removed
        """
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()