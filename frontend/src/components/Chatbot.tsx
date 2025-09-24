import { useState, useRef, useEffect, FC } from 'react';
import robotIcon from './assets/robot.png';
import { fetchChat, fetchHistory } from './chat_client';

interface Message {
  content: string;
  isUser: boolean;
}

const Chatbot: FC = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [isHoveringClosed, setIsHoveringClosed] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { content: "Hello! I'm your research assistant. How can I help you today?", isUser: false }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  /**
   * Loads chat history from backend when component mounts
   */
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const history = await fetchHistory();
        if (history && history.length > 0) {
          setMessages(history);
        }
      } catch (error) {
        console.error("Failed to load history", error);
      }
    };
    loadHistory();
  }, []);

  /**
   * Handles sending a message to the chatbot service
   */
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { content: inputValue, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetchChat(inputValue);
      setMessages(prev => [...prev, { content: response, isUser: false }]);
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { content: 'Sorry, something went wrong. Please try again.', isUser: false }
      ]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  /**
   * Auto-scrolls to newest message
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    if (!isLoading) inputRef.current?.focus();
  }, [messages, isLoading]);

  if (!isOpen) {
    return (
      <div
        className="fixed right-0 top-1/2 transform -translate-y-1/2 w-16 h-16 transition-all duration-300 hover:right-8 cursor-pointer z-50"
        onMouseEnter={() => setIsHoveringClosed(true)}
        onMouseLeave={() => setIsHoveringClosed(false)}
        onClick={() => {
          setIsOpen(true);
          setIsHoveringClosed(false);
        }}
      >
        <img
          src={robotIcon}
          alt="AI Assistant"
          className={`w-full h-full object-contain transition-transform duration-300 ${
            isHoveringClosed ? 'scale-110' : 'scale-100'
          }`}
        />
      </div>
    );
  }

  return (
    <div className="fixed right-8 bottom-8 w-96 h-[600px] flex flex-col rounded-2xl overflow-hidden shadow-xl z-50">
      <div className="bg-[#474646] text-white p-4 flex-shrink-0 relative">
        <div className="flex items-center justify-center">
          <img src={robotIcon} alt="AI Assistant" className="w-10 h-10 mr-2 absolute left-4" />
          <h2 className="text-3xl font-semibold text-center">Chatbot</h2>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white bg-transparent border-none p-0"
          aria-label="Close chat"
        >
          <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div className="flex-1 bg-[#D9D9D9] overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-3 ${msg.isUser ? 'text-right' : 'text-left'}`}>
            {!msg.isUser && (
              <div className="flex items-center mb-1">
                <img src={robotIcon} alt="AI" className="w-5 h-5 mr-2" />
                <span className="text-sm text-gray-600">AI</span>
              </div>
            )}
            <div
              className={`inline-block px-4 py-2 max-w-[80%] shadow-md ${
                msg.isUser
                  ? 'bg-white text-gray-800 rounded-2xl rounded-tr-none'
                  : 'bg-[#CDE5FF] text-gray-800 rounded-2xl rounded-tl-none'
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="text-left">
            <div className="flex items-center mb-1">
              <img src={robotIcon} alt="AI" className="w-5 h-5 mr-2" />
              <span className="text-sm text-gray-600">AI</span>
            </div>
            <div className="inline-block bg-[#CDE5FF] px-4 py-2 rounded-2xl rounded-tl-none shadow-md">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="bg-white p-4 border-t border-gray-300 flex-shrink-0">
        <div className="flex items-center">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none placeholder-[#737373] text-gray-800"
            placeholder="Type a message..."
            disabled={isLoading}
            autoFocus
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className={`bg-[#4467FB] text-white p-2 rounded-full ml-2 ${
              (!inputValue.trim() || isLoading) ? 'opacity-50' : 'hover:bg-blue-600'
            }`}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" stroke="#FFFFFF" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
