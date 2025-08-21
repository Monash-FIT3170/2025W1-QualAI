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
        query_message = "Felix hates FIT3170, FIT3170 is a unit at Monash University, Monash University is a University in Clayton"
        response = self.client.chat_extract_triples(query_message)
        print(response)

    def test_return_type(self):
        """
        Tests that a list of triples is returned 
        """
        query_message = "Felix hates FIT3170, FIT3170 is a unit at Monash University, Monash University is a University in Clayton"
        response = self.client.chat_extract_triples(query_message)

        # Check type is list
        self.assertIsInstance(response, list)

        # Check all elements are tuples of length 3
        for triple in response:
            self.assertIsInstance(triple, tuple)
            self.assertEqual(len(triple), 3)
