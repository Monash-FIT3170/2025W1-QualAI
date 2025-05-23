from flask import Flask
from flask_cors import CORS

from chatbot.chat_service import ChatService
from chatbot.text_transformer.neo4j_interactor import Neo4JInteractor
from chatbot.text_transformer.text_vectoriser import TextVectoriser
from mongodb.DocumentStore import DocumentStore
from upload.DocumentUploader import DocumentUploader
from chatbot.deepseek_client import DeepSeekClient

def initialise_collection() -> DocumentStore.Collection:
    ds: DocumentStore = DocumentStore()
    db: DocumentStore.Database = ds.create_database("Documents")
    collection: DocumentStore.Collection = db.create_collection("Initial Collection")
    return collection

def initialise_vector_database() -> tuple[Neo4JInteractor, TextVectoriser]:
    return Neo4JInteractor(), TextVectoriser()

def initialise_deepseek() -> DeepSeekClient:
    return DeepSeekClient()

def register_routes(app: Flask) -> None:
    vector_db, vectoriser = initialise_vector_database()
    register_upload_routes(app, vector_db, vectoriser)
    register_chat_routes(app, vector_db, vectoriser)
    

def register_upload_routes(app: Flask, vector_db: Neo4JInteractor, vectoriser: TextVectoriser) -> None:
    collection = initialise_collection()
    document_uploader = DocumentUploader(collection, vector_db, vectoriser)
    document_uploader.register_routes(app)
    
def register_chat_routes(app: Flask, vector_db: Neo4JInteractor, vectoriser: TextVectoriser) -> None:
    deepseek_client = initialise_deepseek()
    chat_service = ChatService(vector_db, vectoriser, deepseek_client)
    chat_service.register_routes(app)

def start_app() -> None:
    app = Flask(__name__)
    CORS(app)
    register_routes(app)
    app.run()

if __name__ == "__main__":
    start_app()
