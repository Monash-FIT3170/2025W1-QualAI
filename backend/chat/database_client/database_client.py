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
    def search(self, query) -> list:
        """
        Searches database per search parameter
        
        :param query: the search query parameter
        
        :return list: a list of relevant database entries
        """ 
        pass 
    
    @abstractmethod
    def remove_node_by_file_id(self, file_id):
        """
            Searches the NEO4J database for any nodes matching the provided file_id, and removes them.

                :param str file_id: the file_id to be matched and removed
        """
        pass
    
    @abstractmethod 
    def rekey_node(self, file_id: str, new_id: str) -> None:
        """
        Searches the database for any nodes matching the provided file id, and rekeys with the provided id.

        :param file_id: the id of the file to be rekeyed
        :param new_id: the new id of the file
        """
        pass