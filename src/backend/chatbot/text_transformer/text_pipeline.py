from backend.mongodb.DocumentStore import DocumentStore
from backend.chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from backend.chatbot.text_transformer.text_vectoriser import TextVectoriser

class TextPipeline():
    """
    A class for transforming text data from mongodb to neo4j

    :author: Jonathan Farrand
    """
    def __init__(self, mongodb: DocumentStore = None, neo4jdb: Neo4JInteractor = None, vectoriser: TextVectoriser = None):
        """
            Initializes the TextPipeline class with the relevant classes

            :param mongodb: An instance of DocumentStore to access MongoDB (optional)
            :param neo4jdb: An instance of Neo4JInteractor to access Neo4j (optional)
            :param vectoriser: An instance of TextVectoriser to handle text vectorisation (optional)
        """
        if mongodb is not None:
            self._document_store = mongodb
        else:
            self._document_store = DocumentStore()

        if neo4jdb is not None:
            self._neo4jdb = neo4jdb
        else:
            self._neo4jdb = Neo4JInteractor()
        
        if vectoriser is not None:
            self._vectoriser = vectoriser
        else:
            self._vectoriser = TextVectoriser()
    

    def process_and_store_single_file(self, database_name: str, collection_name: str, file_id: str, data_key: str = "content") -> None:
        """
            Accesses data from mongodb, converts it to vector data and then saves it in neo4j

            :param database_name: The name of the database to access the data from
            :param collection_name: The name of the collection to access the data from
            :param file_identifier: The identifier of the json file to access
            :param identifier_key: The json key that the identifier is linked to *Initially set to "title" should be changed to the default once agreed upon*
            :param data_key: The json key for where the text can be found *Initially set to "content" should be changed to the default once agreed upon*

        """
        db = self._document_store.get_database(database_name)
        if db is None:
            db = self._document_store.create_database(database_name)
        

        documents = db.get_collection(collection_name)
        if documents is None:
            documents = db.create_collection(collection_name)
        
        file_data = documents.find_document(file_id)

        text_data = file_data[data_key]
        self.process_and_store_text(file_id, text_data)

    def process_and_store_text(self, file_id: str, text: str) -> None:
        """
            Converts string to individual chunks and vectors before embedding in neo4j

            :param file_id: The id of the file that the text is linked to.
            :param text: The text to be chunked and embedd into neo4j
        """

        vector_data = self._vectoriser.chunk_and_embed_text(text)
        self._neo4jdb.store_multiple_vectors(vector_data, file_id)

