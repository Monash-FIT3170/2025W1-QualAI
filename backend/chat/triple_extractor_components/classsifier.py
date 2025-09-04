import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

from backend.chat.triple_extractor_components.constants import WORD_TYPES, WordType, SUBJECT_BAD_APPLES





class Classifier:
    """
    Classifies and groups words in a sentence based on their POS tags.
    """

    def __init__(self, sentence, tagged = False, speaker = "Speaker", interviewer = "Interviewer"):
        """
        Initializes the Classifier with a sentence.
        """
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('tagsets_json')

        if tagged:
            self.tagged_words = sentence
        else:
            self.tagged_words = self._sentence_reader(sentence)

        self.classified_sentence = []
        self.classified = False

        self.grouped_sentence = []
        self.grouped = False

        self._grouped_2_sentence = []
        self.grouped_2 = False
        

        self.speaker = speaker
        self.interviewer = interviewer


    def _sentence_reader(self, sentence):
        """
        Tokenizes and POS-tags the input sentence.
        """
        tokens = word_tokenize(sentence)
        tagged_words = pos_tag(tokens)
        return tagged_words

    def classify_sentence(self):
        """
        Classifies each word in the sentence based on its POS tag.
        """
        sentence_start = True
        for word, tag in self.tagged_words:
            word_type = self._classify_word(word, tag, sentence_start)
            if word_type is None:
                nltk.help.upenn_tagset(tag)
                
                raise ValueError(f"Unrecognized POS tag: {tag} | word: {word}")
              
            self.classified_sentence.append((word, tag, word_type))
            if tag == ".":
                sentence_start = True
            else:
                sentence_start = False

        self.classified = True


    def _classify_word(self, word, word_tag, sentence_start=True):
        """
        Classify individual words
        """
        if word.lower() != word and len(word) > 1 and sentence_start:
            word_tag = pos_tag([word.lower()])[0][1]
        
        if not sentence_start and word[0] == word[0].upper() and len(word) > 1:
            return WordType.SUBJECT
        return WORD_TYPES.get(word_tag)
    
    def print_classified_sentence(self):
        """
        Print classified sentence
        """
        if not self.classified:
            self.classify_sentence()
        for word, tag, word_type in self.classified_sentence:
            print(f"Word: {word}, Tag: {tag}, Classified as: {word_type}")
    
    def get_classified_sentence(self):
        """
        Return classified sentence
        """
        return self.classified_sentence
    

    def group_sentence(self):
        """
        Group sentence based on classifiers
        """

        if not self.classified:
            self.classify_sentence()
        grouped = []

        self.current_subject = ""
        self.subject_started = False
        self.current_connector = ""
        self.connector_started = False
        

        for index, (word, tag, word_type) in enumerate(self.classified_sentence):
            if index > 0:
                prev_word = self.classified_sentence[index-1][0]
                prev_type = self.classified_sentence[index-1][1]

            else:
                prev_word = None
                prev_type = None
            
            if index < len(self.classified_sentence) - 1:
                next_word = self.classified_sentence[index+1][0]
                next_type = self.classified_sentence[index+1][1]
            
            else:
                next_word = None
                next_type = None

            match word_type:
                case WordType.SUBJECT:
                    self.group_subject(word, word_type, next_word, next_type, prev_word, prev_type)
                    
                case WordType.CONNECTOR:
                    self.group_connector(word, word_type, next_word, next_type, prev_word, prev_type)
                    
                case WordType.QUALITY:
                    self.group_quality(word, word_type, next_word, next_type, prev_word, prev_type)
                    
                case WordType.SEPERATOR:
                    self.group_seperator(word, word_type, next_word, next_type, prev_word, prev_type)
                    
                case WordType.IGNORE:
                    self.group_ignore(word, word_type, next_word, next_type, prev_word, prev_type)
                    
                case WordType.PRONOUN:
                    self.group_pronoun(word, word_type, next_word, next_type, prev_word, prev_type)
                    

        if self.subject_started:
            self.grouped_sentence.append((self.current_subject, WordType.SUBJECT))
        
        elif self.connector_started:
            self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))

        self.grouped = True
        return self.grouped_sentence
    
    def get_grouped_2_sentence(self):
        if not self._grouped_2_sentence:
            self.sentence_grouper_two()
        return self._grouped_2_sentence
    
    
    def group_subject(self, word, word_type, next_word, next_type, prev_word, prev_type):
        if (word_type == WordType.SUBJECT) and (word.lower() not in SUBJECT_BAD_APPLES):
                
                if self.connector_started:
                    self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))
                self.current_connector = ""
                self.connector_started = False

                if not self.subject_started:
                    self.current_subject = word
                    self.subject_started = True
                
                elif self.subject_started:
                    self.current_subject += " " + word

    def group_quality(self, word, word_type, next_word, next_type, prev_word, prev_type):
        if self.connector_started:
            self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))
            self.connector_started = False
            self.current_connector = ""
        
        if prev_type != WordType.SUBJECT and self.subject_started:
            self.grouped_sentence.append((self.current_subject, WordType.SUBJECT))
            self.subject_started = False
            self.current_subject = ""
        
        if next_type == WordType.QUALITY:
            self.grouped_sentence.append((word + " " + next_word, word_type))
        
        elif prev_type != WordType.QUALITY:
            self.grouped_sentence.append((word, word_type))

    def group_connector(self, word, word_type, next_word, next_type, prev_word, prev_type):
        if self.subject_started:
            self.grouped_sentence.append((self.current_subject, WordType.SUBJECT))
        self.subject_started = False
        self.current_subject = ""
        
        if self.connector_started:
            # For cases like: I like to run
            self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))
            self.connector_started = False
            self.current_connector = ""
            self.subject_started = True
            self.current_subject = word

        else:
            self.connector_started = True
            self.current_connector = word
    
    def group_pronoun(self, word, word_type, next_word, next_type, prev_word, prev_type):
        if (word.lower() not in WORD_TYPES.keys()):
            person = self.interviewer

        elif (WORD_TYPES.get(word.lower()) == WordType.PRONOUN):
            person = self.interviewer

        else:
            if self.subject_started:
                self.grouped_sentence.append((self.current_subject, WordType.SUBJECT))
                self.current_subject = ""
                self.subject_started = False
            elif self.connector_started:
                self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))
                self.connector_started = False
                self.current_connector = ""
            
            self.grouped_sentence.append((word, WordType.SUBJECT_PRONOUN))
            return
        
        if self.subject_started:
            self.current_subject += " " + person
        else:
            if self.connector_started:
                self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))
                self.connector_started = False
                self.current_connector = ""
            self.subject_started = True
            self.current_subject = person

    def group_seperator(self, word, word_type, next_word, next_type, prev_word, prev_type):

        if self.connector_started:
            self.grouped_sentence.append((self.current_connector, WordType.CONNECTOR))
            self.connector_started = False
            self.current_connector = ""

        if self.subject_started:
            self.grouped_sentence.append((self.current_subject, WordType.SUBJECT))
            self.subject_started = False
            self.current_subject = ""

        self.grouped_sentence.append((word, word_type))
    
    def group_ignore(self, word, word_type, next_word, next_type, prev_word, prev_type):
        if prev_type == next_type:
            if self.subject_started:
                self.current_subject += " " + word
            elif self.connector_started:
                self.current_connector += "_" + word
        else:
            if self.subject_started and prev_type == WordType.SUBJECT:
                self.current_subject += " " + word
            elif self.connector_started and prev_type == WordType.CONNECTOR:
                self.current_connector += "_" + word
            elif prev_type == WordType.QUALITY:
                prev = self.grouped_sentence.pop()
                self.grouped_sentence.append((prev_word + " " + word, prev_type))


            

        #self.grouped_sentence.append((word, word_type))

    
    
    def print_grouped_sentence(self):
        if not self.grouped:
            self.group_sentence()

        sentence = ""
        for group, word_type in self.grouped_sentence:
            sentence += f"{group} ({word_type}) "
        print(sentence)

    def reset_sentence(self, new_sentence, tagged=False):
        if tagged:
            self.tagged_words = new_sentence
        else:
            self.tagged_words = self._sentence_reader(new_sentence)
        self.classified_sentence = []
        self.classified = False
        self.grouped_sentence = []
        self.grouped = False
        self.grouped_2 = False
        self._grouped_2_sentence = []

    def sentence_grouper_two(self):
        if not self.grouped:
            self.group_sentence()
        prev_word = None
        prev_type = None

        next_word = None
        next_type = None

        for count, (word, word_type) in enumerate(self.grouped_sentence):

            if count > 0:
                prev_word = self.grouped_sentence[count-1][0]
                prev_type = self.grouped_sentence[count-1][1]

            else:
                prev_word = None
                prev_type = None
            
            if count < len(self.grouped_sentence) - 1:
                next_word = self.grouped_sentence[count+1][0]
                next_type = self.grouped_sentence[count+1][1]
            
            else:
                next_word = None
                next_type = None
            
            if (word_type == WordType.SUBJECT) and (prev_type == WordType.QUALITY):
                self._grouped_2_sentence.append((prev_word + " " + word, word_type))
            

            elif (word_type == WordType.QUALITY) and (next_type == WordType.SUBJECT):
                pass

            else:
                self._grouped_2_sentence.append((word, word_type))
        
        self.grouped_2 = True
        self._connect_sentence()
        
    
    def _connect_sentence(self):
        prev_word = None
        prev_type = None

        next_word = None
        next_type = None

        store = []
        count = 0

        for count, (word, word_type) in enumerate(self._grouped_2_sentence):

            if count > 0:
                prev_word = self._grouped_2_sentence[count-1][0]
                prev_type = self._grouped_2_sentence[count-1][1]

            else:
                prev_word = None
                prev_type = None
            
            
            if count < len(self._grouped_2_sentence) - 1:
                next_word = self._grouped_2_sentence[count+1][0]
                next_type = self._grouped_2_sentence[count+1][1]
            
            else:
                next_word = None
                next_type = None

            if prev_type == word_type:
                store.append((prev_word + " " + word, word_type))
            
            elif word_type == next_type:
                pass

            else:
                store.append((word, word_type))

        self._grouped_2_sentence = store

    
    def print_grouped_sentence_two(self):
        if not self.grouped_2:
            self.sentence_grouper_two()
        sentence = ""
        for group, word_type in self._grouped_2_sentence:
            sentence += f"{group} ({word_type}) "
        print(sentence)    

    def get_subjects(self, sentence = None):
        if sentence:
            self.reset_sentence(sentence)
            response = self.get_grouped_2_sentence()
        else:
            response = self.get_grouped_2_sentence()
        
        subjects = []
        for word, word_type in response:
            if word_type == WordType.SUBJECT:
                subjects.append(word)
        return subjects

        
