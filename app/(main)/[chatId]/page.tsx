import ChatContent from '@/components/chat/chat-content'
import ChatHeader from '@/components/chat/chat-header'
import ChatInput from '@/components/chat/chat-input'
import { currentUser } from '@/lib/current-user'
import prisma from '@/lib/prisma'
import React from 'react'

const page = async ({params}: {params: {chatId: string}}) => {
  const user = await currentUser()

  const chat = await prisma.chat.findUnique({
    where: {
      id: params.chatId,
      userId: user?.id
    }
  })
  return (
    <div className='h-full flex flex-col'>
      <ChatHeader />
      <div className='flex h-full flex-col container md:px-[12rem]'>
        <div className='flex flex-1 h-full'>
          <ChatContent />
        </div>
        <ChatInput />
      </div>
    </div>
  )
}

export default page
