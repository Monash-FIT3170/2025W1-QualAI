from neo4j import GraphDatabase, Driver
from torch import Tensor

from config import NEO4J_URL, NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4JInteractor:
    """
        A class for accessing and interacting with neo4j

        :author: Jonathan Farrand
    """
    def __init__(self):
        """
            Initialises NEO4JInteractor with driver to be used
        """
        self._driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))    
    
    def close_driver(self) -> None:
        """
            Closes the connection to the Neo4j database.
        """
        self._driver.close()

    def store_multiple_vectors(self, vectors: list[tuple[str, list[float]]]) -> None:
        """
            Stores multiple vectors in the Neo4j database.

                :param list[tuple[str, list[float]]] vectors: A list containing the tuple pair of string and its corresponding vector
        """
        for vector_data in vectors:
            name = vector_data[0]
            vector = vector_data[1]
            self.store_vector(name, vector)

    
    def store_vector(self, name: str, vector: list[Tensor]) -> None:
        """
            Stores a vector in the Neo4j database.

                :param str name:                a name for the vector to be stored
                :param list[Tensor] vector:     the vector to be stored
        """
        client = self._driver
        with client.session() as session:
            session.run(
                """
                CREATE (e:Embedding {name: $name, vector: $vector})
                """,
                name=name, vector=vector
            )

    def search(self, vector: list[float], limit: int = 5) -> list[str]:
        """
            Searches the Neo4j database for the vectors nearest to the one provided, using the cosine metric.

                :param list[Tensor] vector: the search query vector
                :param int limit:           the maximum number of results to return

                :return list[str]: the names of the nearest vectors to the one provided
        """
        client = self._driver
        with client.session() as session:
            result = session.run(
                """
                MATCH (e:Embedding)
                RETURN e.name
                ORDER BY vector.similarity.cosine(e.vector, $vector) DESC
                LIMIT $limit
                """,
                vector=vector, limit=limit
            )

            return [datum['e.name'] for datum in result.data()]
        
    
    def remove_node_by_name(self, name: str) -> None:
        """
            Searches the Neo4j database for any nodes matching the provided name, and removes them.

                :param str name: the name of the nodes to be matched and removed
        """
        client = self._driver
        with client.session() as session:
            session.run(
                """
                MATCH (n)
                WHERE n.name = $name
                DELETE n
                """,
                name=name
            )

