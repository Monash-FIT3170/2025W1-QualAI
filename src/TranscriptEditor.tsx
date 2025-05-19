// TranscriptEditor.tsx
import React, { useState, useEffect } from 'react';
import RichTextEditor from './RichTextEditor';

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

  // Debounce setup for autosave
  useEffect(() => {
    const timer = setTimeout(() => {
      if (content.html !== initialContent && onSave) {
        setIsSaving(true);
        
        // Simulate API call for saving
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

  return (
    <div className="flex flex-col h-full">
      {/* Optional status bar */}
      <div className="flex justify-end mb-2 text-sm text-gray-500">
        {isSaving ? (
          <span>Saving...</span>
        ) : (
          lastSaved && <span>Last saved: {lastSaved.toLocaleTimeString()}</span>
        )}
      </div>

      {/* Editor with full height */}
      <div className="flex-grow">
        <RichTextEditor
          content={content.html}
          onChange={handleContentChange}
          className="h-full flex flex-col"
        />
      </div>
    </div>
  );
};

export default TranscriptEditor;