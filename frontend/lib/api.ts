// API client for task management

export type Task = {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
};

type TaskCreateData = {
  title: string;
  description?: string;
};

type TaskUpdateData = {
  title?: string;
  description?: string;
  completed?: boolean;
};

// Helper function to get auth headers
const getAuthHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
});

// Get all tasks with optional filtering
export const getAllTasks = async (status: 'all' | 'pending' | 'completed' = 'all'): Promise<Task[]> => {
  const queryParams = new URLSearchParams({
    status,
  }).toString();

  console.log(`Fetching tasks from: ${process.env.NEXT_PUBLIC_API_URL}/api/tasks?${queryParams}`);
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/tasks?${queryParams}`,
    {
      headers: getAuthHeaders(),
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch tasks: ${response.statusText}`);
  }

  const data = await response.json();
  return data.tasks || data; // Handle different response formats
};

// Create a new task
export const createTask = async (taskData: TaskCreateData): Promise<Task> => {
  console.log(`Creating task at: ${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, taskData);
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    console.error('Create task failed:', errorData);
    throw new Error(`Failed to create task: ${response.statusText}`);
  }

  return response.json();
};

// Get a single task
export const getTask = async (id: string): Promise<Task> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tasks/${id}`, {
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch task: ${response.statusText}`);
  }

  return response.json();
};

// Update a task
export const updateTask = async (id: string, taskData: TaskUpdateData): Promise<Task> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to update task: ${response.statusText}`);
  }

  return response.json();
};

// Delete a task
export const deleteTask = async (id: string): Promise<void> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error(`Failed to delete task: ${response.statusText}`);
  }
};

// Mark a task as complete
export const completeTask = async (id: string): Promise<Task> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}/complete`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error(`Failed to complete task: ${response.statusText}`);
  }

  return response.json();
};

// Mark a task as incomplete
export const incompleteTask = async (id: string): Promise<Task> => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${id}/incomplete`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
  });

  if (!response.ok) {
    throw new Error(`Failed to mark task as incomplete: ${response.statusText}`);
  }

  return response.json();
};