'use client'

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Plane, Send } from 'lucide-react'
import { useState } from 'react'
import Markdown from 'react-markdown'
import remarkBreaks from 'remark-breaks'

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Skeleton } from "@/components/ui/skeleton"

const fetchMessages = async () => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/messages`)
  if (!response.ok) {
    return []
  }
  return response.json()
}

export default function DashboardPage() {
  const [message, setMessage] = useState('')
  const queryClient = useQueryClient()

  const { data: messages = [], isLoading, error } = useQuery({
    queryKey: ['messages'],
    queryFn: fetchMessages,
    staleTime: Infinity,
    refetchOnWindowFocus: false,
  })

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
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      return response.json()
    },
    onMutate: async (newMessage) => {
      const newMessageObj = {
        id: Date.now(),
        message: newMessage,
        sender: 'user',
        timestamp: new Date().toISOString(),
      }

      const previousMessages = queryClient.getQueryData(['messages']) || []
      queryClient.setQueryData(['messages'], [...previousMessages, newMessageObj])

      return { previousMessages }
    },
    onError: (err, newMessage, context) => {
      queryClient.setQueryData(['messages'], context.previousMessages)
    },
    onSuccess: (response) => {
      if (response.response) {
        const aiMessageObj = {
          id: Date.now(),
          message: response.response,
          sender: 'assistant',
          timestamp: new Date().toISOString(),
        }

        const currentMessages = queryClient.getQueryData(['messages']) || []
        queryClient.setQueryData(['messages'], [...currentMessages, aiMessageObj])
      }
    }
  })

  const handleSendMessage = (e) => {
    e.preventDefault()
    if (!message.trim()) return

    sendMessageMutation.mutate(message)
    setMessage('')
  }

  return (
    <Card className="flex flex-col h-[calc(100vh-2rem)] m-4 w-full">
      <CardHeader className="border-b">
        <CardTitle className="flex items-center gap-2 text-teal-600">
          <Plane className="h-5 w-5" />
          Travel Assistant
        </CardTitle>
      </CardHeader>
      <div className="flex-1 overflow-hidden flex flex-col">
        <CardContent className="flex-1 p-0 flex flex-col min-h-0">
          <ScrollArea className="flex-1 p-4 bg-gradient-to-b from-gray-50 to-white h-dvh">
            {isLoading ? (
              <div className="space-y-4">
                <Skeleton className="h-12 w-3/4" />
                <Skeleton className="h-12 w-1/2" />
                <Skeleton className="h-12 w-2/3" />
              </div>
            ) : error ? (
              <div className="bg-red-50 p-3 rounded-lg text-red-600 text-center">
                Failed to load messages. Please try again.
              </div>
            ) : messages.length === 0 ? (
              <>
                <Card className="w-fit max-w-[60%] bg-teal-50 border-teal-200 mb-4">
                  <CardContent className="p-3">
                    <p className="text-sm text-teal-800">Welcome to Wandere.ai! How can I help you plan your next adventure?</p>
                  </CardContent>
                </Card>
                <div className="space-y-2">
                  <p className="text-sm text-gray-500">Here are some suggestions to get started:</p>
                  <Button variant="outline" size="sm" onClick={() => setMessage("I'm planning a trip to Bali in July. Can you suggest the best areas to stay, must-visit attractions, and any cultural etiquette I should be aware of?")}>
                    Plan a trip to Bali
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => setMessage("I have 3 days in Tokyo and want to experience both traditional and modern Japan. Can you create an itinerary that includes major landmarks, a day trip, and some unique local experiences?")}>
                    3-day Tokyo itinerary
                  </Button>
                  <Button variant="outline" size="sm" onClick={() => setMessage("I'm looking for budget-friendly destinations in Europe for a 2-week trip. Can you suggest countries or cities with affordable accommodations, food, and attractions, along with estimated daily budgets?")}>
                    Budget Europe trip ideas
                  </Button>
                </div>
              </>
            ) : (
              <div className="space-y-4">
                {messages.map((msg) => (
                  <Card
                    key={msg.id}
                    className={`w-fit max-w-[60%] ${
                      msg.sender === 'user' ? 'ml-auto bg-teal-50 border-teal-200' : 'border-gray-200'
                    } transition-all duration-300 ease-in-out animate-fadeIn`}
                  >
                    <CardContent className="p-3">
                      <Markdown className="text-sm prose" remarkPlugins={[remarkBreaks]}>{msg.message}</Markdown>
                      <span className="text-xs text-gray-400 mt-1 block">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </span>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
            {sendMessageMutation.isPending && (
              <Card className="w-fit max-w-[60%] bg-gray-100 border-gray-200 animate-pulse">
                <CardContent className="p-3">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                  </div>
                </CardContent>
              </Card>
            )}
          </ScrollArea>
        </CardContent>
        {messages.length > 0 && (
          <div className="flex flex-wrap gap-2 p-4 border-t">
            <Button variant="outline" size="sm" onClick={() => setMessage("What's the best time to visit Bali?")}>
              Best time for Bali
            </Button>
            <Button variant="outline" size="sm" onClick={() => setMessage("Suggest a 3-day itinerary for Tokyo")}>
              Tokyo itinerary
            </Button>
            <Button variant="outline" size="sm" onClick={() => setMessage("Budget-friendly destinations in Europe")}>
              Budget Europe trips
            </Button>
          </div>
        )}
        <CardFooter className="border-t p-4">
          <form onSubmit={handleSendMessage} className="flex gap-2 w-full">
            <div className="relative flex-1">
              <Input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                className="pr-12 focus-visible:ring-teal-500"
              />
              <Button
                type="submit"
                size="sm"
                disabled={sendMessageMutation.isPending}
                className="absolute right-1 top-1 bottom-1 bg-teal-600 hover:bg-teal-700 text-white"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </form>
        </CardFooter>
      </div>
    </Card>
  )
}