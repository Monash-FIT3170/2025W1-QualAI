import React, { useState, useEffect, useRef } from 'react';
import RichTextEditor from './RichTextEditor';
import DropZone from './DropZone';

interface TranscriptEditorProps {
  initialContent: string;
  onSave?: (content: { html: string; text: string }) => void;
}

const TranscriptEditor: React.FC<TranscriptEditorProps> = ({
  initialContent,
  onSave,
}) => {
  const [content, setContent] = useState({
    html: initialContent,
    text: initialContent,
  });
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const editorRef = useRef<any>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (content.html !== initialContent && onSave) {
        setIsSaving(true);
        setTimeout(() => {
          onSave(content);
          setLastSaved(new Date());
          setIsSaving(false);
        }, 500);
      }
    }, 1500);

    return () => clearTimeout(timer);
  }, [content, initialContent, onSave]);

  const handleContentChange = (newContent: { html: string; text: string }) => {
    setContent(newContent);
  };

  // Handler for dropped files
  const handleFilesDropped = (files: File[]) => {
    setUploadedFiles(prev => [...prev, ...files]);
    files.forEach(file => {
      // For image files, optionally insert into editor
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          if (editorRef.current && typeof editorRef.current.insertImage === 'function') {
            editorRef.current.insertImage(e.target?.result as string);
          }
        };
        reader.readAsDataURL(file);
      }
      // For audio files, just display player for now
      // You can also trigger transcription here if needed
    });
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-end mb-2 text-sm text-gray-500">
        {isSaving ? (
          <span>Saving...</span>
        ) : (
          lastSaved && <span>Last saved: {lastSaved.toLocaleTimeString()}</span>
        )}
      </div>
      {/* DropZone for file upload */}
      <DropZone onFilesDropped={handleFilesDropped} />
      {/* Show uploaded files */}
      {uploadedFiles.length > 0 && (
        <div className="mb-2">
          <strong>Uploaded Files:</strong>
          <ul>
            {uploadedFiles.map((file, idx) => (
              <li key={idx}>
                {file.name}
                {file.type.startsWith('audio/') && (
                  <audio controls src={URL.createObjectURL(file)} />
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="flex-grow">
        <RichTextEditor
          ref={editorRef}
          content={content.html}
          onChange={handleContentChange}
          className="h-full flex flex-col"
        />
      </div>
    </div>
  );
};

export default TranscriptEditor;