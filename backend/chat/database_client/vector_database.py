from chat.database_client.database_client import DatabaseClient
from chat.text_transformer.text_vectoriser import TextVectoriser

from chat.highlighting.highlight_prioritiser import HighlightPrioritiser

from neo4j import GraphDatabase
from torch import Tensor
import re

class VectorDatabase(DatabaseClient):
    """
        A class for accessing and interacting with neo4j

        :author: Jonathan Farrand
        :modified: Felix Chung
    """
    def __init__(self):
        """
            Initialises NEO4JInteractor with driver to be used
        """
        # self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        # using one below for testing, top one isn't working for me - Rohan
        self._driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

        self.__vectoriser = TextVectoriser()

        self.__create_vector_index()
    
    def close_driver(self) -> None:
        """
            Closes the connection to the Neo4j database.
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
    
    def store_entries(self, entries, file_id, highlights):
        """
            Stores multiple vectors in the Neo4j database.

                :param list[tuple[str, list[float]]] vectors: A list containing the tuple pair of string and its corresponding vector
        """
        PRIORITY_MAP = {
            "IGNORE": -1,
            "LOW": 0,
            "HIGH": 1
        }
        entries = re.sub(r"<.*?>", "", entries)

        normalized_highlights = []
        for h in highlights:
            if "indexes" in h and isinstance(h["indexes"], dict):
                start = h["indexes"].get("index_start", 0)
                end = h["indexes"].get("index_end", 0)

                # Clamp indices to transcript length
                start = max(0, min(len(entries), start))
                end = max(start, min(len(entries), end))

                # Map priority string to number
                priority_str = h.get("priority", "").upper()  # make sure uppercase
                priority_num = PRIORITY_MAP.get(priority_str, 0)  # default to 0 if missing/unknown

                normalized_highlights.append({
                    "index_start": start,
                    "index_end": end,
                    "priority": priority_num
                })

        prioritiser = HighlightPrioritiser(transcript=entries, highlights=normalized_highlights)
        segments = prioritiser.priority_map

        for seg in segments:
            text= seg["text"]
            priority = seg["priority"]

            vectors = self.__vectoriser.chunk_and_embed_text(text)
            for text_chunk, vector in vectors: 
                self.store_vector_priority(text_chunk, file_id, vector, priority)

    def store_vector_priority(self, text_chunk, file_id, vector, priority) -> None:
        # Flatten and convert to float
        if isinstance(vector[0], Tensor):  # if it's a list of Tensors
            vector = [float(x) for x in vector[0]]

        client = self._driver
        with client.session() as session:
            session.run(
                """
                CREATE (e:Embedding {
                    text_chunk: $text_chunk, 
                    file_id: $file_id, 
                    vector: $vector, 
                    priority:$priority})
                """,
                text_chunk=text_chunk, vector=vector, file_id=file_id , priority=priority
            )

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

    def search(self, query):
        limit = 3
        client = self._driver 
        vector = self.__vectoriser.chunk_and_embed_text(query)[0][1]

        alpha = 1.0  # similarity weight
        beta = 0.5   # priority weight

        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (e:Embedding)
                WHERE e.priority IS NULL OR e.priority <> -1
                WITH e,
                    COALESCE(e.priority, 0) AS prio,
                    vector.similarity.cosine(e.vector, $vector) AS sim
                WITH e, sim, prio,
                    sim * $alpha + prio * $beta AS final_score
                RETURN e.text_chunk AS text, prio, sim, final_score
                ORDER BY final_score DESC
                LIMIT $limit
                """,
                vector=vector,
                alpha=alpha,
                beta=beta,
                limit=limit
            )

            return [record["text"] for record in result]

    # def search(self, query) -> list[str]:
    #     """
    #         Searches the Neo4j database for the vectors nearest to the one provided, using the cosine metric.

    #             :param list[Tensor] vector: the search query vector
    #             :param int limit:           the maximum number of results to return

    #             :return list[str]: the text chunks of the nearest vectors to the one provided
    #     """
    #     limit = 3
    #     client = self._driver
    #     vector = self.__vectoriser.chunk_and_embed_text(query)[0][1]
    #     with client.session() as session:
    #         result = session.run(
    #             """
    #             MATCH (e:Embedding)
    #             RETURN e.text_chunk
    #             ORDER BY vector.similarity.cosine(e.vector, $vector) DESC
    #             LIMIT $limit
    #             """,
    #             vector=vector, limit=limit
    #         )

    #         return [datum['e.text_chunk'] for datum in result.data()]
        
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
