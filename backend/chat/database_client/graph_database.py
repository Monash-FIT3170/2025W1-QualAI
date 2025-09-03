from ...chat.database_client.database_client import DatabaseClient
from ...chat.deepseek_client import DeepSeekClient

from neo4j import GraphDatabase as Neo4jGraphDatabase
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
        self._driver = Neo4jGraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
        # using one below for testing, top one isn't working for me - Rohan
        # self._driver = Neo4jGraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

        self.__create_vector_index()
        self.__deepseek_client = DeepSeekClient()
    
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
        triples = self.__deepseek_client.chat_extract_triples(text)
        
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
            query += " SET r.file_id = $file_id"

        tx.run(query, subject=subject, object=object_, file_id=file_id)
            
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
                DELETE n
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

    def search(self, entity): 
        # todo : find entity to search
        subject_query = """
        MATCH (s:Entity)-[r]->(o:Entity)
        WHERE s.name = $subject
        RETURN s.name AS subject, type(r) AS predicate, o.name AS object
        """
        subject_params = {"subject": entity}

        subject_results = self.run_cypher_query(subject_query, subject_params)
        return subject_results
            
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
