import React from 'react';
import { Plane, Map, Calendar, Settings, LogOut, User } from 'lucide-react';
import Link from 'next/link';

const DashboardPage = () => {
  return (
    <div className="h-screen flex">
      {/* Left Sidebar */}
      <div className="w-64 bg-teal-800 text-white p-6 flex flex-col">
        {/* Logo and Brand */}
        <div className="flex items-center gap-3 mb-8">
          <Plane size={24} className="text-teal-400" />
          <h1 className="text-2xl font-bold">Wandere.ai</h1>
        </div>

        {/* User Profile Section */}
        <div className="mb-8 p-3 bg-teal-700/50 rounded-lg">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-teal-600 rounded-full flex items-center justify-center">
              <User size={20} />
            </div>
            <div>
              <h2 className="font-medium">John Doe</h2>
             
            </div>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="flex-1">
          <ul className="space-y-4">
            <li>
              <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <Map size={20} />
                Explore
              </button>
            </li>
            <li>
              <Link  href="/trips" className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <Calendar size={20} />
                Trips
              </Link>
            </li>
            <li>
              <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <User size={20} />
                Profile
              </button>
            </li>
            <li>
              <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <Settings size={20} />
                Settings
              </button>
            </li>
          </ul>
        </nav>

        {/* Logout Button */}
        <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
          <LogOut size={20} />
          Logout
        </button>
      </div>

      {/* Chat Interface */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="p-4 border-b border-gray-200 bg-white">
          <div className="flex items-center gap-2">
            <Plane className="text-teal-600" size={20} />
            <h2 className="font-semibold">Travel Assistant</h2>
          </div>
        </div>

        {/* Chat Messages Area */}
        <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
          <div className="space-y-4">
            <div className="bg-white p-3 rounded-lg shadow-sm max-w-[80%]">
              <p className="text-sm">Welcome to Wandere.ai! How can I help you plan your next adventure?</p>
            </div>
          </div>
        </div>

        {/* Chat Input */}
        <div className="p-4 border-t border-gray-200 bg-white">
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Type your message..."
              className="flex-1 p-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
            <button className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors">
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;