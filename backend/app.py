from flask import Flask, jsonify
from flask_cors import CORS

from chat.bot import Chatbot
from chat.text_transformer.neo4j_interactor import Neo4JInteractor
from chat.text_transformer.text_vectoriser import TextVectoriser
from mongodb.DocumentStore import DocumentStore
from upload.DocumentUploader import DocumentUploader


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
    chat_bot = Chatbot(vector_db, vectoriser)

    document_uploader.register_routes(app)
    chat_bot.register_routes(app)
    register_document_routes(app, collection)

def register_document_routes(app: Flask, collection: DocumentStore.Collection) -> None:
    @app.route('/documents', methods=['GET'])
    def get_documents():
        try:
            documents_cursor = collection.get_all_documents()
            documents = list(documents_cursor)
            # Extract key for each document
            result = [{"key": doc.get("key")} for doc in documents]
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @app.route('/documents/<string:file_key>', methods=['GET'])
    def get_document(file_key):
        try:
            doc = collection.find_document(file_key)  # You need this method
            if not doc:
                return jsonify({"error": "Document not found"}), 404
            return jsonify({"content": doc.get("content", "")}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        


def start_app() -> None:
    app = Flask(__name__)
    CORS(app)

    @app.route('/health', methods=['GET'])
    def health():
        return "OK", 200


    register_upload_routes(app)
    app.run(host="0.0.0.0", port=5001)


if __name__ == "__main__":
    start_app()
