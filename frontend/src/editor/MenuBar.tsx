// MenuBar.tsx
import React, { useState, useEffect } from 'react';
import { Editor } from '@tiptap/react';
import {
  AlignCenter,
  AlignLeft,
  AlignRight,
  Bold,
  Heading1,
  Heading2,
  Heading3,
  Highlighter,
  Italic,
  List,
  ListOrdered,
  Strikethrough,
  ChevronDown,
  Minus,
  Plus
} from 'lucide-react';
import Toggle from './Toggle';


interface MenuBarProps {
  editor: Editor | null;
  fileKey: string;
}



const MenuBar: React.FC<MenuBarProps> = ({ editor, fileKey }) => {

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

  if (!editor) {
    return null;
  }

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

  const options = [
    {
      icon: <Heading1 className="size-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 1 }).run(),
      pressed: editor.isActive('heading', { level: 1 }),
    },
    {
      icon: <Heading2 className="size-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 2 }).run(),
      pressed: editor.isActive('heading', { level: 2 }),
    },
    {
      icon: <Heading3 className="size-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 3 }).run(),
      pressed: editor.isActive('heading', { level: 3 }),
    },
    {
      icon: <Bold className="size-4" />,
      onClick: () => editor.chain().focus().toggleBold().run(),
      pressed: editor.isActive('bold'),
    },
    {
      icon: <Italic className="size-4" />,
      onClick: () => editor.chain().focus().toggleItalic().run(),
      pressed: editor.isActive('italic'),
    },
    {
      icon: <Strikethrough className="size-4" />,
      onClick: () => editor.chain().focus().toggleStrike().run(),
      pressed: editor.isActive('strike'),
    },
    {
      icon: <AlignLeft className="size-4" />,
      onClick: () => editor.chain().focus().setTextAlign('left').run(),
      pressed: editor.isActive({ textAlign: 'left' }),
    },
    {
      icon: <AlignCenter className="size-4" />,
      onClick: () => editor.chain().focus().setTextAlign('center').run(),
      pressed: editor.isActive({ textAlign: 'center' }),
    },
    {
      icon: <AlignRight className="size-4" />,
      onClick: () => editor.chain().focus().setTextAlign('right').run(),
      pressed: editor.isActive({ textAlign: 'right' }),
    },
    {
      icon: <List className="size-4" />,
      onClick: () => editor.chain().focus().toggleBulletList().run(),
      pressed: editor.isActive('bulletList'),
    },
    {
      icon: <ListOrdered className="size-4" />,
      onClick: () => editor.chain().focus().toggleOrderedList().run(),
      pressed: editor.isActive('orderedList'),
    },
    {
      icon: <Highlighter className="size-4" />,
      onClick: () => editor.chain().focus().toggleHighlight().run(),
      pressed: editor.isActive('highlight'),
    },
  ];

  return (
    <div className="border rounded-md p-1 mb-1 bg-slate-50 space-x-2 z-50 flex flex-wrap">
            {/* Font Size Controls */}
      <div className="flex items-center space-x-1 border-r pr-2 mr-2">
        <button
          onClick={decreaseFontSize}
          className="rounded-md p-1 hover:bg-gray-200"
          title="Decrease font size"
        >
          <Minus className="size-4" />
        </button>
        
        <div className="relative">
          <button
            onClick={() => setShowFontSizes(!showFontSizes)}
            className="flex items-center space-x-1 px-2 py-1 rounded-md hover:bg-gray-200 min-w-[50px]"
          >
            <span className="text-sm font-medium">{currentFontSize}</span>
            <ChevronDown className="size-3" />
          </button>
          
          {showFontSizes && (
            <div className="absolute top-full left-0 mt-1 bg-white border rounded-md shadow-lg z-10 max-h-48 overflow-y-auto">
              {fontSizes.map((size) => (
                <button
                  key={size}
                  onClick={() => setFontSize(size)}
                  className={`block w-full text-left px-3 py-1 text-sm hover:bg-gray-100 ${
                    currentFontSize === size ? 'bg-blue-50 text-blue-600' : ''
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
          className="rounded-md p-1 hover:bg-gray-200"
          title="Increase font size"
        >
          <Plus className="size-4" />
        </button>
      </div>
      {options.map((option, index) => (
        <Toggle
          key={index}
          pressed={option.pressed}
          onPressedChange={option.onClick}
        >
          {option.icon}
        </Toggle>
      ))}
      <button onClick={handleFileUpdate} className="rounded-md px-2 hover:bg-gray-200">Save Changes</button>
    </div>
  );
};

export default MenuBar;