import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Trash2 } from 'lucide-react';
import DropZone from '../DropZone'; // Adjust path as needed

const Sidebar = () => {
  const navigate = useNavigate();
  const files = ['File One', 'File Two', 'File Three', 'File Four', 'File Five'];
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const handleFilesDropped = (newFiles: File[]) => {
    setUploadedFiles(prev => [...prev, ...newFiles]);
  };

  // New: remove file by index
  const handleRemoveFile = (idx: number) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== idx));
  };

  return (
    <div className="w-64 bg-secondary/50 p-4 flex flex-col">
      <div className="flex items-center gap-2 mb-8 cursor-pointer" onClick={() => navigate('/')}>
        <div className="w-8 h-8">
          <svg viewBox="0 0 100 100" className="w-full h-full text-gray-400">
            <circle cx="50" cy="50" r="45" fill="currentColor"/>
            <circle cx="35" cy="40" r="8" fill="black"/>
            <circle cx="65" cy="40" r="8" fill="black"/>
            <circle cx="50" cy="60" r="10" fill="black"/>
          </svg>
        </div>
        <span className="text-xl font-bold">QualAI</span>
      </div>

      <div className="flex-1">
        {files.map((file, index) => (
          <div
            key={index}
            className="px-4 py-2 rounded-lg hover:bg-white/10 cursor-pointer transition-colors"
          >
            {file}
          </div>
        ))}
      </div>

      <div className="mt-4">
        <DropZone onFilesDropped={handleFilesDropped} />
        {uploadedFiles.length > 0 && (
          <div className="mt-4">
            <strong>Uploaded Files:</strong>
            <ul className="text-xs">
              {uploadedFiles.map((file, idx) => (
                <li key={idx} className="mb-2 flex items-center gap-2">
                  <span>{file.name}</span>
                  {file.type.startsWith("audio/") && (
                    <audio controls src={URL.createObjectURL(file)} className="mt-1 w-full" />
                  )}
                  {file.type.startsWith("image/") && (
                    <img src={URL.createObjectURL(file)} alt={file.name} className="mt-1 max-h-16 rounded" />
                  )}
                  {/* Delete button */}
                  <button
                    className="ml-2 p-1 rounded hover:bg-red-100"
                    title="Remove file"
                    onClick={() => handleRemoveFile(idx)}
                  >
                    <Trash2 className="w-4 h-4 text-red-500" />
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;