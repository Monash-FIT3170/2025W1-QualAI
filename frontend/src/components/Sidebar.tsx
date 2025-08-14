import { useNavigate } from 'react-router-dom';
import { Upload } from 'lucide-react';
import UploadFileButton from './UploadFileButton';
import { useState, useCallback, useEffect } from "react";
import FileTree, { buildTree, NodeType } from "@/components/FileTree.tsx";

type SidebarProps = {
  files: { key: string }[];
  onFileSelect: (fileKey: string) => void;
  onFileDelete: (fileKey: string) => void;
  onRefreshFiles?: () => void;
};

const Sidebar = ({ files = [], onFileSelect, onFileDelete, onRefreshFiles }: SidebarProps) => {
  const navigate = useNavigate();

  const [editingFileKey, setEditingFileKey] = useState<string | null>(null);
  const [editingFileType, setEditingFileType] = useState<NodeType | null>(null);
  const [newFileKey, setNewFileKey] = useState("");
  const [isDraggingOver, setIsDraggingOver] = useState(false);

  /** --- GLOBAL DRAG PREVENTION --- **/
  useEffect(() => {
    const preventDefaults = (e: Event) => {
      e.preventDefault();
      e.stopPropagation();
    };
    ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      document.body.addEventListener(eventName, preventDefaults, false);
    });
    return () => {
      ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
        document.body.removeEventListener(eventName, preventDefaults, false);
      });
    };
  }, []);

  const handleDelete = async (fileKey: string, type: NodeType | null) => {
    if (!type) return;
    if (!window.confirm('Are you sure you want to permanently remove the file?')) return;
    onFileDelete(fileKey);
    try {
      const response = await fetch(`http://localhost:5001/` + (type === "file" ? "delete/" : "delete-dir/") + fileKey, {
        method: 'DELETE'
      });
      if (response.ok) onRefreshFiles?.();
    } catch (err) {
      console.error("Delete Failed", err);
    }
  };

  const handleRename = (fileKey: string) => async (newFileKey: string, type: NodeType | null) => {
    if (!type) return;
    try {
      const response = await fetch(`http://localhost:5001/` + (type === "file" ? "rename/" : "rename-dir/") + fileKey, {
        method: 'PATCH',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content: type === "file"
            ? fileKey.replace(fileKey.split("/").pop() ?? "", newFileKey)
            : newFileKey,
        })
      });
      if (response.ok) onRefreshFiles?.();
    } catch (err) {
      console.error("Edit Failed", err);
    }
  };

  /** --- DROPZONE LOGIC --- **/
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDraggingOver) setIsDraggingOver(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.currentTarget.contains(e.relatedTarget as Node)) return;
    setIsDraggingOver(false);
  };
  const handleFileUpload = (folder : boolean = false) => async (event : React.ChangeEvent<HTMLInputElement>) => {
        const items = event.dataTransfer.items;
        if ( !items ) return;

        const formData = new FormData();

        for ( let idx = 0; idx < items.length; idx++ ) {
            const file = items[idx].getAsFile();
            formData.append("files[]", file);
            console.log(file);
            //onFileSelected?.(file);
        }
        const response = await fetch("http://localhost:5001/upload", {
                method : "POST",
                body : formData,
        });
    };
  /** ------------------------ **/

  return (
    <div className="w-64 bg-secondary/50 p-4 flex flex-col">
      {/* Header */}
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

      {/* File tree */}
      <div className="flex-1">
        <FileTree
          treeData={buildTree(files.map(obj => obj.key))}
          onDelete={handleDelete}
          onSelect={onFileSelect}
          onEdit={(name: string, type: NodeType) => {
            setEditingFileKey(name);
            setNewFileKey(name);
            setEditingFileType(type);
          }}
        />
      </div>

      {/* Dropzone */}
      <div className="mt-4">
        <div
          className={`dropzone border-2 border-dashed rounded-lg p-4 text-center transition ${
            isDraggingOver ? "border-blue-500 bg-blue-50" : "border-gray-400 hover:bg-gray-100"
          }`}
          onDragOver={handleDragOver}
          onDragEnter={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleFileUpload()}
        >
          <Upload className="mx-auto mb-2" />
          <p>Drop files or folders here</p>
          <p className="text-sm text-gray-400 mt-2">Or</p>
          <div className="flex flex-col gap-1">
            <UploadFileButton onUploadComplete={onRefreshFiles} />
          </div>
        </div>
      </div>

      {/* Rename modal */}
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
