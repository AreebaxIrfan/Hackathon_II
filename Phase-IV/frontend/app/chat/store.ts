// Simple store for chat state management

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
}

interface ChatStore {
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  addMessage: (message: Message) => void;
  setMessages: (messages: Message[]) => void;
  setConversationId: (id: string | null) => void;
  setIsLoading: (loading: boolean) => void;
  clearChat: () => void;
}

// In a real application, you might use a state management library like Zustand or Redux
// For simplicity, we'll use a simple global object
let chatStore: ChatStore = {
  messages: [],
  conversationId: null,
  isLoading: false,
  addMessage: (message: Message) => {
    chatStore.messages = [...chatStore.messages, message];
  },
  setMessages: (messages: Message[]) => {
    chatStore.messages = [...messages];
  },
  setConversationId: (id: string | null) => {
    chatStore.conversationId = id;
  },
  setIsLoading: (loading: boolean) => {
    chatStore.isLoading = loading;
  },
  clearChat: () => {
    chatStore.messages = [];
    chatStore.conversationId = null;
  }
};

export default chatStore;