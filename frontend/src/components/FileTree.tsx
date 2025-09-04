import React, { useState } from "react";
import { Pencil, Trash } from "lucide-react";

export type NodeType = "file" | "folder";

type TreeNode = {
    name: string;
    relativeName: string;
    type: NodeType;
    children?: TreeNode[];
};

type NodeContentProps = {
    node: TreeNode;
    onEdit: (name: string, type: NodeType) => void;
    onDelete: (name: string, type: NodeType) => void;
}

type FileNodeProps = {
    onSelect: (name: string) => void;
} & NodeContentProps;

const NodeContent: React.FC<NodeContentProps> = ({ node, onEdit, onDelete }) => {
    return <>
        <div style={{display: "flex", gap: "10px"}}>
            <div className = " opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <Pencil
                    onClick={(e) => {
                        e.stopPropagation();
                        onEdit(node.name, node.type);
                    }}
                    className="size-6 p-1 rounded-md hover:bg-gray-200 cursor-pointer"
                />
            </div>
            <div className = "opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <Trash
                    onClick={(e) => {
                        e.stopPropagation();
                        onDelete(node.name, node.type);
                    }}
                    className="size-6 p-1 rounded-md hover:bg-gray-200 curser-pointer"
                />
            </div>
        </div>
    </>
}

const FileNode: React.FC<FileNodeProps> = ({ node, onSelect, onEdit, onDelete }) => {
    const [isOpen, setIsOpen] = useState(false);

    if (node.type === "file") {
        return <div onClick={() => onSelect(node.name)} style={{ paddingLeft: 20 }}  className="flex-1 group cursor-pointer" >
            📄 {node.relativeName}
            <NodeContent node={node} onDelete={onDelete} onEdit={onEdit} />
        </div>
    }

    return (
        <div style={{ paddingLeft: 20 }}>
            <div
                style={{ cursor: "pointer", userSelect: "none" }}
                className="flex-1 group cursor-pointer"
                onClick={() => setIsOpen(!isOpen)}
            >
                {isOpen ? "📂" : "📁"} {node.relativeName}
                <NodeContent node={node} onEdit={onEdit} onDelete={onDelete} />
            </div>
            {isOpen &&
                node.children?.map((child, i) => <FileNode onEdit={onEdit} onDelete={onDelete} onSelect={onSelect} key={i} node={child} />)}
        </div>
    );
};

interface FileTreeProps {
    treeData: TreeNode[];
    onSelect: (name: string) => void;
    onEdit: (name: string, type: NodeType) => void;
    onDelete: (name: string, type: NodeType) => void;
}

const FileTree: React.FC<FileTreeProps> = ({ treeData, onSelect, onEdit, onDelete }) => {
    return (
        <div>
            {treeData.map((node, i) => (
                <FileNode onEdit={onEdit} onDelete={onDelete} key={i} node={node} onSelect={onSelect} />
            ))}
        </div>
    );
};

// Utility to convert flat paths into a nested tree
export function buildTree(paths: string[]): TreeNode[] {
    const root: TreeNode[] = [];

    for (const path of paths) {
        const parts = path.split("/");
        let currentLevel = root;

        let resolvedPath: string = "";
        for (let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const isFile = i === parts.length - 1;

            resolvedPath += (resolvedPath.length > 0 ? "/" : "") + part;

            let existingNode = currentLevel.find((node) => node.name === resolvedPath);

            if (!existingNode) {
                existingNode = {
                    name: resolvedPath,
                    relativeName: part,
                    type: isFile ? "file" : "folder",
                    children: isFile ? undefined : [],
                };
                currentLevel.push(existingNode);
            }

            if (!isFile && existingNode.children) {
                currentLevel = existingNode.children;
            }
        }
    }

    return root;
}

export default FileTree;