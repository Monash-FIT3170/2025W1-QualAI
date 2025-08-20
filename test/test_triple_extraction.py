import unittest

from backend.chat.deepseek_client import DeepSeekClient

class TestTripleExtraction(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.client = DeepSeekClient()

    def test_request(self):
        """
        Test that the chat can process a request and return a response.
        """
        query_message = "Felix hates FIT3170"
        response = self.client.chat_extract_triples(query_message)
        print(response)
