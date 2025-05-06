from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URI

class MongoInteractor:
    """
        A class for accessing and interacting with Mongo D

        :author: Jonathan Farrand
    """
    def __init__(self):
        """
            Initializes the MongoInteractor class for interacting with the MongoDB database client
        """
        self.client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

    def retrieve_single_file(self, database_name: str, collection_name: str, file_identifier: str, identifier_key: str="title", data_key: str = "content"):
        """
            Retrieves a single file data from the mongo database

            :param database_name: The name of the database to access the data from
            :param collection_name: The name of the collection to access the data from
            :param file_identifier: The identifier of the json file to access
            :param identifier_key: The json key that the identifier is linked to *Initially set to "title" should be changed to the default once agreed upon*
            :param data_key: The json key for where the text can be found *Initially set to "content" should be changed to the default once agreed upon*

            :return: The data for the specified file
        """
        client = self.client
        db = client[database_name]
        collection = db[collection_name]
        query = {identifier_key : file_identifier}
        file = collection.find_one(query)

        if not file or data_key not in file:
            raise ValueError(f"Document with {identifier_key}='{file_identifier}' not found or missing {data_key}.")
        
        return file[data_key]
    
    def retrieve_multiple_files(self, database_name: str, collection_name: str, file_identifier: str, identifier_key: str = "title", data_key: str = "content"):
        """
            Retrieves multiples files data from the mongo database

            :param database_name: The name of the database to access the data from
            :param collection_name: The name of the collection to access the data from
            :param file_identifier: The identifier of the json file to access
            :param identifier_key: The json key that the identifier is linked to *Initially set to "title" should be changed to the default once agreed upon*
            :param data_key: The json key for where the text can be found *Initially set to "content" should be changed to the default once agreed upon*

            :return: An array containing the data for all files that match the set of keys
        """
        client = self.client
        db = client[database_name]
        collection = db[collection_name]
        query = {identifier_key : file_identifier}
        files = collection.find(query)

        data = []
        for file in files:
            if data_key not in file:
                raise ValueError(f"Document with {identifier_key}='{file.get(identifier_key, '?')}' is missing {data_key}.")
            data.append(file[data_key])

        if not data:
            raise ValueError(f"No documents with key '{identifier_key}' in {file_identifier} found.")

        return data