import React from 'react';

interface Message {
  id: number;
  sender: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatWindowProps {
  messages?: Message[];
  isLoading?: boolean;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages = [],
  isLoading = false
}) => {
  return (
    <div className="chat-window p-4 space-y-4">
      <div className="chat-messages space-y-4">
        {messages.length > 0 ? (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-3 shadow-sm ${message.sender === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-none'
                    : 'bg-gray-100 text-gray-800 rounded-bl-none'
                  }`}
              >
                <div className="message-content text-sm whitespace-pre-wrap">{message.content}</div>
                <div className={`text-[10px] mt-1 opacity-70 ${message.sender === 'user' ? 'text-right' : 'text-left'
                  }`}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        ) : !isLoading && (
          <div className="empty-state text-center text-gray-400 py-10 italic">
            <p>Start a conversation by sending a message!</p>
          </div>
        )}
        {isLoading && (
          <div className="assistant-loading flex justify-start">
            <div className="bg-gray-100 text-gray-500 rounded-lg p-3 rounded-bl-none shadow-sm flex items-center space-x-2">
              <div className="flex space-x-1">
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
              <span className="text-xs">Assistant is thinking...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatWindow;