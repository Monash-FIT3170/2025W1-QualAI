import spacy
from torch import Tensor
from sentence_transformers import SentenceTransformer

class TextVectoriser:
    """
    A class for converting files and text to vectors

    :author: Jonathan Farrand
    """
    def __init__(self, chunker_name: str = "en_core_web_sm", model_name: str = "all-MiniLM-L6-v2"):
        """
            Initializes the TextVectoriser class with the chunker name and the model name. 
            Creates variables to store whether the chunker and sentence transformer model have already been used.

            :param chunker_name: the name of the chunker model being used
            :param model_name: the type of LLM being used
        """
        self._chunker = spacy.load(chunker_name)
        self._model = SentenceTransformer(model_name)
    
    def chunk_text(self, text:str, max_length: int = 200, overlap: int = 50) -> list[str]:
        """
            Chunks the text into semanitcally meaningful divisions, with a maxium given length. 
            Gives overlap between chunks to ensure provide further context to the model
            
            :param str text: the text to be chunked
            :param int max_length: the maximum length of each chunk
            :param int overlap: the number of tokens to overlap between chunks
            
            :return list[str]: a list containing the chunks processed from the text
        """
        chunker = self._chunker
        doc = chunker(text)

        tokens = [token.text_with_ws for token in doc]
        chunks = []
        start = 0

        while start < len(tokens):
            end = start + max_length
            chunk_tokens = tokens[start:end]
            chunk_text = "".join(chunk_tokens).strip()
            chunks.append(chunk_text)

            # Shift start index back by overlap to include previous context
            start = end - overlap if end - overlap > start else end 

        return chunks

    def embed_text(self, chunks: list[str]) -> list[tuple[str, list[Tensor]]]:
        """
            Generates a vector embedding for each of the provided chunks of text using a sentence transformer model.

            :param list[str] chunks:    the list of chunks

            :return list[tuple[str, list[Tensor]]]:  a list of tuples containing chunks and corresponding embeddings
        """
        model = self._model
        embeddings = model.encode(chunks)
        return list(zip(chunks, embeddings))


    def chunk_and_embed_text(self, text: str) -> list[tuple[str, list[Tensor]]]:
        """
            Chunks text and generates a vector embedding for each chunk. See #chunk_text and #embed_chunks.
        """
        return self.embed_text(self.chunk_text(text))