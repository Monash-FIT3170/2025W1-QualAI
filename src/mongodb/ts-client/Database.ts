import {Db} from "mongodb";
import {DocumentStore} from "./DocumentStore";
import {Collection} from "./Collection";

/**
 * A database is a class wrapping a MongoDB {@link Db} instance.
 *
 * Each database consists of several collections, and each collection consists of several documents.
 *
 * @author Kays Beslen
 */
export class Database {
    /** The database client being wrapped. */
    private readonly _database: Db;

    private constructor(databaseClient: Db) {
        this._database = databaseClient;
    }

    /**
     * A static factory for constructing a {@link Database} instance from the provided {@link Db} that it will
     * be wrapping.
     *
     * @param databaseClient the database client being wrapped
     *
     * @return the {@link Database} instance wrapping the provided client
     */
    public static fromClient(databaseClient: Db) : Database {
        return new this(databaseClient);
    }

    /**
     * A static factory for constructing a {@link Database} instance from the provided {@link DocumentStore} wrapper,
     * along with a database name.
     *
     * This instantiates a new {@link Db}, and immediately wraps it.
     *
     * @param documentStore the document store to create this database within
     * @param databaseName the name of the database to be created
     *
     * @return the {@link Database} instance wrapping the instantiated {@link Db} client
     */
    public static fromName(documentStore: DocumentStore, databaseName: string) : Database {
        return new this(documentStore.client().db(databaseName));
    }

    /**
     * Creates a new {@link Collection} with the specified name.
     *
     * @param collectionName the name of the collection to be created
     *
     * @return a promise containing the created {@link Collection} instance, when resolved
     */
    public async createCollection(collectionName: string) : Promise<Collection> {
        return await Collection.fromName(this, collectionName);
    }

    /** The database client being wrapped by this class. */
    public client() : Db {
        return this._database;
    }
}