'use client';

import { useState } from 'react';
import { useAuth } from '@/providers/auth-provider';
import ChatInput from './chat-input';
import ChatMessage from './chat-message';
import Image from 'next/image';
import { Role } from '@prisma/client';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  createdAt: Date;
}

export default function ChatContainer() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || !user) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      createdAt: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: content }),
      });

      if (!response.ok) throw new Error('Failed to send message');

      const data = await response.json();
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: 'assistant',
        createdAt: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // You might want to show an error toast here
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Gemini chat interface image banner */}
      <div className="w-full flex justify-center mb-4">
        <Image
          src="/gimini chat interface.webp"
          alt="Gemini Chat Interface"
          width={600}
          height={200}
          className="rounded-lg shadow"
        />
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            Start a conversation with GoogleGPT
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))
        )}
      </div>
      <div className="border-t p-4">
        <ChatInput chat={{ id: 'current-chat-id', name: 'Current Chat', userId: user?.uid || '', createdAt: new Date(), updatedAt: new Date(), messages: messages }} />
      </div>
    </div>
  );
} 