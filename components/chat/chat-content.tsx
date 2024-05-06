import { Chat, Message } from '@prisma/client'
import React from 'react'

interface ChatContentProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatContent = ({chat}: ChatContentProps) => {
  return (
    <div className='flex flex-1 overflow-y-auto h-full'>
      <pre>
        {JSON.stringify(chat.messages, null, 2)}
      </pre>
    </div>
  )
}

export default ChatContent
