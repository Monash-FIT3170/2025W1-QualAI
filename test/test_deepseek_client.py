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
        text = "Alice adopted a golden retriever named Max from the local animal shelter. " \
        "She takes him for a walk every morning in Central Park. " \
        "Max loves to play fetch with Alice, and he is very friendly with other dogs in the park. " \

        triples = self.deepseek_client.chat_extract_triples(text)
        print(triples)
        triples = self.deepseek_client.remove_think_blocks(triples)
        triples = self.deepseek_client.string_to_triples(triples)
        print()
        print(triples)
        print()
        self.assertGreater(len(triples), 0, "There should be at least one triple extracted.")




