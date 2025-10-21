import React, { FC, useEffect, useRef, useState } from 'react';
import { useParams } from "react-router-dom";

type UploadFileButtonProps = {
    onFileSelected? : (file : File) => void;
    onUploadComplete? : () => void;
    onRefresh? : () => void;
    externalUploading?: boolean;
    externalFolderUploading?: boolean;
};

const UploadFileButton : FC<UploadFileButtonProps> = ({ onFileSelected, onUploadComplete, onRefresh, externalUploading, externalFolderUploading }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const folderInputRef = useRef<HTMLInputElement>(null);

    const { projectName } = useParams<{ projectName : string }>();
    const [ isFolderUploading, setIsFolderUploading ] = useState(false);
    const [ isUploading, setIsUploading ] = useState(false);
    const [ dotCount, setDotCount ] = useState(1);

    useEffect(() => {
        let interval : NodeJS.Timeout;

        if ( isUploading || isFolderUploading || externalFolderUploading || externalUploading ) {
            interval = setInterval(() => {
                setDotCount((prev) => (prev % 3) + 1);
            }, 500);
        } else {
            setDotCount(1);
        }

        return () => clearInterval(interval)
    }, [ isUploading, isFolderUploading, externalUploading, externalFolderUploading ]);

    const handleButtonClick = (folder : boolean = false) => () => {
        if ( !isUploading && !isFolderUploading ) {
            !folder ? fileInputRef.current?.click() : folderInputRef.current?.click();
        }
    };

    const handleFileUpload = (folder : boolean = false) => async (event : React.ChangeEvent<HTMLInputElement>) => {
        const files = event.target.files;
        if ( !files ) return;

        const formData = new FormData();
        
        for ( let idx = 0; idx < files.length; idx++ ) {
            const file = files[idx];
            formData.append("files[]", file);
            onFileSelected?.(file);
        }

        folder ? setIsFolderUploading(true) : setIsUploading(true);
        formData.append("project", projectName as string);

        try {
            const response = await fetch("http://localhost:5001/upload", {
                method : "POST",
                body : formData,
            });

            const result = await response.json();
            console.log("Server response:", result);
            onUploadComplete?.();
            onRefresh?.();
        } catch ( err ) {
            console.error("Upload failed", err);
        } finally {
            folder ? setIsFolderUploading(false) : setIsUploading(false);
        }

    };

    const effectiveUploading = isUploading || externalUploading;
    const effectiveFolderUploading = isFolderUploading || externalFolderUploading;

    const fileButtonDisabled = effectiveUploading || effectiveFolderUploading;
    const folderButtonDisabled = effectiveUploading || effectiveFolderUploading;

    const fileButtonInactive = isFolderUploading || externalFolderUploading;
    const folderButtonInactive = isUploading || externalUploading;

    return (
        <>
            <button
                onClick={ handleButtonClick() }  disabled={fileButtonDisabled}
                style={ {
                    backgroundColor: "blue", width: "100%", color : 'white', padding: "5px 0px", borderRadius: "4px",
                    cursor: fileButtonInactive ? "not-allowed" : "pointer",
                    opacity: fileButtonInactive ? 0.6 : 1
                } }
            >
              { effectiveUploading ? `Uploading${ '.'.repeat(dotCount) }` : 'Select File' }
            </button>

            <button
                onClick={ handleButtonClick(true) } disabled={folderButtonDisabled}
                style={ {
                    backgroundColor: "blue", width: "100%", color : 'white', padding: "5px 0px", borderRadius: "4px",
                    cursor: folderButtonInactive ? "not-allowed" : "pointer",
                    opacity: folderButtonInactive ? 0.6 : 1
                } }
            >
              { effectiveFolderUploading ? `Uploading${ '.'.repeat(dotCount) }` : 'Select Folder' }
            </button>


            <input
                type="file"
                ref={ fileInputRef }
                style={ { display : 'none' } }
                onChange={ handleFileUpload() }
                multiple
            />
            <input
                type="file"
                ref={ folderInputRef }
                multiple
                //@ts-ignore
                webkitdirectory="true"
                directory=""
                style={ { display : "none" } }
                onChange={ handleFileUpload(true) }
            />
        </>
    );
};

export default UploadFileButton;