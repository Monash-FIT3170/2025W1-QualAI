#
# vector_db.py
#
# A spike for testing the usage of the neo4j graph database for storage and retrieval of vector embeddings.
#
# Author: Kays Beslen
# Last modified: 29/03/25
#

from neo4j import GraphDatabase, Driver
from torch import Tensor

from openai_whisper import transcribe
from sentence_transformer import chunk_and_embed


def get_client(url: str, username: str, password: str) -> Driver:
    """
        Retrieves a client for the neo4j database.

            :param str url:         the location of the database server
            :param str username:    the user's username
            :param str password:    the user's password

            :return Driver: a driver acting as an authenticated database client
    """
    return GraphDatabase.driver(url, auth=(username, password))


def store_vector(client: Driver, name: str, vector: list[Tensor]) -> None:
    """
        Stores a vector in the neo4j database.

            :param Driver client:           the database client
            :param str name:                a name for the vector to be stored
            :param list[Tensor] vector:     the vector to be stored
    """
    with client.session() as session:
        session.run(
            """
            CREATE (e:Embedding {name: $name, vector: $vector})
            """,
            name=name, vector=vector
        )


def search(client: Driver, vector: list[Tensor], limit: int = 5) -> list[str]:
    """
        Searches the neo4j database for the vectors nearest to the one provided, using the cosine metric.

            :param Driver client:       the database client
            :param list[Tensor] vector: the search query vector
            :param int limit:           the maximum number of results to return

            :return list[str]: the names of the nearest vectors to the one provided
    """
    with client.session() as session:
        result = session.run(
            """
            MATCH (e:Embedding)
            RETURN e.name
            ORDER BY vector.similarity.cosine(e.vector, $vector)
            LIMIT $limit
            """,
            vector=vector, limit=limit
        )

        return [datum['e.name'] for datum in result.data()]


def close_client(client: Driver) -> None:
    """
        Closes the connection to the database.

            :param Driver client: the database client
    """
    client.close()


if __name__ == '__main__':
    cl = get_client("bolt://localhost:7687", "neo4j", "password")

    transcription = transcribe("../resources/hello.mp3")
    data = chunk_and_embed(transcription)

    store_vector(cl, data[0][0], data[0][1])
    print(search(cl, data[0][1], 1))

    close_client(cl)
