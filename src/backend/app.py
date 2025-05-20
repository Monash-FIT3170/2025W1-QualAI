from flask import Flask
from flask_cors import CORS

from backend.mongodb.DocumentStore import DocumentStore
from backend.upload.DocumentUploader import DocumentUploader


def initialise_collection() -> DocumentStore.Collection:
    ds: DocumentStore = DocumentStore()
    db: DocumentStore.Database = ds.create_database("Documents")
    collection: DocumentStore.Collection = db.create_collection("Initial Collection")
    return collection

def register_upload_routes(app: Flask) -> None:
    collection = initialise_collection()
    document_uploader = DocumentUploader(collection)
    document_uploader.register_routes(app)

def start_app() -> None:
    app = Flask(__name__)
    CORS(app)
    register_upload_routes(app)
    app.run()

if __name__ == "__main__":
    start_app()
