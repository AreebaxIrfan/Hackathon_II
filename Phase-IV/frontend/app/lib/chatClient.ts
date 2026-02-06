// Frontend chat API client

interface ChatMessageRequest {
  message: string;
  conversation_id?: string;
}

interface ChatMessageResponse {
  response: string;
  conversation_id: string;
  action_taken: string;
}

class ChatClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async sendMessage(request: ChatMessageRequest): Promise<ChatMessageResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message to chat API:', error);
      throw error;
    }
  }
}

export default ChatClient;