// MenuBar.tsx
import React, { useState, useEffect, useRef } from 'react';
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
  Paintbrush, // for text colour
  MessageSquarePlus, // comments
  ChevronDown,
  Minus,
  Plus
} from 'lucide-react';
import Toggle from './Toggle';
import { HighlightData, HighlightPriority, HIGHLIGHT_COLORS } from '../types/highlight';

interface MenuBarProps {
  editor: Editor | null;
  fileKey: string;
}

const MenuBar: React.FC<MenuBarProps> = ({ editor, fileKey }) => {
  if (!editor) {
    return null;
  }

  const [currentFontSize, setCurrentFontSize] = useState(16);
  const [showFontSizes, setShowFontSizes] = useState(false);
  const [highlights, setHighlights] = useState<HighlightData[]>([]);
  const [isLoadingHighlights, setIsLoadingHighlights] = useState(false);
  const [showHighlightDropdown, setShowHighlightDropdown] = useState(false);
  const previousTextRef = useRef<string>('');
  const fontSizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72, 96];

  // Load highlights when fileKey changes
  useEffect(() => {
    if (!fileKey || !editor) return;

    const loadHighlights = async () => {
      setIsLoadingHighlights(true);
      try {
        const response = await fetch(`http://localhost:5001/documents/${fileKey}`);
        if (!response.ok) {
          console.error('Failed to load highlights');
          return;
        }

        const data = await response.json();
        const loadedHighlights: HighlightData[] = data.highlights || [];
        
        setHighlights(loadedHighlights);
        applyHighlightsToEditor(loadedHighlights);
        previousTextRef.current = editor.getText();
      } catch (error) {
        console.error('Error loading highlights:', error);
      } finally {
        setIsLoadingHighlights(false);
      }
    };

    loadHighlights();
  }, [fileKey, editor]);

  // Apply highlights to editor
  const applyHighlightsToEditor = (highlightsToApply: HighlightData[]) => {
    if (!editor) return;

    // Clear all existing highlights first
    editor.chain().focus().unsetHighlight().run();

    // Apply each highlight
    highlightsToApply.forEach((highlight) => {
      const { index_start, index_end } = highlight.indexes;
      const color = HIGHLIGHT_COLORS[highlight.priority];

      try {
        editor
          .chain()
          .setTextSelection({ from: index_start + 1, to: index_end + 1 })
          .setHighlight({ color })
          .run();
      } catch (error) {
        console.error('Error applying highlight:', error, highlight);
      }
    });

    // Reset selection
    editor.commands.focus();
  };

  // Monitor text changes and invalidate affected highlights
  useEffect(() => {
    if (!editor) return;

    const handleUpdate = () => {
      const currentText = editor.getText();
      const previousText = previousTextRef.current;

      // If text length changed significantly, we need to validate highlights
      if (currentText.length !== previousText.length) {
        const validHighlights = highlights.filter((highlight) => {
          const { index_start, index_end } = highlight.indexes;
          return index_end <= currentText.length;
        });

        // Update state only if highlights were removed
        if (validHighlights.length !== highlights.length) {
          setHighlights(validHighlights);
          console.log(`Removed ${highlights.length - validHighlights.length} invalid highlights due to text changes`);
        }
      }

      previousTextRef.current = currentText;
    };

    editor.on('update', handleUpdate);

    return () => {
      editor.off('update', handleUpdate);
    };
  }, [editor, highlights]);

  // Font size tracking
  useEffect(() => {
    if (!editor) return;

    const updateFontSize = () => {
      const attributes = editor.getAttributes('textStyle');
      if (attributes.fontSize) {
        const numericSize = parseInt(attributes.fontSize.replace('px', ''));
        setCurrentFontSize(numericSize);
      } else {
        setCurrentFontSize(16);
      }
    };

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
    const nonOverlappingHighlights = highlights.filter((h) => {
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

    setHighlights([...nonOverlappingHighlights, newHighlight]);
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
    const updatedHighlights = highlights.filter((h) => {
      const overlaps = !(
        h.indexes.index_end <= selection.index_start ||
        h.indexes.index_start >= selection.index_end
      );
      return !overlaps;
    });

    setHighlights(updatedHighlights);
    console.log('Highlight removed at:', selection);
  };

  // Save document with highlights
  const handleFileUpdate = () => {
    if (!editor || !fileKey) {
      console.warn("Cannot save: missing editor or fileKey");
      return;
    }

    const content = editor.getHTML();
    console.log('Saving fileKey:', fileKey);
    console.log('Saving content:', content);
    console.log('Saving highlights:', highlights);

    fetch(`http://localhost:5001/edit/${fileKey}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
        highlights: highlights.map(h => ({  //can be used to update highlights in backend
          indexes: h.indexes,
          priority: h.priority
        }))
      }),
    })
      .then(res => {
        if (!res.ok) {
          throw new Error('Failed to save document');
        }
        return res.json();
      })
      .then(data => {
        console.log('Save successful:', data);
        alert('Document saved successfully!');
      })
      .catch(err => {
        console.error('Save error:', err);
        alert('Failed to save document. Please try again.');
      });
  };

  // Handle comment
  const handleComment = () => {
    const commentId = `comment-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
    const commentText = prompt("Enter your comment:");

    if (commentText) {
      console.log(`Comment to save: ID=${commentId}, Text=${commentText}, User: rachana-barak, Timestamp: ${new Date().toISOString()}`);
      editor.chain().focus().setComment({ commentId }).run();
    }
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
    <div className="border rounded-md p-1 mb-1 bg-slate-50 dark:bg-slate-800 space-x-0.5 md:space-x-1 z-50 flex flex-wrap items-center">
      
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
          className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
        >
          {option.icon}
        </Toggle>
      ))}

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
            disabled={isLoadingHighlights}
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
          disabled={!editor.isActive('highlight') || isLoadingHighlights}
          title="Remove Highlight"
          className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Highlighter className="size-4 text-slate-700 dark:text-slate-300" />
        </button>
      </div>

      {/* Separator */}
      <div className="h-6 w-px bg-slate-300 dark:bg-slate-600 mx-1 md:mx-2" />

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
        pressed={false}
        disabled={!editor.getAttributes('textStyle').color}
        title="Remove Text Color"
        className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
      >
        <Paintbrush className="size-4 text-slate-700 dark:text-slate-300 opacity-60" />
      </Toggle>

      {/* Comment Section */}
      <Toggle
        pressed={editor.isActive('comment')}
        onPressedChange={handleComment}
        title="Add Comment"
        className="p-2 hover:bg-slate-200 dark:hover:bg-slate-700 rounded"
      >
        <MessageSquarePlus className="size-4 text-slate-700 dark:text-slate-300" />
      </Toggle>
      
      <button 
        onClick={handleFileUpdate} 
        className="rounded-md px-2 py-1 hover:bg-gray-200 dark:hover:bg-slate-700 font-medium"
        disabled={isLoadingHighlights}
      >
        Save Changes
      </button>
    </div>
  );
};

export default MenuBar;