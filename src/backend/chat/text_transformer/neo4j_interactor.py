from neo4j import GraphDatabase
from torch import Tensor

from config.config import NEO4J_URL


class Neo4JInteractor:
    """
        A class for accessing and interacting with neo4j

        :author: Jonathan Farrand
    """
    def __init__(self):
        """
            Initialises NEO4JInteractor with driver to be used
        """
        self._driver = GraphDatabase.driver(NEO4J_URL, auth=("neo4j", "testing123"))
        self.__create_vector_index()
    
    def close_driver(self) -> None:
        """
            Closes the connection to the Neo4j database.
        """
        self._driver.close()

    def store_multiple_vectors(self, vectors: list[tuple[str, list[Tensor]]], file_id) -> None:
        """
            Stores multiple vectors in the Neo4j database.

                :param list[tuple[str, list[float]]] vectors: A list containing the tuple pair of string and its corresponding vector
        """
        for vector_data in vectors:
            text_chunk = vector_data[0]
            vector = vector_data[1]
            self.store_vector(text_chunk, file_id, vector)

    def store_vector(self, text_chunk: str, file_id: str, vector: list[Tensor]) -> None:
        """
            Stores a vector in the Neo4j database.
                :param str file_id: the id of the file that the text chunk is coming from
                :param str text_chunk:                a text chunk for the vector to be stored
                :param list[Tensor] vector:     the vector to be stored
                
        """

        # Flatten and convert to float
        if isinstance(vector[0], Tensor):  # if it's a list of Tensors
            vector = [float(x) for x in vector[0]]

        client = self._driver
        with client.session() as session:
            session.run(
                """
                CREATE (e:Embedding {text_chunk: $text_chunk, file_id: $file_id, vector: $vector})
                """,
                text_chunk=text_chunk, vector=vector, file_id=file_id 
            )

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

    def search_text_chunk(self, vector: list[float], limit: int = 5) -> list[str]:
        """
            Searches the Neo4j database for the vectors nearest to the one provided, using the cosine metric.

                :param list[Tensor] vector: the search query vector
                :param int limit:           the maximum number of results to return

                :return list[str]: the text chunks of the nearest vectors to the one provided
        """
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
