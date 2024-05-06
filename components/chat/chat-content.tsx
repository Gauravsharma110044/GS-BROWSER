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
    <div className='flex flex-1 overflow-y-auto'>
      {/* <pre>
        {JSON.stringify(chat.messages, null, 2)}
      </pre> */}
      <ScrollArea>
        {chat.messages.map((message, idx) => {
          return(
            <div>{message.content}</div>
          )
        })}
      </ScrollArea>
    </div>
  )
}

export default ChatContent
