"use client"
import React, { useState } from 'react'
import { Input } from '../ui/input'
import { Button } from '@/components/ui/button'
import { Send } from 'lucide-react'
import { Chat, Message } from '@prisma/client'
import axios from 'axios'
import { useRouter } from 'next/navigation'

interface ChatInputProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatInput = ({chat}: ChatInputProps) => {
  const router = useRouter()
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || loading) return

    try {
      setLoading(true)
      const response = await axios.post('/api/chat', {chatId: chat.id, prompt: message})
      router.refresh()
      setMessage('')
    } catch (error) {
      console.error('Error sending message:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-2 p-4 border-t">
      <Input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
        disabled={loading}
        className="flex-1"
      />
      <Button type="submit" disabled={loading || !message.trim()}>
        <Send className="h-4 w-4" />
      </Button>
    </form>
  )
}

export default ChatInput
