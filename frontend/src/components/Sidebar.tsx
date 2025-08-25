import { useNavigate } from 'react-router-dom';
import { Upload, Trash2 } from 'lucide-react';
import UploadFileButton from './UploadFileButton';
import { useState } from "react";
import FileTree, { buildTree, NodeType } from "@/components/FileTree.tsx";
import DropZone from '../DropZone'; // Adjust path as needed

type SidebarProps = {
  files: { key : string }[];
  onFileSelect: (fileKey: string) => void;
  onFileDelete: (fileKey: string) => void;
  onRefreshFiles?: () => void;
}

const Sidebar = ({ files = [], onFileSelect, onFileDelete, onRefreshFiles } : SidebarProps) => {
  const navigate = useNavigate();

  const [editingFileKey, setEditingFileKey] = useState<string | null>(null);
  const [editingFileType, setEditingFileType] = useState<NodeType | null>(null);
  const [newFileKey, setNewFileKey] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);

  const handleFilesDropped = (newFiles: File[]) => {
    setUploadedFiles(prev => [...prev, ...newFiles]);
  };

  const handleDelete = async(fileKey : string, type: NodeType | null) => {
    if ( !type ) {
      // setUploadedFiles(prev => prev.filter((_, i) => i !== idx));
      return;
    }
    if(!window.confirm('Are you sure you want to permanently remove the file?')) return;

    onFileDelete(fileKey);
    try {
      const response = await fetch(`http://localhost:5001/` + (type == "file" ? "delete/" : "delete-dir/") + fileKey, {
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

  const handleRename = (fileKey: string) => async (newFileKey: string, type: NodeType | null) => {
    if ( !type ) {
      // TODO: Error handling.
      return;
    }
    try {
      const response = await fetch(`http://localhost:5001/` + (type == "file" ? "rename/" : "rename-dir/") + fileKey, {
        method: 'PATCH',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          // TODO: This logic should really all be in backend.
          content: type == "file" ? fileKey.replace(fileKey.split("/").pop() ?? "", newFileKey) : newFileKey,
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
        <FileTree treeData={buildTree(files.map(obj => obj.key))} onDelete={handleDelete} onSelect={onFileSelect} onEdit={(name : string, type: NodeType) => {
            setEditingFileKey(name);
            setNewFileKey(name);
            setEditingFileType(type);
          }
        } />
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
                          // onClick={() => handleDelete(idx)}
                      >
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </button>
                    </li>
                ))}
              </ul>
            </div>)}
      </div>

  {editingFileKey && (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white p-6 rounded-lg shadow-lg w-96">
          <h2 className="text-lg font-bold mb-4">Rename {editingFileType}</h2>
          <input
              type="text"
              value={newFileKey.split("/").pop() || ""}
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
                  await handleRename(editingFileKey)(newFileKey, editingFileType);
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
