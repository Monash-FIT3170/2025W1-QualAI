from backend.chat.knowledge_graph_constructor.knowledge_graph_pipeline import KnowledgeGraphPipeline
import unittest
from backend.chat.text_transformer.neo4j_interactor import Neo4JInteractor
from backend.chat.context_retriever.triple_context_retriever import TripleContextRetriever
from backend.chat.bot import Chatbot

class TestChatbot(unittest.TestCase):
    """
    A class for testing the KnowledgeGraphPipeline functionality.
    
    Author: Jonathan Farrand
    
    Requirements:
        - ollama running locally
        - neo4j database running locally
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment by creating an instance of KnowledgeGraphPipeline.
        """
        cls.neo4j_interactor = Neo4JInteractor()
        cls.knowledge_graph_pipeline = KnowledgeGraphPipeline(neo4j_interactor=cls.neo4j_interactor, chunk_length=300, overlap=100)
        cls.text = "Joe has three dogs. The dogs names are Leo, Ella and Liam. Leo is a german shepherd, Ella is a Labrador and Liam is a border collie. " \
        "Joe likes to go on runs with his dogs. They run to the park. There are lots of ducks at the park. The dogs like to chase the ducks."
        cls.query = "How many dogs does joe have?"
        
        cls.context_retriever = TripleContextRetriever()
        cls.bot = Chatbot(cls.context_retriever)
    
        cls.neo4j_interactor.clear_database()

    def test_chatbot(self):
        """
        Test that triples are extracted correctly from the text.
        """
        self.knowledge_graph_pipeline.process_and_store_triples(self.text)
        data = self.bot.chat_with_model(self.query)

        print(data)    
    
    @classmethod
    def tearDown(self):
        """
        Clean up the test environment by closing the Neo4j driver.
        """
        self.neo4j_interactor.clear_database()
        self.neo4j_interactor.close_driver()