import { Chat, Message } from '@prisma/client'
import React from 'react'
import UserAvatar from '../user-avatar'
import BotAvatar from '../bot-avatar'
import ChatRecommendation from './chat-recommendation'

interface ChatContentProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatContent = ({chat}: ChatContentProps) => {
  if(chat.messages.length === 0){
    return (<ChatRecommendation chat={chat} />)
  }
  return (
    <div className='flex flex-1 flex-col py-4 overflow-y-auto'>
      <div className='flex flex-col space-y-8'>
        {chat.messages.map((message, idx) => {
          return(
            <div key={idx} className='flex space-x-3'>
              {message.role === 'USER' ? (<UserAvatar name='chetan' />) : (<BotAvatar />)}
              <div className='mt-1'>
                <span className='font-bold'>{message.role === 'USER' ? 'You' : 'ChatGPT'}</span>
                <p>{message.content}</p>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default ChatContent
