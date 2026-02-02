'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/auth';
import { apiClient } from '@/lib/api-client';
import TaskForm from '@/components/task-form';
import TaskList from '@/components/task-list';
import TaskToggle from '@/components/task-toggle';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const { user, loading, isAuthenticated } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loadingTasks, setLoadingTasks] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      fetchTasks();
    }
  }, [isAuthenticated]);

  const fetchTasks = async () => {
    try {
      setLoadingTasks(true);
      const data = await apiClient.get<Task[]>('/api/tasks');
      setTasks(data);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoadingTasks(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (taskId: number) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  const handleToggleComplete = async (taskId: number) => {
    try {
      const updatedTask = await apiClient.patch<Task>(`/api/tasks/${taskId}/complete`, {});
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (!isAuthenticated) {
    // Redirect to sign in (this would typically be handled by a higher-level auth guard)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Please sign in to access your dashboard.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
          <p className="mt-1 text-sm text-gray-600">Welcome back, {user?.email}</p>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <TaskForm onTaskCreated={handleTaskCreated} />
            </div>

            <div className="mt-8">
              {loadingTasks ? (
                <div className="text-center py-8">Loading tasks...</div>
              ) : tasks.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <p>No tasks yet. Create your first task above!</p>
                </div>
              ) : (
                <TaskList
                  tasks={tasks}
                  onTaskUpdated={handleTaskUpdated}
                  onTaskDeleted={handleTaskDeleted}
                  onToggleComplete={handleToggleComplete}
                />
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}