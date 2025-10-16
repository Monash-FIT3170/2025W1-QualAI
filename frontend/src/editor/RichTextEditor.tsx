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
        class: 'min-h-[156px] border rounded-md bg-slate-50 py-2 px-3 focus:outline-none',
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

  return (
      <div className={`flex flex-col h-full ${className}`}>
        <MenuBar editor={editor} fileKey={fileKey ?? ""}/>
        <div className="flex-grow">
          <EditorContent editor={editor}/>
        </div>
      </div>
  );
}
  export default RichTextEditor;