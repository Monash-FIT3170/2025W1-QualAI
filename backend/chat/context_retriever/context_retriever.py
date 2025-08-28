from abc import ABC, abstractmethod

class ContextRetriever(ABC):
    """
    An interface for retriever context from the database for a llm query 
    Different strategies (vector search, KG search) implement this
    
    :author: Felix Chung
    """
    
    @abstractmethod
    def get_context(self, query: str) -> str:
        """
        Retrieve context relevant to the query   
        """
        pass
