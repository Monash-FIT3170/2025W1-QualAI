from __future__ import annotations

import re
from typing import Mapping, Any

from pymongo import MongoClient
from pymongo.synchronous.cursor import Cursor
from pymongo.synchronous.database import Database

from config import config


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

        def get_collection_names(self) -> list[str]:
            return self.__database.list_collection_names()

        def get_collections(self) -> list[DocumentStore.Collection]:
            collections = []
            for collection_name in self.__database.list_collection_names():
                collections.append(self.create_collection(collection_name))
            return collections

        def get_collection(self, collection_name: str) -> DocumentStore.Collection | None:
            """
            Retrieves a collection within this database, with the provided name.

            :return: the retrieved collection, if it exists; else, None
            """
            if collection_name in self.__database.list_collection_names():
                return self.create_collection(collection_name)
            return None

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
            db = database.client()

            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)

            self.__collection = db.get_collection(collection_name)

        def get_all_documents(self) -> Cursor[Mapping[str, Any]]:
            """
            Retrieves all documents within this collection.

            :return: A mapping for all documents within this collection
            """
            return self.__collection.find()

        def add_document(self, document_name: str, content: str) -> str:
            """
            Inserts the provided document into the collection.

            :param document_name: the name associated with the provided document
            :param content: the document content to be added to the collection

            :return: the updated document_name

            :raises KeyError: if the provided document key is not unique amongst all documents in this collection
            """
            if self.find_document(document_name) is not None:
                raise KeyError(
                    f"The provided document key, {document_name}, must be unique between all documents within the "
                    f"collection."
                )

            document: dict[str, str] = {"key": document_name, "content": content}
            self.__collection.insert_one(document)
            return document_name

        def update_document_name(self, document_name: str) -> str:
            base_name = document_name

            prefix_regex = f"^{re.escape(base_name)}"
            existing_count = self.__collection.count_documents({"key": {"$regex": prefix_regex}})

            if existing_count > 0:
                count = existing_count
                document_name = f"{base_name}_{count}"

                while self.find_document(document_name) is not None:
                    count += 1
                    document_name = f"{base_name}_{count}"

            return document_name

        def update_dir_name(self, dir_name: str) -> str:
            prefix_regex = f"^{re.escape(dir_name)}(_\\d+)?/"
            existing_keys = list(self.__collection.find({"key": {"$regex": prefix_regex}}))

            if not existing_keys or len(existing_keys) == 0:
                return dir_name

            max_suffix = 0
            for doc in existing_keys:
                key = doc["key"]
                m = re.match(f"{re.escape(dir_name)}_(\\d+)/", key)
                if m:
                    suffix = int(m.group(1))
                    max_suffix = suffix if suffix > max_suffix else max_suffix

            return f"{dir_name}_{max_suffix + 1}"

        def find_document(self, document_key: str) -> Mapping[str, Any] | None:
            """
            Finds a document with the provided key from within the collection.

            :param document_key: a unique identifier associated with the document

            :return: the document with the corresponding key
            """
            return self.__collection.find_one({"key": document_key})
        
        def update_document(self, document_key: str, new_content: str) -> bool:
            """
            Updates the content of the document with the provided key within the collection.

            :param document_key: a unique identifier associated with the document
            :param new_content: the new content to be set for the document
            """
            result = self.__collection.update_one({"key": document_key}, {"$set": {"content": new_content}})
            return result.modified_count > 0

        def rename_document(self, document_key: str, new_name: str) -> bool:
            """
            Renames the document, by updating its key in the database.

            :param document_key: a unique identifier associated with the document
            :param new_name: the name to be used as the new key for the document

            :returns: whether the document was successfully renamed
            """
            if self.find_document(new_name) is not None:
                raise KeyError(
                    f"The provided document key, {new_name}, must be unique between all documents within the "
                    f"collection."
                )
            result = self.__collection.update_one({ "key": document_key }, { "$set": { "key" : new_name } })
            return result.modified_count > 0

        def matching_documents(self, regex: str) -> Cursor[Mapping[str, Any]]:
            """
            :return: the set of documents with key matching the provided regex expression
            """
            return self.__collection.find({ "key" : { "$regex": regex }})
        
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
        return None

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

