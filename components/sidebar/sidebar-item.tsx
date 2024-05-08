"use client"
import { Chat } from '@prisma/client'
import { Archive, MoreHorizontal, Pencil, Share, Trash } from 'lucide-react'
import { useParams, useRouter } from 'next/navigation'
import React, { useState } from 'react'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from '../ui/dropdown-menu'
import { useModal } from '@/hooks/use-modal-store'
import { SideBarItemEdit } from './sidebar-name-edit-form'
import { cn } from '@/lib/utils'

const SideBarItem = ({chat}: {chat: Chat}) => {
  const [isEditing, setIsEditing] = useState(false)
  const router = useRouter()
  const params = useParams()
  const {onOpen} = useModal()

  return (
    <button key={chat.id} onClick={() => router.push(`/${chat.id}`)} className={cn('group p-2 rounded-md flex items-center gap-x-3 w-full hover:bg-zinc-700/30 transition', params.chatId === chat.id && 'bg-zinc-700/30')}>
      {!isEditing && (<p className='text-sm'>{chat.name}</p>)}
      {isEditing && (<SideBarItemEdit chat={chat} setIsEditing={setIsEditing} />)}
      <div className='space-x-2 ml-auto flex'>
        <DropdownMenu>
          <DropdownMenuTrigger className="focus:outline-none" asChild>
            <MoreHorizontal className='w-4 h-4 mr-2 text-gray-300 hover:text-white' />
          </DropdownMenuTrigger>
          <DropdownMenuContent className='text-xs font-medium space-y-[2px]'>
            <DropdownMenuItem 
              onClick={(e) => {
                e.stopPropagation()
                onOpen('shareChat', {chat})
              }} 
              className='px-3 p-2 text-sm cursor-pointer'>
              <Share className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Share
            </DropdownMenuItem>
            <DropdownMenuItem 
              onClick={(e) => {
                e.stopPropagation()
                setIsEditing(true)
              }} 
              className='px-3 p-2 text-sm cursor-pointer'>
              <Pencil className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Rename
            </DropdownMenuItem>
            <DropdownMenuItem 
              onClick={(e) => {
                e.stopPropagation()
                onOpen('deleteChat', {chat})
              }} 
              className='px-3 p-2 text-sm cursor-pointer'>
              <Trash className='flex-shrink-0 w-5 h-5 text-zinc-500 dark:text-zinc-400 mr-2'/> Delete chat
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <Archive className='w-4 h-4 mr-2 text-gray-300 hover:text-white' onClick={() => console.log('Archive')} />
      </div>
    </button>
  )
}

export default SideBarItem
