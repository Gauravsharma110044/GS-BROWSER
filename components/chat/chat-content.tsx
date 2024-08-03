"use client"
import { Chat, Message } from '@prisma/client'
import React, { useEffect, useRef } from 'react'
import UserAvatar from '../user-avatar'
import BotAvatar from '../bot-avatar'
import ChatRecommendation from './chat-recommendation'
import ReactMarkdown from 'react-markdown'

interface ChatContentProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatContent = ({chat}: ChatContentProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };
  useEffect(() => {
    scrollToBottom();
  }, [chat.messages]);

  if(chat.messages.length === 0){
    return (<ChatRecommendation chat={chat} />)
  }
  return (
    <div className='flex flex-1 flex-col py-4 overflow-y-auto no-scrollbar'>
      <div className='flex flex-col space-y-8'>
        {chat.messages.map((message, idx) => {
          return(
            <div key={idx} className='flex space-x-3'>
              {message.role === 'USER' ? (<UserAvatar name='chetan' />) : (<BotAvatar />)}
              <div className='mt-1'>
                <span className='font-bold'>{message.role === 'USER' ? 'You' : 'ChatGPT'}</span>
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          )
        })}
        <div ref={messagesEndRef} />
      </div>
    </div>
  )
}

export default ChatContent
