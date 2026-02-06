// Types for the Chat Interface

export interface ChatInterfaceState {
  isLoading: boolean;
  error: string | null;
  chatInitialized: boolean;
  connectionStatus: 'connected' | 'connecting' | 'disconnected';
}

export interface Message {
  id: number;
  user_id: string;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: Date;
}

export interface ToolCall {
  id: number;
  conversation_id: number;
  tool_name: string;
  arguments: string; // JSON string
  result?: string; // JSON string
  created_at: Date;
}

export interface Conversation {
  id: number;
  user_id: string;
  created_at: Date;
  updated_at: Date;
}

export interface ErrorMessageProps {
  message: string;
  isVisible: boolean;
  onDismiss?: () => void;
}

export interface ChatRequest {
  user_id: string;
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
}