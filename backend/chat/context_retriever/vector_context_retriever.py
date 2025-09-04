from chat.context_retriever.context_retriever import ContextRetriever
from chat.text_transformer.neo4j_interactor import Neo4JInteractor
from chat.text_transformer.text_vectoriser import TextVectoriser


class VectorContextRetriever(ContextRetriever):
    def __init__(self):
        self.vector_db = Neo4JInteractor()
        self.text_converter = TextVectoriser()
        
    def get_context(self, query: str) -> str:
        search_vector = self.text_converter.chunk_and_embed_text(query)[0][1]
        results = self.vector_db.search_text_chunk(search_vector, limit=3)
        return " ".join(results) if results else ""