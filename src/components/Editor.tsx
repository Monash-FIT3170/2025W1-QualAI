

const Editor = () => {
  return (
    <div className="bg-secondary/30 rounded-lg shadow-lg">
      <div className="border-b border-gray-700 p-2 flex gap-2">
        <button className="p-2 hover:bg-white/10 rounded">B</button>
        <button className="p-2 hover:bg-white/10 rounded">I</button>
        <button className="p-2 hover:bg-white/10 rounded">U</button>
        <div className="h-6 w-px bg-gray-700 mx-2" />
        <button className="p-2 hover:bg-white/10 rounded">•</button>
        <button className="p-2 hover:bg-white/10 rounded">1.</button>
        <div className="h-6 w-px bg-gray-700 mx-2" />
        <select className="bg-transparent border-none outline-none">
          <option>Font</option>
        </select>
        <select className="bg-transparent border-none outline-none">
          <option>Size</option>
        </select>
      </div>

      <div
        className="editor-content"
        contentEditable
        suppressContentEditableWarning
      >
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
        <p className="mt-4">Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
      </div>

      <div className="border-t border-gray-700 p-2 flex justify-between">
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
          Save Changes
        </button>
        <button className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors">
          Discard
        </button>
      </div>
    </div>
  );
};

export default Editor;
