from __future__ import annotations

from typing import Mapping, Any

from src.config import config

from pymongo import MongoClient
from pymongo.synchronous.database import Database


class DocumentStore:
    """
    This class represents a store for documents, utilising a MongoDB database.

    A document store consists of a set of databases, which each consists of a set of collections. Each collection
    contains a set of documents, which are constructed from dict instances.

    :author: Kays Beslen
    """

    class Database:
        """
        This class represents a database within the document store.

        :author: Kays Beslen
        """

        def __init__(self, document_store: DocumentStore, database_name: str) -> None:
            """
            Instantiates a database with the provided name, within the provided document store.

            :param document_store: the document store this database is to be constructed within
            :param database_name: the name of the database
            """
            self.__database = document_store.client()[database_name]

        def get_collection(self, collection_name: str) -> DocumentStore.Collection | None:
            """
            Retrieves a collection within this database, with the provided name.

            :return: the retrieved collection, if it exists; else, None
            """
            if collection_name in self.__database.list_collection_names():
                return self.create_collection(collection_name)

        def create_collection(self, collection_name: str) -> DocumentStore.Collection:
            """
            Creates a collection within this database, with the provided name.

            :return: the created collection, if it does not exist; else, the existing collection with the same name
            """
            return DocumentStore.Collection(self, collection_name)

        def delete_collection(self, collection_name: str) -> None:
            """
            Deletes the collection with the provided name from this database.
            """
            self.__database.drop_collection(collection_name)

        def client(self) -> Database[Mapping[str, Any]]:
            """
            The database client.
            """
            return self.__database

    class Collection:
        """
        This class represents a collection within the document store.

        :author: Kays Beslen
        """
        def __init__(self, database: DocumentStore.Database, collection_name: str) -> None:
            self.__collection = database.client().get_collection(collection_name)

        def add_document(self, document_name: str, document_key: str, document: dict) -> None:
            """
            Inserts the provided document into the collection.

            :param document_key: the unique key associated with the provided document
            :param document: the document to be added into the collection

            :raises KeyError: if the provided document key is not unique amongst all documents in this collection
            """
            if self.find_document(document_key) is not None:
                raise KeyError(
                    f"The provided document key, {document_key}, must be unique between all documents within the "
                    f"collection."
                )
            document["name"] = document_name
            document["key"] = document_key
            self.__collection.insert_one(document)

        def find_document(self, document_key: str) -> Mapping[str, Any] | None:
            """
            Finds a document with the provided key from within the collection.

            :param document_key: a unique identifier associated with the document

            :return: the document with the corresponding key
            """
            return self.__collection.find_one({"key": document_key})
        
        def remove_document(self, document_key: str) -> None:
            """
            Removes the document with the provided key from the collection.

            :param document_key: a unique identifier associated with the document
            """
            self.__collection.delete_one({"key": document_key})
        

    # Global variable for connecting to the MongoDB client.
    URI = config.MONGO_URI

    def __init__(self) -> None:
        self.__client = MongoClient(DocumentStore.URI)

    def get_database(self, database_name: str) -> DocumentStore.Database | None:
        """
        Retrieves the database with the specified name.

        :return: the database with the specified name, if it exists; else, None
        """
        if database_name in self.__client.list_database_names():
            return self.create_database(database_name)

    def create_database(self, database_name: str) -> DocumentStore.Database:
        """
        Creates a database with the specified name within this document store.

        :return: the created database, if it does not exist; else, the database with the same name
        """
        return DocumentStore.Database(self, database_name)

    def client(self) -> MongoClient:
        """
        The MongoDB client.
        """
        return self.__client


if __name__ == "__main__":
    ds = DocumentStore()
    db = ds.create_database("test_db")
    collection = db.create_collection("test")
    doc = {"content": "hello"}
    collection.add_document("test-doc", "test", doc)
    print(collection.find_document("test"))
