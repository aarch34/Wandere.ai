import { Plane } from 'lucide-react';

const DashboardPage = () => {
  return (
      <div className="flex-1 flex flex-col">
        <div className="p-4 border-b border-gray-200 bg-white">
          <div className="flex items-center gap-2">
            <Plane className="text-teal-600" size={20} />
            <h2 className="font-semibold">Travel Assistant</h2>
          </div>
        </div>

        <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
          <div className="space-y-4">
            <div className="bg-white p-3 rounded-lg shadow-sm max-w-[80%]">
              <p className="text-sm">Welcome to Wandere.ai! How can I help you plan your next adventure?</p>
            </div>
          </div>
        </div>

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
  );
};

export default DashboardPage;