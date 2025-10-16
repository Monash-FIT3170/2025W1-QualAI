// RichTextEditor.tsx
import React, { useEffect } from 'react';
import { EditorContent, useEditor } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import TextAlign from '@tiptap/extension-text-align';
import {TextStyle} from '@tiptap/extension-text-style'; // Verify package installation
// import Color from '@tiptap/extension-color';      // Verify package installation
import Highlight from '@tiptap/extension-highlight';
import CommentMark from '../tiptap-extensions/CommentMark';
import FontSize from './FontSize';
import MenuBar from './MenuBar';



interface RichTextEditorProps {
  initialContent?: string;
  fileKey?: string;
  onChange?: (content: { html: string; text: string }) => void;
  className?: string;
}

const RichTextEditor: React.FC<RichTextEditorProps> = ({
  initialContent = '',
  onChange,
  className = '',
  fileKey,
}) => {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        bulletList: {
          HTMLAttributes: {
            class: 'list-disc ml-3',
          },
        },
        orderedList: {
          HTMLAttributes: {
            class: 'list-decimal ml-3',
          },
        },
      }),
      TextAlign.configure({
        types: ['paragraph'],
      }),
      TextStyle,
//      Color,
      Highlight.configure({
        multicolor: true,
      }),
      FontSize.configure({
        types: ['textStyle'],
        defaultSize: '16px',
      }),
      CommentMark,
    ],
    content: initialContent,
    editorProps: {
      attributes: {
        class: 'min-h-[156px] border rounded-md bg-[#D9D9D9] py-2 px-3 focus:outline-none',
      },
    },
    onUpdate: ({editor}) => {
      if (onChange) {
        onChange({
          html: editor.getHTML(),
          text: editor.getText(),
        });
      }
    },
  });

  // Update editor when initialContent changes (for loading files)
  useEffect(() => {
    if (editor && initialContent !== editor.getHTML()) {
      editor.commands.setContent(initialContent);
    }
  }, [initialContent, editor]);

  const handleFileUpdate = () => {
    if (!editor || !fileKey) {
    console.warn("Cannot save: missing editor or fileKey");
    return;
  }
    const content = editor.getHTML();
    console.log('Saving fileKey:', fileKey);
    console.log('Saving content:', content);
    fetch(`http://localhost:5001/edit/${fileKey}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content }),
    })
      .then(res => {
        if (!res.ok) {
          throw new Error('Failed to save document');
        }
        return res.json();
      })
      .then(data => {
        console.log('Save successful:', data);
      })
      .catch(err => {
        console.error('Save error:', err);
      });
  };

  return (
      <div className={`flex flex-col h-full ${className}`}>
        <MenuBar editor={editor}/>
        <div className="flex-grow">
          <EditorContent editor={editor}/>
        </div>
        <div className="mt-3 pb-4 flex justify-center">
        <button 
          onClick={handleFileUpdate}
          className="cursor-pointer px-8 py-2.5 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors shadow-lg font-medium hover:shadow-xl transform hover:scale-105 transition-all duration-200"
        >
          Save Changes
        </button>
      </div>
        
      </div>
  );
}
  export default RichTextEditor;