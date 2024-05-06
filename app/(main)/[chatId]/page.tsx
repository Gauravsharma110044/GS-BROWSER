import ChatContent from '@/components/chat/chat-content'
import ChatHeader from '@/components/chat/chat-header'
import ChatInput from '@/components/chat/chat-input'
import { currentUser } from '@/lib/current-user'
import prisma from '@/lib/prisma'
import { redirect } from 'next/navigation'
import React from 'react'

const page = async ({params}: {params: {chatId: string}}) => {
  const user = await currentUser()
  if(!user){
    return redirect('/login')
  }
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
      <ChatHeader />
      <div className='flex flex-1 overflow-y-auto'>
        <ChatContent chat={chat} />
      </div>
      <ChatInput chat={chat} />
    </div>
  )
}

export default page
