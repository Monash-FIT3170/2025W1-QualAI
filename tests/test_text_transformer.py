import unittest

from backend.chatbot.text_transformer import TextPipeline
from backend.chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from backend.chatbot.text_transformer.text_vectoriser import TextVectoriser
from backend.mongodb.DocumentStore import DocumentStore

class TestTextTransformer(unittest.TestCase):
    """
    
    A class for testing the text transformer functionality.
    Author: Jonathan Farrand
    This class contains unit tests for the TextPipeline, Neo4JInteractor, and TextVectoriser classes.
    
    """
    
    @classmethod
    def setUpClass(self):
        """
        Set up the test environment by creating connections to the relevant services
        """
        self.neo4j_interactor = Neo4JInteractor()
        self.text_vectoriser = TextVectoriser()
        self.doc_store = DocumentStore()
        self.transformer = TextPipeline(mongodb=self.doc_store, neo4jdb=self.neo4j_interactor, vectoriser=self.text_vectoriser)

    def test_vectorise_text(self):
        """
        Test that text is vectorised correctly.
        """
        text = "Hello World. This is an important test."
        chunks = self.text_vectoriser.chunk_text(text)
        self.assertGreaterEqual(len(chunks), 0, "Text should be chunked into at least one part.")

        vectors = self.text_vectoriser.embed_text(chunks)
        self.assertIsInstance(vectors, list, "Vectors should be a list.")
        self.assertGreater(len(vectors), 0, "There should be at least one vector generated.")

    def test_store_vector(self):
        """
        Test that vectors are stored in the database correctly.
        """
        text = "Hello World. This is an important test."
        vectors = self.text_vectoriser.chunk_and_embed_text(text)

        self.neo4j_interactor.store_multiple_vectors(vectors, "file_id")

        search_vector = self.text_vectoriser.chunk_and_embed_text(text)[0][1]
        result = self.neo4j_interactor.search_text_chunk(search_vector)

        self.assertGreater(len(result), 0, "There should be at least one vector stored in the database.")

    def test_test_pipeline(self):
        """
        Testthat the entire pipeline operates correctly and stores the data in the neo4j database.
        """
        database = 'chatbot'
        collection_id = "qualitative_analysis"
        fileIdentifier = "biomedical_interview"

        text_content = "Thank you for joining us today. To start off, could you tell me a bit about your current role and your work in biomedical research? " \
        "Sure. I'm a biomedical data scientist working in a translational medicine lab. My focus is on analyzing high-throughput sequencing data, especially RNA-seq datasets, " \
        "to identify biomarkers for early-stage cancer detection. We work closely with both clinicians and molecular biologists to ensure our findings are biologically and clinically " \
        "meaningful."

        file_data = {
        "title": fileIdentifier,
        "content": text_content
        }
        

        db = self.doc_store.get_database(database)
        if db is None:
            db = self.doc_store.create_database(database)

        collection = db.get_collection(collection_id)
        if collection is None:
            collection = db.create_collection(collection_id)

        file = collection.find_document(fileIdentifier)
        if file is None:
            collection.add_document(fileIdentifier, fileIdentifier, file_data)

        file = collection.find_document(fileIdentifier)

        self.transformer.process_and_store_single_file(database, collection_id, fileIdentifier)

        chunks = self.text_vectoriser.chunk_text(text_content)
        vectors = self.text_vectoriser.embed_text(chunks)

        search_text = "Thank you for joining us today."
        search_vector = self.text_vectoriser.chunk_and_embed_text(search_text)[0][1]

        self.assertEqual(search_text,
                         self.neo4j_interactor.search_text_chunk(search_vector)[0], "The search result should match the expected text.")

        for vector_data in vectors:
            title = vector_data[0]
            vector = vector_data[1]
            self.neo4j_interactor.remove_node_by_text(title)

        collection.remove_document(fileIdentifier)

