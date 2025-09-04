import backend.chat.triple_extractor_components.classsifier as clf
import unittest

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
        cls.__classifier = clf.Classifier("", False, "Josh", "John Smith")

    def test_chatbot(self):
        """
        Test that triples are extracted correctly from the text.
        """
        question = "What questions was Josh asked?"
        self.__classifier.reset_sentence(question)

        print(self.__classifier.get_subjects()) 
    
    @classmethod
    def tearDown(self):
        """
        Clean up the test environment by closing the Neo4j driver.
        """
        


