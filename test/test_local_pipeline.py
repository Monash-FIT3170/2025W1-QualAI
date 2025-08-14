import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from backend.mongodb.DocumentStore import DocumentStore
from backend.chat.text_transformer.text_pipeline import TextPipeline

# Step 1: Connect to MongoDB and insert a test document
store = DocumentStore()
db = store.create_database("test_db")
collection = db.create_collection("test_collection")

# Clear old document if it exists
if collection.find_document("test_doc_1"):
    collection.remove_document("test_doc_1")

collection.add_document(
    document_name="test_doc_1",
    content="Alice loves programming. She met Bob yesterday."
)

# Step 2: Initialize pipeline (no vectoriser needed)
pipeline = TextPipeline(mongodb=store)
pipeline._neo4jdb.clear_database()

# Step 3: Process the document (triples only)
pipeline.process_and_store_single_file(
    database_name="test_db",
    collection_name="test_collection",
    file_id="test_doc_1"
)

print("Document processed. Check Neo4j for nodes and relationships.")
