import { useNavigate, useParams } from 'react-router-dom';
import React, { useState } from "react";
import FileTree, { buildTree, NodeType } from "@/components/FileTree.tsx";
import DropZone from "@/components/DropZone.tsx";

type SidebarProps = {
    files: { key: string }[];
    onFileSelect: (fileKey: string) => void;
    onFileDelete: (fileKey: string) => void;
    onRefreshFiles?: () => void;
};

const Sidebar = ({ files = [], onFileSelect, onFileDelete, onRefreshFiles }: SidebarProps) => {
    const navigate = useNavigate();
    const { projectName } = useParams<{ projectName: string }>();

    const [editingFileKey, setEditingFileKey] = useState<string | null>(null);
    const [editingFileType, setEditingFileType] = useState<NodeType | null>(null);
    const [newFileKey, setNewFileKey] = useState("");

    const handleDelete = async (fileKey: string, type: NodeType | null) => {
        if (!type) return;
        if (!window.confirm('Are you sure you want to permanently remove the file?')) return;
        onFileDelete(fileKey);
        try {
            const response = await fetch(`http://localhost:5001/` + (type === "file" ? "delete/" : "delete-dir/") + fileKey, {
                method: 'DELETE',
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ project: projectName }),
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
                    project: projectName,
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

            {/* Dropzone now modular */}
            <DropZone projectName={projectName} onRefreshFiles={onRefreshFiles} />


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
