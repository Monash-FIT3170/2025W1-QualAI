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

def extract_triples(sentence):
    inputs = tokenizer(sentence, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=256)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded

if __name__ == '__main__':
    sentences = define_sentences(path)

    triples = []
    for sentence in sentences:
        result = extract_triples(sentence)
        triples.append(result)
        print(result)

    

