from enum import Enum

class WordType(Enum):
    SUBJECT = 1
    QUALITY = 2
    CONNECTOR = 3
    IGNORE = 4
    SEPERATOR = 5
    PRONOUN = 6
    SELF_PRONOUN = 7
    SUBJECT_PRONOUN = 8
    MAIN_SUBJECT = 9
    OTHER = 10

PRONOUN = ["PRP", "PRP$"]
SELF_PRONOUN = ["i", "me", "we", "myself", "our", "ourselves", "us"]
SUBJECT_PRONOUN = ["it", "he", "she", "they", "these"]


SUBJECT = [ "NN", "NNS", "NNP", "CD"]
QUALITY = ["JJ", "JJS", "JJR"]
CONNECTOR = ["VBP", "VBG", "VBZ", "VB", "TO", "MD", "VBN", "RBR",  "VBD"]
SEPERATOR = [",", ".", "CC", "WRB"]
IGNORE = ["DT", "RB", "RP", "WP", "POS", "WDT", "IN"]

SUBJECT_BAD_APPLES = ["on"]

WORD_TYPES = dict()

for tag in SUBJECT:
    WORD_TYPES[tag] = WordType.SUBJECT

for tag in QUALITY:
    WORD_TYPES[tag] = WordType.QUALITY

for tag in CONNECTOR:
    WORD_TYPES[tag] = WordType.CONNECTOR

for tag in SEPERATOR:
    WORD_TYPES[tag] = WordType.SEPERATOR

for tag in PRONOUN:
    WORD_TYPES[tag] = WordType.PRONOUN

for tag in IGNORE:
    WORD_TYPES[tag] = WordType.IGNORE

for tag in SELF_PRONOUN:
    WORD_TYPES[tag] = WordType.SELF_PRONOUN

for tag in SUBJECT_PRONOUN:
    WORD_TYPES[tag] = WordType.SUBJECT_PRONOUN

