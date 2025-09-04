from chat.triple_extractor_components.classsifier import Classifier


class BasicTripleExtractor:
    """
    Class to extract basic triples from interview data,
    triples are focused around the question, response and interviewee.

    Author: Jonathan Farrand
    """
    def __init__(self):
        """
        Nothing needed at the moment
        """
        # self.__classifier = cl
        pass

    def get_triples(self, text, interviewer_id, interviewee_id):
        """
        Returns a list of triples based on responses and questions.
        """

        get_information = self._get_question_response_pair(text)
        triples_list = []

        for question in get_information.keys():
            response = get_information.get(question)
            triples_list.append((interviewee_id, "answered", question))
            triples_list.append((question, "hasResponse", response))
            triples_list.append((response, "answeredBy", interviewee_id))

            for subject in self._get_subjects(response):
                triples_list.append((response, "mentions", subject))
        
        return triples_list

    def _get_subjects(self, response):
        """
        Yet to be implemented, will be used to draw themes and subjects from responses.
        """
        return []

    def _get_question_response_pair(self, text):
        """
        Divides the text into questions and responses
        """
        pairs = dict()

        cur_response = ""
        prev_question = ""
        cur_sentence = ""

        sentence_finishes = [".", "!", ";", "?"]

        for letter in text:
            cur_sentence += letter
            if letter == "?":
                if prev_question is not None and cur_response is not None:
                    pairs[prev_question] = cur_response
                    cur_response = ""

                prev_question = cur_sentence
                cur_sentence = ""
                
            elif letter in sentence_finishes:
                cur_response += cur_sentence
                cur_sentence = ""
        if prev_question not in pairs:
            pairs[prev_question] = cur_response
        
        return pairs
