from abc import ABC, abstractmethod 

class LLMClient(ABC):
    """
    At interface for LLM interation. Connects to LLM and provides methods for connection. 
    Different strategies (deepseek, gemini) implement this.
    
    :author: Felix Chung
    :modified by: Jaemin Park
    """
    @abstractmethod
    def init_client(self): 
        """
        Initilises the chatbot class with API url and key.
        """

    @abstractmethod
    def extract_triples(self, text: str) -> list[tuple[str,str,str]]:
        """
        Extracts knowledge triples from the input text in the format:
        (Subject, Predicate, Object)

        :param text: The input text.
        :return: A list of extracted triples.
        """

    @abstractmethod
    def chat_with_model_context_injection(self, context_text, message: str) -> str:
        """
        Sends a message to the LLM model with additional context injected as a system message.

        :param context_text: The external context (e.g., from a document).
        :param message: The user's question.

        :return: A string which is the response from the LLM to the user question.
        """

    @abstractmethod
    def chat_with_model_triples(self, triples: list[tuple[str, str, str]], message: str) -> str:
        """
        Chat with an LLM model with additional knowledge triples injected as context.

        :param triple: A list of knowledge triples in the form (SUBJECT, OBJECT, PREDICATE).
        :param message: The user's question.
        
        :return: A string which is the response from the LLM to the user question.
        """

    @abstractmethod
    def chat_with_model(self, message: str) -> str:
        """
        Sends a basic message to the model and returns the response.

        :param message: The user message to send to the model.

        :return: A string which is the response from the LLM to the user question.
        """
