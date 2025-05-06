import unittest

from src.chatbot.text_transformer.text_pipeline import TextPipeline
from src.chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from src.chatbot.text_transformer.text_vectoriser import TextVectoriser

class TestTextTransformer(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.transformer = TextPipeline()
        self.neo4j_interactor = Neo4JInteractor()
        self.text_vectoriser = TextVectoriser()

    def test_vectorise_text(self):
        text = "Hello World. This is an important test."
        chunks = self.text_vectoriser.chunk_text(text)
        self.assertGreaterEqual(len(chunks), 0, "Text should be chunked into at least one part.")

        vectors = self.text_vectoriser.embed_text(chunks)
        self.assertIsInstance(vectors, list, "Vectors should be a list.")
        self.assertGreater(len(vectors), 0, "There should be at least one vector generated.")

    def test_store_vector(self):
        text = "Hello World. This is an important test."
        vectors = self.text_vectoriser.chunk_and_embed_text(text)

        self.neo4j_interactor.store_multiple_vectors(vectors)

        
        search_vector = self.text_vectoriser.chunk_and_embed_text(text)[0][1]

        self.assertGreater(len(search_vector), 0, "There should be at least one vector stored in the database.")
