import { FC, useEffect, useRef, useState } from 'react';

type UploadFileButtonProps = {
    onFileSelected? : (file : File) => void;
    onUploadComplete? : () => void;
    onRefresh? : () => void;
};

const UploadFileButton : FC<UploadFileButtonProps> = ({ onFileSelected, onUploadComplete, onRefresh }) => {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const folderInputRef = useRef<HTMLInputElement>(null);

    const [ isFolderUploading, setIsFolderUploading ] = useState(false);
    const [ isUploading, setIsUploading ] = useState(false);
    const [ dotCount, setDotCount ] = useState(1);

    useEffect(() => {
        let interval : NodeJS.Timeout;

        if ( isUploading || isFolderUploading ) {
            interval = setInterval(() => {
                setDotCount((prev) => (prev % 3) + 1);
            }, 500);
        } else {
            setDotCount(1);
        }

        return () => clearInterval(interval)
    }, [ isUploading ]);

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

    return (
        <>
            <button onClick={ handleButtonClick() } style={ { backgroundColor: "blue", width: "100%", color : 'white', padding: "5px 0px", borderRadius: "4px" } } disabled={ isUploading || isFolderUploading }>
              { isUploading ? `Uploading${ '.'.repeat(dotCount) }` : 'Select File' }
            </button>

            <button onClick={ handleButtonClick(true) } style={ { backgroundColor: "blue", width: "100%", color : 'white', padding: "5px 0px", borderRadius: "4px" } } disabled={ isUploading || isFolderUploading }>
              { isFolderUploading ? `Uploading${ '.'.repeat(dotCount) }` : 'Select Folder' }
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