from src.mongodb.py_client.document_store import DocumentStore
from src.chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from src.chatbot.text_transformer.text_vectoriser import TextVectoriser

class TextPipeline():
    """
    A class for transforming text data from mongodb to neo4j

    :author: Jonathan Farrand
    """
    def __init__(self):
        """
            Initializes the TextPipeline class with the relevant classes
        """
        self._mongodb = DocumentStore()
        self._neo4jdb = Neo4JInteractor()
        self._vectoriser = TextVectoriser()
        pass

    def process_and_store_single_file(self, database_name: str, collection_name: str, file_identifier: str, identifier_key: str = "title", data_key: str = "content") -> None:
        """
            Accesses data from mongodb, converts it to vector data and then saves it in neo4j

            :param database_name: The name of the database to access the data from
            :param collection_name: The name of the collection to access the data from
            :param file_identifier: The identifier of the json file to access
            :param identifier_key: The json key that the identifier is linked to *Initially set to "title" should be changed to the default once agreed upon*
            :param data_key: The json key for where the text can be found *Initially set to "content" should be changed to the default once agreed upon*

        """
        collection_data = self._mongodb.Collection(database_name, collection_name)
        documents = collection_data.get_all_documents()

        for file in documents:
            text_data = file[data_key]
            vector_data = self._vectoriser.chunk_and_embed_text(text_data)
            self._neo4jdb.store_multiple_vectors(vector_data)

    def process_chunk(self, database_name: str, collection_name: str, file_identifier: str, data_key: str) -> None:
        """
            Processes a chunk of text and stores it in the database

            :param database_name: The name of the database to access the data from
            :param collection_name: The name of the collection to access the data from
            :param file_identifier: The identifier of the json file to access
            :param chunk: The chunk of text to process

        """
        file_data = self._mongodb.Collection(database_name, collection_name).find_document(file_identifier)
        text_data = file_data[data_key]
        vector_data = self._vectoriser.chunk_and_embed_text(text_data)
        self._neo4jdb.store_multiple_vectors(vector_data)
