// app/(loggedin)/plan-trip/layout.tsx

import React from 'react';

export default function PlanTripLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col flex-1">
      {/* If you want to add a header specific to plan-trip pages */}
      <header className="border-b bg-white p-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Trip Planning</h1>
        </div>
      </header>

      {/* Main content area */}
      <div className="flex-1">
        {children}
      </div>

      {/* If you want to add a footer specific to plan-trip pages */}
      <footer className="border-t bg-white p-4 mt-auto">
        <div className="max-w-7xl mx-auto text-sm text-gray-500">
          Need help planning? Check our <button className="text-teal-600 hover:underline">travel guides</button>
        </div>
      </footer>
    </div>
  );
}