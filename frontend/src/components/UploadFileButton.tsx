import {FC, useRef} from 'react';

type UploadFileButtonProps = {
  onFileSelected?: (file: File) => void;
  onUploadComplete?: () => void;
};

const UploadFileButton: FC<UploadFileButtonProps> = ({ onFileSelected, onUploadComplete }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Optional callback
    //onFileSelected?.(file);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5001/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      console.log("Server response:", result);
      onUploadComplete?.();
    } catch (err) {
      console.error("Upload failed", err);
    }
    
  };

  return (
    <>
      <button onClick={handleButtonClick} style={{ color: 'white'}}>Select File</button>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none'}}
        onChange={handleFileUpload}
      />
    </>
  );
};

export default UploadFileButton;