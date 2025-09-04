from flask import Flask
from flask_cors import CORS

from chat.bot import Chatbot
from chat.database_client.database_client import DatabaseClient
from chat.database_client.vector_database import VectorDatabase
from chat.database_client.graph_database import GraphDatabase

from mongodb.DocumentStore import DocumentStore
from project.ProjectManager import ProjectManager
from upload.DocumentUploader import DocumentUploader
from editor.DocumentRetriever import DocumentRetriever
from editor.DocumentEditor import DocumentEditor
from editor.DocumentRemover import DocumentRemover


def initialise_collection() -> tuple[DocumentStore.Collection, DocumentStore.Database]:
    ds: DocumentStore = DocumentStore()
    db: DocumentStore.Database = ds.create_database("Documents")
    collection: DocumentStore.Collection = db.create_collection("Initial Collection")
    return collection, db


def initialise_database() -> DatabaseClient:
    return VectorDatabase()


def register_upload_routes(app: Flask) -> None:
    collection, mongodb = initialise_collection()
    db = initialise_database()
    document_uploader = DocumentUploader(collection, db)
    chat_bot = Chatbot(db)
    document_retriever = DocumentRetriever(collection)
    document_editor = DocumentEditor(collection, db)
    document_remover = DocumentRemover(collection, db)
    project_manager = ProjectManager(mongodb)

    document_uploader.register_routes(app)
    chat_bot.register_routes(app)
    document_retriever.register_routes(app)
    document_editor.register_routes(app)
    document_remover.register_routes(app)
    project_manager.register_routes(app)


def start_app() -> None:
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    @app.route('/health', methods=['GET'])
    def health():
        return "OK", 200

    register_upload_routes(app)
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    start_app()