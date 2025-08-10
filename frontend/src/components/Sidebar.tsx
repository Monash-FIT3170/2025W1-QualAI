import { useNavigate } from 'react-router-dom';
import { Pencil, Trash, Upload } from 'lucide-react';
import UploadFileButton from './UploadFileButton';
import { useState } from "react";

type SidebarProps = {
  files: { key : string }[];
  onFileSelect: (fileKey: string) => void;
  onFileDelete: (fileKey: string) => void;
  onRefreshFiles?: () => void;
}

const Sidebar = ({ files = [], onFileSelect, onFileDelete, onRefreshFiles } : SidebarProps) => {
  const navigate = useNavigate();

  const [editingFileKey, setEditingFileKey] = useState<string | null>(null);
  const [newFileKey, setNewFileKey] = useState("");

  const handleDelete = async(fileKey : string) => {
    if(!window.confirm('Are you sure you want to permanently remove the file?')) return;

    onFileDelete(fileKey);
    try {
      const response = await fetch(`http://localhost:5001/delete/${fileKey}`, {
        method: 'DELETE'
      });

      // Allows for files to be refreshed and remove deleted file from sidebar
      if (response.ok) {
        console.log(`Deleted file: ${fileKey}`);
        onRefreshFiles?.();
      } 
    } catch(err) {
      console.error("Delete Failed", err);
    }
  };

  const handleRename = async (fileKey : string, newFileKey: string) => {
    try {
      const response = await fetch(`http://localhost:5001/rename/${fileKey}`, {
        method: 'PATCH',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: newFileKey
        })
      });

      // Allows for files to be refreshed and remove deleted file from sidebar
      if ( response.ok ) {
        console.log(`Edited file: ${fileKey}`);
        onRefreshFiles?.();
      }
    } catch(err) {
      console.error("Edit Failed", err);
    }
  }

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
            className="group flex items-center justify-between -4 py-2 rounded-lg hover:bg-white/10 cursor-pointer transition-colors"
          >
            <div
              className = "cursor-pointer flex-1 truncate"
              onClick={() => onFileSelect(file.key)} // pass selected file key up
            >
              {file.key}
            </div>
            <div className = "flex items-center gap-2 ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <Pencil
                  onClick={(e) => {
                    e.stopPropagation();
                    setEditingFileKey(file.key);
                    setNewFileKey(file.key);
                  }}
                  className="size-6 p-1 rounded-md hover:bg-gray-200 cursor-pointer"
              />
            </div>
            <div className = "flex items-center gap-2 ml-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200"> 
              <Trash 
              onClick={(e) => {
                e.stopPropagation();
                handleDelete(file.key)
              }}
                className="size-6 p-1 rounded-md hover:bg-gray-200 curser-pointer"
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4">
        <div className="dropzone">
          <Upload className="mx-auto mb-2" />
          <p>Drop files here</p>
          <p className="text-sm text-gray-400 mt-2">Or</p>
          <div style={{ display: "flex", flexDirection: "column", gap: "5px" }} >
            <UploadFileButton onUploadComplete={onRefreshFiles} />
          </div>
        </div>
      </div>

  {editingFileKey && (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg w-96">
          <h2 className="text-lg font-bold mb-4">Rename File</h2>
          <input
              type="text"
              value={newFileKey}
              onChange={(e) => setNewFileKey(e.target.value)}
              className="w-full px-3 py-2 border rounded mb-4"
          />
          <div className="flex justify-end gap-2">
            <button
                onClick={() => setEditingFileKey(null)}
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
                onClick={async () => {
                  await handleRename(editingFileKey, newFileKey);
                  setEditingFileKey(null);
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Rename
            </button>
          </div>
        </div>
      </div>
    )}
    </div>
  );
};

export default Sidebar;
