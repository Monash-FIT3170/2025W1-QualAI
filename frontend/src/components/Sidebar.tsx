import React, { useState, useEffect } from 'react';  
import { useNavigate } from 'react-router-dom';
import { Upload } from 'lucide-react';
import UploadFileButton from './UploadFileButton';

const Sidebar = ({ files = [], onFileSelect, onRefreshFiles }) => {
  const navigate = useNavigate();

  return (
    <div className="w-64 bg-secondary/50 p-4 flex flex-col">
      <div className="flex items-center gap-2 mb-8 cursor-pointer" onClick={() => navigate('/')}>
        <div className="w-8 h-8">
          <svg viewBox="0 0 100 100" className="w-full h-full text-gray-400">
            <circle cx="50" cy="50" r="45" fill="currentColor" />
            <circle cx="35" cy="40" r="8" fill="black" />
            <circle cx="65" cy="40" r="8" fill="black" />
            <circle cx="50" cy="60" r="10" fill="black" />
          </svg>
        </div>
        <span className="text-xl font-bold">QualAI</span>
      </div>

      <div className="flex-1">
        {files.map((file, index) => (
          <div
            key={index}
            className="px-4 py-2 rounded-lg hover:bg-white/10 cursor-pointer transition-colors"
            onClick={() => onFileSelect(file.key)} // pass selected file key up
          >
            {file.key}
          </div>
        ))}
      </div>

      <div className="mt-4">
        <div className="dropzone">
          <Upload className="mx-auto mb-2" />
          <p>Drop files here</p>
          <p className="text-sm text-gray-400 mt-2">Or</p>
          <div className="mt-2 px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">
            <UploadFileButton onUploadComplete={onRefreshFiles} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
