// MenuBar.tsx
import React, { useState, useEffect } from 'react';
import { Editor } from '@tiptap/react';
import {
  AlignCenter,
  AlignLeft,
  AlignRight,
  Bold,
  Highlighter,
  Italic,
  List,
  ListOrdered,
  Strikethrough,
  Palette,         // For multi-color highlight picker
  Paintbrush,      // For text color picker
  MessageSquarePlus, // For comments
  ChevronDown,
  Minus,
  Plus
} from 'lucide-react';
import Toggle from './Toggle';
import { useParams } from "react-router-dom";

interface MenuBarProps {
  editor: Editor | null;
  fileKey: string;
}

const MenuBar: React.FC<MenuBarProps> = ({ editor, fileKey }) => {
  if (!editor) {
    return null;
  }

  const { projectName } = useParams<{ projectName: string }>();
  const [currentFontSize, setCurrentFontSize] = useState(16);
  const [showFontSizes, setShowFontSizes] = useState(false);
  
  const fontSizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72, 96];

  useEffect(() => {
    if (!editor) return;

    const updateFontSize = () => {
      // Try to get the current font size from the selection
      const attributes = editor.getAttributes('textStyle');
      if (attributes.fontSize) {
        const numericSize = parseInt(attributes.fontSize.replace('px', ''));
        setCurrentFontSize(numericSize);
      } else {
        setCurrentFontSize(16); // default size
      }
    };

    // Update font size when selection changes
    editor.on('selectionUpdate', updateFontSize);
    editor.on('transaction', updateFontSize);

    return () => {
      editor.off('selectionUpdate', updateFontSize);
      editor.off('transaction', updateFontSize);
    };
  }, [editor]);

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
      body: JSON.stringify({ content, project: projectName }),
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
  // Handler for adding a comment
  const handleComment = () => {
    // 1. Generate a unique ID for the comment
    // A more robust ID generation might be needed in a production app
    const commentId = `comment-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

    // 2. Prompt for comment text (Placeholder for a real UI)
    // In a real application, you would open a modal, sidebar, or inline input here.
    const commentText = prompt("Enter your comment:");

    if (commentText) {
      // If the user entered text, apply the comment mark.
      // You would also save `commentText` associated with `commentId`
      // in your application's state or send it to a backend.
      console.log(`Comment to save: ID=${commentId}, Text=${commentText}, User: rachana-barak, Timestamp: ${new Date().toISOString()}`);
      editor.chain().focus().setComment({ commentId }).run();
    }
    // If commentText is null (user cancelled), do nothing or handle as needed.
  };

  // Font size controls
  const setFontSize = (size: number) => {
    (editor as any).chain().focus().setFontSize(`${size}px`).run();
    setCurrentFontSize(size);
    setShowFontSizes(false);
  };

  const increaseFontSize = () => {
    const newSize = currentFontSize + 1;
    setFontSize(newSize);
  };

  const decreaseFontSize = () => {
    const newSize = Math.max(8, currentFontSize - 1); 
    setFontSize(newSize);
  };

  // Original options array - we'll remove the generic highlight toggle later
  const existingOptions = [
    {
      icon: <Bold className="size-4" />,
      onClick: () => editor.chain().focus().toggleBold().run(),
      pressed: editor.isActive('bold'),
      title: "Bold",
      disabled: !editor.can().chain().focus().toggleBold().run(),
    },
    {
      icon: <Italic className="size-4" />,
      onClick: () => editor.chain().focus().toggleItalic().run(),
      pressed: editor.isActive('italic'),
      title: "Italic",
      disabled: !editor.can().chain().focus().toggleItalic().run(),
    },
    {
      icon: <Strikethrough className="size-4" />,
      onClick: () => editor.chain().focus().toggleStrike().run(),
      pressed: editor.isActive('strike'),
      title: "Strikethrough",
      disabled: !editor.can().chain().focus().toggleStrike().run(),
    },
    {
      icon: <AlignLeft className="size-4" />,
      onClick: () => editor.chain().focus().setTextAlign('left').run(),
      pressed: editor.isActive({ textAlign: 'left' }),
      title: "Align Left",
    },
    {
      icon: <AlignCenter className="size-4" />,
      onClick: () => editor.chain().focus().setTextAlign('center').run(),
      pressed: editor.isActive({ textAlign: 'center' }),
      title: "Align Center",
    },
    {
      icon: <AlignRight className="size-4" />,
      onClick: () => editor.chain().focus().setTextAlign('right').run(),
      pressed: editor.isActive({ textAlign: 'right' }),
      title: "Align Right",
    },
    {
      icon: <List className="size-4" />,
      onClick: () => editor.chain().focus().toggleBulletList().run(),
      pressed: editor.isActive('bulletList'),
      title: "Bullet List",
    },
    {
      icon: <ListOrdered className="size-4" />,
      onClick: () => editor.chain().focus().toggleOrderedList().run(),
      pressed: editor.isActive('orderedList'),
      title: "Ordered List",
    },
  ];

  return (
      <div
          className="border rounded-md p-1 mb-1 bg-slate-50 dark:bg-slate-800 space-x-0.5 md:space-x-1 z-50 flex flex-wrap items-center">
          
          {/* Font Size Controls */}
          <div className="flex items-center space-x-1 border-r pr-2 mr-2">
            <button
              onClick={decreaseFontSize}
              className="rounded-md p-1 hover:bg-slate-200 dark:hover:bg-slate-700"
              title="Decrease font size"
            >
              <Minus className="size-4" />
            </button>
            
            <div className="relative">
              <button
                onClick={() => setShowFontSizes(!showFontSizes)}
                className="flex items-center space-x-1 px-2 py-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 min-w-[50px]"
              >
                <span className="text-sm font-medium">{currentFontSize}</span>
                <ChevronDown className="size-3" />
              </button>
              
              {showFontSizes && (
                <div className="absolute top-full left-0 mt-1 bg-white dark:bg-slate-800 border rounded-md shadow-lg z-10 max-h-48 overflow-y-auto">
                  {fontSizes.map((size) => (
                    <button
                      key={size}
                      onClick={() => setFontSize(size)}
                      className={`block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 dark:hover:bg-slate-700 ${
                        currentFontSize === size ? 'bg-blue-50 text-blue-600 dark:bg-blue-900 dark:text-blue-300' : ''
                      }`}
                    >
                      {size}
                    </button>
                  ))}
                </div>
              )}
            </div>
            
            <button
              onClick={increaseFontSize}
              className="rounded-md p-1 hover:bg-slate-200 dark:hover:bg-slate-700"
              title="Increase font size"
            >
              <Plus className="size-4" />
            </button>
          </div>
          
          {existingOptions.map((option, index) => (
              <Toggle
                  key={index}
                  pressed={option.pressed}
                  onPressedChange={option.onClick}
                  disabled={option.disabled}
                  title={option.title}
                  className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded" // Example styling
              >
                  {option.icon}
              </Toggle>
          ))}

          {/* Separator */}
          <div className="h-6 w-px bg-slate-300 dark:bg-slate-600 mx-1 md:mx-2"/>

          {/* Highlight Color Section */}
          <div className="flex items-center p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700"
               title="Highlight Color">
              <Palette className="size-4 mr-1 text-slate-700 dark:text-slate-300"/>
              <input
                  type="color"
                  onInput={(event) => editor.chain().focus().toggleHighlight({color: (event.target as HTMLInputElement).value}).run()}
                  value={editor.getAttributes('highlight')?.color || '#FFFF00'} // Default to yellow if no highlight or get current
                  className="w-5 h-5 border-none bg-transparent cursor-pointer p-0 m-0"
                  title="Pick highlight color"
              />
          </div>
          <Toggle
              onPressedChange={() => editor.chain().focus().unsetHighlight().run()}
              pressed={false} // Not a toggle state, just an action
              disabled={!editor.isActive('highlight')}
              title="Remove Highlight"
              className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
          >
              {/* Using Highlighter icon with different styling to signify "remove" */}
              <Highlighter className="size-4 text-slate-700 dark:text-slate-300 opacity-60"/>
          </Toggle>

          {/* Text Color Section */}
          <div className="flex items-center p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700" title="Text Color">
              <Paintbrush className="size-4 mr-1 text-slate-700 dark:text-slate-300"/>
              <input
                  type="color"
                  onInput={() => editor.chain().focus().run()}
                  value={editor.getAttributes('textStyle').color || (document.documentElement.classList.contains('dark') ? '#FFFFFF' : '#000000')}
                  className="w-5 h-5 border-none bg-transparent cursor-pointer p-0 m-0"
                  title="Pick text color"
              />
          </div>
          <Toggle
              onPressedChange={() => editor.chain().focus().run()}
              pressed={false} // Not a toggle state
              disabled={!editor.getAttributes('textStyle').color}
              title="Remove Text Color"
              className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
          >
              <Paintbrush className="size-4 text-slate-700 dark:text-slate-300 opacity-60"/>
          </Toggle>

          {/* Comment Section */}
          <Toggle
              pressed={editor.isActive('comment')} // This will be true if any part of selection is a comment
              onPressedChange={handleComment}
              title="Add Comment"
              className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
          >
              <MessageSquarePlus className="size-4 text-slate-700 dark:text-slate-300"/>
          </Toggle>
          <button onClick={handleFileUpdate} className="rounded-md px-2 hover:bg-gray-200">Save Changes</button>

      </div>
  );
};

export default MenuBar;