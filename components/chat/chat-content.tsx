import { Chat, Message } from '@prisma/client'
import React from 'react'
import UserAvatar from '../user-avatar'
import BotAvatar from '../bot-avatar'

interface ChatContentProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatContent = ({chat}: ChatContentProps) => {
  if(chat.messages.length === 0){
    return (
      <div className='flex flex-col flex-1 justify-center items-center'>
        <div className='flex flex-col items-center space-y-5 fixed'>
          <BotAvatar className='w-10 h-10' />
          <h2 className='text-2xl font-semibold'>How can I help you today?</h2>
        </div>

        <div className='grid grid-cols-2 gap-2 w-full mt-auto'>
          <button className='text-left pl-4 px-2 py-4 border-zinc-600 border rounded-xl hover:bg-zinc-700/30 transition'>
            <p className='font-bold'>Make me a personal webpage</p>
            <span className='text-sm text-gray-300'>after asking me three questions</span>
          </button>
          <button className='text-left pl-4 px-2 py-4 border-zinc-600 border rounded-xl hover:bg-zinc-700/30 transition'>
            <p className='font-bold'>Suggest fun activities</p>
            <span className='text-sm text-gray-300'>to help me make friends in a new city</span>
          </button>
          <button className='text-left pl-4 px-2 py-4 border-zinc-600 border rounded-xl hover:bg-zinc-700/30 transition'>
            <p className='font-bold'>Write an email</p>
            <span className='text-sm text-gray-300'>to request a quote from local plumbers</span>
          </button>
          <button className='text-left pl-4 px-2 py-4 border-zinc-600 border rounded-xl hover:bg-zinc-700/30 transition'>
            <p className='font-bold'>Create a morning routine</p>
            <span className='text-sm text-gray-300'>to boost my productivity</span>
          </button>
        </div>
      </div>
    )
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
