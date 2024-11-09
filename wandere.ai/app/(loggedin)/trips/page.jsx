'use client';

import React from 'react';
import { Plane, Map, Calendar, Settings, LogOut, User, MapPin, ChevronRight } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const DashboardPage = () => {
  const previousTrips = [
    {
      id: 1,
      destination: "Paris, France",
      date: "March 15-22, 2024",
      highlights: ["Eiffel Tower", "Louvre Museum"],
      image: "/img/paris.png"
    },
    {
      id: 2,
      destination: "Tokyo, Japan",
      date: "January 5-15, 2024",
      highlights: ["Shibuya Crossing", "Mount Fuji"],
      image: "/img/japan.png"
    },
    {
      id: 3,
      destination: "New York City, USA",
      date: "December 20-27, 2023",
      highlights: ["Central Park", "Times Square"],
      image: "/img/ny.png"
    }
  ];

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
              <button className="flex items-center gap-3 text-white w-full p-2 rounded-lg bg-teal-700 transition-colors">
                <Calendar size={20} />
                Trips
              </button>
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

      {/* Main Content Area */}
      <div className="flex-1 overflow-auto bg-gray-50">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-semibold flex items-center gap-2">
              <MapPin className="text-teal-600" />
              Your Trips
            </h1>
            <button className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors flex items-center gap-2">
              <Plane size={20} />
              Plan New Trip
            </button>
          </div>

          {/* Grid of Trips */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {previousTrips.map((trip) => (
              <Card 
                key={trip.id}
                className="group hover:shadow-lg transition-shadow duration-200"
              >
                <CardContent className="p-0">
                  <div className="relative">
                    <img
                      src={trip.image}
                      alt={trip.destination}
                      className="w-full h-40 object-cover rounded-t-lg"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent rounded-t-lg" />
                  </div>
                  
                  <div className="p-4">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {trip.destination}
                    </h3>
                    
                    <div className="flex items-center text-sm text-gray-500 mb-3">
                      <Calendar size={16} className="mr-2" />
                      {trip.date}
                    </div>
                    
                    <div className="flex flex-wrap gap-2">
                      {trip.highlights.map((highlight, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-teal-50 text-teal-700 text-sm rounded-full"
                        >
                          {highlight}
                        </span>
                      ))}
                    </div>
                    
                    <button className="mt-4 w-full flex items-center justify-center gap-2 py-2 px-4 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors">
                      View Details
                      <ChevronRight size={16} />
                    </button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Empty State */}
          {previousTrips.length === 0 && (
            <Card className="p-8 text-center">
              <div className="flex flex-col items-center gap-4">
                <MapPin className="w-12 h-12 text-gray-400" />
                <h3 className="text-xl font-semibold text-gray-900">No trips yet</h3>
                <p className="text-gray-500">Start planning your first adventure!</p>
                <button className="mt-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors">
                  Plan a Trip
                </button>
              </div>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;