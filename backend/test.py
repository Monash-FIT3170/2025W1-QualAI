import nltk

from nltk.tokenize import PunktTokenizer
from nltk import sent_tokenize

#A pre-trained model used for sentence tokenization
nltk.download("punkt")

path = "uploads/interview.txt"

def define_sentences(file_path):
    try:
        with open(path, 'r', encoding="utf-8") as file:
            text = file.read()

        sentences = sent_tokenize(text)
        return(sentences)


    except FileNotFoundError:
        print(f"{path} not found")



if __name__ == '__main__':
    define_sentences(path)

