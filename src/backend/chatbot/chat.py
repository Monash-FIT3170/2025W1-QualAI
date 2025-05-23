from chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from chatbot.text_transformer.text_vectoriser import TextVectoriser
from deepseek_client import DeepSeekClient


class Chatbot:
    """
    A class to process chat messages and get responses from the deepseek-r1 model via client

    :author: Felix Chung
    """

    def __init__(self):
        """
        Initializes the Chatbot class by with instances of the DeepSeekClient, TextVectoriser, and Neo4JInteractor classes.
        """
        self.deepseek_client = DeepSeekClient()
        self.text_converter = TextVectoriser()
        self.neoInteractor = Neo4JInteractor()

    def chat(self, query: str) -> str:
        """
        Processes a chat message and returns the model's response.
        Chunks, vectorises the query then searches in Neo4JInteractor for context.  

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """

        search_vector = self.text_converter.chunk_and_embed_text(query)[0][1]
        context = self.neoInteractor.search_text_chunk(search_vector)
        if len(context) > 0:
            response = self.deepseek_client.chat_with_model_context_injection(context, query)
        else:
            response = self.deepseek_client.chat_with_model(query)
        
        return response
    
    def close_connections(self) -> None:
        """
        Closes the connections to the Neo4j database.
        """
        self.neoInteractor.close_driver()