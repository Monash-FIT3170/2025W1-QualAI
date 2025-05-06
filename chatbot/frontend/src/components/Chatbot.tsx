import React, { useState, useRef, useEffect, use } from 'react';
import robotIcon from '../assets/robot.png'; // our robot avatar icon guy 
import { fetchChat } from './chat_client'; // function to fetch chat responses from the backend


// this is what each message will look like
interface Message {
  content: string;  // the actual words
  isUser: boolean; // who's talking - us or the bot
}

const Chatbot: React.FC = () => {
    // state stuff - keeping track of what's happening
  const [isOpen, setIsOpen] = useState(true); // is chat open or not
  const [isHoveringClosed, setIsHoveringClosed] = useState(false); // hovering over closed icon?
  const [messages, setMessages] = useState<Message[]>([ // all our chat history
    { content: "Hello! I'm your research assistant. How can I help you today?", isUser: false } // first bot message
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null); // ref for the input field

  // when we hit send
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return; // don't send empty messages or while loading
    
    // add our message to the chat
    const userMessage = { content: inputValue, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInputValue(''); // clear the input
    setIsLoading(true); // bot is "thinking"

    try {
      const response = await fetchChat(inputValue); // fetch response from chatbot service
      setMessages(prev => [...prev, { content: response, isUser: false }]);       // add bot's reply
    } catch (error) {
      setMessages(prev => [
        ...prev,
        { content: 'Sorry, something went wrong. Please try again.', isUser: false }
      ]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus(); // focus the input after bot responds
    }
  };

  // auto-scroll to newest message and focus input when not loading
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    if (!isLoading) {
      inputRef.current?.focus();
    }
  }, [messages, isLoading]);

  // if chat is closed, just show the robot icon on the side
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
            isHoveringClosed ? 'scale-110' : 'scale-100' // little zoom on hover
          }`}
        />
      </div>
    );
  }

  // main chat window
  return (
    <div className="fixed right-8 bottom-8 w-96 h-[600px] flex flex-col rounded-2xl overflow-hidden shadow-xl z-50">
      {/* header with robot icon and centered text */}
      <div className="bg-[#474646] text-white p-4 flex-shrink-0 relative">
        <div className="flex items-center justify-center">
          <img src={robotIcon} alt="AI Assistant" className="w-10 h-10 mr-2 absolute left-4" />
          <h2 className="text-3xl font-semibold text-center">Chatbot</h2> {/* Changed text-x1 to text-2xl */}
        </div>
        {/* close button (the x) - removed background/box */}
        <button 
          onClick={() => setIsOpen(false)}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white focus:outline-none bg-transparent border-none p-0"
          aria-label="Close chat"
        >
          <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      {/* main body where all the messages are visible */}
      <div className="flex-1 bg-[#D9D9D9] overflow-y-auto p-4">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-3 ${msg.isUser ? 'text-right' : 'text-left'}`}>
            {/* show robot icon and "ai" text for bot messages */}
            {!msg.isUser && (
              <div className="flex items-center mb-1">
                <img src={robotIcon} alt="AI" className="w-5 h-5 mr-2" />
                <span className="text-sm text-gray-600">AI</span>
              </div>    
            )}
            {/* the actual message bubble */}
            <div 
              className={`inline-block px-4 py-2 max-w-[80%] shadow-md ${
                msg.isUser 
                  ? 'bg-white text-gray-800 rounded-2xl rounded-tr-none' // our messages
                  : 'bg-[#CDE5FF] text-gray-800 rounded-2xl rounded-tl-none' // bot messages
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {/* loading animation when bot is "thinking" */}
        {isLoading && (
          <div className="text-left">
            <div className="flex items-center mb-1">
              <img src={robotIcon} alt="AI" className="w-5 h-5 mr-2" />
              <span className="text-sm text-gray-600">AI</span>
            </div>
            <div className="inline-block bg-[#CDE5FF] px-4 py-2 rounded-2xl rounded-tl-none shadow-md">
            {/* little bouncing dots animation */}
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}
        {/* invisible div for auto-scrolling */}
        <div ref={messagesEndRef} />
      </div>
      
      {/* input area at the bottom/footer */}
      <div className="bg-white p-4 border-t border-gray-300 flex-shrink-0">
        <div className="flex items-center">
        {/* message input */}
          <input
            ref={inputRef} // reference to the input element
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none placeholder-[#737373] text-gray-800"
            placeholder="Type a message..."
            disabled={isLoading}
            autoFocus // automatically focus when component mounts
          />
        {/* send button */}
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