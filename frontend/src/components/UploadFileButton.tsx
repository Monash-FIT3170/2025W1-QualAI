import {FC, useRef, useState, useEffect } from 'react';

type UploadFileButtonProps = {
  onFileSelected?: (file: File) => void;
  onUploadComplete?: () => void;
};

const UploadFileButton: FC<UploadFileButtonProps> = ({ onFileSelected, onUploadComplete }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [dotCount, setDotCount] = useState(1);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isUploading) {
      interval = setInterval(() => {
        setDotCount((prev) => (prev % 3) + 1);
      }, 500);
    } else {
      setDotCount(1);
    }

    return () => clearInterval(interval)
  }, [isUploading]);

  const handleButtonClick = () => {
    if (!isUploading) {
      fileInputRef.current?.click();
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Optional callback
    //onFileSelected?.(file);

    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);

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
    } finally {
      setIsUploading(false);
    }
    
  };

  return (
    <>
      <button onClick={handleButtonClick} style={{ color: 'white'}} disabled={isUploading}>
        {isUploading ? `Uploading${'.'.repeat(dotCount)}` : 'Select File'}
      </button>
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