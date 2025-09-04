from backend.chat.knowledge_graph_constructor.knowledge_graph_pipeline import KnowledgeGraphPipeline
import unittest
from backend.chat.text_transformer.neo4j_interactor import Neo4JInteractor


class TestKnowledgeGraphPipeline(unittest.TestCase):
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
        cls.neo4j_interactor.clear_database()



    def test_storing_triples(self):
        """
        Test that triples are extracted correctly from the text.
        """

        self.knowledge_graph_pipeline.process_and_store_triples(self.text)
        data = self.neo4j_interactor.run_cypher_query("MATCH (n) RETURN n LIMIT 25")
        print(data)
        self.assertGreater(len(data), 0, "There should be at least one triple stored in the database.")
    
    @classmethod
    def tearDown(self):
        """
        Clean up the test environment by closing the Neo4j driver.
        """
        self.neo4j_interactor.clear_database()
        self.neo4j_interactor.close_driver()
        
        



