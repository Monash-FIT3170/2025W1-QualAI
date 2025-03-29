#
# test.py
#
# Tests the functionality of several of the spikes within this directory using the Python unittest framework.
#
# Author: Kays Beslen
# Last modified: 29/03/25
#

import unittest

from openai_whisper import transcribe
from sentence_transformer import chunk_and_embed
from vector_db import get_client, close_client, store_vector, search, remove_node_by_name


class TestSpikes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
            This runs once before testing starts. Initialises a Neo4j client connection.
        """
        cls.client = get_client("bolt://localhost:7687", "neo4j", "password")
        cls.audio_filepath = "../resources/hello.mp3"

    def test_whisper(self):
        """
            Tests the OpenAI-whisper framework.
        """
        transcribed_text = transcribe(self.audio_filepath)
        self.assertEquals(transcribed_text.strip(), "Hello.")

    def test_vector_store_and_search(self):
        """
            Tests that a vector that is stored within the vector database can be retrieved.
        """
        datum = chunk_and_embed("Test.")[0]
        store_vector(self.client, datum[0], datum[1])
        self.assertEquals(search(self.client, datum[1])[0], datum[0])

    @classmethod
    def tearDownClass(cls):
        """
            This runs once after testing is completed. Closes the Neo4j client connection, and clears test data from
            the database.
        """
        remove_node_by_name(cls.client, "Test.")
        close_client(cls.client)


if __name__ == '__main__':
    unittest.main()
