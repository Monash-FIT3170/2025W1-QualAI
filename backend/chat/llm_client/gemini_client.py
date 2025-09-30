import json 
import re 
import requests
import os  

from chat.llm_client.llm_client import LLMClient

# USED FOR GOOGLE GEMINI API 
from dotenv import load_dotenv

class GeminiClient(LLMClient):
    def __init__(self):
        self.init_client()

    def init_client(self):
        try:
            load_dotenv()
            self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        except:
            self.gemini_api_key = None

        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}"
        self.headers = {"Content-Type": "application/json"}


    def extract_triples(self, text: str) -> list[tuple[str, str, str]]:
        """
        Uses the Gemini API to extract knowledge triples from the input text in the format:
        (Subject, Predicate, Object)

        :param text: The input text
        :return: A list of extracted triples
        """

        prompt = (
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

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        response = requests.post(self.url, headers=self.headers, json=payload)

        if not response.ok:
            print("Gemini API Error:", response.text)
            return []

        data = response.json()

        try:
            reply = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError) as e:
            print("Unexpected Gemini API response format:", e)
            return []

        if hasattr(self, "remove_think_blocks"):
            reply = self.remove_think_blocks(reply)

        if reply == "NONE":
            return []

        matches = re.findall(r"\(([^)]*)\)", reply)
        tuples = [tuple(part.strip() for part in m.split(',', 2)) for m in matches if ',' in m]

        return tuples

    def chat_with_model_context_injection(self, context_text, message):
        """
        Sends a message to the google gemini API with additional context injected as a system message

        :param context_text: The external context (e.g., from a document).
        :param message: The user's question.
        :return: The JSON response from the API.
        """
        prompt = (
            "You are a helpful, highly concise assistant. "
            "Answer the user's question using only the provided context below. "
            "Return a short and factual answer, sticking to the question's scope. "
            "Use as few words as possible. Avoid explanation unless asked for more detail. "
            "Do not speculate. If the answer is not inthe context, respond with: "
            "'I don't have enough information to answer that. '\n\n"
            f"Context:\n{context_text}\n\n"
            f"User: {message}"
        )

        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.9,
                "topK": 50,
                "maxOutputTokens": 2048
            }
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Gemini API error {response.status_code}: {response.text}")

        result = response.json()

        try:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise Exception(f"Unexpected response format: {result}")

        # Preserve your existing post-processing
        reply = self.remove_think_blocks(reply)

        return reply
    
    def chat_with_model(self, message):
        """
        Sends a message to the google gemini API with additional context injected as a system message

        :param context_text: The external context (e.g., from a document).
        :param message: The user's question.
        :return: The JSON response from the API.
        """

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"

        headers = {"Content-Type": "application/json"}

        prompt = (
            "You are a helpful, highly concise assistant. "
            "Answer the user's question using only the provided context below. "
            "Return a short and factual answer, sticking to the question's scope. "
            "Use as few words as possible. Avoid explanation unless asked for more detail. "
            "Do not speculate. If the answer is not inthe context, respond with: "
            "'I don't have enough information to answer that. '\n\n"
            f"User: {message}"
        )

        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "temperature": 0.2,
                "topP": 0.9,
                "topK": 50,
                "maxOutputTokens": 2048
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Gemini API error {response.status_code}: {response.text}")

        result = response.json()

        try:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            raise Exception(f"Unexpected response format: {result}")

        # Preserve your existing post-processing
        reply = self.remove_think_blocks(reply)

        return reply

    @staticmethod
    def remove_think_blocks(text: str) -> str:
        """
        Removes all text enclosed in deepseek-r1 model's think blocks 

        :param text: the text to clean 

        :return: the cleaned text with think block removed
        """
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()