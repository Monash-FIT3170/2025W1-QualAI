import { useNavigate, useParams } from 'react-router-dom';
import { Upload } from 'lucide-react';
import UploadFileButton from './UploadFileButton';
import React, { useState, useEffect } from "react";
import FileTree, { buildTree, NodeType } from "@/components/FileTree.tsx";

type SidebarProps = {
    files: { key: string }[];
    onFileSelect: (fileKey: string) => void;
    onFileDelete: (fileKey: string) => void;
    onRefreshFiles?: () => void;
};

type UploadItem = {
    kind: "file";
    file: File;
    entry?: FileSystemEntry;
};


const Sidebar = ({ files = [], onFileSelect, onFileDelete, onRefreshFiles }: SidebarProps) => {
    const navigate = useNavigate();

    const { projectName } = useParams<{ projectName: string }>();
    const [editingFileKey, setEditingFileKey] = useState<string | null>(null);
    const [editingFileType, setEditingFileType] = useState<NodeType | null>(null);
    const [newFileKey, setNewFileKey] = useState("");
    const [isDraggingOver, setIsDraggingOver] = useState(false);

    const [isUploadingFile, setIsUploadingFile] = useState(false);
    const [isUploadingFolder, setIsUploadingFolder] = useState(false);

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
// Extract files (and folders) from either input change or drag event
    const extractFilesAndDirs = (
        event: React.ChangeEvent<HTMLInputElement> | React.DragEvent
    ): UploadItem[] => {
        const items: UploadItem[] = [];

        if ("dataTransfer" in event) {
            // Drag & drop
            const dtItems = event.dataTransfer?.items;
            if (dtItems) {
                for (let i = 0; i < dtItems.length; i++) {
                    const item = dtItems[i];
                    if (item.kind === "file") {
                        const file = item.getAsFile();
                        if (file) {
                            const entry = (item as any).webkitGetAsEntry?.(); // Safari/Chrome only
                            items.push({ kind: "file", file, entry });
                        }
                    }
                }
            }
        } else if (event.target.files) {
            // <input type="file">
            for (const file of Array.from(event.target.files)) {
                items.push({ kind: "file", file });
            }
        }

        return items;
    };

    async function readAllFilesFromEntry(
        entry: FileSystemEntry,
        path: string = ""
    ): Promise<{ file: File; path: string }[]> {
        return new Promise((resolve, reject) => {
            if (entry.isFile) {
                const fileEntry = entry as FileSystemFileEntry;
                fileEntry.file((file) => resolve([{ file, path: path + file.name }]), reject);
            } else if (entry.isDirectory) {
                const dirReader = (entry as FileSystemDirectoryEntry).createReader();
                const entries: Promise<{ file: File; path: string }[]>[] = [];

                const readEntries = () => {
                    dirReader.readEntries(async (results) => {
                        if (!results.length) {
                            // directory fully read
                            Promise.all(entries).then((all) => resolve(all.flat()));
                            return;
                        }

                        for (const ent of results) {
                            entries.push(readAllFilesFromEntry(ent, path + entry.name + "/"));
                        }

                        readEntries(); // keep reading until empty
                    }, reject);
                };

                readEntries();
            } else {
                resolve([]); // neither file nor dir
            }
        });
    }


    const handleFileUpload =
        () => async (event: React.ChangeEvent<HTMLInputElement> | React.DragEvent<HTMLDivElement>) => {
            const items = extractFilesAndDirs(event);
            if (!items.length) return;

            const hasFolder = items.some(item => item.entry?.isDirectory);

            if (hasFolder) setIsUploadingFolder(true);
            else setIsUploadingFile(true);

            const formData = new FormData();

            for (const item of items) {
                if (item.entry?.isDirectory) {
                    for (const item of items) {
                        if (item.entry?.isDirectory) {
                            const files = await readAllFilesFromEntry(item.entry);
                            for (const { file, path } of files) {
                                formData.append("files[]", file, path);
                            }
                        } else {
                            formData.append("files[]", item.file);
                        }
                    }
                } else {
                    formData.append("files[]", item.file);
                }
            }

            formData.append("project", projectName as string);
            try {
                const response = await fetch("http://localhost:5001/upload", {
                    method: "POST",
                    body: formData,
                });

                if (response.ok) onRefreshFiles?.();
            } catch (err) {
                console.error("Error while uploading", err);
            } finally {
                setIsUploadingFile(false);
                setIsUploadingFolder(false);
            }


        };

    /** ------------------------ **/

    return (
        <div className="w-64 bg-[#1A1A1A] p-4 flex flex-col text-white">
            {/* Header */}
            <div className="flex items-center gap-2 mb-8 cursor-pointer" onClick={() => navigate('/')}>
                <div className="w-8 h-8">
                    <img
                        src="/Logo.png"
                        alt="QualAI Logo"
                        className="w-full h-full object-cover"
                    />
                </div>
                <span className="text-xl font-bold" >QualAI</span>
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
                    onDrop={(e) => handleFileUpload()(e)}

                >
                    <Upload className="mx-auto mb-2" color='#4467FB' />
                    <p style={{ marginBottom: '5px', color: '#4467FB' }}>Drop files or folders here</p>
                    <div className="flex flex-col gap-1">
                        <UploadFileButton onUploadComplete={onRefreshFiles} externalUploading={isUploadingFile} externalFolderUploading={isUploadingFolder} />
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