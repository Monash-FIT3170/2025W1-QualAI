import unittest

from backend.chat.database_client.graph_database import GraphDatabase
from backend.chat.basic_triple_extractor import BasicTripleExtractor
from backend.chat.deepseek_client import DeepSeekClient

class TestQuestionAnswerTriples(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.database = GraphDatabase()
        self.database.clear_database()
        self.triple_extractor = BasicTripleExtractor()
        self.deepseek = DeepSeekClient()


    def test_upload(self):
        self.database.store_triple("Jonathan", "is_mad", "with NEO4J")
        print(self.database.search("Jonathan"))
        self.database.close_driver()

    def test_interview_one(self):
        interview_text = "How has AI influenced your learning experience? It’s made studying faster — I can get summaries of long readings in minutes. " \
        "But sometimes I feel like I’m skipping the real depth of the material. Can you describe a time when AI was especially helpful or frustrating? " \
        "Helpful when I used an AI writing tool to brainstorm essay ideas — it gave me perspectives I hadn’t thought of. " \
        "Frustrating when it gave me wrong references, and I wasted time checking them. How do you feel about relying on AI tools for assignments? " \
        "I feel guilty if I use it too much. It’s like I’m not building the skill myself, even though it helps me finish on time."

        interviewee_name = "John"
        interviewer_name = "Josh"

        triples = self.triple_extractor.get_triples(interview_text, interviewer_name, interviewee_name)
        for (subject, predicate, object) in triples:
            self.database.store_triple(subject, predicate, object, "interview_one")

        results = self.database.search(interviewee_name)
        print(results)


        response = self.deepseek.chat_with_model_triples(results, "What was Josh's response to the questions?")
        print(f"Response {response}")

    
    def test_interview_two(self):
        interview_text = "How has AI influenced your learning experience? It’s boosted my confidence." \
        " I can ask AI to explain tough math concepts in simpler terms, which teachers don’t always have time for." \
        " Can you describe a time when AI was especially helpful or frustrating? Helpful when I had an exam — AI gave me practice questions." \
        " Frustrating when the answers it gave were too simplified, and I didn’t learn the deeper logic." \
        " How do you feel about relying on AI tools for assignments? Honestly, I see it as a calculator." \
        " It’s fine to use, but I don’t want to depend on it so much that I can’t think critically on my own."

        interviewee_name = "Alex"
        interviewer_name = "Josh"

        triples = self.triple_extractor.get_triples(interview_text, interviewer_name, interviewee_name)
        for (subject, predicate, object) in triples:
            self.database.store_triple(subject, predicate, object, "interview_two")
        
        results = self.database.search(interviewee_name)

    
    def test_interview_three(self):
        interview_text = "How has AI influenced your learning experience? Mixed feelings." \
        " It makes learning more accessible — I can get personalized feedback instantly." \
        " But it also feels like I’m talking to a machine, not a mentor." \
        " Can you describe a time when AI was especially helpful or frustrating?" \
        " Helpful when I was practicing English writing — it corrected my grammar and style instantly." \
        " Frustrating when I asked it about history, and it gave me overconfident but wrong facts." \
        " How do you feel about relying on AI tools for assignments? I like using it as a helper, but I wouldn’t trust it fully." \
        " I’d rather combine AI input with my own research and what my professors teach."

        interviewee_name = "Sam"
        interviewer_name = "Josh"

        triples = self.triple_extractor.get_triples(interview_text, interviewer_name, interviewee_name)
        for (subject, predicate, object) in triples:
            self.database.store_triple(subject, predicate, object, "interview_two")
        
        results = self.database.search(interviewee_name)



        


