'use client';

import { useAuth } from '@/providers/auth-provider';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  createdAt: Date;
}

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const { user } = useAuth();
  const isUser = message.role === 'user';

  return (
    <div className={`flex items-start gap-4 p-4 ${isUser ? 'bg-gray-50 dark:bg-gray-800' : ''}`}>
      <Avatar className="h-8 w-8">
        {isUser ? (
          <>
            <AvatarImage src={user?.photoURL || ''} />
            <AvatarFallback>{user?.email?.[0]?.toUpperCase()}</AvatarFallback>
          </>
        ) : (
          <>
            <AvatarImage src="/logo.svg" />
            <AvatarFallback>GPT</AvatarFallback>
          </>
        )}
      </Avatar>
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <span className="font-medium">{isUser ? 'You' : 'GoogleGPT'}</span>
          <span className="text-xs text-gray-500">
            {new Date(message.createdAt).toLocaleTimeString()}
          </span>
        </div>
        <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
          {message.content}
        </p>
      </div>
    </div>
  );
} 