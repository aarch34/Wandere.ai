"use client"
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Plane } from 'lucide-react';
import { useState } from 'react';
import Markdown from 'react-markdown';
import remarkBreaks from 'remark-breaks';

const fetchMessages = async () => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/messages`);
  if (!response.ok) {
    return [];
  }
  return response.json();
};

const DashboardPage = () => {
  const [message, setMessage] = useState('');
  const queryClient = useQueryClient();

  // Fetch messages query only on mount
  const { data: messages = [], isLoading, error } = useQuery({
    queryKey: ['messages'],
    queryFn: fetchMessages,
    staleTime: Infinity, // Prevent automatic refetching
    refetchOnWindowFocus: false, // Prevent refetch on window focus
  });

  const sendMessageMutation = useMutation({
    mutationFn: async (newMessage) => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'current-user-id',
          message: newMessage,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      return response.json();
    },
    onMutate: async (newMessage) => {
      // Create the new message object
      const newMessageObj = {
        id: Date.now(),
        message: newMessage,
        sender: 'user',
        timestamp: new Date().toISOString(),
      };

      // Get current messages
      const previousMessages = queryClient.getQueryData(['messages']) || [];

      // Update messages in the cache directly
      queryClient.setQueryData(['messages'], [...previousMessages, newMessageObj]);

      return { previousMessages };
    },
    onError: (err, newMessage, context) => {
      // On error, revert to previous messages
      queryClient.setQueryData(['messages'], context.previousMessages);
    },
    onSuccess: (response) => {
      // Add the AI response to the messages if the API returns one
      if (response.response) {
        const aiMessageObj = {
          id: Date.now(),
          message: response.response,
          sender: 'assistant',
          timestamp: new Date().toISOString(),
        };

        const currentMessages = queryClient.getQueryData(['messages']) || [];
        queryClient.setQueryData(['messages'], [...currentMessages, aiMessageObj]);
      }
    }
  });

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    sendMessageMutation.mutate(message);
    setMessage('');
  };

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
          {isLoading ? (
            <div className="flex justify-center py-4">
              <div className="animate-pulse text-gray-500">Loading messages...</div>
            </div>
          ) : error ? (
            <div className="bg-red-50 p-3 rounded-lg text-red-600 text-center">
              Failed to load messages. Please try again.
            </div>
          ) : messages.length === 0 ? (
            <div className="bg-white p-3 rounded-lg shadow-sm max-w-[80%]">
              <p className="text-sm">Welcome to Wandere.ai! How can I help you plan your next adventure?</p>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`bg-white p-3 rounded-lg shadow-sm ${
                  msg.sender === 'user' ? 'ml-auto bg-teal-50' : ''
                } max-w-[80%]`}
              >
                <Markdown className="text-sm prose" remarkPlugins={[remarkBreaks]}>{msg.message}</Markdown>
                <span className="text-xs text-gray-400 mt-1 block">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))
          )}
          
          {sendMessageMutation.isPending && (
            <div className="bg-teal-50 p-3 rounded-lg shadow-sm ml-auto max-w-[80%]">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-teal-600 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-teal-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                <div className="w-2 h-2 bg-teal-600 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="p-4 border-t border-gray-200 bg-white">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
          <button
            type="submit"
            disabled={sendMessageMutation.isPending}
            className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors disabled:bg-teal-400"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default DashboardPage;