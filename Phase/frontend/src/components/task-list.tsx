'use client';

import { useState } from 'react';
import TaskToggle from './task-toggle';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: (task: Task) => void;
  onTaskDeleted: (taskId: number) => void;
  onToggleComplete: (taskId: number) => void;
}

export default function TaskList({ tasks, onTaskUpdated, onTaskDeleted, onToggleComplete }: TaskListProps) {
  const [deletingTaskId, setDeletingTaskId] = useState<number | null>(null);

  const handleDelete = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setDeletingTaskId(taskId);
    try {
      await fetch(`/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      onTaskDeleted(taskId);
    } catch (error) {
      console.error('Failed to delete task:', error);
    } finally {
      setDeletingTaskId(null);
    }
  };

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`border rounded-lg p-4 shadow-sm ${
            task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
          }`}
        >
          <div className="flex items-start gap-3">
            <TaskToggle
              taskId={task.id}
              completed={task.completed}
              onToggle={() => onToggleComplete(task.id)}
            />
            <div className="flex-1 min-w-0">
              <h3
                className={`text-lg font-medium truncate ${
                  task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                }`}
              >
                {task.title}
              </h3>
              {task.description && (
                <p className="mt-1 text-sm text-gray-600 truncate">{task.description}</p>
              )}
              <div className="mt-2 text-xs text-gray-500">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </div>
            </div>
            <button
              onClick={() => handleDelete(task.id)}
              disabled={deletingTaskId === task.id}
              className="ml-2 inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-red-700 hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              {deletingTaskId === task.id ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}