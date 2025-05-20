import { Mark, mergeAttributes, MarkConfig } from '@tiptap/core';

// 1. Define an interface for the Extension's Options
export interface CommentMarkOptions {
  HTMLAttributes: {
    class?: string;
    [key: string]: any; // Allows for other HTML attributes if needed
  };
  // You could add other configuration options for the CommentMark extension here
}

// 2. This interface describes the attributes of an INSTANCE of the comment mark
export interface CommentMarkInstanceAttributes {
  commentId: string | null;
}

// 3. Update the declared commands to use CommentMarkInstanceAttributes for clarity
//    (Note: for setComment, commentId should ideally be non-null)
declare module '@tiptap/core' {
  interface Commands<ReturnType> {
    comment: {
      setComment: (attributes: { commentId: string }) => ReturnType;
      toggleComment: (attributes?: { commentId: string }) => ReturnType;
      unsetComment: () => ReturnType;
    };
  }
}

// 4. Use CommentMarkOptions as the generic for Mark.create
//    and CommentMarkInstanceAttributes for the attributes within addAttributes
export const CommentMark = Mark.create<CommentMarkOptions, any>({ // Second generic 'any' is for storage, if not used explicitly
  name: 'comment',

  spanning: true,
  inclusive: false,

  // addOptions now correctly returns CommentMarkOptions
  addOptions() {
    return {
      HTMLAttributes: {
        class: 'comment-mark', // Default class for styling
      },
    };
  },

  // addAttributes defines the data attributes of the mark instance
  addAttributes() {
    return {
      commentId: { // This key should align with CommentMarkInstanceAttributes
        default: null,
        parseHTML: element => element.getAttribute('data-comment-id'),
        // The 'attributes' parameter here refers to all attributes of the mark instance
        renderHTML: (attributes: CommentMarkInstanceAttributes) => {
          if (!attributes.commentId) {
            return {};
          }
          return { 'data-comment-id': attributes.commentId };
        },
      },
    };
  },

  parseHTML() {
    return [
      {
        tag: 'span[data-comment-id]',
        getAttrs: element => {
          const commentId = (element as HTMLElement).getAttribute('data-comment-id');
          // Ensure it returns CommentMarkInstanceAttributes or false
          return commentId ? { commentId } : false;
        },
      },
    ];
  },

  // renderHTML for the mark itself
  // The 'HTMLAttributes' parameter here contains the resolved attributes for this specific mark instance
  // (e.g., { 'data-comment-id': '123', class: 'comment-mark' } after merging)
  renderHTML({ HTMLAttributes }) {
    // this.options.HTMLAttributes now correctly refers to the defaults from addOptions
    // HTMLAttributes (the parameter) contains the specific attributes from addAttributes
    return ['span', mergeAttributes(this.options.HTMLAttributes, HTMLAttributes), 0];
  },

  addCommands() {
    return {
      setComment: (attributes) => ({ commands, editor }) => {
        if (!attributes.commentId) return false;
        if (!editor.schema.marks[this.name]) {
            console.warn(`Mark type '${this.name}' not registered with the editor schema.`);
            return false;
        }
        // attributes here are { commentId: string } which is compatible with CommentMarkInstanceAttributes
        return commands.setMark(this.name, attributes as CommentMarkInstanceAttributes);
      },
      toggleComment: (attributes) => ({ commands, editor }) => {
        if (!editor.schema.marks[this.name]) {
            console.warn(`Mark type '${this.name}' not registered with the editor schema.`);
            return false;
        }
        const { selection } = editor.state;
        const { from, to } = selection;
        let isActive = false;

        if (attributes?.commentId) {
          editor.state.doc.nodesBetween(from, to, (node) => {
            if (node.marks.some(mark => mark.type.name === this.name && mark.attrs.commentId === attributes.commentId)) {
              isActive = true;
            }
          });
        } else {
          isActive = editor.isActive(this.name);
        }

        if (isActive) {
          return commands.unsetMark(this.name, { extendEmptyMarkRange: true });
        } else if (attributes?.commentId) {
          return commands.setMark(this.name, attributes as CommentMarkInstanceAttributes);
        }
        return false;
      },
      unsetComment: () => ({ commands, editor }) => {
        if (!editor.schema.marks[this.name]) {
            console.warn(`Mark type '${this.name}' not registered with the editor schema.`);
            return false;
        }
        return commands.unsetMark(this.name, { extendEmptyMarkRange: true });
      },
    };
  },
} as MarkConfig<CommentMarkOptions, any>); // Explicitly cast to MarkConfig if needed for stricter type checking

export default CommentMark;