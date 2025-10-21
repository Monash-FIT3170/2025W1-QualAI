import unittest

from chat.database_client.graph_database import GraphDatabase

from chat.llm_client.gemini_client import GeminiClient

class TestQuestionAnswerTriples(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.database = GraphDatabase(GeminiClient())
        self.database.clear_database()

    def test_interview_one(self):
        interview_text = "How has AI influenced your learning experience? It’s made studying faster — I can get summaries of long readings in minutes. " \
        "But sometimes I feel like I’m skipping the real depth of the material. Can you describe a time when AI was especially helpful or frustrating? " \
        "Helpful when I used an AI writing tool to brainstorm essay ideas — it gave me perspectives I hadn’t thought of. " \
        "Frustrating when it gave me wrong references, and I wasted time checking them. How do you feel about relying on AI tools for assignments? " \
        "I feel guilty if I use it too much. It’s like I’m not building the skill myself, even though it helps me finish on time."

        question = "how does AI help with assignments?"

        self.database.store_triples(interview_text)

        print(self.database.get_KG_context(question))



        


