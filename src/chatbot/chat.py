from src.chatbot.deepseek_client import DeepSeekClient
from src.chatbot.text_transformer.text_vectoriser import TextVectoriser
from src.chatbot.text_transformer.neo4j_interactor import Neo4JInteractor

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
        
        self.system_prompt = None 
        self.set_parameters()
        
    def set_parameters(self, temperature: float = 0.8, top_k: int = 40, top_p: float = 0.9, num_ctx: int = 2048, num_vectors: int = 5):
        self.deepseek_client.set_parameters(temperature, top_k, top_p, num_ctx)
        self.num_vectors = num_vectors
        
    def set_system_prompt(self, system_prompt: str):
        """
        Sets the system prompt for the model.

        :param system_prompt: The system prompt to set.
        """
        self.system_prompt = system_prompt

    def chat(self, query: str) -> str:
        """
        Processes a chat message and returns the model's response.
        Chunks, vectorises the query then searches in Neo4JInteractor for context.  

        :param message: The message to send to the model.
        :return: The JSON response from the API.
        """

        search_vector = self.text_converter.chunk_and_embed_text(query)[0][1]
        context = self.neoInteractor.search_text_chunk(search_vector, limit=self.num_vectors)
        # if len(context) > 0:
        #     response = self.deepseek_client.chat_with_model_context_injection(context, query)
        # else:
        #     response = self.deepseek_client.chat_with_model(query)
            
        response = self.deepseek_client.chat_with_model(query, self.system_prompt, context)
        
        return response
    
    
    def close_connections(self) -> None:
        """
        Closes the connections to the Neo4j database.
        """
        self.neoInteractor.close_driver()
        
if __name__ == "__main__":
    chatbot = Chatbot()
    print(chatbot.chat("Hello, how are you?"))
    chatbot.close_connections()