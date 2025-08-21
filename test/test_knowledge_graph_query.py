from backend.chat.knowledge_graph_constructor.knowledge_graph_pipeline import KnowledgeGraphPipeline
import unittest
from backend.chat.text_transformer.neo4j_interactor import Neo4JInteractor
from backend.chat.deepseek_client import DeepSeekClient

class TestKnowledgeGraphQuery(unittest.TestCase):
    """
    A class for testing the querying the knowledge database.
    
    Author: Jonathan Farrand, Felix Chung
    Last Update: Felix Chung
    
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
        cls.deepseek_client = DeepSeekClient()
        cls.knowledge_graph_pipeline = KnowledgeGraphPipeline(neo4j_interactor=cls.neo4j_interactor, chunk_length=300, overlap=100)
        cls.text = "Felix eats apples, apples grow on trees"
        cls.query = "what does felix eat" 


    def test_query_triples(self):
        """
        Tests triple extraction and knowledge graph search
        """

        self.knowledge_graph_pipeline.process_and_store_triples(self.text)
        data = self.neo4j_interactor.run_cypher_query("MATCH (n) RETURN n LIMIT 25")
        self.assertGreater(len(data), 0, "There should be at least one triple stored in the database.")
        
        triples = self.deepseek_client.chat_extract_triples(self.query)
        
        context_triples = ""

        for triple in triples: 
            subject = triple[0]
            object = triple[1]
            result = self.neo4j_interactor.search_by_entity(subject)

            for row in result:
                context_triples += f"{row['subject']} {row['predicate']} {row['object']}, "
            
            result = self.neo4j_interactor.search_by_entity(object)

            for row in result:
                context_triples += f"{row['subject']} {row['predicate']} {row['object']}, "

        print(f"triple context: {context_triples}")

        print(self.deepseek_client.chat_with_model_triples(context_triples, self.query))

    @classmethod
    def tearDown(self):
        """
        Clean up the test environment by closing the Neo4j driver.
        """
        self.neo4j_interactor.clear_database()
        self.neo4j_interactor.close_driver()
        
        



