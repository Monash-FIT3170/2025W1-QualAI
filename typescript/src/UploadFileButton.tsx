import React, { useRef } from 'react';

type UploadFileButtonProps = {
  onFileSelected: (file: File) => void;
};

const UploadFileButton: React.FC<UploadFileButtonProps> = ({ onFileSelected }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelected(file);
    }
  };

  return (
    <>
      <button onClick={handleButtonClick}>
        Select File
      </button>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </>
  );
};

export default UploadFileButton;