// Frontend Todo API client

interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
}

interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

class TodoClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async getTodos(): Promise<Todo[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/todos/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching todos:', error);
      throw error;
    }
  }

  async createTodo(todo: TodoCreate): Promise<Todo> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/todos/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(todo),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error creating todo:', error);
      throw error;
    }
  }

  async updateTodo(id: string, todo: TodoUpdate): Promise<Todo> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/todos/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(todo),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error updating todo:', error);
      throw error;
    }
  }

  async deleteTodo(id: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/todos/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting todo:', error);
      throw error;
    }
  }
}

export default TodoClient;