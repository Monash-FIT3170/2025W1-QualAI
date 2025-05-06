import React, { useRef } from 'react';

type BrowseFolderButtonProps = {
  onFilesSelected: (files: FileList) => void;
};

const BrowseFolderButton: React.FC<BrowseFolderButtonProps> = ({ onFilesSelected }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      onFilesSelected(files);
    }
  };

  return (
    <>
      <button onClick={handleButtonClick}>
        Select Folder
      </button>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
        webkitdirectory="true" // enables folder selection
        multiple
      />
    </>
  );
};

export default BrowseFolderButton;