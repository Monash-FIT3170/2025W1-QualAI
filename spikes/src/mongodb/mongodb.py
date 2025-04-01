from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://test_user:Username1!@cluster0.d2100na.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["sample_mflix"]
collection = db["movies"]

# Insert
# collection.insert_one({"Name": "Monkey", "Number": 12})

# Update
# collection.update_one({"Name": "Monkey", "Number": 12}, {"$set": {"Number": 999999999}})

# Delete
# collection.delete_one({"Name": "Monkey", "Number": 999999999})
# collection.delete_many({"Name": "Monkey"})

# Find
documents = collection.find({"Name": "Monkey"})
for document in documents:
    print(document)