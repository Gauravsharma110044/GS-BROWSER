import ChatContent from '@/components/chat/chat-content'
import ChatHeader from '@/components/chat/chat-header'
import ChatInput from '@/components/chat/chat-input'
import ShareChatButton from '@/components/share-chat-button'
import { currentUser } from '@/lib/current-user'
import prisma from '@/lib/prisma'
import { CircleHelp, Share } from 'lucide-react'
import { redirect } from 'next/navigation'
import React from 'react'

const page = async ({params}: {params: {chatId: string}}) => {
  const user = await currentUser()
  if(!user){
    return redirect('/login')
  }
  const chats = await prisma.chat.findMany({
    where: {
      userId: user.id
    }
  })
  const chat = await prisma.chat.findUnique({
    where: {
      id: params.chatId,
      userId: user.id
    },
    include: {
      messages: true
    }
  })
  if(!chat){
    return redirect('/')
  }
  return (
    <div className='flex flex-col h-full'>
      <ChatHeader chats={chats} user={user} />
      <div className='flex flex-1 overflow-y-auto container no-scrollbar lg:px-[14rem]'>
        <ChatContent chat={chat} />
      </div>
      <div className='container lg:px-[12rem]'>
        <ChatInput chat={chat} />
        <span className='flex justify-center mb-3 text-xs text-gray-300 text-center'>ChatGPT can make mistakes. Consider checking important information.</span>
      </div>

      <ShareChatButton chat={chat} />
      <button className='absolute bottom-6 right-6'>
        <CircleHelp className='h-5 w-5 text-gray-300' />
      </button>
    </div>
  )
}

export default page
