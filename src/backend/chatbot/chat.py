from chatbot.deepseek_client import DeepSeekClient
from chatbot.text_transformer.text_vectoriser import TextVectoriser
from chatbot.text_transformer.neo4j_interactor import Neo4JInteractor

class Chatbot: 
    """
    A class to process chat messages and get responses from the deepseek-r1 model via client

    :author: Felix Chung
    """

    def __init__(
            self, deepseek_client: DeepSeekClient, vector_database: Neo4JInteractor, vectoriser: TextVectoriser
        ):
        """
        Initializes the Chatbot class by with instances of the DeepSeekClient, TextVectoriser, and Neo4JInteractor classes.
        """
        self.__deepseek_client = deepseek_client
        self.__text_converter = vectoriser
        self.__neoInteractor = vector_database

    def chat(self, query: str) -> str:
        """
        Processes a chat message and returns the model's response.
        Chunks, vectorises the query then searches in Neo4JInteractor for context.  

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """

        search_vector = self.__text_converter.chunk_and_embed_text(query)[0][1]
        context = self.__neoInteractor.search_text_chunk(search_vector)
        if len(context) > 0:
            response = self.__deepseek_client.chat_with_model_context_injection(context, query)
        else:
            response = self.__deepseek_client.chat_with_model(query)
        
        return response