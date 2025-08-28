from flask import Flask, jsonify
from flask_cors import CORS

from chat.bot import Chatbot
from chat.text_transformer.neo4j_interactor import Neo4JInteractor
from chat.text_transformer.text_vectoriser import TextVectoriser
from chat.context_retriever import vector_context_retriever

from mongodb.DocumentStore import DocumentStore
from upload.DocumentUploader import DocumentUploader
from editor.DocumentRetriever import DocumentRetriever
from editor.DocumentEditor import DocumentEditor
from editor.DocumentRemover import DocumentRemover



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
    context_retriever = vector_context_retriever()
    
    chat_bot = Chatbot(context_retriever)
    document_retriever = DocumentRetriever(collection)
    document_editor = DocumentEditor(collection, vector_db, vectoriser)
    document_remover = DocumentRemover(collection, vector_db)

    document_uploader.register_routes(app)
    chat_bot.register_routes(app)
    document_retriever.register_routes(app)
    document_editor.register_routes(app)
    document_remover.register_routes(app)

def start_app() -> None:
    app = Flask(__name__)
    CORS(app)

    @app.route('/health', methods=['GET'])
    def health():
        return "OK", 200


    register_upload_routes(app)
    app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    start_app()
