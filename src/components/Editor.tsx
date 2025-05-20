import React from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import TextStyle from '@tiptap/extension-text-style'; // Verify package installation
import { Color } from '@tiptap/extension-color';      // Verify package installation
import Highlight from '@tiptap/extension-highlight';  // Verify package installation
import TextAlign from '@tiptap/extension-text-align'; // Verify package installation

// Verify this path is correct relative to Editor.tsx's location
import CommentMark from '../tiptap-extensions/CommentMark';

// Verify this path is correct relative to Editor.tsx's location (e.g., if both are in src/components/)
import MenuBar from '../MenuBar';      // MenuBar.tsx is in src/

const Editor = () => {
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        heading: {
          levels: [1, 2, 3],
        },
      }),
      TextAlign.configure({
        types: ['heading', 'paragraph'],
      }),
      TextStyle,
      Color,
      Highlight.configure({
        multicolor: true,
      }),
      CommentMark,
    ],
    content: `
      <h2>TipTap Editor</h2>
      <p>This editor is now configured with text styling, highlighting, and commenting capabilities.</p>
      <p>Selected text can be styled using the menu bar options.</p>
    `,
  });

  if (!editor) {
    return <p>Editor loading...</p>;
  }

  return (
    <div className="bg-secondary/30 rounded-lg shadow-lg">
      <MenuBar editor={editor} />
      <EditorContent editor={editor} className="editor-content min-h-[250px] bg-white dark:bg-slate-900 text-black dark:text-white p-4 rounded-b-md outline-none" />
      <div className="border-t border-gray-700 p-2 flex justify-between mt-1">
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          onClick={() => {
            const htmlContent = editor.getHTML();
            console.log("Editor HTML content:", htmlContent);
            // Add actual save logic here
          }}
        >
          Save Changes
        </button>
        <button
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          onClick={() => {
            editor.commands.setContent("<p>Content discarded.</p>");
            // Add actual discard logic here
          }}
        >
          Discard
        </button>
      </div>
    </div>
  );
};

export default Editor;