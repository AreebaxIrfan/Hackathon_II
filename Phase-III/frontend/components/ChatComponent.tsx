'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import chatStore from '../app/chat/store';
import { useAuth } from '../lib/auth';

import chatService from '../src/services/chatService';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

const ChatComponent = () => {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>(chatStore.messages);
  const [isLoading, setIsLoading] = useState(chatStore.isLoading);
  const { user, isAuthenticated, isLoading: isAuthLoading } = useAuth();

  // Sync local state with store
  useEffect(() => {
    const updateMessages = () => {
      setMessages(chatStore.messages);
      setIsLoading(chatStore.isLoading);
    };

    updateMessages();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || !user) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    // Update store and local state
    chatStore.addMessage(userMessage);
    setMessages([...chatStore.messages]);

    setInputValue('');
    chatStore.setIsLoading(true);
    setIsLoading(true);

    try {
      // Send message to backend using chatService
      const response = await chatService.sendMessage({
        user_id: user.id,
        message: inputValue,
        conversation_id: chatStore.conversationId || undefined
      });

      // Add assistant response to chat
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        sender: 'assistant',
        timestamp: new Date(),
      };

      // Update store and local state
      chatStore.addMessage(assistantMessage);
      setMessages([...chatStore.messages]);

      // Set conversation ID if returned
      if (response.conversation_id && !chatStore.conversationId) {
        chatStore.setConversationId(response.conversation_id);
      }
    } catch (error: any) {
      console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error.message || 'Sorry, I encountered an error processing your request.',
        sender: 'assistant',
        timestamp: new Date(),
      };

      // Update store and local state
      chatStore.addMessage(errorMessage);
      setMessages([...chatStore.messages]);
    } finally {
      chatStore.setIsLoading(false);
      setIsLoading(false);
    }
  };

  if (isAuthLoading) {
    return <div>Loading authentication...</div>;
  }

  if (!isAuthenticated) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center space-y-4">
        <p className="text-gray-600">Please log in to use the chat assistant.</p>
        <Link
          href="/auth/login"
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
        >
          Login Now
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto mb-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${message.sender === 'user'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-800'
                }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
              Thinking...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type your message here..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
          disabled={isLoading || !inputValue.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatComponent;