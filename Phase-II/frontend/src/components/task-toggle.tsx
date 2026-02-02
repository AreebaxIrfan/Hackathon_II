'use client';

import { useState } from 'react';

interface TaskToggleProps {
  taskId: number;
  completed: boolean;
  onToggle: () => void;
}

export default function TaskToggle({ taskId, completed, onToggle }: TaskToggleProps) {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleToggle = async () => {
    if (isUpdating) return;

    setIsUpdating(true);
    try {
      onToggle();
    } catch (error) {
      console.error('Failed to toggle task:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <button
      onClick={handleToggle}
      disabled={isUpdating}
      className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 ${
        completed ? 'bg-indigo-600' : 'bg-gray-200'
      } disabled:opacity-50`}
      aria-pressed={completed}
    >
      <span className="sr-only">Toggle task completion</span>
      <span
        aria-hidden="true"
        className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
          completed ? 'translate-x-5' : 'translate-x-0'
        }`}
      />
    </button>
  );
}