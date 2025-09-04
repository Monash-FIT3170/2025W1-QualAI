from ..deepseek_client import DeepSeekClient
from ..text_transformer.neo4j_interactor import Neo4JInteractor
from ..text_transformer.text_vectoriser import TextVectoriser

class KnowledgeGraphPipeline:
    """
    A class for converting texts to triples and storing them in a database.

    :author: Jonathan Farrand
    """
    def __init__(self, chunk_length = 300, overlap = 100, deepseek_client: DeepSeekClient = None, neo4j_interactor: Neo4JInteractor = None, text_vectoriser: TextVectoriser = None):
        """
        Initialises the TriplesPipeline class with the relevant classes.
        """
        self.deepseek_client = deepseek_client
        self.neo4j_interactor = neo4j_interactor
        self.text_vectoriser = text_vectoriser
        self.chunk_length = chunk_length
        self.overlap = overlap
        
        if deepseek_client is None:
            self.deepseek_client = DeepSeekClient()

        if neo4j_interactor is None:
            self.neo4j_interactor = Neo4JInteractor()
        
        if text_vectoriser is None:
            self.text_vectoriser = TextVectoriser()

    def process_and_store_triples(self, text):
        """
        Processes the text to extract triples and stores them in the Neo4j database.
        """
        chunks = self.text_vectoriser.chunk_by_sentence(text, 4, 1)
        all_triples = []
        print("Chunking")

        for chunk in chunks:  
            print(f"Processing chunk: {chunk}")
            triples = self.deepseek_client.text_to_triples(chunk)
            print(f"Extracted triples: {triples}")
            for triple in triples:
                all_triples.append(triple)

        for triple in all_triples:
            try:
                subject, predicate, object = triple
                print(f"Storing triple: {subject}, {predicate}, {object}")
                
                self.neo4j_interactor.store_triple(subject, predicate, object)
            except Exception as e:
                print(f"Error storing triple {triple}: {e}")
        return all_triples