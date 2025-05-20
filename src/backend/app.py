from flask import Flask
from flask_cors import CORS

from backend.chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from backend.chatbot.text_transformer.text_vectoriser import TextVectoriser
from backend.mongodb.DocumentStore import DocumentStore
from backend.upload.DocumentUploader import DocumentUploader


def initialise_collection() -> DocumentStore.Collection:
    ds: DocumentStore = DocumentStore()
    db: DocumentStore.Database = ds.create_database("Documents")
    collection: DocumentStore.Collection = db.create_collection("Initial Collection")
    return collection

def initialise_vector_database() -> tuple[Neo4JInteractor, TextVectoriser]:
    return Neo4JInteractor(), TextVectoriser()

def register_upload_routes(app: Flask) -> None:
    collection = initialise_collection()
    vector_db, vectoriser = initialise_vector_database()
    document_uploader = DocumentUploader(collection, vector_db, vectoriser)
    document_uploader.register_routes(app)

def start_app() -> None:
    app = Flask(__name__)
    CORS(app)
    register_upload_routes(app)
    app.run()

if __name__ == "__main__":
    start_app()
