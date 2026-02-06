'use client';

import React from 'react';
import ChatComponent from '../components/ChatComponent';
import TodoList from '../components/TodoList';
import Navbar from '../components/Navbar';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">AI Todo Assistant</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Chat Interface */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Chat with AI Assistant</h2>
            <div className="h-[500px] flex flex-col">
              <ChatComponent />
            </div>
          </div>

          {/* Todo List */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-700">Your Todo List</h2>
            <TodoList />
          </div>
        </div>

        <div className="mt-8 text-center text-gray-600">
          <p>Interact with the AI assistant to manage your tasks using natural language.</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;