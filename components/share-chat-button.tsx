"use client"
import { useModal } from '@/hooks/use-modal-store'
import { Chat } from '@prisma/client'
import { Share } from 'lucide-react'
import React from 'react'

const ShareChatButton = ({chat}: {chat: Chat}) => {
  const {onOpen} = useModal()
  return (
    <button onClick={() => onOpen('shareChat', {chat})} className='absolute top-3 right-3 px-2 py-2 border-zinc-600 border rounded-md hover:bg-zinc-700/30 transition'>
      <Share className='h-5 w-5 text-gray-300' />
    </button>
  )
}

export default ShareChatButton
