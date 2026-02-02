'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '../../lib/auth';
import { getAllTasks, createTask, updateTask, deleteTask, type Task } from '../../lib/api';



export default function DashboardPage() {
  const { logout, user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');
  const [error, setError] = useState('');

  // Fetch tasks
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const tasksData = await getAllTasks(filter);
        setTasks(tasksData);
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [filter]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!title.trim()) return;

    try {
      const newTask = await createTask({ title, description });
      setTasks([newTask, ...tasks]);
      setTitle('');
      setDescription('');
    } catch (error) {
      console.error('Failed to create task:', error);
      setError('Failed to create task. Please check your connection and try again.');
    }
  };

  const handleToggleComplete = async (id: string, currentStatus: boolean) => {
    try {
      const updatedTask = await updateTask(id, { completed: !currentStatus });
      setTasks(tasks.map(task =>
        task.id === id ? updatedTask : task
      ));
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">Task Manager</h1>
            </div>
            <div className="flex items-center">
              <span className="mr-4 text-sm text-gray-700">Welcome, {user?.email}</span>
              <button
                onClick={logout}
                className="ml-4 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Task Creation Form */}
          <div className="mb-8 bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h2>
            {error && (
              <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                <p className="text-sm">{error}</p>
              </div>
            )}
            <form onSubmit={handleCreateTask} className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                  Title *
                </label>
                <input
                  type="text"
                  id="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 text-black focus:border-indigo-500 sm:text-sm"
                  required
                />
              </div>
              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  id="description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 text-black focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Add Task
              </button>
            </form>
          </div>

          {/* Task Filters */}
          <div className="mb-4 flex space-x-4">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 text-sm font-medium rounded-md ${filter === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
            >
              All Tasks
            </button>
            <button
              onClick={() => setFilter('pending')}
              className={`px-4 py-2 text-sm font-medium rounded-md ${filter === 'pending'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
            >
              Pending
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 text-sm font-medium rounded-md ${filter === 'completed'
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
            >
              Completed
            </button>
          </div>

          {/* Task List */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            {loading ? (
              <div className="p-6 text-center">Loading tasks...</div>
            ) : filteredTasks.length === 0 ? (
              <div className="p-6 text-center text-gray-500">No tasks found</div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {filteredTasks.map((task) => (
                  <li key={task.id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            checked={task.completed}
                            onChange={() => handleToggleComplete(task.id, task.completed)}
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                          />
                          <p
                            className={`ml-4 text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                              }`}
                          >
                            {task.title}
                          </p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-500">
                            {new Date(task.created_at).toLocaleDateString()}
                          </span>
                          <button
                            onClick={() => handleDeleteTask(task.id)}
                            className="ml-2 inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                          >
                            Delete
                          </button>
                        </div>
                      </div>
                      {task.description && (
                        <div className="mt-2 ml-8 text-sm text-gray-600">
                          {task.description}
                        </div>
                      )}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}