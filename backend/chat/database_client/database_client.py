from abc import ABC, abstractmethod 

class DatabaseClient(ABC):
    """
    At interface for database upload and connection to handle file processing, upload and queries 
    Different strategies (vector search, KG search) implement this
    
    :author: Felix Chung
    """
    @abstractmethod
    def store_entries(self, entries: list, file_id):
        """
        Stores entries into database
        
        :param entries: List of entries 
        :param file_id: Optional document ID for metadata
        """ 
        pass
    
    @abstractmethod
    def search(self, parameter) -> list:
        """
        Searches database per search parameter
        
        :param parameter: the search query parameter
        
        :return list: a list of relevant database entries
        """ 
        pass 