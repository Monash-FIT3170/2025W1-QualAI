from backend.chat.deepseek_client import DeepSeekClient
import unittest

class TestDeepSeekClient(unittest.TestCase):
    """
    A class for testing the DeepSeekClient functionality.
    
    Author: Jonathan Farrand
    
    Requirements:
        - ollama running locally
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment by creating an instance of DeepSeekClient.
        """
        cls.deepseek_client = DeepSeekClient()

    def test_chat_extract_triples(self):
        """
        Test that triples are extracted correctly from the text.
        """
        text = "Alice loves Bob. Bob hates Charlie."
        triples = self.deepseek_client.chat_extract_triples(text)
        self.assertGreater(len(triples), 0, "There should be at least one triple extracted.")




