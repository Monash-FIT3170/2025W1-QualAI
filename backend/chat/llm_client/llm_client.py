from abc import ABC, abstractmethod 

class LLMClient(ABC):
    """
    At interface for LLM interation. Connects to LLM and provides methods for connection. 
    Different strategies (deepseek, gemini) implement this
    
    :author: Felix Chung
    """
    @abstractmethod
    def init_client(self): 
        """
        Initilises the chatbot class with API url and key
        """
        pass

    @abstractmethod
    def extract_triples(self, text: str) -> list[tuple[str,str,str]]:
        """
        Extracts knowledge triples from the input text in the format:
        (Subject, Predicate, Object)

        :param text: The input text
        :return: A list of extracted triples
        """
        pass 

    @abstractmethod
    def chat_with_model_context_injection(self, context_text: str, message: str):
        """
        Sends a message to the google gemini API with additional context injected as a system message

        :param context_text: The external context (e.g., from a document).
        :param message: The user's question.
        :return: The JSON response from the API.
        """

    @abstractmethod
    def chat_with_model(self, message: str):
        """
        Sends a basic message to the model and returns the response.

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """
