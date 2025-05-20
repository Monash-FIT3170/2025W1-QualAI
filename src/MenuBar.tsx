import React from 'react';
import { Editor } from '@tiptap/react';
import {
  AlignCenter,
  AlignLeft,
  AlignRight,
  Bold,
  Heading1,
  Heading2,
  Heading3,
  Highlighter, // We'll use this for the "remove highlight" button
  Italic,
  List,
  ListOrdered,
  Strikethrough,
  Palette,         // For multi-color highlight picker
  Paintbrush,      // For text color picker
  MessageSquarePlus // For comments
} from 'lucide-react';
import Toggle from './Toggle'; // Assuming Toggle is your existing component for buttons

interface MenuBarProps {
  editor: Editor | null;
}

const MenuBar: React.FC<MenuBarProps> = ({ editor }) => {
  if (!editor) {
    return null;
  }

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


  // Original options array - we'll remove the generic highlight toggle later
  const existingOptions = [
    {
      icon: <Heading1 className="size-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 1 }).run(),
      pressed: editor.isActive('heading', { level: 1 }),
      title: "Heading 1",
    },
    {
      icon: <Heading2 className="size-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 2 }).run(),
      pressed: editor.isActive('heading', { level: 2 }),
      title: "Heading 2",
    },
    {
      icon: <Heading3 className="size-4" />,
      onClick: () => editor.chain().focus().toggleHeading({ level: 3 }).run(),
      pressed: editor.isActive('heading', { level: 3 }),
      title: "Heading 3",
    },
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
    // The generic 'Highlighter' toggle is removed as we have a color picker now.
    // {
    //   icon: <Highlighter className="size-4" />,
    //   onClick: () => editor.chain().focus().toggleHighlight().run(),
    //   pressed: editor.isActive('highlight'),
    //   title: "Highlight (Default)",
    // },
  ];

  return (
    <div className="border rounded-md p-1 mb-1 bg-slate-50 dark:bg-slate-800 space-x-0.5 md:space-x-1 z-50 flex flex-wrap items-center">
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
      <div className="h-6 w-px bg-slate-300 dark:bg-slate-600 mx-1 md:mx-2" />

      {/* Highlight Color Section */}
      <div className="flex items-center p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700" title="Highlight Color">
        <Palette className="size-4 mr-1 text-slate-700 dark:text-slate-300" />
        <input
            type="color"
            onInput={(event) => editor.chain().focus().toggleHighlight({ color: (event.target as HTMLInputElement).value }).run()}
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
        <Highlighter className="size-4 text-slate-700 dark:text-slate-300 opacity-60" />
      </Toggle>

      {/* Text Color Section */}
      <div className="flex items-center p-1 rounded hover:bg-slate-200 dark:hover:bg-slate-700" title="Text Color">
        <Paintbrush className="size-4 mr-1 text-slate-700 dark:text-slate-300" />
        <input
            type="color"
            onInput={(event) => editor.chain().focus().setColor((event.target as HTMLInputElement).value).run()}
            value={editor.getAttributes('textStyle').color || (document.documentElement.classList.contains('dark') ? '#FFFFFF' : '#000000')}
            className="w-5 h-5 border-none bg-transparent cursor-pointer p-0 m-0"
            title="Pick text color"
        />
      </div>
       <Toggle
        onPressedChange={() => editor.chain().focus().unsetColor().run()}
        pressed={false} // Not a toggle state
        disabled={!editor.getAttributes('textStyle').color}
        title="Remove Text Color"
        className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
      >
        <Paintbrush className="size-4 text-slate-700 dark:text-slate-300 opacity-60" />
      </Toggle>

      {/* Comment Section */}
      <Toggle
        pressed={editor.isActive('comment')} // This will be true if any part of selection is a comment
        onPressedChange={handleComment}
        title="Add Comment"
        className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
      >
        <MessageSquarePlus className="size-4 text-slate-700 dark:text-slate-300" />
      </Toggle>
    </div>
  );
};

export default MenuBar;