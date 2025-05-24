import { X } from 'lucide-react';

const Chatbot = () => {
  return (
    <div className="w-80 bg-secondary/50 p-4 flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-2">
          <span className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
            AI
          </span>
          <span className="font-semibold">Chatbot</span>
        </div>
        <button className="p-1 hover:bg-white/10 rounded">
          <X size={20} />
        </button>
      </div>

      <div className="flex-1 space-y-4">
        <div className="bg-white/5 p-3 rounded-lg">
          How can I assist you?
        </div>
        <div className="bg-white/5 p-3 rounded-lg">
          Please summarize the key topics of this file.
        </div>
      </div>

      <div className="mt-4 flex gap-2">
        <input
          type="text"
          placeholder="Type a message..."
          className="flex-1 bg-white/10 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button className="p-2 bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors">
          →
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
