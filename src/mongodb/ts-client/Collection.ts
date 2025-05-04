import {Collection as Col, Document} from "mongodb";
import {Database} from "./Database";

/**
 * A collection is a class wrapping a MongoDB {@link Col} instance.
 *
 * Each collection consists of several documents, structured as json documents.
 *
 * @author Kays Beslen
 */
export class Collection {
    /** The collection client being wrapped. */
    private readonly _collection: Col;

    private constructor(collectionClient: Col) {
        this._collection = collectionClient;
    }

    /**
     * A static factory for constructing a {@link Collection} instance from the provided {@link Col} that it will
     * be wrapping.
     *
     * @param collectionClient the collection client being wrapped
     *
     * @return the {@link Collection} instance wrapping the provided client
     */
    public static fromClient(collectionClient: Col): Collection {
        return new this(collectionClient);
    }

    /**
     * A static factory for constructing a {@link Collection} instance from the provided {@link Database} wrapper,
     * along with a collection name.
     *
     * This instantiates a new {@link Col}, and immediately wraps it.
     *
     * @param database the database to create this collection within
     * @param collectionName the name of the collection to be created
     *
     * @return a promise containing the {@link Collection} instance wrapping the instantiated {@link Col} client, 
     *  once resolved
     */
    public static async fromName(database: Database, collectionName: string): Promise<Collection> {
        const collection: Col<Document> = await database.client().createCollection(collectionName);
        return new Collection(collection);
    }

    /**
     * Adds a document to the collection.
     *
     * @param documentName the name of the document
     * @param documentKey the unique identifier associated with the document
     * @param document the document itself
     *
     * @return a void promise that is resolved once the document is successfully inserted into the collection
     */
    public async addDocument(documentName: string, documentKey: string, document: Document): Promise<void> {
        // Checking if the key is unique within the collection.
        if ( await this._collection.findOne({"key": documentKey}) ) {
            throw new Error(
                "The provided document key, " + documentKey + ", must be unique between all documents within the " +
                "collection."
            )
        }

        document["name"] = documentName;
        document["key"] = documentKey;
        await this._collection.insertOne(document)
    }

    /**
     * Removes a document with the specified key from the collection.
     *
     * @param documentKey the unique identifier associated with the document
     *
     * @return a void promise that is resolved once the document is removed from the collection
     */
    public async removeDocument(documentKey: string): Promise<void> {
        await this._collection.deleteOne({"key": documentKey});
    }

    /**
     * Finds a document matching the provided document key.
     *
     * @param documentKey the unique identifier associated with the document
     *
     * @return a promise containing the document with the specified key, once resolved
     */
    public async findDocument(documentKey: string): Promise<Document> {
        return await this._collection.findOne({"key": documentKey});
    }

    /**
     * Renames a document within the collection.
     *
     * @param documentKey the unique identifier associated with the document
     * @param name the new name for the document
     *
     * @return a void promise that is resolved once the document is renamed
     */
    public async renameDocument(documentKey: string, name: string): Promise<void> {
        await this._collection.updateOne({"key": documentKey}, {"name": name});
    }
}
