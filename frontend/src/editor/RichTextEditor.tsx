// RichTextEditor.tsx
import React, { useEffect, useRef, useState } from 'react';
import { EditorContent, useEditor } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import TextAlign from '@tiptap/extension-text-align';
import { TextStyle } from '@tiptap/extension-text-style'; // Verify package installation
import Highlight from '@tiptap/extension-highlight';
import CommentMark from '../tiptap-extensions/CommentMark';
import FontSize from './FontSize';
import MenuBar from './MenuBar';
import { useParams } from "react-router-dom";
import { HIGHLIGHT_COLORS, HighlightData } from "@/types/highlight.ts";

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
  const { projectName } = useParams<{ projectName: string }>()

    const previousTextRef = useRef<string>('');
    const [highlights, setHighlights] = useState<HighlightData[]>([]);

const [isLoadingHighlights, setIsLoadingHighlights] = useState(false);

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


    // Load highlights when fileKey changes
    useEffect(() => {
        if (!editor) return;

        const loadHighlights = async () => {
            setIsLoadingHighlights(true);
            if ( !fileKey ) {
                return;
            }

            try {

                const response = await fetch(`http://localhost:5001/${projectName}/documents/${fileKey}`);
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
      body: JSON.stringify({
          content, project: projectName,
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
      })
      .catch(err => {
        console.error('Save error:', err);
      });
  };

  return (
      <div className={`flex flex-col h-full ${className}`}>
        <MenuBar editor={editor} hl={highlights} fileKey={fileKey ?? null} loading={isLoadingHighlights} />
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