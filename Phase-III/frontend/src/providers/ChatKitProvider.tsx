import React, { createContext, useContext, ReactNode } from 'react';
import config from '../config';

interface ChatKitContextType {
  isConnected: boolean;
  userId: string | null;
  connect: (userId: string) => Promise<void>;
  disconnect: () => void;
}

const ChatKitContext = createContext<ChatKitContextType | undefined>(undefined);

interface ChatKitProviderProps {
  children: ReactNode;
}

export const ChatKitProvider: React.FC<ChatKitProviderProps> = ({ children }) => {
  const [isConnected, setIsConnected] = React.useState(false);
  const [userId, setUserId] = React.useState<string | null>(null);

  const connect = async (userId: string) => {
    try {
      // In a real implementation, this would connect to the actual ChatKit service
      // For now, we'll simulate the connection
      console.log(`Connecting to ChatKit for user: ${userId}`);

      // Simulate connection process
      await new Promise(resolve => setTimeout(resolve, 300));

      setUserId(userId);
      setIsConnected(true);
    } catch (error) {
      console.error('Failed to connect to ChatKit:', error);
      throw error;
    }
  };

  const disconnect = () => {
    setUserId(null);
    setIsConnected(false);
  };

  const value: ChatKitContextType = {
    isConnected,
    userId,
    connect,
    disconnect
  };

  return (
    <ChatKitContext.Provider value={value}>
      {children}
    </ChatKitContext.Provider>
  );
};

export const useChatKit = () => {
  const context = useContext(ChatKitContext);
  if (context === undefined) {
    throw new Error('useChatKit must be used within a ChatKitProvider');
  }
  return context;
};