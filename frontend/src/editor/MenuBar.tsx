// MenuBar.tsx
import React, { useEffect, useState } from 'react';
import { Editor } from '@tiptap/react';
import {
    AlignCenter,
    AlignLeft,
    AlignRight,
    Bold,
    ChevronDown,
    Highlighter,
    Italic,
    List,
    ListOrdered,
    MessageSquarePlus,
    Minus,
    Paintbrush,
    Plus,
    Strikethrough
} from 'lucide-react';
import Toggle from './Toggle';
import { HIGHLIGHT_COLORS, HighlightData, HighlightPriority } from '../types/highlight';

interface MenuBarProps {
  editor: Editor | null;
  hl: HighlightData[];
  fileKey: string | null;
  loading: boolean;
}

const MenuBar: React.FC<MenuBarProps> = ({ editor, hl, fileKey, loading }) => {
  if (!editor) {
    return null;
  }

  const [currentFontSize, setCurrentFontSize] = useState(16);
  const [showFontSizes, setShowFontSizes] = useState(false);
  const [showHighlightDropdown, setShowHighlightDropdown] = useState(false);
  const fontSizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72, 96];

  // Font size tracking
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

  // Get plain text selection positions
  const getTextSelection = (): { index_start: number; index_end: number } | null => {
    if (!editor) return null;

    const { from, to } = editor.state.selection;

    if (from === to) {
      console.warn('No text selected');
      return null;
    }

    return {
      index_start: from - 1,  // TipTap uses 1-based indexing
      index_end: to - 1
    };
  };

  // Handle highlight with priority
  const handleHighlight = (priority: HighlightPriority) => {
    const selection = getTextSelection();
    if (!selection) {
      return;
    }

    const color = HIGHLIGHT_COLORS[priority];

    // Check for overlapping highlights and remove them
    const nonOverlappingHighlights = hl.filter((h) => {
      const overlaps = !(
        h.indexes.index_end <= selection.index_start ||
        h.indexes.index_start >= selection.index_end
      );
      return !overlaps;
    });

    // Apply highlight in editor
    editor.chain().focus().setHighlight({ color }).run();

    // Add new highlight to state
    const newHighlight: HighlightData = {
      indexes: selection,
      priority
    };

    hl.splice(0, hl.length);
    nonOverlappingHighlights.forEach(h => hl.push(h));
    hl.push(newHighlight);
    console.log('Highlight added:', newHighlight);
  };

  // Remove highlight at selection
  const handleRemoveHighlight = () => {
    const selection = getTextSelection();
    if (!selection) {
      // If no selection, remove highlight at cursor position
      editor.chain().focus().unsetHighlight().run();
      return;
    }

    // Remove highlight from editor
    editor.chain().focus().unsetHighlight().run();

    // Remove from state - find any highlight that overlaps with selection
    const updatedHighlights = hl.filter((h) => {
      const overlaps = !(
        h.indexes.index_end <= selection.index_start ||
        h.indexes.index_start >= selection.index_end
      );
      return !overlaps;
    });

    hl.splice(0, hl.length);
    updatedHighlights.forEach(h => hl.push(h));
    console.log('Highlight removed at:', selection);
  };

  // Handle comment
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
      <div className="menubar menubar-icon border rounded-md p-1 mb-1] dark:bg-slate-800 space-x-0.5 md:space-x-1 z-50 flex flex-wrap items-center">
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

          <div className='menubar-icon'>
            {existingOptions.map((option, index) => (
                <Toggle
                    key={index}
                    pressed={option.pressed}
                    onPressedChange={option.onClick}
                    disabled={option.disabled}
                    title={option.title}
                    className="p-2 hover:bg-slate-700 rounded"
                >
                    {option.icon}
                </Toggle>
            ))}
          </div>

      {/* Separator */}
      <div className="h-6 w-px bg-slate-300 dark:bg-slate-600 mx-1 md:mx-2" />

      {/* Priority-Based Highlight Section - DROPDOWN STYLE */}
      <div className="flex items-center space-x-1">
        {/* Highlight Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowHighlightDropdown(!showHighlightDropdown)}
            className="flex items-center space-x-1 px-2 py-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700"
            title="Highlight Priority"
            disabled={loading}
          >
            <Highlighter className="size-4" />
            <ChevronDown className="size-3" />
          </button>

          {showHighlightDropdown && (
            <div className="absolute top-full left-0 mt-1 bg-white dark:bg-slate-800 border rounded-md shadow-lg z-10 min-w-[150px]">
              <button
                onClick={() => {
                  handleHighlight('HIGH');
                  setShowHighlightDropdown(false);
                }}
                className="flex items-center space-x-2 w-full px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-slate-700"
              >
                <div className="w-4 h-4 rounded" style={{ backgroundColor: HIGHLIGHT_COLORS.HIGH }}></div>
                <span>High Priority</span>
              </button>

              <button
                onClick={() => {
                  handleHighlight('LOW');
                  setShowHighlightDropdown(false);
                }}
                className="flex items-center space-x-2 w-full px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-slate-700"
              >
                <div className="w-4 h-4 rounded" style={{ backgroundColor: HIGHLIGHT_COLORS.LOW }}></div>
                <span>Low Priority</span>
              </button>

              <button
                onClick={() => {
                  handleHighlight('IGNORE');
                  setShowHighlightDropdown(false);
                }}
                className="flex items-center space-x-2 w-full px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-slate-700"
              >
                <div className="w-4 h-4 rounded" style={{ backgroundColor: HIGHLIGHT_COLORS.IGNORE }}></div>
                <span>Ignore</span>
              </button>
            </div>
          )}
        </div>

        {/* Remove Highlight Button */}
        <button
          onClick={handleRemoveHighlight}
          disabled={!editor.isActive('highlight') || loading}
          title="Remove Highlight"
          className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Highlighter className="size-4 text-slate-700 dark:text-slate-300" />
        </button>
      </div>

      {/* Separator */}
      <div className="h-6 w-px bg-slate-300 dark:bg-slate-600 mx-1 md:mx-2" />

          {/* Text Color Section */}
          <div className="flex items-center p-1 rounded menubar-icon" title="Text Color">
              <Paintbrush className="size-4 mr-1 menubar-icon"/>
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
              className="p-2 menubar-icon dark:hover:bg-slate-700 rounded"
          >
              <Paintbrush className="menubar-icon size-4 0 opacity-60"/>
          </Toggle>

          {/* Comment Section */}
          <Toggle
              pressed={editor.isActive('comment')} // This will be true if any part of selection is a comment
              onPressedChange={handleComment}
              title="Add Comment"
              className="p-2 menubar-icon dark:hover:bg-slate-700 rounded"
          >
              <MessageSquarePlus className="size-4 menubar-icon"/>
          </Toggle>
    </div>
  );
};

export default MenuBar;