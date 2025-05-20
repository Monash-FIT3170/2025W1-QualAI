
import { MongoClient } from "mongodb";
import { Database } from "./Database";

// TODO: Move this to the appropriate location.
import * as dotenv from "dotenv";
dotenv.config();

/**
 * A document store is a class wrapping a {@link MongoClient} instance.
 *
 * Each document store consists of several databases, each database consists of several collections,
 * and each collection consists of several documents.
 *
 * @author Kays Beslen
 */
export class DocumentStore {
    /** The URI to access the MongoDB client. */
    private static readonly URI: string = process.env.MONGO_URI ?? "mongodb://localhost:27017";

    /** The MongoDB client being wrapped. */
    private readonly _client: MongoClient;

    public constructor() {
        this._client = new MongoClient(DocumentStore.URI);
    }

    /**
     * Creates a new {@link Database} with the specified name.
     *
     * @param databaseName the name for the new database
     *
     * @return the created database
     */
    public createDatabase(databaseName: string): Database {
        return Database.fromClient(this._client.db(databaseName));
    }

    /** The MongoDB client instance being wrapped by this class. */
    public client(): MongoClient {
        return this._client;
    }
}
