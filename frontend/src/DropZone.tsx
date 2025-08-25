import React, { useRef } from 'react';

interface DropZoneProps {
  onFilesDropped: (files: File[]) => void;
}

const DropZone: React.FC<DropZoneProps> = ({ onFilesDropped }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFilesDropped(Array.from(e.dataTransfer.files));
      e.dataTransfer.clearData();
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleBrowseClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFilesDropped(Array.from(e.target.files));
    }
  };

  return (
    <div
      className="dropzone"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      style={{ marginBottom: '12px', cursor: 'pointer' }}
      data-testid="dropzone"
    >
      <span>Drop files here</span>
      <p className="text-sm text-gray-400 mt-2">Or</p>
      <button
        type="button"
        className="mt-2 px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors text-white"
        onClick={handleBrowseClick}
      >
        Browse
      </button>
      <input
        type="file"
        multiple
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
        accept="audio/*,image/*"
      />
    </div>
  );
};

export default DropZone;