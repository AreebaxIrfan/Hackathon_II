import axios, { AxiosResponse } from 'axios';

interface ChatRequest {
  user_id: string;
  message: string;
  conversation_id?: string;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
}

interface TaskOperationRequest {
  user_id: string;
  title?: string;
  description?: string;
  task_id?: number;
  status?: 'all' | 'pending' | 'completed';
}

class ChatService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response: AxiosResponse<ChatResponse> = await axios.post(
        `${this.baseUrl}/api/v1/${request.user_id}/chat`,
        {
          message: request.message,
          conversation_id: request.conversation_id
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          withCredentials: true
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API Error: ${error.response?.data?.error || error.message}`);
      }
      throw new Error(`Network Error: ${(error as Error).message}`);
    }
  }

  async getConversations(userId: string): Promise<any[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/api/v1/${userId}/conversations`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch conversations:', error);
      return [];
    }
  }

  async getHistory(userId: string, conversationId: string): Promise<any[]> {
    try {
      const response = await axios.get(`${this.baseUrl}/api/v1/${userId}/conversations/${conversationId}/history`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch chat history:', error);
      return [];
    }
  }

  async addTask(request: TaskOperationRequest): Promise<{ task_id: number; status: string; title: string }> {
    try {
      const response = await axios.post(`${this.baseUrl}/api/tasks/`, {
        title: request.title,
        description: request.description,
      }, {
        headers: {
          'Content-Type': 'application/json',
          // Authorization will be handled by interceptor or we assume cookie/token is present
          // If ChatService doesn't handle auth, we might need to pass token. 
          // But usually axios is configured globally or credentials are included.
        },
        withCredentials: true
      });
      return {
        task_id: response.data.id,
        status: 'created',
        title: response.data.title
      };
    } catch (error) {
      console.error('Failed to add task:', error);
      throw error;
    }
  }

  async listTasks(request: TaskOperationRequest): Promise<{ tasks: Array<any> }> {
    try {
      const response = await axios.get(`${this.baseUrl}/api/tasks/`, {
        params: {
          completed: request.status || 'all'
        },
        withCredentials: true
      });
      // Backend returns list of objects. Frontend expects { tasks: [] }? 
      // Based on original code: return { tasks: [...] }
      return { tasks: response.data };
    } catch (error) {
      console.error('Failed to list tasks:', error);
      return { tasks: [] };
    }
  }

  async completeTask(request: TaskOperationRequest): Promise<{ task_id: number; status: string; title: string }> {
    try {
      const response = await axios.patch(`${this.baseUrl}/api/tasks/${request.task_id}/complete`, {}, {
        withCredentials: true
      });
      return {
        task_id: response.data.id,
        status: 'completed',
        title: response.data.title
      };
    } catch (error) {
      console.error('Failed to complete task:', error);
      throw error;
    }
  }

  async deleteTask(request: TaskOperationRequest): Promise<{ task_id: number; status: string; title: string }> {
    try {
      await axios.delete(`${this.baseUrl}/api/tasks/${request.task_id}`, {
        withCredentials: true
      });
      return {
        task_id: request.task_id || 0,
        status: 'deleted',
        title: 'Task deleted'
      };
    } catch (error) {
      console.error('Failed to delete task:', error);
      throw error;
    }
  }

  async updateTask(request: TaskOperationRequest): Promise<{ task_id: number; status: string; title: string }> {
    try {
      // Note: Frontend request doesn't seem to pass 'updates' object cleanly in TaskOperationRequest interface in my view
      // But assuming request properties map to updates
      const updates: any = {};
      if (request.title) updates.title = request.title;
      if (request.description) updates.description = request.description;

      const response = await axios.put(`${this.baseUrl}/api/tasks/${request.task_id}`, updates, {
        withCredentials: true
      });
      return {
        task_id: response.data.id,
        status: 'updated',
        title: response.data.title
      };
    } catch (error) {
      console.error('Failed to update task:', error);
      throw error;
    }
  }
}

export default new ChatService();