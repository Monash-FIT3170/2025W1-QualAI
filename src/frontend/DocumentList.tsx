import {useState, useEffect, FC} from 'react';

import { Document } from "mongodb";
import {Collection} from "./mongodb/Collection";

/**
 * This functional component enlists each document in the provided collection in a column, and allows a user to rename
 * and delete each document via a menu that appears on-click.
 *
 * @param collection the MongoDB collection wrapper containing the list of documents
 *
 * @author Kays Beslen
 */
const DocumentList: FC<{ collection: Collection }> = ({ collection }) => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [idx, setIdx] = useState<number | null>(null);

    // When the component is mounted onto the DOM, and whenever the collection is changed, the list of documents is
    // re/loaded.
    useEffect(() => {
        const documents = async () => {
            const docs = await collection.documents();
            setDocuments(docs);
        };
        documents();
    }, [collection]);
    
    // A callback for renaming a document. 
    const onRename = async (key: string) => {
        const newName = window.prompt("Enter a new name:");
        if ( newName && newName.trim() ) {
            await collection.renameDocument(key, newName.trim());
            const docs = await collection.documents();
            setDocuments(docs);
        }
    };
    
    // A callback for deleting a document.
    const onDelete = async (key: string) => {
        if ( window.confirm("Are you sure you want to delete this document?") ) {
            await collection.removeDocument(key);
            const docs = await collection.documents();
            setDocuments(docs);
        }
    };

    return (
        <div style={{ width: '300px', margin: '0 auto' }}>
            {documents.map((doc, index) => (
                // Generates a row per document.
                <div key={doc.key} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    padding: '8px 0',
                    borderBottom: '1px solid #ddd',
                    alignItems: 'center',
                }}>
                    <span>{doc.name}</span>
                    <div style={{ position: 'relative' }}>
                        <button onClick={() => setIdx(idx === index ? null : index)}>⋯</button>
                        {idx === index && (
                            // Each row contains a button that opens a menu. This menu contains a rename button and a
                            // delete button.
                            <div style={{
                                position: 'absolute',
                                right: 0,
                                top: '100%',
                                background: '#fff',
                                border: '1px solid #ccc',
                                boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                                zIndex: 1000,
                                padding: '4px',
                            }}>
                                <button onClick={() => onRename(doc.key)}>Rename</button>
                                <button onClick={() => onDelete(doc.key)}>Delete</button>
                            </div>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default DocumentList;
