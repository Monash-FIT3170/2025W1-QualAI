import nltk

from nltk.tokenize import PunktTokenizer
from nltk import sent_tokenize

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#A pre-trained model used for sentence tokenization
nltk.download("punkt")

path = "uploads/interview.txt"

model_name = "Babelscape/rebel-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def define_sentences(file_path): 
    try:
        with open(path, 'r', encoding="utf-8") as file:
            text = file.read()

        sentences = sent_tokenize(text)
        return(sentences)

    except FileNotFoundError:
        print(f"{path} not found")


def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets


if __name__ == '__main__':
    sentences = define_sentences(path)

    # print(sentences)

    # triples = []
    # for sentence in sentences:
    #     result = extract_triples(sentence)
    #     triples.append(result)
    #     print(result)

    

