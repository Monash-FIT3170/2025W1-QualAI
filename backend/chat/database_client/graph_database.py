from chat.database_client.database_client import DatabaseClient
from chat.deepseek_client import DeepSeekClient

from neo4j import GraphDatabase as Neo4jGraphDatabase
from chat.basic_triple_extractor import BasicTripleExtractor
from chat.text_transformer.text_vectoriser import TextVectoriser
import random
from torch import Tensor
import re

class GraphDatabase(DatabaseClient):
    """
        A class for accessing and interacting with neo4j

        :author: Jonathan Farrand
    """
    def __init__(self):
        """
            Initialises NEO4JInteractor with driver to be used
        """
        #self._driver = Neo4jGraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
        # using one below for testing, top one isn't working for me - Rohan
        self._driver = Neo4jGraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

        self.__create_vector_index()
        self.__deepseek_client = DeepSeekClient()
        self.__triple_extractor = BasicTripleExtractor()
        self.__vectoriser = TextVectoriser()
    
    def close_driver(self) -> None:
        """
            Closes the connection to the Neo4j database.
        """
        self._driver.close()
        
    def store_entries(self, text, file_id: str = None):
        """
            Stores multiple triples in Neo4j.

            :param triples: List of (subject, predicate, object) tuples
            :param file_id: Optional document ID for metadata
        """
        interviewee_id = "id" + str(random.randrange(0,1000))
        triples = self.__triple_extractor.get_triples(text, "John Smith", interviewee_id)
        #triples = self.__deepseek_client.chat_extract_triples(text)
        
        for subj, pred, obj in triples:
            self.store_triple(subj, pred, obj, file_id)

    @staticmethod
    def slugify_reltype(rel_type: str) -> str:
        """
            Converts a relationship string into a Neo4j-safe relationship type.

            :param rel_type: Relationship string
            :return: Uppercase, underscore-separated string
        """
        rel_type = rel_type.strip().lower()
        rel_type = re.sub(r'[^a-z0-9]+', '_', rel_type)
        return rel_type.upper()
    
    def store_triple(self, subject: str, predicate: str, object_: str, file_id: str = None):
        """
            Stores a single triple in Neo4j as nodes and a relationship.

            :param subject: Subject node
            :param predicate: Relationship type
            :param object_: Object node
            :param file_id: Optional document ID for metadata
        """
        rel_type = self.slugify_reltype(predicate)
        with self._driver.session() as session:
            session.execute_write(self._merge_triple, subject, object_, rel_type, file_id)
   
    @staticmethod
    def _merge_triple(tx, subject, object_, rel_type, file_id):
        """
            Internal Cypher query to merge nodes and create a relationship.

            :param tx: Transaction object
            :param subject: Subject node
            :param object_: Object node
            :param rel_type: Relationship type
            :param file_id: Optional document ID
        """
        query = f"""
        MERGE (s:Entity {{name: $subject}})
        MERGE (o:Entity {{name: $object}})
        MERGE (s)-[r:{rel_type}]->(o)
        """
        # Add file_id if provided
        if file_id:
            query += """
            SET r.file_id = $file_id
            SET s.file_id = $file_id
            SET o.file_id = $file_id
            """

        vectoriser = TextVectoriser()
        subject_vector = vectoriser.chunk_and_embed_text(subject)[0][1]
        object_vector = vectoriser.chunk_and_embed_text(object_)[0][1]

        if subject_vector is not None:
            query += """
            MERGE (sv:Embedding {file_id: $file_id, text_chunk: $subject})
            SET sv.vector = $subject_vector
            MERGE (s)-[:HAS_EMBEDDING]->(sv)
            """
        if object_vector is not None:
            query += """
            MERGE (ov:Embedding {file_id: $file_id, text_chunk: $object})
            SET ov.vector = $object_vector
            MERGE (o)-[:HAS_EMBEDDING]->(ov)
            """

        tx.run(query, subject=subject, object=object_, file_id=file_id, subject_vector=subject_vector, object_vector=object_vector)
            
    def __create_vector_index(self, vector_dimension: int = 384):
        """
        Creates a vector index on the 'vector' property of Embedding nodes.

        :param vector_dimension: Dimensionality of the stored vectors.
        """
        client = self._driver
        with client.session() as session:
            session.run("""
            CREATE VECTOR INDEX embedding_vector_index IF NOT EXISTS
            FOR (e:Embedding) ON (e.vector)
            OPTIONS { 
                indexConfig: {
                    `vector.dimensions`: $dims,
                    `vector.similarity_function`: 'cosine'
                }
            }
            """, dims=vector_dimension)
        
    def remove_node_by_file_id(self, file_id: str) -> None:
        """
            Searches the Neo4j database for any nodes matching the provided file_id, and removes them.

                :param str file_id: the file_id to be matched and removed
        """
        client = self._driver
        
        with client.session() as session:
            session.run(
                """
                MATCH (n)
                WHERE n.file_id = $file_id
                DETACH DELETE n
                """,
                file_id=file_id
            )

        

    def remove_node_by_text(self, text_chunk: str) -> None:
        """
            Searches the Neo4j database for any nodes matching the provided name, and removes them.

                :param str text_chunk: the text chunk of the nodes to be matched and removed
        """
        client = self._driver
        with client.session() as session:
            session.run(
                """
                MATCH (n)
                WHERE n.text_chunk = $text_chunk
                DELETE n
                """,
                text_chunk=text_chunk
            )
    
    def clear_database(self):
        """
            Clears the entire Neo4j database by deleting all nodes and relationships.
        """
        with self._driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def search(self, entity, top_k: int = 3, hops: int = 1): 
        # todo : find entity to search
        results = self.__triple_extractor.get_subjects(entity)
        vector = self.__vectoriser.chunk_and_embed_text(results[0])
    
        if not vector:
            return []

        query_vector = vector[0][1]  # first subject for testing

        
        vector_search_query = """
        MATCH (e:Embedding)
        RETURN e.text_chunk AS chunk, e.file_id AS file_id, vector.similarity.cosine(e.vector, $vector) AS score
        ORDER BY score DESC
        LIMIT $limit
        """

        with self._driver.session() as session:
            top_chunks = session.run(vector_search_query, vector=query_vector, limit=top_k)
            results = []

            for record in top_chunks:
                chunk_text = record["chunk"]
                file_id = record["file_id"]

                
                traverse_query = f"""
                MATCH (e:Embedding {{text_chunk: $chunk}})
                OPTIONAL MATCH (e)<-[:HAS_EMBEDDING]-(n1:Entity)-[r1*1..{hops}]-(m1:Entity)
                OPTIONAL MATCH (e)<-[:MENTIONS]-(n2:Entity)-[r2*1..{hops}]-(m2:Entity)
                OPTIONAL MATCH (e)<-[:HASRESPONSE]-(n3:Entity)-[r3*1..{hops}]-(m3:Entity)
                RETURN DISTINCT 
                    n1.name AS subject1, [rel IN r1 | type(rel)] AS relations1, m1.name AS object1,
                    n2.name AS subject2, [rel IN r2 | type(rel)] AS relations2, m2.name AS object2,
                    n3.name AS subject3, [rel IN r3 | type(rel)] AS relations3, m3.name AS object3
                """
                neighbors = session.run(traverse_query, chunk=chunk_text)

                neighbor_list = [dict(neighbor) for neighbor in neighbors if neighbor is not None]

                results.append({
                    "text_chunk": chunk_text,
                    "file_id": file_id,
                    "neighbors": neighbor_list
                })
        
        # todo fix filter method so it works better
        text_chunks = []
        responses = []

        for res in results:
            text_chunks.append(res["text_chunk"])
            for neighbor in res["neighbors"]:
                # Flatten all non-None values from subject/relations/object
                for key, value in neighbor.items():
                    if value is not None:
                        responses.append(value)

        print("Text chunks:", text_chunks)
        print("Responses:", responses)
        return text_chunks
            
    def run_cypher_query(self, query: str, params: dict = None):
        """
        Executes a raw Cypher query against the Neo4j database.

        :param query: The Cypher query string to run.
        :param params: Optional dictionary of parameters to pass to the query.
        :return: List of dictionaries representing each record returned.
        """
        with self._driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]
        
    def rekey_node(self, file_id: str, new_id: str) -> None:
        """
        Searches the database for any nodes matching the provided file id, and rekeys with the provided id.

        :param file_id: the id of the file to be rekeyed
        :param new_id: the new id of the file
        """
        client = self._driver
        with client.session() as session:
            session.run(
                """
                MATCH (n)
                WHERE n.file_id = $file_id
                SET n.file_id = $new_id
                """,
                file_id=file_id,
                new_id=new_id
            )