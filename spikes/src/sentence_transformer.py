#
# sentence_transformer.py
#
# A spike for testing the usage of the sentence-transformer framework for embedding text as vectors, as
# well as testing the usage of chunking models from the spacy framework.
#
# Author: Kays Beslen
# Last modified: 26/03/25
#

import spacy

from numpy import ndarray
from sentence_transformers import SentenceTransformer
from torch import Tensor


def chunk(text: str, chunker_name: str = 'en_core_web_sm') -> list[str]:
    """
        Chunks the provided text into semantically meaningful divisions. In this case, we are chunking by sentences.

            :param str text: the text to be chunked
            :param str chunker_name: the name of the chunking model to be used

            :return list[str]: a list containing the chunks processed from the text
    """
    chunker = spacy.load(chunker_name)
    chunks = chunker(text)

    return [sentence.text for sentence in chunks.sents]


def embed_chunks(chunks: list[str], model_name: str = 'all-MiniLM-L6-v2') -> list[tuple[str, list[Tensor]]]:
    """
        Generates a vector embedding for each of the provided chunks of text using a sentence transformer model.

            :param list[str] chunks:    the list of chunks
            :param str model_name:      the name of the sentence transformer model being used

            :return list[tuple[str, list[Tensor]]]:  a list of tuples containing chunks and corresponding embeddings
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(chunks)

    return list(zip(chunks, embeddings))


def chunk_and_embed(
    text: str, chunker_name: str = 'en_core_web_sm', model_name: str = 'all-MiniLM-L6-v2'
) -> list[tuple[str, list[Tensor]]]:
    """
        Chunks text and generates a vector embedding for each chunk. See #chunk_text and #embed_chunks.
    """
    return embed_chunks(chunk(text, chunker_name), model_name)


if __name__ == '__main__':
    print(chunk_and_embed("Sentence 1. Sentence 2."))
