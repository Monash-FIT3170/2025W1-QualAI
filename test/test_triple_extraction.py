import unittest

from backend.chat.llm_client.deepseek_client import DeepSeekClient

class TestTripleExtraction(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.client = DeepSeekClient()

    # def test_request(self):
    #     """
    #     Test that the chat can process a request and return a response.
    #     """
    #     query_message = "Felix hates FIT3170, FIT3170 is a unit at Monash University, Monash University is a university in Clayton"
    #     response = self.client.chat_extract_triples(query_message)
    #     print(response)

    # def test_request_adv(self):
    #     """
    #     Test extraction of triples on more complex situations.
    #     Specifically: testing temporal and spatial extraction
    #     """
    #     adv_query_message = "The Eiffel Tower, located in Paris, was constructed in 1889 for the World's Fair."
    #     response = self.client.chat_extract_triples(adv_query_message)

    #     print(response)

    def test_request_long(self):
        """
        Test extraction of triples on longer chunks of text.
        """
        long_query = "In 1969, Neil Armstrong became the first human to walk on the Moon during the Apollo 11 mission. He was joined by Buzz Aldrin, while Michael Collins piloted the command module in orbit. The mission was launched by NASA and is considered one of humanity's greatest achievements. After returning to Earth, Armstrong became a professor of aerospace engineering at the University of Cincinnati."
        response = self.client.extract_triples(long_query)
        print(response)
        
    # def test_object_extraction(self):
    #     """
    #     Test query object extraction with deep seek client
    #     """
    #     query = "What did Neil Armstrong do?"
    #     response = self.client.chat_extract_triples_entities(query)
    #     print(response)

    # def test_return_type(self):
    #     """
    #     Tests that a list of triples is returned 
    #     """
    #     query_message = "Felix hates FIT3170, FIT3170 is a unit at Monash University, Monash University is a University in Clayton"
    #     response = self.client.chat_extract_triples(query_message)

    #     # Check type is list
    #     self.assertIsInstance(response, list)

    #     # Check all elements are tuples of length 3
    #     for triple in response:
    #         self.assertIsInstance(triple, tuple)
    #         self.assertEqual(len(triple), 3)
