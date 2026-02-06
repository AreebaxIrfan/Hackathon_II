import React, { useState, useEffect, useRef } from 'react';
import { ChatWindow } from './ChatWindow';
import { MessageInput } from './MessageInput';
import { ErrorMessage } from './ErrorMessage';
import chatService from '../services/chatService';

interface Message {
  id: number;
  sender: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  userId: string;
  apiKey?: string; // Optional now as we use backend
  instanceLocator?: string; // Optional now
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  userId
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversationId, setConversationId] = useState<string | undefined>(undefined);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Load history on mount
  useEffect(() => {
    const loadHistory = async () => {
      if (!userId) return;

      setIsLoading(true);
      try {
        const conversations = await chatService.getConversations(userId);
        if (conversations && conversations.length > 0) {
          // Get the most recent conversation
          const latestConv = conversations[0];
          setConversationId(latestConv.id);

          const history = await chatService.getHistory(userId, latestConv.id);
          const formattedMessages: Message[] = history.map((msg: any) => ({
            id: msg.id,
            sender: msg.role,
            content: msg.content,
            timestamp: new Date(msg.created_at)
          }));
          setMessages(formattedMessages);
        }
      } catch (err) {
        console.error('Failed to load chat history:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadHistory();
  }, [userId]);

  const handleSendMessage = async (content: string) => {
    // Optimistically add user message
    const userMessage: Message = {
      id: Date.now(),
      sender: 'user',
      content,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await chatService.sendMessage({
        user_id: userId,
        message: content,
        conversation_id: conversationId
      });

      setConversationId(response.conversation_id);

      const assistantMessage: Message = {
        id: Date.now() + 1,
        sender: 'assistant',
        content: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to send message');
      console.error('Chat error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface flex flex-col h-[500px] border rounded-lg bg-white shadow-sm">
      <div className="flex-1 overflow-y-auto">
        <ChatWindow messages={messages} isLoading={isLoading} />
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t">
        <ErrorMessage
          message={error || ''}
          isVisible={!!error}
          onDismiss={() => setError(null)}
        />
        <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;