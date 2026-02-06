'use client';

import React, { useState, useEffect } from 'react';

interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: Date;
  created_at: Date;
  updated_at: Date;
}

import { getAllTasks, type Task } from '../lib/api';

const TodoList = () => {
  const [todos, setTodos] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const tasks = await getAllTasks('all');
      setTodos(tasks);
    } catch (error) {
      console.error('Error fetching todos:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading todos...</div>;
  }

  return (
    <div className="mt-4">
      <h2 className="text-xl font-bold mb-2">Your Todo List</h2>
      <ul className="space-y-2">
        {todos.map((todo) => (
          <li
            key={todo.id}
            className={`p-2 border rounded ${todo.completed ? 'bg-green-100' : 'bg-white'}`}
          >
            <div className="flex items-center">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleTodoComplete(todo.id)}
                className="mr-2"
              />
              <span className={`${todo.completed ? 'line-through text-gray-500' : ''}`}>
                {todo.title}
              </span>
            </div>
            {todo.description && (
              <p className="text-sm text-gray-600 ml-6">{todo.description}</p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );

  // Placeholder function for toggling todo completion
  function toggleTodoComplete(id: string) {
    console.log(`Toggle todo ${id} completion`);
  }
};

export default TodoList;