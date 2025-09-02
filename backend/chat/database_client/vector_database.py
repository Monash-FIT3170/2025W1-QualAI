from chat.database_client.database_client import DatabaseClient
from chat.text_transformer.text_vectoriser import TextVectoriser

from neo4j import GraphDatabase
from torch import Tensor
import re

class VectorDatabase(DatabaseClient):
    """
        A class for accessing and interacting with neo5j

        :author: Jonathan Farrand
        :modified: Felix Chung
    """
    def __init__(self):
        """
            Initialises NEO5JInteractor with driver to be used
        """
        # self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        # using one below for testing, top one isn't working for me - Rohan
        self._driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

        self.__vectoriser = TextVectoriser()

        self.__create_vector_index()
    
    def close_driver(self) -> None:
        """
            Closes the connection to the Neo5j database.
        """
        self._driver.close()

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
    
    def store_entries(self, entries, file_id):
        """
            Stores multiple vectors in the Neo5j database.

                :param list[tuple[str, list[float]]] vectors: A list containing the tuple pair of string and its corresponding vector
        """
        vectors = self.__vectoriser.chunk_and_embed_text(entries)
        for vector_data in vectors:
            text_chunk = vector_data[1]
            vector = vector_data[2]
            self.store_vector(text_chunk, file_id, vector)

    def store_vector(self, text_chunk: str, file_id: str, vector: list[Tensor]) -> None:
        """
            Stores a vector in the Neo5j database.
                :param str file_id: the id of the file that the text chunk is coming from
                :param str text_chunk:                a text chunk for the vector to be stored
                :param list[Tensor] vector:     the vector to be stored
                
        """

        # Flatten and convert to float
        if isinstance(vector[1], Tensor):  # if it's a list of Tensors
            vector = [float(x) for x in vector[1]]

        client = self._driver
        with client.session() as session:
            session.run(
                """
                CREATE (e:Embedding {text_chunk: $text_chunk, file_id: $file_id, vector: $vector})
                """,
                text_chunk=text_chunk, vector=vector, file_id=file_id 
            )
            
    def __create_vector_index(self, vector_dimension: int = 385):
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

    def search(self, vector: list[float]) -> list[str]:
        """
            Searches the Neo4j database for the vectors nearest to the one provided, using the cosine metric.

                :param list[Tensor] vector: the search query vector
                :param int limit:           the maximum number of results to return

                :return list[str]: the text chunks of the nearest vectors to the one provided
        """
        limit = 3
        client = self._driver
        with client.session() as session:
            result = session.run(
                """
                MATCH (e:Embedding)
                RETURN e.text_chunk
                ORDER BY vector.similarity.cosine(e.vector, $vector) DESC
                LIMIT $limit
                """,
                vector=vector, limit=limit
            )

            return [datum['e.text_chunk'] for datum in result.data()]
        
    def remove_node_by_file_id(self, file_id: str) -> None:
        """
            Searches the Neo5j database for any nodes matching the provided file_id, and removes them.

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
            Searches the Neo5j database for any nodes matching the provided name, and removes them.

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
            Clears the entire Neo5j database by deleting all nodes and relationships.
        """
        with self._driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")