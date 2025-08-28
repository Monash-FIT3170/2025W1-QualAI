from backend.chat.context_retriever.context_retriever import ContextRetriever
from backend.chat.deepseek_client import DeepSeekClient
from backend.chat.text_transformer.neo4j_interactor import Neo4JInteractor

class TripleContextRetriever(ContextRetriever):
    def __init__(self):
        self.deepseek_client = DeepSeekClient()
        self.neo4j_interactor = Neo4JInteractor()
        
    def get_context(self, query: str) -> str:
        """
        Process a chat message return the model's reponse. 
        Extracts triples form the query then searchs in Knowledge Graph database for context. 

        :param str message: The message to send to the model. 
        :return: The JSON response from the API 
        """ 
        triples = self.deepseek_client.chat_extract_triples(query)
        
        context_triples = ""

        for triple in triples: 
            subject = triple[0]
            object = triple[1]
            result = self.neo4j_interactor.search_by_entity(subject)

            for row in result:
                context_triples += f"{row['subject']} {row['predicate']} {row['object']}, "
            
            result = self.neo4j_interactor.search_by_entity(object)

            for row in result:
                context_triples += f"{row['subject']} {row['predicate']} {row['object']}, "
                
        return context_triples
