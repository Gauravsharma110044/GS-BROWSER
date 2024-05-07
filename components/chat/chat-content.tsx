import { Chat, Message } from '@prisma/client'
import React from 'react'
import { ScrollArea } from '../ui/scroll-area'

interface ChatContentProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatContent = ({chat}: ChatContentProps) => {
  return (
    <div className='flex flex-1 flex-col py-4 overflow-y-auto'>
      <div className='flex flex-col-reverse mt-auto'>
        {chat.messages.map((message, idx) => {
          return(
            <div key={idx}>{message.content}</div>
          )
        })}
      </div>
    </div>
  )
}

export default ChatContent
