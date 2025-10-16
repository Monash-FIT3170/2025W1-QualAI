// DropZone.tsx
import React, { useEffect, useState } from "react";
import { Upload } from "lucide-react";
import UploadFileButton from "./UploadFileButton";

type DropZoneProps = {
  projectName?: string;
  onRefreshFiles?: () => void;
};

/** Keep structure & UX identical to the current Sidebar dropzone */
type UploadItem = {
  kind: "file";
  file: File;
  entry?: FileSystemEntry;
};

const DropZone: React.FC<DropZoneProps> = ({ projectName, onRefreshFiles }) => {
  const [isDraggingOver, setIsDraggingOver] = useState(false);
  const [isUploadingFile, setIsUploadingFile] = useState(false);
  const [isUploadingFolder, setIsUploadingFolder] = useState(false);

  /** --- GLOBAL DRAG PREVENTION (same behaviour as before) --- **/
  useEffect(() => {
    const preventDefaults = (e: Event) => {
      e.preventDefault();
      e.stopPropagation();
    };
    const events = ["dragenter", "dragover", "dragleave", "drop"] as const;
    events.forEach((eventName) => {
      document.body.addEventListener(eventName, preventDefaults, false);
    });
    return () => {
      events.forEach((eventName) => {
        document.body.removeEventListener(eventName, preventDefaults, false);
      });
    };
  }, []);

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
        resolve([]);
      }
    });
  }

  const handleFileUpload =
    () =>
    async (
      event: React.ChangeEvent<HTMLInputElement> | React.DragEvent<HTMLDivElement>
    ) => {
      event.preventDefault();
      event.stopPropagation();

      const items = extractFilesAndDirs(event);
      if (!items.length) {
        setIsDraggingOver(false);
        return;
      }

      const hasFolder = items.some((item) => item.entry?.isDirectory);
      if (hasFolder) setIsUploadingFolder(true);
      else setIsUploadingFile(true);

      const formData = new FormData();

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

      // ✅ restore missing field
      if (projectName) formData.append("project", projectName);

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
        setIsDraggingOver(false);
      }
    };

  return (
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
        <Upload className="mx-auto mb-2" />
        <p style={{ marginBottom: "5px" }}>Drop files or folders here</p>
        <div className="flex flex-col gap-1">
          <UploadFileButton
            onUploadComplete={onRefreshFiles}
            externalUploading={isUploadingFile}
            externalFolderUploading={isUploadingFolder}
          />
        </div>
      </div>
    </div>
  );
};

export default DropZone;
