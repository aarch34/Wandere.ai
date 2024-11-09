'use client';

import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import {MapPin, Calendar, ChevronRight, Plane} from 'lucide-react';
import Link from "next/link"

const TripPage = () => {
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

      <div className="flex-1 overflow-auto bg-gray-50">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-semibold flex items-center gap-2">
              <MapPin className="text-teal-600" />
              Your Trips
            </h1>
            <Link
  href="/plan-trip"
  className={`flex items-center space-x-2 p-2 rounded-lg w-full transition-colors 
     bg-teal-700 hover:bg-teal-700 w-fit text-white
  `}
>
  <span>Plan Trip</span>
</Link>
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
  );
};

export default TripPage;